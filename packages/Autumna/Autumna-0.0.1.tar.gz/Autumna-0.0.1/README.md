
# Unofficial Autumna Python API client

Unofficial Autumna.co.uk API Client for Python.


## Installation

```
pip install autumna
```


## Requirements

- Python 3.7+


# Usage

```Python

import datetime

from autumna.client import APIClient
from autumna.constants import Category
from autumna.resources.lead import Lead

api_client = APIClient('MY_API_KEY')

leads = Lead.many(
    api_client,
    date_from=datetime.date(2022, 1, 1),
    date_to=datetime.date(2022, 4, 1),
    is_anonymised=False,
    category_id=Category.CONTACT_FORM_MESSAGE,
    service_id=28058
)

for lead in leads:
    print(lead)

```
