function populateHourDropdowns() {
    const startHourSelect = document.getElementById('startHour');
    const endHourSelect = document.getElementById('endHour');
    for (let i = 1; i <= 24; i++) {
        const startOption = document.createElement('option');
        startOption.value = i;
        startOption.textContent = i;
        startHourSelect.appendChild(startOption);

        const endOption = document.createElement('option');
        endOption.value = i;
        endOption.textContent = i;
        endHourSelect.appendChild(endOption);
    }
}

function submitData() {
    const date = document.getElementById('date').value;
    const startHour = document.getElementById('startHour').value;
    const endHour = document.getElementById('endHour').value;
    const currentBattery = document.getElementById('currentBattery').value;
    const maxCapacity = document.getElementById('maxCapacity').value;
    const maxChargeRate = document.getElementById('maxChargeRate').value;

    console.log('Date:', date);
    console.log('Start Hour:', startHour);
    console.log('End Hour:', endHour);
    console.log('Current Battery State (kWh):', currentBattery);
    console.log('Battery Max Capacity (kWh):', maxCapacity);
    console.log('Max Charge Rate per Hour (kWh):', maxChargeRate);

    // Implement submission logic here, e.g., sending data to a server
}

// Populate hour dropdowns on page load
window.onload = function() {
    populateHourDropdowns();
};