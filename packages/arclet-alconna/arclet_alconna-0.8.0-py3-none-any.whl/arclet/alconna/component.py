"""Alconna 的组件相关"""
from typing import Union, Dict, List, Any, Optional, Callable, Iterable
from .base import CommandNode, Args, ArgAction


class Option(CommandNode):
    """命令选项, 可以使用别名"""
    aliases: List[str]

    def __init__(
            self,
            name: str,
            args: Union[Args, str, None] = None,
            alias: Optional[List[str]] = None,
            action: Optional[Union[ArgAction, Callable]] = None,
            separator: Optional[str] = None,
            helpText: Optional[str] = None,

    ):
        self.aliases = alias if alias else []
        if "|" in name:
            aliases = name.replace(' ', '').split('|')
            aliases.sort(key=len, reverse=True)
            name = aliases[0]
            self.aliases.extend(aliases[1:])
        self.aliases.insert(0, name)
        super().__init__(name, args, action, separator, helpText)

    def toDict(self) -> Dict[str, Any]:
        return {**super().toDict(), "aliases": self.aliases}

    def __getstate__(self):
        return self.toDict()

    @classmethod
    def fromDict(cls, data: Dict[str, Any]) -> "Option":
        name = data['name']
        aliases = data['aliases']
        args = Args.fromDict(data['args'])
        opt = cls(name, args, alias=aliases, separator=data['separator'], helpText=data['help_text'])
        return opt

    def __setstate__(self, state):
        self.__init__(
            state['name'],
            Args.fromDict(state['args']),
            alias=state['aliases'],
            separator=state['separator'],
            helpText=state['help_text']
        )


class Subcommand(CommandNode):
    """子命令, 次于主命令, 可解析 SubOption"""
    options: List[Option]
    subParams: Dict[str, Option]
    subPartLength: range

    def __init__(
            self,
            name: str,
            options: Optional[Iterable[Option]] = None,
            args: Union[Args, str, None] = None,
            action: Optional[Union[ArgAction, Callable]] = None,
            separator: Optional[str] = None,
            helpText: Optional[str] = None,
    ):
        self.options = list(options or [])
        super().__init__(name, args, action, separator, helpText)
        self.subParams = {}
        self.subPartLength = range(self.nargs)

    def toDict(self) -> Dict[str, Any]:
        return {**super().toDict(), "options": [option.toDict() for option in self.options]}

    def __getstate__(self):
        return self.toDict()

    @classmethod
    def fromDict(cls, data: Dict[str, Any]) -> "Subcommand":
        name = data['name']
        options = [Option.fromDict(option) for option in data['options']]
        args = Args.fromDict(data['args'])
        sub = cls(name, options, args, separator=data['separator'], helpText=data['help_text'])
        return sub

    def __setstate__(self, state):
        self.__init__(
            state['name'],
            [Option.fromDict(option) for option in state['options']],
            args=Args.fromDict(state['args']),
            separator=state['separator'],
            helpText=state['help_text']
        )
