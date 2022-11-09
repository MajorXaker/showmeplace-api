import pytest


@pytest.mark.asyncio
async def test_dummy(dbsession, creator):
    aaa = 5
    assert 5 == 5
