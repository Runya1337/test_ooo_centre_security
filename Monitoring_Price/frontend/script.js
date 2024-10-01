document.addEventListener('DOMContentLoaded', () => {
    const linkForm = document.getElementById('linkForm');
    const urlInput = document.getElementById('urlInput');
    const monitoringList = document.getElementById('monitoringList');
    const searchInput = document.getElementById('searchInput');
    const priceHistoryContainer = document.getElementById('priceHistoryContainer');
    const priceChartCanvas = document.getElementById('priceChart').getContext('2d');
    let priceChart;

    // Отправка ссылки в FastAPI на мониторинг
    linkForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = urlInput.value.trim();

        if (url) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/products/?url=${encodeURIComponent(url)}`, {
                    method: 'POST',
                    headers: {
                        'accept': 'application/json',
                    },
                    body: null,
                });

                if (response.ok) {
                    alert('Ссылка отправлена на мониторинг');
                    urlInput.value = '';
                    loadMonitoringData();
                } else {
                    const errorData = await response.json();
                    if (errorData.detail === "Product already exists") {
                        alert('Этот товар уже добавлен в мониторинг.');
                    } else {
                        alert('Ошибка при отправке ссылки: ' + response.statusText + ' - ' + (errorData.detail || ''));
                    }
                }
            } catch (error) {
                alert('Ошибка: ' + error.message);
            }
        } else {
            alert('Пожалуйста, введите URL');
        }
    });

    // Функция для загрузки мониторинга
    async function loadMonitoringData() {
        try {
            const response = await fetch('http://127.0.0.1:8000/products/');
            if (!response.ok) throw new Error('Ошибка при получении данных: ' + response.statusText);

            const data = await response.json();
            monitoringList.innerHTML = '';

            data.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="product-info">
                        <h3>${item.name}</h3>
                        <p><strong>Link:</strong> <a href="${item.url}" target="_blank">Перейти</a></p>
                        <p><strong>Description:</strong> ${item.description}</p>
                        <p><strong>Price:</strong> ${item.price || 'N/A'} ₽</p>
                        <p><strong>Rating:</strong> ${item.rating}</p>
                        <button class="view-history-btn" data-id="${item.id}">Посмотреть историю цен</button>
                    </div>
                `;
                monitoringList.appendChild(li);
            });

            // Добавляем обработчики на кнопки "Посмотреть историю цен"
            const historyButtons = document.querySelectorAll('.view-history-btn');
            historyButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const productId = e.target.getAttribute('data-id');
                    loadPriceHistory(productId);
                });
            });

        } catch (error) {
            console.error('Ошибка при получении данных мониторинга:', error);
        }
    }

    // Функция для загрузки истории цен и отображения графика
    async function loadPriceHistory(productId) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/products/${productId}/history`);
            if (!response.ok) throw new Error('Ошибка при получении истории: ' + response.statusText);

            const data = await response.json();
            const labels = data.map(item => new Date(item.timestamp).toLocaleDateString());
            const prices = data.map(item => item.price);

            // Отображение графика цен
            if (priceChart) {
                priceChart.destroy(); // Уничтожаем предыдущий график перед созданием нового
            }

            priceChart = new Chart(priceChartCanvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '',
                        data: prices,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        fill: true,
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false // Отключаем отображение легенды
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Дата'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Цена'
                            },
                            beginAtZero: false
                        }
                    }
                }
            });

            // Отображение истории цен
            priceHistoryContainer.innerHTML = `
                <table class="price-history-table">
                    <thead>
                        <tr>
                            <th>Дата</th>
                            <th>Цена</th>
                        </tr>
                    </thead>
                    <tbody class="price-history-list"></tbody>
                </table>`;
            const historyList = document.querySelector('.price-history-list');

            data.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${new Date(item.timestamp).toLocaleString()}</td>
                    <td>${item.price} ₽</td>
                `;
                historyList.appendChild(tr);
            });

        } catch (error) {
            console.error('Ошибка при получении истории цен:', error);
        }
    }

    // Поиск по мониторингу
    searchInput.addEventListener('input', () => {
        const searchValue = searchInput.value.toLowerCase();
        const listItems = monitoringList.getElementsByTagName('li');

        Array.from(listItems).forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(searchValue) ? '' : 'none';
        });
    });

    // Обновление данных мониторинга каждую секунду
    setInterval(loadMonitoringData, 1000);
});
