document.addEventListener("DOMContentLoaded", function () {
    // Initialize Sortable.js on the kanban board
    const taskBoxes = document.querySelectorAll(".project-detail");
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
                console.log('dragging')
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


(function () {
    async function searchTask(value) {
        return fetch('/tasks/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keyword: value,
            }),
        })
            .then(response => response.json())
            .then(data => {
                return data

            })
            .catch(error => {
                console.error('AJAX request error:', error);
            });
    }

    const renderItem = (item) => (item.description
        ? `<a class="tippy-child" href="/tasks/${item.id}">
           <strong>${item.name}</strong>
           <span>${item.desc}</span>
           </a>`
        : `<a class="tippy-child" href="/tasks/${item.id}">
           <strong>${item.name}</strong>
           </a>`)
    const renderList = (list) => list.map(item => renderItem(item))
        .reduce((start, value) => start + value, '')


    const searchInput = document.getElementById("searchInput")
    const searchBar = document.getElementById("searchBar")
    const tippy = document.getElementById("tippy")
    const loading = document.getElementById("loading")

    tippy.style.display = "none"
    loading.style.display = "none"
    let timerId;
    let focus;

    searchInput.onkeyup = (e) => {
        clearTimeout(timerId)
        const value = searchInput.value;
        loading.style.display = "block"

        if (!value) {
            tippy.style.display = "none"
            loading.style.display = "none"
            return;
        }
        timerId = setTimeout(async () => {
            searchTask(value).then(data => {
                if (!focus || !data || data.length === 0) {
                    tippy.style.display = "none"
                    loading.style.display = "none"
                    return;
                }
                tippy.style.display = "flex"
                tippy.innerHTML = `
                    <span>Tìm thấy ${data.length} kết quả với từ khóa <strong>"${value}"</strong></span>
                    <div>
                        ${renderList(data)}
                    </div>`
            }).catch(() => {
                tippy.style.display = "flex"
                tippy.innerHTML = `<span>Không tìm thấy kết quả với từ khóa <strong>"${value}"</strong></span>`
            }).finally(() => {
                loading.style.display = "none"
            })

        }, 500)
    }
    searchInput.onfocus = () => focus = true
    searchBar.onblur = () => {
        focus = false
        tippy.style.display = "none"
        loading.style.display = "none"
    }
})()

