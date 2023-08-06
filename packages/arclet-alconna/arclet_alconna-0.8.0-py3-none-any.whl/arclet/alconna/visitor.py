"""
Alconna 负责命令节点访问与帮助文档生成的部分
"""
from typing import List, Dict, Optional, Any, Literal, Union, TYPE_CHECKING
from abc import ABCMeta, abstractmethod
from .exceptions import DuplicateCommand

from .base import CommandNode
from .component import Subcommand, Option

if TYPE_CHECKING:
    from .main import Alconna


class AbstractHelpTextFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, trace: Dict[str, Union[str, List, Dict]]) -> str:
        """
        help text的生成入口
        """
        pass

    @abstractmethod
    def param(self, parameter: Dict[str, Any]) -> str:
        """
        对单个参数的描述
        """
        pass

    @abstractmethod
    def parameters(self, params: List[Dict[str, Any]], separator: str = " ") -> str:
        """
        参数列表的描述
        """
        pass

    @abstractmethod
    def header(self, root: Dict[str, Any]) -> str:
        """
        头部节点的描述
        """
        pass

    @abstractmethod
    def part(self, sub: Dict[str, Any], nodeType: str) -> str:
        """
        每个子节点的描述
        """
        pass

    @abstractmethod
    def body(self, parts: List[Dict[str, Any]]) -> str:
        """
        子节点列表的描述
        """
        pass


class _BaseNode:
    """
    存储命令节点信息的基础类
    """
    nodeId: int
    type: str
    name: str
    parameters: List[Dict[str, Any]]
    description: str
    separator: str
    subNodes: List[int]
    additionalInfo: Dict[str, Any]

    def __init__(self, nid: int, target: CommandNode, node_type: Literal['command', 'subcommand', 'option']):
        self.nodeId = nid
        self.type = node_type
        self.name = target.name
        self.description = target.helpText
        self.parameters = []
        self.separator = target.separator
        self.additionalInfo = {}
        for key, arg in target.args.argument.items():
            self.parameters.append({'name': key, **arg})
        self.subNodes = []

    def __repr__(self):
        res = f'[{self.name}, {self.description}; {self.parameters}; {self.subNodes}]'
        return res


class AlconnaNodeVisitor:
    """
    命令节点访问器
    """
    nameList: List[str]
    nodeMap: Dict[int, _BaseNode]

    def __init__(self, alconna: "Alconna") -> None:
        self.nameList = [alconna.name]
        self.nodeMap = {0: _BaseNode(0, alconna, 'command')}
        self.nodeMap[0].additionalInfo['command'] = alconna.command
        self.nodeMap[0].additionalInfo['headers'] = alconna.headers
        self.nodeMap[0].additionalInfo['namespace'] = alconna.namespace

        for node in alconna.options:
            real_name = node.name.lstrip('-')
            if isinstance(node, Option):
                if "option:" + real_name in self.nameList:
                    raise DuplicateCommand("该选项已经存在")
                self.nameList.append("option:" + real_name)
            elif isinstance(node, Subcommand):
                if "subcommand:" + real_name in self.nameList:
                    raise DuplicateCommand("该子命令已经存在")
                self.nameList.append("subcommand:" + real_name)
            new_id = max(self.nodeMap) + 1
            if isinstance(node, Subcommand):
                self.nodeMap[new_id] = _BaseNode(new_id, node, 'subcommand')
                for sub_node in node.options:
                    real_sub_name = sub_node.name.lstrip('-')
                    if "subcommand:" + real_name + real_sub_name in self.nameList:
                        raise DuplicateCommand("该子命令选项已经存在")
                    self.nameList.append(f"subcommand:{real_name}:{real_sub_name}")
                    sub_new_id = max(self.nodeMap) + 1
                    self.nodeMap[sub_new_id] = _BaseNode(sub_new_id, sub_node, 'option')
                    self.nodeMap[sub_new_id].additionalInfo['aliases'] = sub_node.aliases
                    self.nodeMap[new_id].subNodes.append(sub_new_id)
            else:
                self.nodeMap[new_id] = _BaseNode(new_id, node, 'option')
                self.nodeMap[new_id].additionalInfo['aliases'] = node.aliases
            self.nodeMap[0].subNodes.append(new_id)

    def require(self, path: Optional[Union[str, List[str]]] = None) -> _BaseNode:
        _cache_name = ""
        _cache_node = self.nodeMap[0]
        if path is None:
            return _cache_node
        if isinstance(path, str):
            path = path.split('.')
        for part in path:
            if part in ("option", "subcommand"):
                _cache_name = part
                continue
            if _cache_name:
                _cache_name = _cache_name + ':' + part
                if _cache_name in self.nameList:
                    _cache_node = self.nodeMap[self.nameList.index(_cache_name)]
            else:
                if 'option:' + part in self.nameList and 'subcommand:' + part in self.nameList:
                    raise ValueError("该名称存在歧义, 请指定具体的选项或子命令")
                if "subcommand:" + part in self.nameList:
                    _cache_name = "subcommand:" + part
                    _cache_node = self.nodeMap[self.nameList.index(_cache_name)]
                elif "option:" + part in self.nameList:
                    _cache_name = "option:" + part
                    _cache_node = self.nodeMap[self.nameList.index(_cache_name)]
        return _cache_node

    def traceNodes(self, root: _BaseNode):
        """
        跟踪所有的节点
        """
        return {
            "type": root.type,
            "name": root.name,
            "description": root.description,
            "parameters": root.parameters,
            "separator": root.separator,
            "additional_info": root.additionalInfo,
            "sub_nodes": [self.traceNodes(self.nodeMap[i]) for i in root.subNodes]
        }

    def formatNode(self, formatter: AbstractHelpTextFormatter, node: Optional[_BaseNode] = None) -> str:
        if not node:
            node = self.nodeMap[0]
        return formatter.format(self.traceNodes(node))
