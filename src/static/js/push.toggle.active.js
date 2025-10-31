document.addEventListener('DOMContentLoaded', function () {
    const toggles = document.querySelectorAll('.limit-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('change', function () {
            const rangeLimitMinutes = document.getElementById("rangeLimit"+this.dataset.limitId)
            fetch(`/api/v1/limits/${this.dataset.limitId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    active: this.checked,
                    minutes: rangeLimitMinutes.value * 10
                })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка при обновлении активации/деактивации');
                    }
                    return response.json();
                })
                .then(data => {
                    const limitId = this.dataset.limitId;
                    const toggleActiveText = document.getElementById("toggleActiveText" + limitId);
                    const rangeLimit = document.getElementById("rangeLimit" + limitId);
                    toggleActiveText.textContent = this.checked ? 'Вкл' : 'Выкл';
                    rangeLimit.disabled = !data.active;
                    displayLimitText(limitId,data.minutes);
                    displayLimitRemainsText(limitId,data.minutes,0,data.active);
                    enableRemainsRange(limitId,data.active)
                })
                .catch(error => console.error('Error:', error));
        });
    });
});

