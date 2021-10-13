

# imports - module imports
from fluxml.exception import (
    FluxmlError
)

# imports - test imports
import pytest

def test_fluxml_error():
    with pytest.raises(FluxmlError):
        raise FluxmlError