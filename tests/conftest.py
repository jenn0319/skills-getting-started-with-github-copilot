from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities() -> None:
    original_activities = deepcopy(app_module.activities)

    # Ensure each test starts from a known state because the app keeps data in memory.
    app_module.activities.clear()
    app_module.activities.update(deepcopy(original_activities))

    yield

    app_module.activities.clear()
    app_module.activities.update(deepcopy(original_activities))
