# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from typing import (
    Any,
    AnyStr,
    List,
)
from attr import (
    define,
    field
)


@define
class Package:
    author: AnyStr = field()
    authorEmail: AnyStr = field()
    disabled: bool = field()
    homePage: AnyStr = field()
    id: AnyStr = field()
    license: AnyStr = field()
    name: AnyStr = field()
    pythonVersion: AnyStr = field()
    requires: List = field()
    summary: AnyStr = field()
    version: AnyStr = field()
    fileId: AnyStr = field(default=None)
