from utils.datagen import get_random_us_coordinate


def test_returns_expected_keys():
    result = get_random_us_coordinate()
    assert set(result.keys()) == {"city", "latitude", "longitude"}


def test_latitude_within_us_bounds():
    for _ in range(30):
        r = get_random_us_coordinate()
        assert 18.0 <= r["latitude"] <= 72.0, f"latitude out of range: {r['latitude']}"


def test_longitude_within_us_bounds():
    for _ in range(30):
        r = get_random_us_coordinate()
        assert -180.0 <= r["longitude"] <= -65.0, f"longitude out of range: {r['longitude']}"


def test_city_is_nonempty_string():
    r = get_random_us_coordinate()
    assert isinstance(r["city"], str)
    assert len(r["city"]) > 0


def test_produces_different_results():
    results = {get_random_us_coordinate()["city"] for _ in range(50)}
    assert len(results) > 1
