from utils.transform import flatten, to_record


def test_flatten_flat_dict():
    assert flatten({"a": 1, "b": 2}) == {"a": 1, "b": 2}


def test_flatten_nested_dict():
    result = flatten({"coord": {"lat": 40.7, "lon": -74.0}})
    assert result == {"coord_lat": 40.7, "coord_lon": -74.0}


def test_flatten_list_of_dicts():
    result = flatten({"weather": [{"id": 800, "main": "Clear"}]})
    assert result["weather_id"] == 800
    assert result["weather_main"] == "Clear"


def test_flatten_custom_separator():
    result = flatten({"a": {"b": 1}}, sep=".")
    assert result == {"a.b": 1}


def test_flatten_skips_non_dict_list_items():
    result = flatten({"tags": ["sunny", "clear"]})
    assert result == {}


def test_to_record_adds_uuid():
    record = to_record({"temp": 72.5})
    assert "uuid" in record
    import re
    assert re.match(r"[0-9a-f-]{36}", record["uuid"])  # type: ignore[arg-type]


def test_to_record_adds_insert_datetime():
    record = to_record({"temp": 72.5})
    assert "insert_datetime" in record


def test_to_record_defaults_wind_gust_when_absent():
    record = to_record({"temp": 72.5})
    assert record["wind_gust"] is None


def test_to_record_preserves_wind_gust_when_present():
    record = to_record({"wind": {"gust": 5.2}})
    assert record["wind_gust"] == 5.2
