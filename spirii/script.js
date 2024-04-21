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
    // Creating a JSON object from FormData
    const jsonPayload = {};
    formData.forEach((value, key) => jsonPayload[key] = value);

    // Optional: Adjust date and time formatting or other preprocessingEr
    // For example, ensure dates are in ISO format if necessary

    console.log('JSON Payload:', jsonPayload);

    // Endpoint URL where the form data needs to be submitted
    const apiEndpoint = 'https://spirii.free.beeceptor.com';

    // Fetch API to send the data
    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonPayload)
    })
    .then(response => response.json())  // Assuming the server responds with JSON
    .then(data => {
        console.log('Success:', data);
        // Handle success, e.g., show a success message or redirect
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle errors, e.g., show an error message
    });
}