def min_cost_charging(predicted_prices, actual_prices, battery_state, battery_capacity, max_charge_rate):
    remaining_capacity = battery_capacity - battery_state
    number_of_charging_hours = len(actual_prices)
    uniform_charge_rate = remaining_capacity / number_of_charging_hours
    uniform_charge_rate = min(uniform_charge_rate, max_charge_rate)
    
    # Create a list of time slots and prices
    price_time_slots = list(enumerate(predicted_prices))
    
    # Sort by price (cheapest first)
    price_time_slots.sort(key=lambda x: x[1])
    
    optimized_total_cost = 0
    actual_total_cost = 0
    optimized_total_kWh_charged = 0
    actual_total_kWh_charged = 0
    
    ## fill the lists with 0's to represent no charging at that time slot
    optimized_charged_pr_hr = [0 for i in range(number_of_charging_hours)]    
    actual_charged_pr_hr = [0 for i in range(number_of_charging_hours)]
    
    # Iterate through sorted price list for planning
    for idx, (time_slot, price) in enumerate(price_time_slots):
        if remaining_capacity <= 0:
            break
        # Charge uniformly across all hours
        possible_charge = min(max_charge_rate, remaining_capacity)
        
        # Calculate optimized cost for this charge
        optimized_cost = possible_charge * price
        
        # Update total optimized cost
        optimized_total_cost += optimized_cost
        
        # Update the remaining capacity
        remaining_capacity -= possible_charge
        
        # Update total kWh charged
        optimized_total_kWh_charged += possible_charge
        
        ### Append the actual charge with the index of the time slot in the original predicted_prices list
        optimized_charged_pr_hr[time_slot] = possible_charge

    # Calculate actual costs based on actual prices and charge distribution
    for time_slot, actual_price in enumerate(actual_prices):
        actual_cost = uniform_charge_rate * actual_price
        actual_total_cost += actual_cost
        
        actual_total_kWh_charged += uniform_charge_rate
        
        actual_charged_pr_hr[time_slot] = uniform_charge_rate


    return optimized_total_cost, actual_total_cost, optimized_total_kWh_charged, actual_total_kWh_charged, optimized_charged_pr_hr, actual_charged_pr_hr