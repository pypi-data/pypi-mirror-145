import abc
import asyncio
import inspect
from asyncio.queues import Queue
from functools import lru_cache
from typing import Optional, Union, Callable, Dict, AsyncIterator, Coroutine, Any, Tuple, TypeVar, Generic
from .types import DataCollection
from .main import Alconna
from .arpamar import Arpamar
from .manager import commandManager
from .builtin.actions import requireHelpSendAction


@lru_cache(4096)
def isCoroutineFunction(o):
    return inspect.iscoroutinefunction(o)


async def runAlwaysAwait(callable_target, *args, **kwargs):
    if isCoroutineFunction(callable_target):
        return await callable_target(*args, **kwargs)
    return callable_target(*args, **kwargs)

T_Origin = TypeVar('T_Origin')
T_Source = TypeVar('T_Source')


class AlconnaProperty(Generic[T_Origin, T_Source]):
    """对解析结果的封装"""

    def __init__(
            self,
            origin: T_Origin,
            result: Arpamar,
            helpText: Optional[str] = None,
            source: Optional[T_Source] = None,
    ):
        self.origin = origin
        self.result = result
        self.helpText = helpText
        self.source = source


class AlconnaMessageProxy(metaclass=abc.ABCMeta):
    """消息解析的代理"""
    loop: asyncio.AbstractEventLoop
    exportResults: Queue
    preTreatments: Dict[
        Alconna,
        Callable[
            [Union[str, DataCollection], Arpamar, Optional[str]],
            AlconnaProperty[Union[str, DataCollection], str]
        ]
    ]

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop or asyncio.get_event_loop()
        self.preTreatments = {}
        self.exportResults = Queue()
        self.defaultPreTreatment = lambda o, r, h, s: AlconnaProperty(o, r, h, s)

    def addProxy(
            self,
            command: Union[str, Alconna],
            preTreatment: Optional[
                Callable[
                    [Union[str, DataCollection], Arpamar, Optional[str]],
                    Union[
                        AlconnaProperty[Union[str, DataCollection], str],
                        Coroutine[None, None, AlconnaProperty[Union[str, DataCollection], str]]
                    ]
                ]
            ] = None,
    ):
        if isinstance(command, str):
            command = commandManager.getCommand(command)  # type: ignore
            if not command:
                raise ValueError(f'Command {command} not found')
        self.preTreatments.setdefault(command, preTreatment or self.defaultPreTreatment)  # type: ignore

    @abc.abstractmethod
    async def fetchMessage(self) -> AsyncIterator[Tuple[Union[str, DataCollection], Any]]:
        """主动拉取消息"""
        yield NotImplemented
        raise NotImplementedError

    @staticmethod
    def laterCondition(result: AlconnaProperty[Union[str, DataCollection], str]) -> bool:
        if not result.result.matched and not result.helpText:
            return False
        return True

    async def pushMessage(
            self,
            message: Union[str, DataCollection],
            source: Optional[Any] = None,
            command: Optional[Alconna] = None,
    ):
        async def __exec(_command, _treatment):
            may_help_text = None

            def _h(string):
                nonlocal may_help_text
                may_help_text = string

            requireHelpSendAction(_h, _command.name)

            _res = _command.parse(message)
            _property = await runAlwaysAwait(_treatment, message, _res, may_help_text, source)
            if not self.laterCondition(_property):
                return
            await self.exportResults.put(_property)
        if command and command in self.preTreatments:
            await __exec(command, self.preTreatments[command])
        else:
            for command, treatment in self.preTreatments.items():
                await __exec(command, treatment)

    async def run(self):
        async for message, source in self.fetchMessage():
            await self.pushMessage(message, source)

    def runBlocking(self):
        self.loop.run_until_complete(self.run())
