import pytest

from core.models import Ping


@pytest.mark.django_db
def test_health(client):
    res = client.get("/health/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "pings": 1}
    assert Ping.objects.count() == 1
