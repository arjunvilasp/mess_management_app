document.addEventListener('DOMContentLoaded', function () {
    // Load meal data on page load
    loadMealData();

    // Update Meal Modal Initialization
    const updateModal = document.getElementById('updateMealModal');
    const updateModalBtn = document.getElementById('update-model-btn');


    updateModalBtn.addEventListener('click',()=>{
        updateModal.style.display = 'initial';
    });

    // Handle update form submission
    const updateForm = document.getElementById('updateMealForm');
    updateForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const id = document.getElementById('updateMealId').value;
        const name = document.getElementById('updateMealName').value;
        const type = document.getElementById('updateMealType').value;
        const day = document.getElementById('updateMealDay').value;
        const price = document.getElementById('updateMealPrice').value;

        // Perform AJAX request to update meal
        fetch(`/update_meal/${id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // Include CSRF token
            },
            body: JSON.stringify({ name, type, day, price }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Server response:', data);
                updateInstance.close();
                loadMealData();
            })
            .catch(error => {
                console.error('Error updating meal:', error);
            });
    });
});


// Function to load meal data into the table
function loadMealData() {
    fetch('/get_meals/') // Replace with your API endpoint to fetch meals
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Meal data:', data);
            const mealTableBody = document.getElementById('mealTableBody');
            mealTableBody.innerHTML = ''; // Clear previous data

            // Populate table with meal data
            data.forEach(meal => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${meal.name}</td>
                    <td>${meal.type}</td>
                    <td>${meal.day}</td>
                    <td>${meal.price}</td>
                    <td>
                        <a class="update-btn modal-trigger" id="update-model-btn"
                            onclick="fillUpdateForm('${meal.id}', '${meal.name}', '${meal.type}', '${meal.day}', '${meal.price}')">
                            Update
                        </a>
                    </td>
                `;
                mealTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching meal data:', error);
        });
}

// Function to fill update form fields when update button is clicked
function fillUpdateForm(id, name, type, day, price) {
    document.getElementById('updateMealId').value = id;
    document.getElementById('updateMealName').value = name;
    document.getElementById('updateMealType').value = type;
    document.getElementById('updateMealDay').value = day;
    document.getElementById('updateMealPrice').value = price;
}

// Function to get CSRF token from the page
function getCSRFToken() {
    const csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfTokenInput) {
        return csrfTokenInput.value;
    } else {
        console.error('CSRF token not found.');
        return null;
    }
}
