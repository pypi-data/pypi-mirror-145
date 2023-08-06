import re
from abc import ABCMeta, abstractmethod
from typing import Dict, Union, List, Optional, TYPE_CHECKING, Tuple, Any, Type, Callable

from arclet.alconna import NullTextMessage, UnexpectedElement

from ..base import Args
from ..component import Option, Subcommand
from ..arpamar import Arpamar
from ..util import splitOnce, split
from ..types import DataUnit, ArgPattern, DataCollection

if TYPE_CHECKING:
    from ..main import Alconna


class Analyser(metaclass=ABCMeta):
    """
    Alconna使用的分析器基类, 实现了一些通用的方法

    Attributes:
        currentIndex(int): 记录解析时当前数据的index
        contentIndex(int): 记录内部index
        headMatched: 是否匹配了命令头部
    """
    alconna: 'Alconna'  # Alconna实例
    currentIndex: int  # 当前数据的index
    contentIndex: int  # 内部index
    isStringOnly: bool  # 是否是字符串
    rawData: Dict[int, Union[List[str], Any]]  # 原始数据
    ndata: int  # 原始数据的长度
    commandParams: Dict[str, Union[Option, Subcommand]]  # 参数
    paramIds: List[str]
    # 命令头部
    commandHeader: Union[
        ArgPattern,
        Tuple[Union[Tuple[List[Any], ArgPattern], List[Any]], ArgPattern],
        List[Tuple[Any, ArgPattern]]
    ]
    separator: str  # 分隔符
    isRaiseException: bool  # 是否抛出异常
    options: Dict[str, Any]  # 存放解析到的所有选项
    subcommands: Dict[str, Any]  # 存放解析到的所有子命令
    mainArgs: Dict[str, Any]  # 主参数
    header: Optional[Union[str, bool]]  # 命令头部
    isNeedMainArgs: bool  # 是否需要主参数
    headMatched: bool  # 是否匹配了命令头部
    partLength: range  # 分段长度
    isMainArgsDefaultOnly: bool  # 默认只有主参数
    selfArgs: Args  # 自身参数
    ARGHANDLER_TYPE = Callable[["Analyser", Union[str, DataUnit], str, Type, Any, int, str, Dict[str, Any], bool], Any]
    argHandlers: Dict[Type, ARGHANDLER_TYPE]
    filterOut: List[str]  # 元素黑名单

    def __init_subclass__(cls, **kwargs):
        cls.argHandlers = {}
        for base in reversed(cls.__bases__):
            if issubclass(base, Analyser):
                cls.argHandlers.update(getattr(base, "arg_handlers", {}))
        if not hasattr(cls, "filter_out"):
            raise TypeError("Analyser subclass must define filter_out")

    @classmethod
    def addArgHandler(cls, arg_type: Type, handler: Optional[ARGHANDLER_TYPE] = None):
        if handler:
            cls.argHandlers[arg_type] = handler
            return handler

        def __wrapper(func):
            cls.argHandlers[arg_type] = func
            return func

        return __wrapper

    def __init__(self, alconna: "Alconna"):
        self.reset()
        self.alconna = alconna
        self.selfArgs = alconna.args
        self.separator = alconna.separator
        self.isRaiseException = alconna.isRaiseException
        self.isNeedMainArgs = False
        self.isMainArgsDefaultOnly = False
        self.__handleMainArgs__(alconna.args, alconna.nargs)
        self.__initHeader__(alconna.command, alconna.headers)

    def __handleMainArgs__(self, mainArgs: Args, nargs: Optional[int] = None):
        nargs = nargs or len(mainArgs)
        if nargs > 0 and nargs > mainArgs.optionalCount:
            self.isNeedMainArgs = True  # 如果need_marg那么match的元素里一定得有main_argument
        _de_count = 0
        for k, a in mainArgs.argument.items():
            if a['default'] is not None:
                _de_count += 1
        if _de_count and _de_count == nargs:
            self.isMainArgsDefaultOnly = True

    def __initHeader__(
            self,
            commandName: str,
            headers: Union[List[Union[str, DataUnit]], List[Tuple[DataUnit, str]]]
    ):
        if headers != [""]:
            if isinstance(headers[0], tuple):
                mixins = []
                for h in headers:  
                    mixins.append((h[0], ArgPattern(re.escape(h[1]) + commandName)))  # type: ignore
                self.commandHeader = mixins
            else:
                elements = []
                ch_text = ""
                for h in headers:
                    if isinstance(h, str):
                        ch_text += re.escape(h) + "|"
                    else:
                        elements.append(h)
                if not elements:
                    self.commandHeader = ArgPattern("(?:{})".format(ch_text[:-1]) + commandName)
                elif not ch_text:
                    self.commandHeader = (elements, ArgPattern(commandName))
                else:
                    self.commandHeader = (
                        (elements, ArgPattern("(?:{})".format(ch_text[:-1]))), ArgPattern(commandName)
                    )
        else:
            self.commandHeader = ArgPattern(commandName)

    @staticmethod
    def defaultParamsGenerator(analyser: "Analyser"):
        analyser.paramIds = []
        analyser.commandParams = {}
        for opts in analyser.alconna.options:
            if isinstance(opts, Subcommand):
                analyser.paramIds.append(opts.name)
                for sub_opts in opts.options:
                    opts.subParams.setdefault(sub_opts.name, sub_opts)
                    analyser.paramIds.extend(sub_opts.aliases)
                opts.subPartLength = range(len(opts.options) + 1)
            else:
                analyser.paramIds.extend(opts.aliases)
            analyser.commandParams[opts.name] = opts
        analyser.partLength = range(len(analyser.commandParams) + 1)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __del__(self):
        self.reset()

    def reset(self):
        """重置分析器"""
        self.currentIndex = 0
        self.contentIndex = 0
        self.isStringOnly = False
        self.options = {}
        self.mainArgs = {}
        self.subcommands = {}
        self.header = None
        self.rawData = {}
        self.headMatched = False
        self.ndata = 0

    def getNextData(self, separate: Optional[str] = None, pop: bool = True) -> Tuple[Union[str, Any], bool]:
        """获取解析需要的下个数据"""
        if self.currentIndex == self.ndata:
            return "", True
        _current_data = self.rawData[self.currentIndex]
        if isinstance(_current_data, list):
            _rest_text: str = ""
            _text = _current_data[self.contentIndex]
            if separate and separate != self.separator:
                _text, _rest_text = splitOnce(_text, separate)
            if pop:
                if _rest_text:  # 这里实际上还是pop了
                    self.rawData[self.currentIndex][self.contentIndex] = _rest_text
                else:
                    self.contentIndex += 1
            if len(_current_data) == self.contentIndex:
                self.currentIndex += 1
                self.contentIndex = 0
            return _text, True
        if pop:
            self.currentIndex += 1
        return _current_data, False

    def getRestDataCount(self, separate: Optional[str] = None) -> int:
        """获取剩余的数据个数"""
        _result = 0
        for i in self.rawData:
            if i < self.currentIndex:
                continue
            if isinstance(self.rawData[i], list):
                for s in self.rawData[i][self.contentIndex:]:
                    if separate and self.separator != separate:
                        _result += len(split(s, separate))
                    _result += 1
            else:
                _result += 1
        return _result

    def reduceData(self, data: Union[str, Any]):
        """把pop的数据放回 (实际只是‘指针’移动)"""
        if not data:
            return
        if self.currentIndex == self.ndata:
            self.currentIndex -= 1
            if isinstance(data, str):
                self.contentIndex = len(self.rawData[self.currentIndex]) - 1
        else:
            _current_data = self.rawData[self.currentIndex]
            if isinstance(_current_data, list) and isinstance(data, str):
                self.contentIndex -= 1
            else:
                self.currentIndex -= 1

    def recoverRawData(self) -> List[Union[str, Any]]:
        """将处理过的命令数据大概还原"""
        _result = []
        for i in self.rawData:
            if i < self.currentIndex:
                continue
            if isinstance(self.rawData[i], list):
                _result.append(f'{self.separator}'.join(self.rawData[i][self.contentIndex:]))
            else:
                _result.append(self.rawData[i])
        self.currentIndex = self.ndata
        self.contentIndex = 0
        return _result

    def handleMessage(self, data: Union[str, DataCollection]) -> Optional[Arpamar]:
        """命令分析功能, 传入字符串或消息链, 应当在失败时返回fail的arpamar"""
        if isinstance(data, str):
            self.isStringOnly = True
            if not (res := split(data.lstrip(), self.separator)):
                if self.isRaiseException:
                    raise NullTextMessage("传入了空的字符串")
                return self.createArpamar(fail=True, exception=NullTextMessage("传入了空的字符串"))
            self.rawData = {0: res}
            self.ndata = 1
        else:
            separate = self.separator
            i, __t, exc = 0, False, None
            raw_data: Dict[int, Any] = {}
            for unit in data:  # type: ignore
                if text := getattr(unit, 'text', None):
                    if not (res := split(text.lstrip(' '), separate)):
                        continue
                    raw_data[i] = res
                    __t = True
                elif isinstance(unit, str):
                    if not (res := split(unit.lstrip(' '), separate)):
                        continue
                    raw_data[i] = res
                    __t = True
                elif unit.__class__.__name__ not in self.filterOut:
                    raw_data[i] = unit
                else:
                    if self.isRaiseException:
                        exc = UnexpectedElement(f"{unit.type}({unit})")
                    continue
                i += 1
            if __t is False:
                if self.isRaiseException:
                    raise NullTextMessage("传入了一个无法获取文本的消息链")
                return self.createArpamar(fail=True, exception=NullTextMessage("传入了一个无法获取文本的消息链"))
            if exc:
                if self.isRaiseException:
                    raise exc
                return self.createArpamar(fail=True, exception=exc)
            self.rawData = raw_data
            self.ndata = i

    @abstractmethod
    def analyse(self, message: Union[str, DataCollection, None] = None) -> Arpamar:
        """主体解析函数, 应针对各种情况进行解析"""
        pass

    @abstractmethod
    def createArpamar(self, exception: Optional[BaseException] = None, fail: bool = False) -> Arpamar:
        """创建arpamar, 其一定是一次解析的最后部分"""
        pass

    @abstractmethod
    def addParam(self, opt):
        """临时增加解析用参数"""
        pass
