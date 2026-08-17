import pandas as pd
import logging
from datetime import datetime,timezone


def flatten(raw_payloads: list[dict]) -> pd.DataFrame:
    """
    Transforms and flattens a list of raw weather API payloads into a cleaned pandas DataFrame.

    Args:
        raw_payloads: A list of raw dictionaries returned from the weather API.

    Returns:
        A pandas DataFrame with extracted, cleaned, and formatted weather metrics.
    """
    if not raw_payloads:
        logging.warning("No raw payloads received.")
        return pd.DataFrame()
    
    clean = []

    # Iterate over each raw weather record to extract and structure relevant fields
    for record in raw_payloads:
        try:
            # Safely extract the primary weather details nested under the 'weather' list
            weather_info = record.get("weather", [{}])[0]

            # Flatten the nested response fields into a flat dictionary structure
            transformed = {
                "City": record.get('name'),
                "Country": record.get('sys', {}).get('country'),
                "Weather": weather_info.get('main'),
                "Description": weather_info.get('description'),
                "Temperature": record.get('main', {}).get('temp'),
                "Feels_like": record.get('main', {}).get('feels_like'),
                "Humidity": record.get('main', {}).get('humidity'),
                "Wind_speed": record.get('wind', {}).get('speed'),
                # Convert the Unix timestamp (dt) into a UTC ISO 8601 formatted string
                "Timestamp": datetime.fromtimestamp(record.get("dt"), tz=timezone.utc).isoformat()
            } 
            clean.append(transformed)
        except (KeyError, TypeError, IndexError) as err:
            logging.error(
                # Log the error, fallback to 'Unknown City' if name key is missing or invalid
                f"Failed to transform for {record.get('name', 'Unknown City')}: {err}"
                f"{err}"
            )

    # Convert the list of flat dictionaries into a pandas DataFrame
    frame = pd.DataFrame(clean)
   
    # Remove duplicate records based on unique combinations of City and Timestamp
    frame.drop_duplicates(subset=['City','Timestamp'])

    # Fill any missing values in the DataFrame with a default 'N/A'
    frame.fillna('N/A')

    return frame