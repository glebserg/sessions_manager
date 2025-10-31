document.addEventListener('DOMContentLoaded', () => {
    const addLimitForm = document.getElementById('add-limit-form');
    const limitFormErrors = document.getElementById('limit-form-errors');
    const addLimitModalElement = document.getElementById('addLimitModal');
    const addLimitModal = new bootstrap.Modal(addLimitModalElement);
    const limitAppSelect = document.getElementById('limitAppId'); // Получаем новый select

    // Функция для загрузки списка приложений
    async function loadAppsIntoSelect() {
        try {
            const response = await fetch('/api/v1/apps'); // Эндпоинт для получения списка приложений
            console.log(response)
            if (!response.ok) {
                throw new Error('Не удалось загрузить список приложений');
            }
            const apps = await response.json();

            // Очищаем существующие опции, кроме первой "Выберите приложение"
            limitAppSelect.innerHTML = '<option value="" disabled selected>Выберите приложение</option>';

            apps.forEach(app => {
                const option = document.createElement('option');
                option.value = app.id;
                option.textContent = app.name;
                limitAppSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Ошибка при загрузке приложений:', error);
            limitFormErrors.textContent = 'Ошибка при загрузке списка приложений: ' + error.message;
            limitFormErrors.classList.remove('d-none');
        }
    }

    // Загружаем список приложений при открытии модального окна
    addLimitModalElement.addEventListener('show.bs.modal', loadAppsIntoSelect);


    addLimitForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        limitFormErrors.classList.add('d-none'); // Скрываем предыдущие ошибки

        const formData = new FormData(addLimitForm);
        const data = Object.fromEntries(formData.entries());

        // Преобразуем user_id, app_id и minutes в числа
        data.user_id = parseInt(data.user_id);
        data.app_id = parseInt(data.app_id); // Теперь это значение из select
        data.minutes = parseInt(data.minutes);

        try {
            const response = await fetch('/api/v1/limits', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                addLimitForm.reset();
                addLimitModal.hide();
                // Перезагружаем страницу, чтобы увидеть обновленный список лимитов
                window.location.reload();
            } else {
                const errorData = await response.json();
                limitFormErrors.textContent = errorData.detail || 'Произошла ошибка при добавлении лимита.';
                limitFormErrors.classList.remove('d-none');
            }
        } catch (error) {
            limitFormErrors.textContent = 'Ошибка сети или сервера: ' + error.message;
            limitFormErrors.classList.remove('d-none');
        }
    });
});