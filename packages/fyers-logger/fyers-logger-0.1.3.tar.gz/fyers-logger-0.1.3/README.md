README
========

This module is installed via pip:

```
pip install fyers-logger
```

Packages Required
 - aws-lambda-powertools


Usage

```
from fyers_logger import FyersLogger

logger = FyersLogger("ServiceName", "DEBUG")
```

Additional parameters

```
import logging
logger = FyersLogger("ServiceName", "DEBUG", logger_handler=logging.FileHandler("filename.log"))
```

Since this is an extension of the aws-lambda-powertools logger, all parameters supported by aws-lambda-powertools logger are supported. Documentation can be found here: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/