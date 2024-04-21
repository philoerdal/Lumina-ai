document.addEventListener('DOMContentLoaded', function() {
    populateHourDropdowns();
});

function populateHourDropdowns() {
    const startHourSelect = document.getElementById('startHour');
    const endHourSelect = document.getElementById('endHour');
    for (let i = 0; i < 24; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `${i}:00`;
        startHourSelect.appendChild(option.cloneNode(true));
        endHourSelect.appendChild(option);
    }
}

function adjustDateTime(input) {
    if (input.type === 'datetime-local' && input.value) {
        input.value = input.value.slice(0, 13) + ':00'; // Keep only the date and hour
    }
}

function validateEndTime() {
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    if (startTime && endTime && endTime <= startTime) {
        document.getElementById('endTime').value = startTime; // Reset end time to start time if it's earlier
    }
}

const form = document.getElementById('carChargingForm');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    submitData();
});

function submitData() {
    const formData = new FormData(form);
    console.log('Form Data:', Object.fromEntries(formData.entries()));
    // Implement submission logic here, e.g., sending data to a server
}