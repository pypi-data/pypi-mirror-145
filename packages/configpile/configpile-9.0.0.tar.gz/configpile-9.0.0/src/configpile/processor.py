"""
Arguments processing

This module contains the internal machinery that processes environment variables, configuration
files and command-line parameters.

As of March 22, 2022, configpile is still pretty much influenced by :mod:`argparse`, and the
machinery below supports a subset of :mod:`argparse` functionality. Later on, we may cut ties
with :mod:`argparse`, add our own help/usage message writing, our own Sphinx extension and
encourage extending those processing classes. 

.. rubric:: Types

This module uses the following types.

.. py:data:: _Value

    Value being parsed by a :class:`.ParamType`

.. py:data:: _Config

    Type of the configuration dataclass to construct
"""

from __future__ import annotations

import argparse
import configparser
import sys
import warnings
from abc import ABC, abstractmethod
from configparser import ConfigParser
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Annotated, get_args, get_origin, get_type_hints

from .arg import Arg, Expander, Param, Positional
from .userr import Err, Res, in_context
from .util import ClassDoc, filter_types_single

if TYPE_CHECKING:
    from .config import Config

_Config = TypeVar("_Config", bound="Config")

_Value = TypeVar("_Value")


class CLHandler(ABC):
    """
    A handler for command-line arguments
    """

    @abstractmethod
    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        """
        Processes arguments, possibly updating the state or returning errors

        Args:
            args: Command-line arguments not processed yet
            state: (Mutable) state to possibly update

        Returns:
            The updated command-line and an optional error
        """
        pass


@dataclass(frozen=True)
class CLSpecialAction(CLHandler):
    """
    A handler that sets the special action
    """

    special_action: SpecialAction  #: Special action to set

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if state.special_action is not None:
            before = state.special_action.name
            now = self.special_action.name
            err = Err.make(f"We had already action {before}, conflicts with action {now}")
            return (args, err)
        state.special_action = self.special_action
        return (args, None)


@dataclass(frozen=True)
class CLInserter(CLHandler):
    """
    Handler that expands a flag into a sequence of args inserted into the command line to be parsed
    """

    #: Arguments inserted in the command-line
    inserted_args: Sequence[str]

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        # TODO: run the command line parser on the inserted args
        return ([*self.inserted_args, *args], None)


@dataclass(frozen=True)
class CLParam(CLHandler, Generic[_Value]):
    """
    Parameter handler

    Takes a single string argument from the command line, parses it and pushes into the
    corresponding sequence of instances
    """

    #: Parameter to handle
    param: Param[_Value]

    def action(self, value: _Value, state: State) -> Optional[Err]:
        """
        A method called on the successful parse of a value

        Can be overridden. By default does nothing.

        Args:
            value: Parsed value
            state: State to possibly update

        Returns:
            An optional error
        """
        return None

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if args:
            res = self.param.parser.parse(args[0])
            if isinstance(res, Err):
                return (args[1:], res.in_context(param=self.param.name))
            else:
                assert self.param.name is not None, "Names are assigned after initialization"
                err = in_context(self.action(res, state), param=self.param.name)
                state.instances[self.param.name] = [*state.instances[self.param.name], res]
                return (args[1:], err)
        else:
            return (
                args,
                Err.make("Expected value, but no argument present", param=self.param.name),
            )


@dataclass(frozen=True)
class CLConfigParam(CLParam[Sequence[Path]]):
    """
    A configuration file parameter handler

    If paths are successfully parsed, it appends configuration files to be parsed to the current
    state.
    """

    def action(self, value: Sequence[Path], state: State) -> Optional[Err]:
        state.config_files_to_process.extend(value)
        return None


@dataclass
class CLPos(CLHandler):
    """
    Handles positional parameters

    Note that this handler has state, namely the positional parameters that are still expected.
    """

    pos: List[Param[Any]]  #: (Mutable) list of positional parameters

    @staticmethod
    def make(seq: Sequence[Param[Any]]) -> CLPos:
        """
        Constructs a positional parameter handler from a sequence of positional parameters

        Args:
            seq: Positional parameters

        Returns:
            Handler
        """
        assert all([p.positional is not None for p in seq]), "All parameters should be positional"
        assert all(
            [not p.positional.should_be_last() for p in seq[:-1] if p.positional is not None]
        ), "Positional parameters with a variable number of arguments should be last"
        l = list(seq)  # makes a mutable copy
        return CLPos(l)

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if not args:
            return (args, None)  # should not happen ,but let's not crash
        if not self.pos:
            return (args[1:], Err.make(f"Unknown argument {args[0]}"))
        p = self.pos[0]
        assert p.name is not None
        res = p.parser.parse(args[0])
        if isinstance(res, Err):
            return (args[1:], in_context(res, param=p.name))
        else:
            state.append(p.name, res)
            if p.positional == Positional.ONCE:
                self.pos = self.pos[1:]
            return (args[1:], None)


@dataclass(frozen=True)
class CLStdHandler(CLHandler):
    """
    The standard command line arguments handler

    It processes arguments one by one. If it recognizes a flag, the corresponding handler is
    called. Otherwise, control is passed to the fallback handler, which by default processes
    positional parameters.
    """

    flags: Mapping[str, CLHandler]
    fallback: CLHandler

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if not args:
            return (args, None)
        flag = args[0]
        handler = self.flags.get(flag)
        if handler is not None:
            next_args, err = handler.handle(args[1:], state)
            err = in_context(err, flag=flag)
            return next_args, err
        else:
            return self.fallback.handle(args, state)


class KVHandler(ABC):
    """
    Handler for key/value pairs found for example in environment variables or INI files

    Note that the key is not stored/processed in this class.
    """

    @abstractmethod
    def handle(self, value: str, state: State) -> Optional[Err]:
        """
        Processes

        Args:
            value: Value to parse and process
            state: State to update

        Returns:
            An error if an error occurred
        """
        pass


@dataclass(frozen=True)
class KVParam(KVHandler, Generic[_Value]):
    """
    Handler for the value following a key corresponding to a parameter
    """

    #: Parameter to handle
    param: Param[_Value]

    def action(self, value: _Value, state: State) -> Optional[Err]:
        """
        A method called on the successful parse of a value

        Can be overridden. By default does nothing.

        Args:
            value: Parsed value
            state: State to possibly update

        Returns:
            An optional error
        """
        return None

    def handle(self, value: str, state: State) -> Optional[Err]:
        res = self.param.parser.parse(value)
        if isinstance(res, Err):
            return res
        else:
            assert self.param.name is not None
            err = self.action(res, state)
            state.instances[self.param.name] = [*state.instances[self.param.name], res]
            return in_context(err, param=self.param.name)


@dataclass(frozen=True)
class KVConfigParam(KVParam[Sequence[Path]]):
    """
    Handler for the configuration file value following a key corresponding to a parameter
    """

    def action(self, value: Sequence[Path], state: State) -> Optional[Err]:
        state.config_files_to_process.extend(value)
        return None


class SpecialAction(Enum):
    """
    Describes special actions that do not correspond to normal execution
    """

    HELP = "help"  #: Display a help message
    VERSION = "version"  #: Print the version number


@dataclass
class State:
    """
    Describes the (mutable) state of a configuration being parsed
    """

    instances: Dict[str, List[Any]]  #: Contains the sequence of values for each parameter
    config_files_to_process: List[Path]  #: Contains a list of configuration files to process
    special_action: Optional[SpecialAction]  #: Contains a special action if flag was encountered

    def append(self, key: str, value: Any) -> None:
        """
        Appends a value to a parameter

        No type checking is performed, be careful.

        Args:
            key: Parameter name
            value: Value to append
        """
        assert key in self.instances, f"{key} is not a Param name"
        self.instances[key] = [*self.instances[key], value]

    @staticmethod
    def make(params: Iterable[Param[Any]]) -> State:
        """
        Creates the initial state, populated with the default values when present

        Args:
            params: Sequence of parameters

        Raises:
            ValueError: If a default value cannot be parsed correctly

        Returns:
            The initial mutable state
        """
        instances: Dict[str, List[Any]] = {}

        for p in params:
            assert p.name is not None, "Arguments have names after initialization"
            if p.default_value is not None:
                res = p.parser.parse(p.default_value)
                if isinstance(res, Err):
                    raise ValueError(f"Invalid default {p.default_value} for parameter {p.name}")
                instances[p.name] = [res]
            else:
                instances[p.name] = []
        return State(instances, config_files_to_process=[], special_action=None)


@dataclass(frozen=True)
class IniProcessor:
    """
    INI configuration file processor
    """

    section_strict: Mapping[str, bool]  #: Sections and their strictness
    kv_handlers: Mapping[str, KVHandler]  #: Handler for key/value pairs

    def _process(self, parser: ConfigParser, state: State) -> Sequence[Err]:
        """
        Processes a filled ConfigParser

        Args:
            parser: INI data to parse
            state: Mutable state to update

        Returns:
            Errors that occurred, if any
        """
        errors: List[Err] = []
        try:
            for section_name in parser.sections():
                if section_name in self.section_strict:
                    for key, value in parser[section_name].items():
                        err: Optional[Err] = None
                        if key in self.kv_handlers:
                            res = self.kv_handlers[key].handle(value, state)
                            if isinstance(res, Err):
                                err = res
                        else:
                            if self.section_strict[section_name]:
                                err = Err.make(f"Unknown key {key}")
                        if err is not None:
                            errors.append(err.in_context(ini_section=section_name))
        except configparser.Error as e:
            errors.append(Err.make(f"Parse error"))
        except IOError as e:
            errors.append(Err.make(f"IO Error"))
        return errors

    def process_string(self, ini_contents: str, state: State) -> Optional[Err]:
        """
        Processes a configuration file given as a string

        Args:
            ini_contents: Contents of the INI file
            state: Mutable state to update

        Returns:
            An optional error
        """
        errors: List[Err] = []
        parser = ConfigParser()
        try:
            parser.read_string(ini_contents)
            errors.extend(self._process(parser, state))
        except configparser.Error as e:
            errors.append(Err.make(f"Parse error"))
        except IOError as e:
            errors.append(Err.make(f"IO Error"))
        if errors:
            return Err.collect(*errors)
        else:
            return None

    def process(self, ini_file_path: Path, state: State) -> Optional[Err]:
        """
        Processes a configuration file

        Args:
            ini_path: Path to the INI file
            state: Mutable state to update

        Returns:
            An optional error
        """
        errors: List[Err] = []
        if not ini_file_path.exists():
            return Err.make(f"Config file {ini_file_path} does not exist")
        if not ini_file_path.is_file():
            return Err.make(f"Path {ini_file_path} is not a file")
        parser = ConfigParser()
        try:
            with open(ini_file_path, "r") as file:
                parser.read_file(file)
                errors.extend(self._process(parser, state))
        except configparser.Error as e:
            errors.append(Err.make(f"Parse error"))
        except IOError as e:
            errors.append(Err.make(f"IO Error"))
        if errors:
            return Err.collect(*errors)
        else:
            return None


@dataclass
class ProcessorFactory(Generic[_Config]):
    """
    Describes a processor in construction

    This factory is passed to the different arguments present in the configuration.
    """

    #: List of parameters indexed by their field name
    params_by_name: Dict[str, Param[Any]]

    #: Argument parser to update, used to display help and for the Sphinx documentation
    argument_parser: argparse.ArgumentParser

    #: Argument parser group for commands
    ap_commands: argparse._ArgumentGroup

    #: Argument parser group for required parameters
    ap_required: argparse._ArgumentGroup

    #: Argument parser group for optional parameters
    ap_optional: argparse._ArgumentGroup

    #: Handlers for environment variables
    env_handlers: Dict[str, KVHandler]  # = {}

    #: List of INI sections with their corresponding strictness
    ini_section_strict: Dict[str, bool]

    #: List of handlers for key/value pairs present in INI files
    ini_handlers: Dict[str, KVHandler]

    #: List of command line flag handlers
    cl_flag_handlers: Dict[str, CLHandler]

    #: List of positional arguments
    cl_positionals: List[Param[Any]]

    validators: List[Callable[[_Config], Optional[Err]]]

    @staticmethod
    def make(config_type: Type[_Config]) -> ProcessorFactory[_Config]:
        """
        Constructs an empty processor factory

        Args:
            config_type: Configuration to process

        Returns:
            A processor factory
        """
        # fill program name from script invocation
        prog = config_type.prog_
        if prog is None:
            prog = sys.argv[0]

        # fill description from class docstring
        description: Optional[str] = config_type.description_
        if description is None:
            description = config_type.__doc__

        argument_parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False,
        )
        argument_parser._action_groups.pop()
        return ProcessorFactory(
            params_by_name={},
            argument_parser=argument_parser,
            ap_commands=argument_parser.add_argument_group("commands"),
            ap_optional=argument_parser.add_argument_group("optional arguments"),
            ap_required=argument_parser.add_argument_group("required arguments"),
            env_handlers={},
            ini_section_strict={s.name: s.strict for s in config_type.ini_sections_()},
            ini_handlers={},
            cl_flag_handlers={},
            cl_positionals=[],
            validators=[*config_type.validators_()],
        )


@dataclass(frozen=True)
class Processor(Generic[_Config]):
    """
    Configuration processor
    """

    #: Configuration to parse
    config_type: Type[_Config]

    #: Completed argument parser, used only for documentation purposes (CLI and Sphinx)
    argument_parser: argparse.ArgumentParser

    #: Environment variable handlers
    env_handlers: Mapping[str, KVHandler]

    #: INI file processor
    ini_processor: IniProcessor

    #: Command line arguments handler
    cl_handler: CLStdHandler

    #: Dictionnary of parameters by field name
    params_by_name: Mapping[str, Param[Any]]

    validators: Sequence[Callable[[_Config], Optional[Err]]]

    @staticmethod
    def process_fields(config_type: Type[_Config]) -> Sequence[Arg]:
        """
        Returns a sequence of the arguments present in a configuration, with updated data

        Args:
            config_type: Configuration to process

        Returns:
            Sequence of arguments
        """
        args: List[Arg] = []
        docs: ClassDoc[_Config] = ClassDoc.make(config_type)
        th = get_type_hints(config_type, include_extras=True)
        for name, typ in th.items():
            arg: Optional[Arg] = None
            if get_origin(typ) is ClassVar:
                a = getattr(config_type, name)
                if isinstance(a, Arg):
                    assert isinstance(a, Expander), "Only commands (Cmd) can be class attributes"
                    arg = a
            if get_origin(typ) is Annotated:
                param = filter_types_single(Param, get_args(typ))
                if param is not None:
                    arg = param
            if arg is not None:
                help_lines = docs[name]
                if help_lines is None:
                    help = ""
                else:
                    help = "\n".join(help_lines)
                arg = arg.updated(name, help, config_type.env_prefix_)
                args.append(arg)
        return args

    @staticmethod
    def make(
        config_type: Type[_Config],
    ) -> Processor[_Config]:
        """
        Creates the processor corresponding to a configuration
        """

        pf = ProcessorFactory.make(config_type)
        for arg in Processor.process_fields(config_type):
            arg.update_processor(pf)

        # if these flags are no longer provided by default, update the overview concept notebook
        # in the documentation
        pf.cl_flag_handlers["-h"] = CLSpecialAction(SpecialAction.HELP)
        pf.cl_flag_handlers["--help"] = CLSpecialAction(SpecialAction.HELP)

        return Processor(
            config_type=config_type,
            argument_parser=pf.argument_parser,
            env_handlers=pf.env_handlers,
            ini_processor=IniProcessor(pf.ini_section_strict, pf.ini_handlers),
            cl_handler=CLStdHandler(pf.cl_flag_handlers, CLPos(pf.cl_positionals)),
            params_by_name=pf.params_by_name,
            validators=pf.validators,
        )

    def _process_config(self, cwd: Path, state: State) -> Optional[Err]:
        """
        Processes configuration files if such processing was requested by a handler

        Args:
            cwd: Working directory, base path for relative paths of config files
            state: Mutable state to update

        Returns:
            An optional error
        """
        paths = state.config_files_to_process
        state.config_files_to_process = []
        errors: List[Err] = []
        for p in paths:
            err = self.ini_processor.process(cwd / p, state)
            if err is not None:
                errors.append(err.in_context(ini_file=p))
        return Err.collect(*errors)

    def process_ini_contents(self, ini_contents: str) -> Res[_Config]:
        """
        Processes the configuration in INI format contained in a string

        Args:
            ini_contents: Multiline string containing information in INI format

        Returns:
            The parsed configuration or an error
        """
        state = self._state_with_default_values()
        err = self.ini_processor.process_string(ini_contents, state)
        if err is not None:
            return err
        return self._finish_processing_state(state)

    def process_ini_file(self, ini_file_path: Path) -> Res[_Config]:
        """
        Processes the configuration contained in an INI file

        Args:
            ini_file_path: Path to the file to parse

        Returns:
            The parsed configuration or an error
        """
        state = self._state_with_default_values()
        err = self.ini_processor.process(ini_file_path, state)
        if err is not None:
            return err
        return self._finish_processing_state(state)

    def process(
        self,
        cwd: Path,
        args: Sequence[str],
        env: Mapping[str, str],
    ) -> Res[Union[_Config, SpecialAction]]:
        """
        Processes command-line arguments (deprecated)

        See also: :meth:`.process_command_line`
        """
        warnings.warn(
            "process has been deprecated, use process_command_line instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.process_command_line(cwd, args, env)

    def _finish_processing_state(self, state: State) -> Res[_Config]:
        """
        Finishes the processing of the state

        This method performs:

        - the collection of parameter values
        - the final validation using validation methods

        Args:
            state: State after parsing all elements, must have :attr:`.State.special_action` set
                   to :data:`None`

        Returns:
            The parsed configuration or an error
        """
        assert state.special_action is None
        errors: List[Err] = []
        collected: Dict[str, Any] = {}
        for name, param in self.params_by_name.items():
            instances = state.instances[name]
            res = param.collector.collect(instances)
            if isinstance(res, Err):
                errors.append(res.in_context(param=name))
            else:
                collected[name] = res

        if errors:
            return Err.collect1(*errors)
        c: _Config = self.config_type(**collected)
        validation_error: Optional[Err] = Err.collect(*[f(c) for f in self.validators])
        if validation_error is not None:
            return validation_error
        else:
            return c

    def _state_with_default_values(self) -> State:
        """
        Returns a new state instance with default values populated
        """
        return State.make(self.params_by_name.values())

    def process_command_line(
        self,
        cwd: Path,
        args: Sequence[str],
        env: Mapping[str, str],
    ) -> Res[Union[_Config, SpecialAction]]:
        """
        Processes command-line arguments, configuration files and environment variables

        Args:
            cwd: Working directory, used as a base for configuration file relative paths
            args: Command line arguments to parse
            env: Environment variables

        Returns:
            Either a parsed configuration, a special action to execute, or (a list of) errors
        """
        errors: List[Err] = []
        state = self._state_with_default_values()
        # process environment variables
        for key, value in env.items():
            handler = self.env_handlers.get(key)
            if handler is not None:
                err = handler.handle(value, state)
                if err is not None:
                    errors.append(err.in_context(environment_variable=key))
            err = self._process_config(cwd, state)
            if err is not None:
                errors.append(err.in_context(environment_variable=key))
        # process command line arguments
        rest_args: Sequence[str] = args
        while rest_args:
            rest_args, err = self.cl_handler.handle(rest_args, state)
            if err is not None:
                errors.append(err)
            err = self._process_config(cwd, state)
            if err is not None:
                errors.append(err)

        if state.special_action is not None:
            return state.special_action

        if errors:
            return Err.collect1(*errors)

        return self._finish_processing_state(state)
