document.addEventListener('DOMContentLoaded', function() {
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    let currentLimitId = null;

    // Обработчик открытия модального окна
    document.getElementById('deleteConfirmModal').addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        currentLimitId = button.getAttribute('data-limit-id');
        console.log('Limit ID:', currentLimitId); // Для отладки
    });

    // Обработчик нажатия "Да"
    confirmDeleteBtn.addEventListener('click', function() {
        if (currentLimitId) {
            deleteLimit(currentLimitId);
        } else {
            console.error('Limit ID не установлен');
        }
    });

    async function deleteLimit(limitId) {
        try {
            console.log('Отправка DELETE запроса для limitId:', limitId);

            const response = await fetch(`/api/v1/limits/${limitId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                // Успешное удаление
                const modal = bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal'));
                modal.hide();

                // Обновляем страницу
                location.reload();
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при удалении: ' + error.message);
        }
    }
});