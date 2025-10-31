document.addEventListener('DOMContentLoaded', () => {
    const addAppForm = document.getElementById('add-app-form');
    const formErrorsDiv = document.getElementById('form-errors');
    const addAppModal = new bootstrap.Modal(document.getElementById('addAppModal'));
    addAppForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        formErrorsDiv.classList.add('d-none');
        formErrorsDiv.innerHTML = '';

        const formData = {
            name: document.getElementById('appName').value,
            description: document.getElementById('appDescription').value
        };

        try {
            const response = await fetch('/api/v1/apps', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            if (response.ok) {
                window.location.href = "/apps";
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

            formErrorsDiv.innerHTML = errorMessage;
            formErrorsDiv.classList.remove('d-none');

        } catch (error) {
            console.error('Ошибка сети или парсинга:', error);
            formErrorsDiv.innerHTML = 'Не удалось подключиться к серверу. Проверьте соединение.';
            formErrorsDiv.classList.remove('d-none');
        }
    });

    // Сброс ошибок при закрытии модального окна
    document.getElementById('addAppModal').addEventListener('hidden.bs.modal', () => {
        formErrorsDiv.classList.add('d-none');
        formErrorsDiv.innerHTML = '';
        addAppForm.reset();
    });
});