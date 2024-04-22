import azure.functions as func
import logging

import pandas as pd
from load_data import read_data
from validate_price_prediction_payload import validate_api_payload
from load_model import load_azure_ml_model_from_blob
from minimize_cost import min_cost_charging
from interpret_power_plan import interpret_power_plan
import joblib
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="predict_price_api")
def predict_price_api(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')



    # Receive arguments from JSON
    try:
        req_body = req.get_json()
    except:
        pass
    else:
        start_time = pd.to_datetime(req_body.get('startTime'))
        end_time = pd.to_datetime(req_body.get('endTime'))
        cur_battery_power = req_body.get('currentBattery')
        desired_battery_power = req_body.get('maxCapacity')
        charge_rate = req_body.get('maxChargeRate')


    # Call the function to get the Excel data
    data, message = read_data("dk_data_clean_demonstration")

    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data.set_index('DateTime', inplace=True)

    if message != "Success":
        return func.HttpResponse(f"Failed to load data to do predictions on.", status_code=404)

    

    # Validate input params from request
    if not validate_api_payload(start_time=start_time, cur_battery_power=cur_battery_power, 
                                desired_battery_power=desired_battery_power,
                                end_time=end_time, prediction_dataset=data):
        return func.HttpResponse(f"The payload received was not valid", status_code=400)



    # Load model from Blob storage
    storagename = "luminaresourcegroupbf89"
    storagekey = "1w6aeiFsYO3KRkiE2eTwCtGASAtV/mtzerad4VKJXtmDSOfweXkGwt6WCT8tZnAwZQGmC6ZxIsup+AStduOCkA=="
    containername = "spiriiblob"
    blobname = "rf_model.pkl"  # EDIT HERE!

    # Execute
    #model, message = load_azure_ml_model_from_blob(
    #    storage_account_name=storagename,
    #    storage_account_key=storagekey,
    #    container_name=containername,
    #    blob_name=blobname,
    #)
    model = joblib.load('RandomForestModel.pkl')

    if message != "Success":
        return func.HttpResponse(f"Failed to load model for doing predictions.", status_code=404)


    # Find the correct datetimes from the prediction dataset
    x_pred = data.loc[start_time:end_time][['Forecast1Hour_Onshore', 'Forecast1Hour_Offshore']]
    y_true = data.loc[start_time:end_time]['SpotPriceDKK'] 

    # Predict y-values
    y_pred = model.predict(x_pred)

    
    # Call optimize power prices
    optimized_total_cost, linear_total_cost, optimized_total_kWh_charged, linear_total_kWh_charged, optimized_charged_pr_hr, linear_charged_pr_hr = min_cost_charging(predicted_prices=y_pred, actual_prices=y_true, battery_state=cur_battery_power, battery_capacity=desired_battery_power, max_charge_rate=charge_rate)

    # Call OpenAI routine
    #text_interpreted = interpret_power_plan(start_time=start_time, end_time=end_time, predicted_prices=y_pred, 
    #                    actual_prices=y_true, battery_state=cur_battery_power, battery_capacity=desired_battery_power, 
    #                    max_charge_rate=11, optimized_total_cost=optimized_total_cost, 
    #                    linear_total_cost=linear_total_cost, optimized_charged_kWh=optimized_total_kWh_charged, 
    #                    linear_charged_kWh=linear_total_kWh_charged, optimized_kWh_charged_pr_hr=optimized_charged_pr_hr, 
    #                    linear_kWh_charged_pr_hr=linear_charged_pr_hr)



    # Create json to return in HTTP request
    response = {
        "predicted_power_prices": y_pred.tolist(),
        "actual_power_prices": y_true.tolist(),
        "optimized_charged_pr_hr": optimized_charged_pr_hr,
        "linear_charged_pr_hr": linear_charged_pr_hr,
        "message": "This is a string message because Sofus' openai script is broken"
    }

    # Serialize the dictionary into a JSON string
    json_data = json.dumps(response)

    return func.HttpResponse(json_data, status_code=200)