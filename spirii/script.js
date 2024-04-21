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