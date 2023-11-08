window.onload = function() {
    const tasks = document.getElementsByClassName("task");
    const kanbanBoard = document.querySelector(".kanban-board");

    function handleDrop(e, list) {
        e.preventDefault();
        const taskId = e.dataTransfer.getData("text");
        const task = document.getElementById(taskId);
        list.appendChild(task);
    }

    for (const task of tasks) {
        task.addEventListener("dragstart", e => {
            e.dataTransfer.setData("text", e.target.id);
        });
    }

    kanbanBoard.addEventListener("dragover", e => {
        e.preventDefault();
        if (e.target.classList.contains("state-box")) {
            e.target.classList.add("hovered");
        }
    });

    kanbanBoard.addEventListener("dragleave", e => {
        if (e.target.classList.contains("state-box")) {
            e.target.classList.remove("hovered");
        }
    });

    kanbanBoard.addEventListener("drop", e => {
        if (e.target.classList.contains("state-box")) {
            handleDrop(e, e.target);
            e.target.classList.remove("hovered");
            const taskId = parseInt(e.dataTransfer.getData("text"));
            // convert taskId to int
            const newStatus = e.target.id;
            updateTaskStatus(taskId, newStatus);
        }
    });


    function updateTaskStatus(taskId, newStatus) {
        // 'tasks/<int:task_id>/edit'
        fetch(`/tasks/${taskId}/edit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ taskId, newStatus }),
        })
        .then(response => {
            if (response.ok) {
                // Task status updated successfully
                console.log('Task status updated successfully');
            } else {
                // Error handling
                console.error('Error updating task status');
            }
        })
        .catch(error => {
            console.error('API request error:', error);
        });
    }


}

