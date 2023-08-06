from os import PathLike
from typing_extensions import TypeAlias

import typing

if typing.TYPE_CHECKING:
    from .tool import ToolName


PathList: TypeAlias = typing.Optional[typing.Iterable[typing.Union[str, PathLike]]]
PathTuple: TypeAlias = typing.Optional[typing.Tuple[typing.Union[str, PathLike], ...]]
StrPathOrToolName: TypeAlias = typing.Union[str, PathLike, "ToolName"]
ToolSet: TypeAlias = typing.FrozenSet[StrPathOrToolName]
ToolRequirements: TypeAlias = typing.Mapping[str, ToolSet]
