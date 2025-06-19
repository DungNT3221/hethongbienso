// Statistics Dashboard JavaScript
class StatisticsDashboard {
    constructor() {
        this.statisticsServiceUrl = 'http://localhost:3004/api/statistics';
        this.charts = {};
        this.data = {};
        
        // Initialize dashboard
        this.init();
    }

    async init() {
        console.log('Initializing Statistics Dashboard...');
        await this.loadData();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Auto refresh every 5 minutes
        setInterval(() => {
            this.refreshData();
        }, 5 * 60 * 1000);
    }

    async loadData() {
        try {
            this.showLoading();
            
            // Load overview data
            const overviewResponse = await fetch(`${this.statisticsServiceUrl}/overview`);
            if (!overviewResponse.ok) {
                throw new Error(`HTTP ${overviewResponse.status}: ${overviewResponse.statusText}`);
            }
            
            const overviewData = await overviewResponse.json();
            
            if (overviewData.success) {
                this.data = overviewData.data;
                this.renderDashboard();
                this.hideLoading();
            } else {
                throw new Error(overviewData.error || 'Failed to load overview data');
            }

        } catch (error) {
            console.error('Error loading statistics data:', error);
            this.showError(error.message);
        }
    }

    renderDashboard() {
        this.renderOverviewCards();
        this.renderModelTypesChart();
        this.renderTrendsChart();
        this.renderModelPerformance();
        this.renderTopModelsTable();
    }

    renderOverviewCards() {
        const summary = this.data.summary || {};
        
        document.getElementById('totalModels').textContent = summary.total_models || 0;
        document.getElementById('completedModels').textContent = summary.completed_models || 0;
        document.getElementById('successRate').textContent = `${summary.success_rate || 0}%`;
        document.getElementById('bestMap50').textContent = (summary.best_map50 || 0).toFixed(3);
    }

    renderModelTypesChart() {
        const ctx = document.getElementById('modelTypesChart').getContext('2d');
        
        // Destroy existing chart if exists
        if (this.charts.modelTypes) {
            this.charts.modelTypes.destroy();
        }

        const modelTypeStats = this.data.model_type_stats || [];
        
        const labels = modelTypeStats.map(stat => stat.model_type);
        const data = modelTypeStats.map(stat => stat.count);
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ];

        this.charts.modelTypes = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    async renderTrendsChart() {
        try {
            // Load trends data
            const trendsResponse = await fetch(`${this.statisticsServiceUrl}/trends?months=6`);
            const trendsData = await trendsResponse.json();
            
            if (!trendsData.success) {
                console.error('Failed to load trends data');
                return;
            }

            const ctx = document.getElementById('trendsChart').getContext('2d');
            
            // Destroy existing chart if exists
            if (this.charts.trends) {
                this.charts.trends.destroy();
            }

            const trends = trendsData.data.trends || [];
            const labels = trends.map(trend => trend.month).reverse();
            const totalData = trends.map(trend => trend.total_trainings).reverse();
            const savedData = trends.map(trend => trend.saved).reverse();

            this.charts.trends = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Total Trainings',
                            data: totalData,
                            borderColor: '#36A2EB',
                            backgroundColor: 'rgba(54, 162, 235, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Saved Models',
                            data: savedData,
                            borderColor: '#4BC0C0',
                            backgroundColor: 'rgba(75, 192, 192, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });

        } catch (error) {
            console.error('Error loading trends data:', error);
        }
    }

    async renderModelPerformance() {
        try {
            // Load model type comparison data
            const comparisonResponse = await fetch(`${this.statisticsServiceUrl}/model-types`);
            const comparisonData = await comparisonResponse.json();
            
            if (!comparisonData.success) {
                console.error('Failed to load model comparison data');
                return;
            }

            const container = document.getElementById('modelPerformanceContainer');
            const modelTypes = comparisonData.data.model_types || [];

            let html = '';
            modelTypes.forEach(modelType => {
                const avgMap50 = (modelType.avg_map50 * 100).toFixed(1);
                const successRate = modelType.success_rate;
                
                html += `
                    <div class="row mb-3 align-items-center">
                        <div class="col-md-2">
                            <span class="badge bg-primary model-type-badge">${modelType.model_type}</span>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">mAP50: ${avgMap50}%</small>
                            <div class="performance-bar">
                                <div class="performance-fill" style="width: ${avgMap50}%"></div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">Success Rate: ${successRate}%</small>
                            <div class="performance-bar">
                                <div class="performance-fill" style="width: ${successRate}%"></div>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <small class="text-muted">Count: ${modelType.total_count}</small>
                        </div>
                        <div class="col-md-2">
                            <small class="text-muted">Avg Time: ${modelType.avg_training_time_minutes.toFixed(1)}m</small>
                        </div>
                    </div>
                `;
            });

            container.innerHTML = html || '<p class="text-muted">No model performance data available.</p>';

        } catch (error) {
            console.error('Error loading model performance data:', error);
        }
    }

    renderTopModelsTable() {
        const topModels = this.data.top_models || [];
        const tbody = document.getElementById('topModelsTable');
        
        let html = '';
        topModels.forEach((model, index) => {
            const rank = index + 1;
            const statusBadge = model.is_approved ? 
                '<span class="badge bg-success">Approved</span>' : 
                '<span class="badge bg-secondary">Completed</span>';
            
            const trainingTime = model.training_time ? 
                `${(model.training_time / 60).toFixed(1)}m` : 'N/A';

            html += `
                <tr>
                    <td>
                        <span class="badge bg-warning text-dark">#${rank}</span>
                    </td>
                    <td>
                        <strong>${model.model_name}</strong>
                    </td>
                    <td>
                        <span class="badge bg-info">${model.model_type}</span>
                    </td>
                    <td>
                        <strong class="text-success">${(model.map50 || 0).toFixed(3)}</strong>
                    </td>
                    <td>
                        <strong class="text-primary">${(model.map95 || 0).toFixed(3)}</strong>
                    </td>
                    <td>${trainingTime}</td>
                    <td>
                        <span class="badge bg-light text-dark">${model.dataset_size || 0}</span>
                    </td>
                    <td>${statusBadge}</td>
                </tr>
            `;
        });

        tbody.innerHTML = html || '<tr><td colspan="8" class="text-center text-muted">No models found</td></tr>';
    }

    showLoading() {
        document.getElementById('loadingState').classList.remove('d-none');
        document.getElementById('errorState').classList.add('d-none');
        document.getElementById('statisticsContent').classList.add('d-none');
    }

    hideLoading() {
        document.getElementById('loadingState').classList.add('d-none');
        document.getElementById('statisticsContent').classList.remove('d-none');
    }

    showError(message) {
        document.getElementById('loadingState').classList.add('d-none');
        document.getElementById('statisticsContent').classList.add('d-none');
        document.getElementById('errorState').classList.remove('d-none');
        document.getElementById('errorMessage').textContent = message;
    }
}

// Global functions
async function refreshData() {
    if (window.statisticsDashboard) {
        await window.statisticsDashboard.loadData();
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.statisticsDashboard = new StatisticsDashboard();
});
