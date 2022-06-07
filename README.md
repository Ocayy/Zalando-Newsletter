# Zalando-Newsletter
Zalando-Newsletter is a discount code generator for orders above 200 PLN.

## Features
- Create temp mail to avoid spam messages
- Automatically confirms email using requests
- Possibility to save codes in text file
- Supports multiple regions

## Tech
Zalando-Newsletter uses built-in [Python](https://www.python.org) packages and open source package named [requests](https://github.com/psf/requests) to work properly:

## Installation

Zalando-Newsletter requires [Python 3.10](https://nodejs.org/) to run.

Install via pip:
```
pip install -r requirements.txt
```

## Example Usage
```py
from module import *

generator = ZalandoNewsletter()
newsletter_code = generator.generate_code("pl", True)
print(newsletter_code)
```