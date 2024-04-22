document.addEventListener('DOMContentLoaded', function() {
    populateHourDropdowns();
});

function populateHourDropdowns() {
    for (let i = 0; i < 24; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `${i}:00`;
    }
}

function adjustDateTime(input) {
    if (input.type === 'datetime-local' && input.value) {
        input.value = input.value.slice(0, 13) + ':00'; // Keep only the date and hour
    }
}

function validateEndTime() {
    const startTimeInput = document.getElementById('startTime');
    const endTimeInput = document.getElementById('endTime');
    if (startTimeInput.value && endTimeInput.value) {
        let startTime = new Date(startTimeInput.value);
        let endTime = new Date(endTimeInput.value);
        if (endTime <= startTime) {
            endTimeInput.value = ''; 
        }
        endTimeInput.min = startTime.toISOString().slice(0, 16); 
    }
}

const form = document.getElementById('carChargingForm');
document.getElementById('gridContainer').style.display = 'none';
form.addEventListener('submit', function(event) {
    event.preventDefault();
    submitData();
});

function submitData() {
    const formData = new FormData(form);
    const jsonPayload = {};
    formData.forEach((value, key) => jsonPayload[key] = value);

    console.log('JSON Payload:', jsonPayload);
    document.getElementById('spinner').style.display = 'block'; // Show spinner
    document.getElementById('carChargingForm').style.display = 'none'; // Hide form
    document.getElementById('formContainer').style.display = 'none'; // Hide form container

    const apiEndpoint = 'https://spirii.free.beeceptor.com';

    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonPayload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Assuming the response is in JSON format
    })
    .then(data => {
        console.log('Success:', data);
        const jsonResponse = JSON.stringify(data.json_response, null, 2); // Format the 'json_response' part of JSON data
        document.getElementById('gridContainer').style.display = 'block';
        document.getElementById('responseData').textContent = jsonResponse; // Display formatted 'json_response' in 'responseData' element
        document.getElementById('responseArea').style.display = 'block'; // Make sure 'responseArea' is visible
        // Plotting the price comparison graph
        const priceTrace1 = {
            x: data.hour_array, 
            y: data.Actual_prices,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Actual Prices',
            marker: {color: 'red'}
        };
        
        const priceTrace2 = {
            x: data.hour_array,
            y: data.Predicted_prices,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Predicted Prices',
            marker: {color: 'blue'}
        };

        const priceLayout = {
            title: 'Price Comparison',
            xaxis: { title: 'Hour', type: 'category' },
            yaxis: { title: 'Price' }
        };

        Plotly.newPlot('plotArea1', [priceTrace1, priceTrace2], priceLayout);

        // Plotting the plan comparison graph
        const planTrace1 = {
            x: data.hour_array,
            y: data.Linear_plan,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Linear Plan',
            marker: {color: 'green'}
        };
        
        const planTrace2 = {
            x: data.hour_array,
            y: data.Optimized_plan,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Optimized Plan',
            marker: {color: 'orange'}
        };

        const planLayout = {
            title: 'Plan Comparison',
            xaxis: { title: 'Hour', type: 'category' },
            yaxis: { title: 'kWh' }
        };

        Plotly.newPlot('plotArea2', [planTrace1, planTrace2], planLayout); 

        const costTrace = {
            x: ['Optimized Total Cost', 'Linear Total Cost'],
            y: [data.optimized_total_cost, data.linear_total_cost],
            type: 'bar',
            text: [data.optimized_total_cost, data.linear_total_cost], 
            textposition: 'auto', 
            marker: {
                color: ['orange', 'green']
            }
        };
        
        const costLayout = {
            title: 'Cost Comparison',
            xaxis: { title: 'Method' },
            yaxis: { title: 'Total Cost' },
            margin: { t: 30 }
        };
        
        Plotly.newPlot('plotArea3', [costTrace], costLayout);

        //document.getElementById('responseText').innerHTML = `<strong>Server Response:</strong> ${data.json_response}`;

    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('responseData').textContent = 'Failed to retrieve data: ' + error.message;
        document.getElementById('responseArea').style.display = 'block'; // Show error in response area
    })
    .finally(() => {
        document.getElementById('spinner').style.display = 'none'; // Hide spinner
    });
}