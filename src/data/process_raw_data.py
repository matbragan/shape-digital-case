import os
import re

import pandas as pd
from data.extract_tar_gz import extract_tar_gz


def get_log_dataframe(log_file_path: str) -> pd.DataFrame:
    """Read a log file with the specific format, and convert it to a Pandas DataFrame."""

    if not os.path.exists(log_file_path):
        extract_tar_gz("data/equipment_failure_sensors.tar.gz", "data/extracted")

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


def process_data() -> pd.DataFrame:
    """Process the raw data and return the equipment failures."""

    print("Loading data...")
    equipment = pd.read_json("data/equipment.json")
    equipment_sensors = pd.read_csv("data/equipment_sensors.csv")
    equipment_failure_sensors = get_log_dataframe("data/extracted/equipment_failure_sensors/equpment_failure_sensors.txt")

    print("Processing data...")
    equipment_failures = (
        equipment
        .merge(equipment_sensors, on="equipment_id", how="left")
        .merge(equipment_failure_sensors, on="sensor_id", how="left")
        .drop_duplicates()
    )

    equipment_failures = equipment_failures[equipment_failures["status"] == "ERROR"]
    equipment_failures.rename(columns={"name": "equipment_name", "group_name": "equipment_group"}, inplace=True)
    
    print("Data processed successfully!")
    return equipment_failures
