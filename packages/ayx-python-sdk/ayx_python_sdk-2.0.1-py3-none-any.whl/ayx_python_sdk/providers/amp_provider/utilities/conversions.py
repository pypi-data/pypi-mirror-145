# Copyright (C) 2021 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Conversion methods for AMP Provider classes."""
from datetime import datetime, timedelta

from pyarrow import Date32Scalar, int32

# Alteryx Epoch is based closely on Excel's, not UNIX
ALTERYX_DATE32_EPOCH = datetime(1900, 1, 1, 0, 0)


def arrow_scalar_date32_to_py(arrow_date: Date32Scalar) -> datetime:
    """
    Convert a Arrow Date32Scalar to a Python datetime object.

    Parameters
    ----------
    arrow_date
        An Arrow date represented as days since Epoch.

    Returns
    -------
    datetime
        The converted date value.
    """
    return ALTERYX_DATE32_EPOCH + timedelta(arrow_date.cast(int32()).as_py() - 2)
