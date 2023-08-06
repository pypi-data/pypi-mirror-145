#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Exchange library DI container
"""

# pylint: disable=no-value-for-parameter

# Library dependencies
from typing import List, Optional

# Library dependencies
from kink import di, inject

# Library libs
from fastybird_exchange.consumer import Consumer
from fastybird_exchange.publisher import IPublisher, IQueue, Publisher


def register_services() -> None:
    """Create exchange services"""
    di[Publisher] = Publisher()
    di["fb-exchange_publisher"] = di[Publisher]

    di[Consumer] = Consumer()
    di["fb-exchange_consumer"] = di[Consumer]

    @inject(
        bind={
            "queue": IQueue,
            "publishers": List[IPublisher],
        }
    )
    def register_queue(queue: Optional[IQueue] = None, publishers: Optional[List[IPublisher]] = None) -> None:
        if queue is None:
            return

        di[Publisher].register_queue(queue=queue)

        if publishers is not None:
            queue.set_publishers(publishers=publishers)

    register_queue()
