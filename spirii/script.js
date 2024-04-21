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

    // Replace with your actual API endpoint
    const apiEndpoint = 'https://your-api-url.com/submit';

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
        return response.text(); // Use text() first to see what you received that isn't JSON
    })
    .then(data => {
        try {
            const jsonData = JSON.parse(data); // Try parsing as JSON
            console.log('Success:', jsonData);
        } catch (e) {
            console.error("Data received was not valid JSON:", data);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}