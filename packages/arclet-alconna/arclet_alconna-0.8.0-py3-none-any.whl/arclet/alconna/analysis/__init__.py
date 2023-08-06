from typing import TYPE_CHECKING, Union, Callable, Optional, List, Any, Tuple
import traceback

from .analyser import Analyser
from .arg_handlers import multiArgHandler, antiArgHandler, commonArgHandler, unionArgHandler
from .parts import analyseArgs as ala, analyseHeader as alh, analyseOption as alo, analyseSubcommand as als
from ..component import Option, Subcommand
from ..arpamar import Arpamar
from ..types import DataCollection, MultiArg, ArgPattern, AntiArg, UnionArg, ObjectPattern, SequenceArg, MappingArg
from ..base import Args

if TYPE_CHECKING:
    from ..main import Alconna


def compile(alconna: "Alconna", paramsGenerator: Optional[Callable[[Analyser], None]] = None):
    _analyser = alconna.analyserType(alconna)
    if paramsGenerator:
        paramsGenerator(_analyser)
    else:
        Analyser.defaultParamsGenerator(_analyser)
    return _analyser


def analyse(alconna: "Alconna", command: Union[str, DataCollection]) -> Arpamar:
    return compile(alconna).analyse(command)


class AnalyseError(Exception):
    """分析时发生错误"""


class _DummyAnalyser(Analyser):
    filterOut = ["Source", "File", "Quote"]

    def __new__(cls, *args, **kwargs):

        cls.addArgHandler(MultiArg, multiArgHandler)
        cls.addArgHandler(ArgPattern, commonArgHandler)
        cls.addArgHandler(AntiArg, antiArgHandler)
        cls.addArgHandler(UnionArg, unionArgHandler)
        cls.addArgHandler(ObjectPattern, commonArgHandler)
        cls.addArgHandler(SequenceArg, commonArgHandler)
        cls.addArgHandler(MappingArg, commonArgHandler)
        cls.commandParams = {}
        return super().__new__(cls)

    def analyse(self, message: Union[str, DataCollection, None] = None):
        pass

    def createArpamar(self, exception: Optional[BaseException] = None, fail: bool = False):
        pass

    def addParam(self, opt):
        pass


def analyseArgs(
        args: Args,
        command: Union[str, DataCollection],
        sep: str = " "
):
    _analyser = _DummyAnalyser.__new__(_DummyAnalyser)
    _analyser.reset()
    _analyser.separator = ' '
    _analyser.isRaiseException = True
    try:
        _analyser.handleMessage(command)
        return ala(_analyser, args, sep, len(args))
    except Exception as e:
        traceback.print_exception(AnalyseError, e, e.__traceback__)


def analyseHeader(
        headers: Union[List[Union[str, Any]], List[Tuple[Any, str]]],
        commandName: str,
        command: Union[str, DataCollection],
        sep: str = " "
):
    _analyser = _DummyAnalyser.__new__(_DummyAnalyser)
    _analyser.reset()
    _analyser.separator = sep
    _analyser.isRaiseException = True
    _analyser.handleMessage(command)
    _analyser.__initHeader__(commandName, headers)
    r = alh(_analyser)
    if r is False:
        traceback.print_exception(
            AnalyseError, AnalyseError(f"header {_analyser.recoverRawData()} analyse failed"), None
        )
    return r


def analyseOption(
        option: Option,
        command: Union[str, DataCollection],
):
    _analyser = _DummyAnalyser.__new__(_DummyAnalyser)
    _analyser.reset()
    _analyser.separator = " "
    _analyser.isRaiseException = True
    try:
        _analyser.handleMessage(command)
        return alo(_analyser, option)
    except Exception as e:
        traceback.print_exception(AnalyseError, e, e.__traceback__)


def analyseSubcommand(
        subcommand: Subcommand,
        command: Union[str, DataCollection],
):
    _analyser = _DummyAnalyser.__new__(_DummyAnalyser)
    _analyser.reset()
    _analyser.separator = " "
    _analyser.isRaiseException = True
    try:
        _analyser.handleMessage(command)
        return als(_analyser, subcommand)
    except Exception as e:
        traceback.print_exception(AnalyseError, e, e.__traceback__)
