document.addEventListener('DOMContentLoaded', () => {
    const kanbanCards = document.querySelectorAll('.kanban-card');
    const kanbanColumns = document.querySelectorAll('.kanban-column');
    
    let draggedCard = null;
    
    kanbanCards.forEach(card => {
        card.addEventListener('dragstart', (e) => {
            draggedCard = card;
            setTimeout(() => card.classList.add('dragging'), 0);
        });
        
        card.addEventListener('dragend', () => {
            draggedCard.classList.remove('dragging');
            draggedCard = null;
        });
    });
    
    kanbanColumns.forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
            // Optional: Add some visual feedback to the column
        });
        
        column.addEventListener('drop', (e) => {
            e.preventDefault();
            if(draggedCard) {
                const newStatus = column.getAttribute('data-status');
                const taskId = draggedCard.getAttribute('data-task-id');
                
                // Append card to column UI immediately for responsiveness
                const container = column.querySelector('.kanban-cards-container');
                if(container) {
                    container.appendChild(draggedCard);
                }
                
                // Call API
                updateTaskStatus(taskId, newStatus);
            }
        });
    });
    
    function updateTaskStatus(taskId, status) {
        fetch(`/api/tasks/${taskId}/status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: status })
        })
        .then(response => response.json())
        .then(data => {
            if(!data.success) {
                alert('Failed to update status.');
                window.location.reload();
            }
        })
        .catch(err => {
            console.error(err);
            alert('Error updating task.');
        });
    }
});
