from typing import Any, Dict, Union
from aws_lambda_powertools import Logger
from threading import local


class FyersLogger(Logger):

    __fyId = local()
    __requestId = local()

    def __init__(self, service: str, level: str, **kwargs) -> None:
        """Create FyersLogger object

        Args:
            service (str): Service name. This should be the same across the code wherever the logger is initialized
            level (str): Logger level. Possible values are [INFO, DEBUG, CRITICAL, WARNING]
        """
        super().__init__(
            service=service,
            level=level,
            location="[%(funcName)s:%(lineno)s] %(module)s",
            **kwargs
        )
        self.__fyId.val = ""
        self.__requestId.val = ""
        self.__stacklevel = 4

    def set_fyId(self, fyId: str) -> None:
        """Sets FyId for a particular request. This function needs to be called only once for each request

        Args:
            fyId (str): Fyers ID
        """
        self.__fyId.val = fyId

    def set_requestId(self, requestId: str) -> None:
        """Sets RequestId for a particular request. This function needs to be called only once for each request

        Args:
            requestId (str): Request ID [This should be unique for each request]
        """
        self.__requestId.val = requestId

    def __populate_request_data(self, **kwargs) -> Dict[str, Any]:
        """Adds additional log data to log statement

        Returns:
            Dict[str, Any]: all the keyword arguments along with extra data
        """
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        kwargs["extra"]["fyId"] = self.__fyId.val
        kwargs["extra"]["requestId"] = self.__requestId.val

        return kwargs

    def error(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs error statement

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(**kwargs)
                super().error(msg, *args, stacklevel=stacklevel, **kwargs)
                break
            except:
                stacklevel -= 1

    def info(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs info statement

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(**kwargs)
                super().info(msg, *args, stacklevel=stacklevel, **kwargs)
                break
            except:
                stacklevel -= 1

    def debug(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs debug statement

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(**kwargs)
                super().debug(msg, *args, stacklevel=stacklevel, **kwargs)
                break
            except:
                stacklevel -= 1

    def exception(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs exception statement. Should be called only from exception block

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(**kwargs)
                super().exception(msg, *args, stacklevel=stacklevel, **kwargs)
                break
            except:
                stacklevel -= 1
