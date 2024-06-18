// Function to generate the calendar
function generateCalendar(year, month) {
    const monthElement = document.getElementById('month-year');
    const calendarElement = document.getElementById('calendar');

    // Clear the calendar element
    calendarElement.innerHTML = '';

    // Get the first and last day of the month
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);

    // Get the date of the first day of the month
    const firstDayDate = firstDay.getDate();
    const firstDayDay = firstDay.getDay();

    // Get the month name and year
    const monthName = firstDay.toLocaleString('default', { month: 'long' });
    const yearValue = firstDay.getFullYear();

    // Update the month and year display
    monthElement.textContent = `${monthName} ${yearValue}`;

    // Create the calendar table
    const table = document.createElement('table');

    // Create the table header
    const headerRow = document.createElement('tr');
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    daysOfWeek.forEach(day => {
        const th = document.createElement('th');
        th.textContent = day;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Create the table rows and cells
    let date = 1;
    for (let i = 0; i < 6; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDayDay) {
                const cell = document.createElement('td');
                row.appendChild(cell);
            } else if (date > lastDay.getDate()) {
                break;
            } else {
                const cell = document.createElement('td');
                const dayNumber = document.createElement('span');
                dayNumber.textContent = date;
                dayNumber.classList.add('day-number');
                cell.appendChild(dayNumber);
                row.appendChild(cell);
                date++;
            }
        }
        table.appendChild(row);
    }

    // Append the calendar table to the calendar element
    calendarElement.appendChild(table);

    // Fetch attendance data
    fetchAttendanceData(year, month);
}

// Function to fetch attendance data from the server
function fetchAttendanceData(year, month) {
    const url = `/attendance/data/${year}/${month}/`;
    const csrfToken = document.querySelector('script[type="text/javascript"]').text;

    fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Update the calendar with attendance data
        updateCalendarWithAttendanceData(data);
    })
    .catch(error => {
        console.error('Error fetching attendance data:', error);
    });
}

// Function to update the calendar with attendance data
function updateCalendarWithAttendanceData(attendanceData) {
    const calendarElement = document.getElementById('calendar');
    const tableCells = calendarElement.getElementsByTagName('td');

    // Reset the cell styles
    for (let i = 0; i < tableCells.length; i++) {
        tableCells[i].classList.remove('present', 'absent');
    }

    // Update the cell styles based on attendance data
    for (const date in attendanceData) {
        const day = new Date(date).getDate();
        const present = attendanceData[date];

        for (let i = 0; i < tableCells.length; i++) {
            const cell = tableCells[i];
            const dayNumber = cell.getElementsByClassName('day-number')[0];
            if (dayNumber && dayNumber.textContent === day.toString()) {
                cell.classList.add(present ? 'present' : 'absent');
                break;
            }
        }
    }
}

// Initial calendar generation
const currentDate = new Date();
const currentYear = currentDate.getFullYear();
const currentMonth = currentDate.getMonth() + 1;

generateCalendar(currentYear, currentMonth);