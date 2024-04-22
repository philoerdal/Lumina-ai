def min_cost_charging(predicted_prices, actual_prices, battery_state, battery_capacity, max_charge_rate):
    remaining_capacity = battery_capacity - battery_state
    number_of_charging_hours = len(actual_prices)
    uniform_charge_rate = remaining_capacity / number_of_charging_hours
    uniform_charge_rate = min(uniform_charge_rate, max_charge_rate)
    
    price_time_slots = list(enumerate(predicted_prices))
    
    price_time_slots.sort(key=lambda x: x[1])
    
    optimized_total_cost = 0
    linear_total_cost = 0
    optimized_total_kWh_charged = 0
    linear_total_kWh_charged = 0
    
    optimized_charged_pr_hr = [0 for i in range(number_of_charging_hours)]    
    linear_charged_pr_hr = [0 for i in range(number_of_charging_hours)]
    
    for idx, (time_slot, price) in enumerate(price_time_slots):
        if remaining_capacity <= 0:
            break
        possible_charge = min(max_charge_rate, remaining_capacity)
        
        optimized_cost = possible_charge * price
        
        optimized_total_cost += optimized_cost
        
        remaining_capacity -= possible_charge
        
        optimized_total_kWh_charged += possible_charge
        
        optimized_charged_pr_hr[time_slot] = possible_charge

    for time_slot, linear_price in enumerate(actual_prices):
        linear_cost = uniform_charge_rate * linear_price
        linear_total_cost += linear_cost
        
        linear_total_kWh_charged += uniform_charge_rate
        
        linear_charged_pr_hr[time_slot] = uniform_charge_rate


    return optimized_total_cost, linear_total_cost, optimized_total_kWh_charged, linear_total_kWh_charged, optimized_charged_pr_hr, linear_charged_pr_hr

