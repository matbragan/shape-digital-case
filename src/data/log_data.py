import re
import pandas as pd

def get_log_dataframe(log_file_path: str) -> pd.DataFrame:
    """Read a log file with the specific format, and convert it to a Pandas DataFrame."""
    regex = re.compile(r"^\[(\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:\s\d{1,2}:\d{1,2}:\d{1,2})?)\]\t(\w+)\tsensor\[(\d+)\]:\t\(temperature\t(-?\d+\.\d+|err),\svibration\t(-?\d+\.\d+|err)\)$")
    log_data = []

    with open(log_file_path, "r") as f:
        for row in f:
            match = regex.match(row.strip())
            
            if match:
                timestamp = match.group(1)
                status = match.group(2)
                sensor_id = match.group(3)
                temperature = match.group(4)
                vibration = match.group(5)
                
                log_data.append({
                    "timestamp": timestamp,
                    "status": status,
                    "sensor_id": sensor_id,
                    "temperature": temperature,
                    "vibration": vibration
                })

    df = pd.DataFrame(log_data)

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["sensor_id"] = pd.to_numeric(df["sensor_id"])
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["vibration"] = pd.to_numeric(df["vibration"], errors="coerce")
    
    return df
