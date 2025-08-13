// Fetch quarterly metrics from Flask API
async function getQuarterlyMetrics(budgetId) {
    const response = await fetch("/getQuarterMetrics", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ budgetId: budgetId })
    });

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
}

// Helper: Format number with commas
function formatNumber(num) {
    return num.toLocaleString();
}

// Render charts
function renderCharts(data) {
    const container = document.getElementById('charts-container');
    container.innerHTML = ""; // Clear old content if re-rendering

    Object.entries(data).forEach(([quarterId, quarterData]) => {
        const section = document.createElement('div');
        section.classList.add('quarter-section');

        const title = document.createElement('div');
        title.classList.add('quarter-title');
        title.textContent = quarterId;
        section.appendChild(title);

        const chartRow = document.createElement('div');
        chartRow.classList.add('chart-row');

        // ====== Performance Pie ======
        const perfContainer = document.createElement('div');
        perfContainer.classList.add('chart-container');
        const perfCanvas = document.createElement('canvas');
        perfContainer.appendChild(perfCanvas);
        chartRow.appendChild(perfContainer);

        const planned = quarterData.financial.planned;
        const expended = quarterData.financial.expended;
        const remaining = Math.max(planned - expended, 0);

        new Chart(perfCanvas, {
            type: 'pie',
            data: {
                labels: ['Expended', 'Remaining'],
                datasets: [{
                    data: [expended, remaining],
                    backgroundColor: ['#4CAF50', '#FFC107']
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const val = ctx.parsed;
                                const pct = ((val / (planned || 1)) * 100).toFixed(1);
                                return `${ctx.label}: ${formatNumber(val)} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });

        // ====== Category Pie ======
        const catContainer = document.createElement('div');
        catContainer.classList.add('chart-container');
        const catCanvas = document.createElement('canvas');
        catContainer.appendChild(catCanvas);
        chartRow.appendChild(catContainer);

        const categoryLabels = [];
        const categoryValues = [];

        Object.entries(quarterData.category_analysis).forEach(([catName, catData]) => {
            let label = `${catName} (Var: ${catData.variance.toFixed(2)})\n`;
            Object.entries(catData.items).forEach(([item, itemData]) => {
                label += `• ${item}: ${formatNumber(itemData.actual)}\n`;
            });
            categoryLabels.push(label);
            categoryValues.push(catData.actual);
        });

        new Chart(catCanvas, {
            type: 'pie',
            data: {
                labels: categoryLabels,
                datasets: [{
                    data: categoryValues,
                    backgroundColor: [
                        '#2196F3', '#FF5722', '#9C27B0', '#009688', '#FFC107', '#E91E63'
                    ]
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const val = ctx.parsed;
                                const pct = ((val / categoryValues.reduce((a,b)=>a+b, 0)) * 100).toFixed(1);
                                return `${ctx.label.trim()}: ${formatNumber(val)} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });

        section.appendChild(chartRow);
        container.appendChild(section);
    });
}

// Load charts on page load
document.addEventListener('DOMContentLoaded', async () => {
    const budgetId = "BUDGET123"; // Replace with actual budgetId or make it dynamic
    try {
        const metrics = await getQuarterlyMetrics(budgetId);
        renderCharts(metrics);
    } catch (error) {
        console.error("Error loading metrics:", error);
    }
});
