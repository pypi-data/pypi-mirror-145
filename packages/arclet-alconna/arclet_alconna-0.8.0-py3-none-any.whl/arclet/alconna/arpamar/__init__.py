from typing import Union, Dict, List, Any, Optional, Type
from ..types import DataUnit
from .behavior import ArpamarBehavior, ArpamarBehaviorInterface


class Arpamar:
    """
    亚帕玛尔(Arpamar), Alconna的珍藏宝书

    Example:

    1. `Arpamar.main_args`: 当 Alconna 写入了 main_argument 时,该参数返回对应的解析出来的值

        2. `Arpamar.header`: 当 Alconna 的 command 内写有正则表达式时,该参数返回对应的匹配值

        3. `Arpamar.has`: 判断 Arpamar 内是否有对应的属性

        4. `Arpamar.get`: 返回 Arpamar 中指定的属性

        5. `Arpamar.matched`: 返回命令是否匹配成功

    """

    def __init__(self):
        self.matched: bool = False
        self.headMatched: bool = False
        self.errorData: List[Union[str, Any]] = []
        self.errorInfo: Optional[Union[str, BaseException]] = None
        self._options: Dict[str, Any] = {}
        self._subcommands: Dict[str, Any] = {}
        self._otherArgs: Dict[str, Any] = {}
        self._header: Optional[Union[str, bool]] = None
        self._mainArgs: Dict[str, Any] = {}

        self._cache_args = {}

    __slots__ = [
        "matched", "headMatched", "errorData", "errorInfo", "_options",
        "_subcommands", "_otherArgs", "_header", "_mainArgs", "_cache_args",
    ]

    @property
    def mainArgs(self):
        """返回可能解析到的 main arguments"""
        return self._mainArgs

    @property
    def header(self):
        """返回可能解析到的命令头中的信息"""
        if self._header:
            return self._header
        return self.headMatched

    @property
    def options(self):
        """返回 Alconna 中解析到的所有 Option"""
        return self._options

    @property
    def subcommands(self):
        """返回 Alconna 中解析到的所有 Subcommand """
        return self._subcommands

    @property
    def allMatchedArgs(self):
        """返回 Alconna 中所有 Args 解析到的值"""
        return {**self._mainArgs, **self._otherArgs}

    @property
    def otherArgs(self):
        """返回 Alconna 中所有 Option 和 Subcommand 里的 Args 解析到的值"""
        return self._otherArgs

    @property
    def interface(self):
        return self._interface

    def encapsulateResult(
            self,
            header: Union[str, bool, None],
            main_args: Dict[str, Any],
            options: Dict[str, Any],
            subcommands: Dict[str, Any]
    ) -> None:
        """处理 Arpamar 中的数据"""
        self._header = header
        self._mainArgs = main_args
        self._options = options
        self._subcommands = subcommands
        for k in options:
            v = options[k]
            if isinstance(v, dict):
                self._otherArgs = {**self._otherArgs, **v}
            elif isinstance(v, list):
                _rr = {}
                for i in v:
                    if not isinstance(i, dict):
                        break
                    for kk, vv in i.items():
                        if kk not in _rr:
                            _rr[kk] = [vv]
                        else:
                            _rr[kk].append(vv)

                self._otherArgs = {**self._otherArgs, **_rr}
        for k, v in subcommands.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if not isinstance(vv, dict):
                        self._otherArgs[kk] = vv
                    else:
                        if not self._options.get(kk):
                            self._options[kk] = vv
                        else:
                            self._options[f"{k}_{kk}"] = vv
                        for kkk, vvv in vv.items():
                            if not self._otherArgs.get(kkk):
                                self._otherArgs[kkk] = vvv
                            else:
                                self._otherArgs[f"{k}_{kk}_{kkk}"] = vvv

    def get(self, name: Union[str, Type[DataUnit]]) -> Union[Dict, str, DataUnit, None]:
        """根据选项或者子命令的名字返回对应的数据"""
        if isinstance(name, str):
            if name in self._options:
                return self._options[name]
            if name in self._subcommands:
                return self._subcommands[name]
            if name in self._otherArgs:
                return self._otherArgs[name]
            if name in self._mainArgs:
                return self._mainArgs[name]
        else:
            for _, v in self.allMatchedArgs.items():
                if isinstance(v, name):
                    return v

    def update(self, behaviors: Optional[List[ArpamarBehavior]] = None):
        abi = ArpamarBehaviorInterface(self)
        if behaviors:
            abi.execute(behaviors)
        return self

    def getFirstArg(self, option_name: str) -> Any:
        """根据选项的名字返回第一个参数的值"""
        if option_name in self._options:
            opt_args = self._options[option_name]
            if not isinstance(opt_args, Dict):
                return opt_args
            return list(opt_args.values())[0]
        if option_name in self._subcommands:
            sub_args = self._subcommands[option_name]
            if not isinstance(sub_args, Dict):
                return sub_args
            return list(sub_args.values())[0]

    def has(self, name: str) -> bool:
        """判断 Arpamar 是否有对应的选项/子命令的解析结果"""
        return any(
            [name in self._otherArgs, name in self._options, name in self._mainArgs, name in self._subcommands]
        )

    def __getitem__(self, item: Union[str, Type[DataUnit]]):
        return self.get(item)

    def __getattr__(self, item):
        r_arg = self.allMatchedArgs.get(item)
        if r_arg and not self._cache_args:
            return r_arg
        if all([item in self._options, item in self._subcommands]):
            raise RuntimeError(
                f"{item} is both a option and a subcommand\nplease add prefix 'options.' or 'subcommands.'"
            )
        if item == "options":
            self._cache_args = self._options
            return self
        if item == "subcommands":
            self._cache_args = self._subcommands
            return self
        if self._cache_args and item in self._cache_args:
            _args = self._cache_args[item]
            if not isinstance(_args, dict):
                self._cache_args = {}
                return _args
            else:
                self._cache_args = _args
                return self
        elif item in self._options:
            if not isinstance(self._options[item], dict):
                self._cache_args = {}
                return self._options[item]
            else:
                self._cache_args = self._options[item]
                return self
        elif item in self._subcommands:
            if not isinstance(self._subcommands[item], dict):
                self._cache_args = {}
                return self._subcommands[item]
            else:
                self._cache_args = self._subcommands[item]
                return self
        return

    def __repr__(self):
        if self.errorInfo:
            attrs = ((s, getattr(self, s)) for s in ["matched", "head_matched", "error_data", "error_info"])
            return ", ".join([f"{a}={v}" for a, v in attrs if v is not None])
        else:
            attrs = ((s, getattr(self, s)) for s in [
                "matched", "head_matched", "main_args", "options", "subcommands", "other_args"
            ])
            return ", ".join([f"{a}={v}" for a, v in attrs if v])
