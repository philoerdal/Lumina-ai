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
        document.getElementById('responseData').textContent = JSON.stringify(data, null, 2); // Format JSON data
        document.getElementById('responseArea').style.display = 'block'; // Show response area
        
        // Plotting the price comparison graph
        const priceTrace1 = {
            x: Array.from({length: data.Actual_prices.length}, (_, i) => i + 1), // Create an array [1, 2, ..., n]
            y: data.Actual_prices,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Actual Prices',
            marker: {color: 'red'}
        };
        
        const priceTrace2 = {
            x: Array.from({length: data.Predicted_prices.length}, (_, i) => i + 1),
            y: data.Predicted_prices,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Predicted Prices',
            marker: {color: 'blue'}
        };

        const priceLayout = {
            title: 'Price Comparison',
            xaxis: { title: 'Time Point' },
            yaxis: { title: 'Price ($)' }
        };

        Plotly.newPlot('plotArea', [priceTrace1, priceTrace2], priceLayout);

        // Plotting the plan comparison graph
        const planTrace1 = {
            x: Array.from({length: data.Linear_plan.length}, (_, i) => i + 1),
            y: data.Linear_plan,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Linear Plan',
            marker: {color: 'green'}
        };
        
        const planTrace2 = {
            x: Array.from({length: data.Optimized_plan.length}, (_, i) => i + 1),
            y: data.Optimized_plan,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Optimized Plan',
            marker: {color: 'orange'}
        };

        const planLayout = {
            title: 'Plan Comparison',
            xaxis: { title: 'Time Point' },
            yaxis: { title: 'Plan Value' }
        };

        Plotly.newPlot('plotArea2', [planTrace1, planTrace2], planLayout); // Ensure you have a div with id="plotArea2" for this plot

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