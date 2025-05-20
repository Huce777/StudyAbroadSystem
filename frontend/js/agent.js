// 初始化图表
const initCharts = () => {
    const ctx = document.getElementById('efficiencyChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['ANU', 'Sydney', 'UNSW'],
            datasets: [{
                label: '平均处理时效 (小时)',
                data: [28, 35, 31],
                backgroundColor: ['#1a4580', '#1A356E', '#1B365D']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
};

// 实时数据更新
const connectWebSocket = () => {
    const ws = new WebSocket('wss://your-domain.com/realtime');
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateDashboard(data);
    };
};

// 更新界面
const updateDashboard = (data) => {
    document.querySelectorAll('.summary-card').forEach(card => {
        const uni = card.classList[1];
        const stats = data[uni];
        
        card.querySelector('.value').textContent = stats.pending;
        // 其他数据更新逻辑...
    });
};

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    connectWebSocket();
    
    // 动态更新进度环
    document.querySelectorAll('.progress-circle').forEach(circle => {
        const percent = circle.dataset.percent;
        circle.style.background = `conic-gradient(var(--primary-blue) ${percent}%, #eee 0)`;
    });
});