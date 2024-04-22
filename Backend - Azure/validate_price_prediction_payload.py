import pandas as pd

def validate_api_payload(start_time, cur_battery_power, desired_battery_power, end_time, prediction_dataset):
    """
    Validate the API payload based on the given datasets.

    Parameters:
    - start_time: Start time in datetime format
    - cur_battery_power: Current battery power level
    - desired_battery_power: Desired battery power level
    - end_time: Time that charging should be finished
    - prediction_dataset: DataFrame containing the dataset

    Returns:
    - True if the payload is valid, False otherwise
    """

    # Check if start_time is within the DateTime column from the dataset
    if start_time not in prediction_dataset.index:
        return False

    # Check if end_time is within the DateTime column from the dataset
    if end_time not in prediction_dataset.index:
        return False

    # Check if cur_battery_power is between 0 and desired_battery_power
    if not (0 <= cur_battery_power <= desired_battery_power):
        return False

    # Check if desired_battery_power is between desired_battery_power and 75
    if not (desired_battery_power <= desired_battery_power <= 75):
        return False

    return True
