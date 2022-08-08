# Copyright 2021 Research Institute of Systems Planning, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Union

from .path_base import PathBase
from ..common import Summarizable, Summary
from ..infra.interface import RecordsProvider, RuntimeDataProvider
from ..record import RecordsInterface
from ..value_objects import Qos, SubscriptionStructValue


class Subscription(PathBase, Summarizable):
    """A class that represents subscription."""

    def __init__(
        self,
        val: SubscriptionStructValue,
        data_provider: Union[RecordsProvider, RuntimeDataProvider],
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        val : SubscriptionStructValue
            static info.
        data_provider : Union[RecordsProvider, RuntimeDataProvider]
            provider to be evaluated.

        """
        super().__init__()
        self._val = val
        self._provider = data_provider

    @property
    def node_name(self) -> str:
        """
        Get node name.

        Returns
        -------
        str
            node name to which the subscription subscribes.

        """
        return self._val.node_name

    @property
    def summary(self) -> Summary:
        """
        Get summary [override].

        Returns
        -------
        Summary
            summary info.

        """
        return self._val.summary

    @property
    def topic_name(self) -> str:
        """
        Get a topic name.

        Returns
        -------
        str
            A topic name to which the subscription subscribes.

        """
        return self._val.topic_name

    @property
    def callback_name(self) -> Optional[str]:
        """
        Get a subscription callback name.

        Returns
        -------
        Optional[str]
            callback name to which the subscription is attached.

        """
        return self._val.callback_name

    @property
    def qos(self) -> Optional[Qos]:
        """
        Get QoS.

        Returns
        -------
        Optional[Qos]
            Subscription QoS.

        """
        if isinstance(self._provider, RuntimeDataProvider):
            return self._provider.get_qos(self._val)
        return None

    def _to_records_core(self) -> RecordsInterface:
        """
        Calculate records.

        Returns
        -------
        RecordsInterface
            Subscribe records.

        """
        records = self._provider.subscribe_records(self._val)
        return records