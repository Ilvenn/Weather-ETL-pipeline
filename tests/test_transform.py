import pandas as pd
from src.transform import flatten

def test_flatten_valid_data():
    raw_payloads = [
        {
            "name": "Maputo",
            "sys": {"country": "MZ"},
            "weather": [{"main": "Clouds", "description": "scattered clouds"}],
            "main": {"temp": 25.5, "feels_like": 26.0, "humidity": 70},
            "wind": {"speed": 4.1},
            "dt": 1692270000
        },
        {
            "name": "Nelspruit",
            "sys": {"country": "ZA"},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 20.0, "feels_like": 19.5, "humidity": 50},
            "wind": {"speed": 3.0},
            "dt": 1692270000
        }
    ]

    df = flatten(raw_payloads)

    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == [
        "City", "Country", "Weather", "Description",
        "Temperature", "Feels_like", "Humidity", "Wind_speed", "Timestamp", "Extracted_At"
    ]
    assert df.loc[0, "City"] == "Maputo"
    assert df.loc[1, "City"] == "Nelspruit"
    assert df.loc[0, "Country"] == "MZ"
    assert df.loc[0, "Humidity"] == 70

def test_flatten_empty_list():
    df = flatten([])
    assert df.empty

def test_flatten_malformed_record():
    raw_payloads = [
        {
            # Missing fields to trigger exception handling
            "name": "Maputo"
        }
    ]
    df = flatten(raw_payloads)
    assert df.empty
