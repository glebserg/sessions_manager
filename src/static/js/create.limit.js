document.addEventListener('DOMContentLoaded', () => {
    const addLimitForm = document.getElementById('add-limit-form');
    const limitFormErrorsDiv = document.getElementById('limit-form-errors');
    const addLimitModal = new bootstrap.Modal(document.getElementById('addLimitModal'));

    addLimitForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        limitFormErrorsDiv.classList.add('d-none');
        limitFormErrorsDiv.innerHTML = '';

        const formData = {
            user_id: parseInt(document.getElementById('limitUserId').value),
            app_id: parseInt(document.getElementById('limitAppId').value),
            minutes: parseInt(document.getElementById('limitMinutes').value)
        };

        try {
            const response = await fetch('/api/v1/limits', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                addLimitForm.reset();
                addLimitModal.hide();
                // Опционально: перезагрузить страницу или обновить список лимитов
                window.location.reload(); // Перезагрузка страницы для отображения нового лимита
                return;
            }

            let errorMessage = 'Произошла ошибка.';
            let errorData = null;

            try {
                errorData = await response.clone().json();
            } catch (_) {
                try {
                    const text = await response.text();
                    if (text) errorMessage = text;
                } catch (_) {}
            }

            if (response.status === 400) {
                if (errorData && (errorData.detail || errorData.message)) {
                    errorMessage = errorData.detail || errorData.message;
                } else if (!errorMessage || errorMessage === 'Произошла ошибка.') {
                    errorMessage = 'Некорректные данные. Проверьте поля формы.';
                }
            } else if (response.status === 422) {
                errorMessage = 'Ошибка валидации:';
                if (errorData && errorData.detail && Array.isArray(errorData.detail)) {
                    errorData.detail.forEach(err => {
                        const loc = Array.isArray(err.loc) ? err.loc.join(' -> ') : err.loc;
                        errorMessage += `<br>- ${loc}: ${err.msg || 'некорректное значение'}`;
                    });
                }
            } else {
                if (errorData && (errorData.detail || errorData.message)) {
                    errorMessage = errorData.detail || errorData.message;
                } else if (!errorMessage || errorMessage === 'Произошла ошибка.') {
                    errorMessage = `Ошибка сервера: ${response.status}`;
                }
            }

            limitFormErrorsDiv.innerHTML = errorMessage;
            limitFormErrorsDiv.classList.remove('d-none');

        } catch (error) {
            console.error('Ошибка сети или парсинга:', error);
            limitFormErrorsDiv.innerHTML = 'Не удалось подключиться к серверу. Проверьте соединение.';
            limitFormErrorsDiv.classList.remove('d-none');
        }
    });

    // Сброс ошибок при закрытии модального окна
    document.getElementById('addLimitModal').addEventListener('hidden.bs.modal', () => {
        limitFormErrorsDiv.classList.add('d-none');
        limitFormErrorsDiv.innerHTML = '';
        addLimitForm.reset();
    });
});