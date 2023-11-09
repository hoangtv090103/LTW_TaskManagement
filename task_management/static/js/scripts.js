document.addEventListener("DOMContentLoaded", function () {
    // Initialize Sortable.js on the kanban board
    const taskBoxes = document.querySelectorAll(".task-box");
    const options = {
        group: "shared",
        animation: 150,
        setData: function (dataTransfer, dragEl) {
            dataTransfer.setData("text", dragEl.id);
        },
        onEnd: function (evt) {
            const taskId = parseInt(evt.item.id);
            const newState = evt.to.id;
            updateTaskStatus(taskId, newState);
            evt.to.classList.remove("drag-over");

        },
    };

    // Add draggable attribute to tasks in each state box
    taskBoxes.forEach((taskBox) => {
        const tasks = taskBox.querySelectorAll(".task");
        tasks.forEach((task) => {
            task.setAttribute("draggable", true);
            task.addEventListener("dragstart", function (e) {
                e.dataTransfer.setData("text", e.target.id);
            });
            task.addEventListener("dragend", function (e) {
                console.log("dragend");
            });
        });

        // Add dragover and dragleave event listeners to each task box
        taskBox.addEventListener("dragover", function (e) {
            e.preventDefault();
            taskBox.classList.add("drag-over");
        });

        taskBox.addEventListener("dragleave", function (e) {
            taskBox.classList.remove("drag-over");
        });


        // Initialize Sortable for each state box
        new Sortable(taskBox, options);
    });
});

function updateTaskStatus(taskId, newState) {
    // Send an API request to update the task status
    fetch(`/tasks/${taskId}/edit`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({taskId, newState}),
    })
        .then(response => {
            if (response.ok) {
                // Task status updated successfully
                console.log('Task status updated successfully');
                location.reload();
            } else {
                // Error handling
                console.error('Error updating task status');
            }
        })
        .catch(error => {
            console.error('API request error:', error);
        });
}

function editTask(taskId) {
    // Send an API request to update the task status
    fetch(`/tasks/${taskId}/edit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({taskId}),
    })
        .then(response => {
            if (response.ok) {
                // Task status updated successfully
                console.log('Task status updated successfully');
                location.reload();
            } else {
                // Error handling
                console.error('Error updating task status');
            }
        })
        .catch(error => {
            console.error('API request error:', error);
        });
}

function saveTask(taskId) {
    // Send an API request to update the task status
    fetch(`/tasks/${taskId}/save`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            taskId,
            name: document.getElementById('name').value,
            description: document.getElementById('description').value,
            active: document.getElementById('active').value,
            priority: document.getElementById('priority').value,
            status: document.getElementById('status').value,
            date_start: document.getElementById('date_start').value,
            date_end: document.getElementById('date_end').value,
            project_id: parseInt(document.getElementById('project_id').value),
        }),
    })
        .then(response => {
            if (response.ok) {
                // Task status updated successfully
                console.log('Task status updated successfully');
                location.reload();
            } else {
                // Error handling
                console.error('Error updating task status');
            }
        })
        .catch(error => {
            console.error('API request error:', error);
        });
}

function searchTask() {
    // Send an API request to update the task status
    fetch('tasks/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            keyword: document.getElementById('searchbar').value,
        }),
    })
        .then(response => {
            if (response.ok) {

                console.log('Task status updated successfully');
            } else {
                // Error handling
                console.error('Error performing search');
            }
        })
        .catch(error => {
            console.error('AJAX request error:', error);
        });
}
