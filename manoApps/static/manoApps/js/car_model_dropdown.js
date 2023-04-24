document.addEventListener('DOMContentLoaded', function () {
    const carDropdown = document.getElementById('id_car');
    const carModelDropdown = document.getElementById('id_car_model');
    console.log(carDropdown, carModelDropdown);

    carSelect.addEventListener('change', function () {
        const carId = this.value;
        fetch(`/manoApps/car_models/${carId}/`)
            .then(response => response.json())
            .then(data => {
                carModelSelect.innerHTML = '';
                for (const carModel of data.car_models) {
                    const option = document.createElement('option');
                    option.value = carModel.id;
                    option.textContent = carModel.model;
                    carModelSelect.appendChild(option);
                }
            });
    });
});
