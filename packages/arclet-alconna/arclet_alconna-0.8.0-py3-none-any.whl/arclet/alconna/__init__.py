"""Alconna 概览"""

from typing import TYPE_CHECKING
from .util import splitOnce, split
from .base import CommandNode, Args, ArgAction
from .component import Option, Subcommand
from .arpamar import Arpamar
from .arpamar.duplication import AlconnaDuplication
from .arpamar.stub import ArgsStub, SubcommandStub, OptionStub
from .types import (
    DataUnit, DataCollection, AnyParam, AllParam, Empty,
    AnyStr, AnyIP, AnyUrl, AnyDigit, AnyFloat, Bool, PatternToken, Email, ObjectPattern,
    addCheck
)
from .exceptions import ParamsUnmatched, NullTextMessage, InvalidParam, UnexpectedElement
from .analysis import compile, analyse, analyseArgs, analyseHeader, analyseOption, analyseSubcommand
from .main import Alconna
from .manager import commandManager
from .builtin.actions import storeValue, requireHelpSendAction, setDefault, exclusion, coolDown
from .builtin.construct import AlconnaDecorate, AlconnaFormat, AlconnaString, AlconnaFire
from .builtin.formatter import ArgParserHelpTextFormatter, DefaultHelpTextFormatter
from .visitor import AlconnaNodeVisitor, AbstractHelpTextFormatter


all_command_help = commandManager.getAllCommandHelp
command_broadcast = commandManager.broadcast
delete_command = commandManager.delete
disable_command = commandManager.setDisable
enable_command = commandManager.setEnable
get_command = commandManager.getCommand
get_commands = commandManager.getCommands
alconna_version = (0, 7, 99)

if TYPE_CHECKING:
    from .builtin.actions import version
