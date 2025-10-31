document.addEventListener('DOMContentLoaded', function () {
    const rangeInputs = document.querySelectorAll('.limit-range');
    rangeInputs.forEach(range => {
        const limitId = parseInt(range.dataset.limitId);
        const limitMinutes = parseInt(range.value) * 10;
        const counter = parseInt(range.dataset.counterToday);
        const isActive = document.getElementById('toggleActiveLimit' + limitId).checked
        displayLimitText(limitId, limitMinutes);
        displayLimitRemainsText(limitId, limitMinutes, counter, isActive);
        enableRemainsRange(limitId, isActive)
        range.addEventListener('input', function () {
            const limitMinutes = parseInt(range.value) * 10;
            const counter = parseInt(range.dataset.counterToday);
            const isActive = document.getElementById('toggleActiveLimit' + limitId).checked
            displayLimitText(limitId, limitMinutes);
            displayLimitRemainsText(limitId, limitMinutes, counter, isActive);
        });
        range.addEventListener('change', function () {
            const limitMinutes = parseInt(range.value) * 10;
            const counter = parseInt(range.dataset.counterToday);
            const isActive = document.getElementById('toggleActiveLimit' + limitId).checked
            updateLimitOnServer(range);
            displayLimitRemainsText(limitId, limitMinutes, counter, isActive);
        });
    });
});

// Функция преобразуется количество минут в строку: {n} ч {n} мин
function minutesToString(countMinutes) {
    const hours = Math.floor(countMinutes / 60);
    const mins = countMinutes % 60;
    let text = '';
    if (hours > 0) {
        text += `${hours} ч`;
        if (mins > 0) {
            text += ` ${mins} мин`;
        }
    } else {
        text += `${mins} мин`;
    }
    return text;
}

// Функция для отображения текста остатка
function displayLimitRemainsText(limitId, limitMinutes, counter, isActive) {
    let text = 'Остаток на сегодня: '
    const textRemainsLimit = document.getElementById(`limitRemainsText${limitId}`);
    if (isActive) {
        const remains = parseInt(limitMinutes) - parseInt(counter)
        text += minutesToString(remains < 0 ? 0 : remains);
    }
    else {
        text += '∞'
    }
    textRemainsLimit.textContent = text;

}

// Функция для отображения текста лимита
function displayLimitText(limitId, limitMinutes) {
    const minutes = parseInt(limitMinutes);
    const textLimit = document.getElementById(`rangeLimitText${limitId}`);
    textLimit.textContent = 'Лимит: ' + minutesToString(minutes);
}

// Функция для отображения ползунка лимита
function enableRemainsRange(limitId, isActive) {
    const rangeLimit = document.getElementById("rangeLimit" + limitId);
    rangeLimit.disabled = !isActive
}

// Функция для отправки на сервер
function updateLimitOnServer(rangeElement) {
    const limitId = rangeElement.dataset.limitId;
    const minutes = parseInt(rangeElement.value) * 10;
    fetch(`/api/v1/limits/${limitId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            minutes: minutes,
            active: true
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при обновлении лимита');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
}

