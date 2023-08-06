#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Helper functions to handle OpenMetadata Entities' properties
"""

import re
import string
from typing import Type, TypeVar, Union
import logging
import time
from pydantic import BaseModel

from metadata.generated.schema.type import basic

T = TypeVar("T", bound=BaseModel)

logger: logging.Logger = logging.getLogger(__name__)

def format_name(name: str) -> str:
    """
    Given a name, replace all special characters by `_`
    :param name: name to format
    :return: formatted string
    """
    subs = re.escape(string.punctuation + " ")
    return re.sub(r"[" + subs + "]", "_", name)


def get_entity_type(
    entity: Union[Type[T], str],
) -> str:
    """
    Given an Entity T, return its type.
    E.g., Table returns table, Dashboard returns dashboard...

    Also allow to be the identity if we just receive a string
    """
    if isinstance(entity, str):
        return entity

    class_name: str = entity.__name__.lower()

    if "service" in class_name:
        # Capitalize service, e.g., pipelineService
        return class_name.replace("service", "Service")

    return class_name


def uuid_to_str(entity_id: Union[str, basic.Uuid]) -> str:
    """
    Given an entity_id, that can be a str or our pydantic
    definition of Uuid, return a proper str to build
    the endpoint path
    :param entity_id: Entity ID to onvert to string
    :return: str for the ID
    """
    if isinstance(entity_id, basic.Uuid):
        return str(entity_id.__root__)

    return entity_id

def timer(method):
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        logger.trace("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def add_logging_level(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)