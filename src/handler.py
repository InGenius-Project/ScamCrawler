from requests.exceptions import HTTPError 
from typing import Callable

class ErrorHanlder:
    def handle(func: Callable, exception_type: Exception = Exception):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exception_type as e:
                print(e)
        return wrapper
    
    def request_error(self, func: Callable):
        self.handle(func, HTTPError)