# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from typing import (
    AnyStr,
    List
)
from attr import (
    define,
    field
)


@define
class WorkflowBase:
    id: AnyStr = field()
    name: AnyStr = field()
    disabled: bool = field()
    parentId: AnyStr = field()

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class ActionBase(WorkflowBase):
    actionType: AnyStr = field()

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class TaskAction(ActionBase):
    autoRun: bool = field()
    taskId: AnyStr = field(default=None)

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class FieldSetAction(ActionBase):
    fieldId: AnyStr = field(default=None)
    value: AnyStr or dict = field(default=None)
    dateActionModifier: AnyStr = field(default=None)
    dateActionType: AnyStr = field(default=None)

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class LayoutAction(ActionBase):
    layoutActions: dict = field(default={})

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class FieldStateAction(ActionBase):
    fieldStates: dict = field(default={})

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)
    

@define
class FilterValuesAction(ActionBase):
    valuesListsIds: List = field(default=[])
    fieldId: AnyStr = field(default=None)

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)

@define
class NotificationAction(ActionBase):
    message: AnyStr = field(default=None)
    recipients: List = field(default=[])
    subject: AnyStr = field(default=None)

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class Condition:
    conditionType: AnyStr = field()
    fieldId: AnyStr = field()
    isCaseSensitive: bool = field()
    value: AnyStr = field(default=None)
    referenceFieldConjunction: AnyStr or int = field(default=None)
    referencedApplicationFieldId: AnyStr = field(default=None)

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)


@define
class StageCondition(WorkflowBase):
    conditionType: AnyStr = field()
    evalType: int or AnyStr = field()
    conditions: List = field(default=[])
    actions: List = field(default=[])
    repeats: List = field(default=[])
    stages: List = field(default=[])

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)

    def __attrs_post_init__(self):
        if self.conditions:
            return_list = []
            for condition in self.conditions:
                try:
                    return_list.append(Condition(**condition))
                except Exception as e:
                    import pprint
                    pprint.pprint(condition)
                    raise e
            self.conditions = return_list
        if self.actions:
            return_list = []
            for action in self.actions:
                value = None
                for item in [StageCondition, FieldStateAction, LayoutAction, FieldSetAction, TaskAction, NotificationAction, FilterValuesAction]:
                    try:
                        value = item(**action)
                    except Exception as e:
                        pass
                if value:
                    return_list.append(value)
                else:
                    import pprint
                    pprint.pprint(self.actions)

            if not len(return_list) == len(self.actions):
                raise f"Formatted objects are different than provided dictionaries."
            self.actions = return_list
        if self.stages:
            return_list = []
            for stage in self.stages:
                try:
                    return_list.append(StageCondition(**stage))
                except Exception as e:
                    raise e
            self.stages = return_list


@define
class Workflow:
    applicationId: AnyStr = field()
    permissions: dict = field()
    uid: AnyStr = field()
    version: int = field()
    id: AnyStr = field()
    disabled: bool = field()
    stages: List = field(default=[])

    def __init__(self, **kwargs):
        from ..base import Base
        Base().scrub(kwargs)
        self.__attrs_init__(**kwargs)

    def __attrs_post_init__(self):
        if self.stages:
            return_list = []
            for stage in self.stages:
                try:
                    return_list.append(StageCondition(**stage))
                except Exception as e:
                    raise e
            self.stages = return_list
