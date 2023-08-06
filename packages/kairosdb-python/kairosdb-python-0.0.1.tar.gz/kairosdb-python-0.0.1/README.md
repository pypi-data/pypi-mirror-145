# PyKairosDB

#### A simple Python package to interact with Timeseries Database called Kairos DB.

---------------------------

Requires: Python 3.10 and above

Example:

```python

from kairosdb import KairosDB
from kairosdb.errors import ApiCallError

kdb = KairosDB(
    uri="https://<host>:<port>"
)

sample_query = {
    "start_absolute": 1357023600000,
    "end_relative": {
        "value": "5",
        "unit": "days"
    },
    "time_zone": "Asia/Kabul",
    "metrics": [
        {
            "tags": {
                "host": ["foo", "foo2"],
                "customer": ["bar"]
            },
            "name": "abc.123",
            "limit": 10000,
            "aggregators": [
                {
                    "name": "sum",
                    "sampling": {
                        "value": 10,
                        "unit": "minutes"
                    }
                }
            ]
        },
        {
            "tags": {
                "host": ["foo", "foo2"],
                "customer": ["bar"]
            },
            "name": "xyz.123",
            "aggregators": [
                {
                    "name": "avg",
                    "sampling": {
                        "value": 10,
                        "unit": "minutes"
                    }
                }
            ]
        }
    ]
}
try:
    results = kdb.query(query=sample_query)
    
    print(results)
except ApiCallError as e:
    print(e)
```
