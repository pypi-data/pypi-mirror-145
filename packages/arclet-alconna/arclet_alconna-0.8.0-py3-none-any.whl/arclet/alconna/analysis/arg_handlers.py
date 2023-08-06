import re
from typing import Union, Dict, Any

from ..types import MultiArg, ArgPattern, DataUnit, PatternToken, AntiArg, Empty, UnionArg, TypePattern
from .analyser import Analyser
from ..exceptions import ParamsUnmatched, ArgumentMissing


def multiArgHandler(
        analyser: Analyser,
        mayArg: Union[str, DataUnit],
        key: str,
        value: MultiArg,
        default: Any,
        nargs: int,
        sep: str,
        resultDict: Dict[str, Any],
        optional: bool
):
    _m_arg_base = value.argValue
    if _m_arg_base.__class__ is ArgPattern:
        if not isinstance(mayArg, str):
            return
    elif isinstance(mayArg, str):
        return
    # 当前args 已经解析 m 个参数， 总共需要 n 个参数，总共剩余p个参数，
    # q = n - m 为剩余需要参数（包括自己）， p - q + 1 为自己可能需要的参数个数
    _m_rest_arg = nargs - len(resultDict) - 1
    _m_all_args_count = analyser.getRestDataCount(sep) - _m_rest_arg + 1
    analyser.reduceData(mayArg)
    if value.flag == 'args':
        result = []

        def __putback(data):
            analyser.reduceData(data)
            for ii in range(min(len(result), _m_rest_arg)):
                analyser.reduceData(result.pop(-1))

        for i in range(_m_all_args_count):
            _m_arg, _m_str = analyser.getNextData(sep)
            if _m_str and _m_arg in analyser.paramIds:
                __putback(_m_arg)
                break
            if _m_arg_base.__class__ is ArgPattern:
                if not _m_str:
                    analyser.reduceData(_m_arg)
                    break
                _m_arg_find = _m_arg_base.find(_m_arg)
                if not _m_arg_find:
                    analyser.reduceData(_m_arg)
                    break
                if _m_arg_base.token == PatternToken.REGEX_TRANSFORM and isinstance(_m_arg_find, str):
                    _m_arg_find = _m_arg_base.transformAction(_m_arg_find)
                if _m_arg_find == _m_arg_base.pattern:
                    _m_arg_find = Ellipsis
                result.append(_m_arg_find)
            else:
                if _m_str:
                    __putback(_m_arg)
                    break
                if _m_arg.__class__ is _m_arg_base:
                    result.append(_m_arg)
                elif isinstance(value, type) and isinstance(mayArg, value):
                    result.append(_m_arg)
                else:
                    analyser.reduceData(_m_arg)
                    break
        if len(result) == 0:
            result = [default] if default else []
        resultDict[key] = tuple(result)
    else:
        result = {}

        def __putback(data):
            analyser.reduceData(data)
            for ii in range(min(len(result), _m_rest_arg)):
                arg = result.popitem()  # type: ignore
                analyser.reduceData(arg[0] + '=' + arg[1])

        for i in range(_m_all_args_count):
            _m_arg, _m_str = analyser.getNextData(sep)
            if _m_str and _m_arg in analyser.commandParams:
                __putback(_m_arg)
                break
            if _m_arg_base.__class__ is ArgPattern:
                if not _m_str:
                    analyser.reduceData(_m_arg)
                    break
                _kwarg = re.findall(r'^(.*)=(.*)$', _m_arg)
                if not _kwarg:
                    analyser.reduceData(_m_arg)
                    break
                _key, _m_arg = _kwarg[0]
                _m_arg_find = _m_arg_base.find(_m_arg)
                if not _m_arg_find:
                    analyser.reduceData(_m_arg)
                    break
                if _m_arg_base.token == PatternToken.REGEX_TRANSFORM and isinstance(_m_arg_find, str):
                    _m_arg_find = _m_arg_base.transformAction(_m_arg_find)
                if _m_arg_find == _m_arg_base.pattern:
                    _m_arg_find = Ellipsis
                result[_key] = _m_arg_find
            else:
                if _m_str:
                    _kwarg = re.findall(r'^(.*)=.*?$', _m_arg)
                    if not _kwarg:
                        __putback(_m_arg)
                        break
                    _key = _kwarg[0]
                    _m_arg, _m_str = analyser.getNextData(sep)
                    if _m_str:
                        __putback(_m_arg)
                        break
                    if _m_arg.__class__ is _m_arg_base:
                        result[_key] = _m_arg
                    elif isinstance(value, type) and isinstance(mayArg, value):
                        result[_key] = _m_arg
                    else:
                        analyser.reduceData(_m_arg)
                        break
                else:
                    analyser.reduceData(_m_arg)
                    break
        if len(result) == 0:
            result = [default] if default else []
        resultDict[key] = result


def antiArgHandler(
        analyser: Analyser,
        mayArg: Union[str, DataUnit],
        key: str,
        value: AntiArg,
        default: Any,
        nargs: int,
        sep: str,
        resultDict: Dict[str, Any],
        optional: bool
):
    _a_arg_base = value.argValue
    if _a_arg_base.__class__ is ArgPattern:
        arg_find = _a_arg_base.find(mayArg)
        if not arg_find:   # and isinstance(may_arg, str):
            resultDict[key] = mayArg
        else:
            analyser.reduceData(mayArg)
            if default is None:
                if optional:
                    return
                raise ParamsUnmatched(f"param {mayArg} is incorrect")
            resultDict[key] = None if default is Empty else default
    else:
        if mayArg.__class__ is not _a_arg_base:
            resultDict[key] = mayArg
        elif default is not None:
            resultDict[key] = None if default is Empty else default
            analyser.reduceData(mayArg)
        else:
            analyser.reduceData(mayArg)
            if optional:
                return
            if mayArg:
                raise ParamsUnmatched(f"param type {mayArg.__class__} is incorrect")
            else:
                raise ArgumentMissing(f"param {key} is required")


def unionArgHandler(
        analyser: Analyser,
        mayArg: Union[str, DataUnit],
        key: str,
        value: UnionArg,
        default: Any,
        nargs: int,
        sep: str,
        resultDict: Dict[str, Any],
        optional: bool
):
    if not value.anti:
        not_equal = True
        not_match = True
        not_check = True
        if mayArg in value.forEqual:
            not_equal = False

        if not_equal:
            for pat in value.forMatch:
                if arg_find := pat.find(mayArg):
                    not_match = False
                    mayArg = arg_find
                    if isinstance(pat, TypePattern):
                        break
                    if pat.token == PatternToken.REGEX_TRANSFORM and isinstance(mayArg, str):
                        mayArg = pat.transformAction(mayArg)
                    if mayArg == pat.pattern:
                        mayArg = Ellipsis  # type: ignore
                    break
        if not_match:
            for t in value.forTypeCheck:
                if isinstance(mayArg, t):
                    not_check = False
                    break
        result = all([not_equal, not_match, not_check])
    else:
        equal = False
        match = False
        type_check = False
        if mayArg in value.forEqual:
            equal = True
        for pat in value.forMatch:
            if pat.find(mayArg):
                match = True
                break
        for t in value.forTypeCheck:
            if isinstance(mayArg, t):
                type_check = True
                break

        result = any([equal, match, type_check])

    if result:
        analyser.reduceData(mayArg)
        if default is None:
            if optional:
                return
            if mayArg:
                raise ParamsUnmatched(f"param {mayArg} is incorrect")
            else:
                raise ArgumentMissing(f"param {key} is required")
        mayArg = None if default is Empty else default  # type: ignore
    resultDict[key] = mayArg


def commonArgHandler(
        analyser: Analyser,
        mayArg: Union[str, DataUnit],
        key: str,
        value: ArgPattern,
        default: Any,
        nargs: int,
        sep: str,
        resultDict: Dict[str, Any],
        optional: bool
):
    arg_find = value.find(mayArg)
    if not arg_find:
        analyser.reduceData(mayArg)
        if default is None:
            if optional:
                return
            if mayArg:
                raise ParamsUnmatched(f"param {mayArg} is incorrect")
            else:
                raise ArgumentMissing(f"param {key} is required")
        else:
            arg_find = None if default is Empty else default
    if value.token == PatternToken.REGEX_TRANSFORM and isinstance(arg_find, str):
        arg_find = value.transformAction(arg_find)
    if arg_find == value.pattern:
        arg_find = Ellipsis
    resultDict[key] = arg_find
