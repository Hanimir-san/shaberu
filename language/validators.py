from django.core.exceptions import ValidationError

from home.utils import is_valid_path

def validate_path(value):
    if not is_valid_path(value) and value:
        raise ValidationError(
            "%(value)s is not an even number",
            params={"value": value},
        )
    
import errno, os

# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123
'''
Windows-specific error code indicating an invalid pathname.

See Also
----------
https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
    Official listing of all such codes.
'''


