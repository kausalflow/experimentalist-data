import pytest
from pathlib import Path

__location__ = Path(__file__).parent


@pytest.fixture
def base_data():
    return __location__ / "data/datasets"

