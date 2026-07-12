import pytest


@pytest.fixture
def user_payload():
    data = {
        "username": "alice",
        "email": "alice@gmail",
        "level": "beginner"
    }
    yield data
    #TODO: написать комманду удаления data из test_db





