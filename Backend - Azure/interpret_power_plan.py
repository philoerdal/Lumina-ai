import json
from openai import OpenAI

# Setup client for call to OpenAI
client = OpenAI(api_key = '')
def interpret_power_plan(start_date, end_date, predicted_prices, actual_prices,
                   battery_state, battery_capacity, max_charge_rate, optimized_total_cost,
                   linear_total_cost, optimized_kWh_charged_pr_hr, linear_kWh_charged_pr_hr):
    # Construct a specific prompt focused on financial impacts of charging plans
    prompt = (
        f"Between {start_date} and {end_date}, we have data on predicted and actual "
        f"electricity prices, alongside battery usage details. The goal is to assess the "
        f"financial impact of using an optimized charging plan compared to a default linear plan.\n"
        f"- Predicted Prices: {predicted_prices}\n"
        f"- Actual Prices: {actual_prices}\n"
        f"- Battery State: {battery_state} kWh (Capacity: {battery_capacity} kWh)\n"
        f"- Max Charge Rate: {max_charge_rate} kWh/hour\n"
        f"- Costs under the optimized plan: ${optimized_total_cost}\n"
        f"- Costs under the linear plan: ${linear_total_cost}\n"
        f"- kWh Charged per Hour (Optimized): {optimized_kWh_charged_pr_hr}\n"
        f"- kWh Charged per Hour (Linear): {linear_kWh_charged_pr_hr}\n\n"
        f"Explain how the optimized plan (machine learning predictions) saves money compared to the linear plan, "
        f"and how the charging distribution differs between the two strategies."
        f"Mention the financial implications of the optimized plan and the benefits of using machine learning predictions."
    )

    # Call the AI API to process this prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are assisting with energy management, focusing on cost optimization."},
            {"role": "user", "content": prompt}
        ]
    )

    json_response = json.dumps(response.choices[0].message.content, indent=4)
    
    return predicted_prices, actual_prices, optimized_kWh_charged_pr_hr, linear_kWh_charged_pr_hr, json_response
