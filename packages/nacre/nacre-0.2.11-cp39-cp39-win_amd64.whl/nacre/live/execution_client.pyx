# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import asyncio

from libc.stdint cimport int64_t
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.live.execution_client cimport LiveExecutionClient as NautilusLiveExecutionClient
from nautilus_trader.model.identifiers cimport AccountId


cdef class LiveExecutionClient(NautilusLiveExecutionClient):
    cpdef void _set_venue(self, Venue venue) except *:
        Condition.not_none(venue, "venue")
        self.venue = venue

    cpdef void _set_account_id(self, AccountId account_id) except *:
        Condition.not_none(account_id, "account_id")
        # Override check
        # Condition.equal(self.id.value, account_id.issuer, "id.value", "account_id.issuer")

        self.account_id = account_id
