/**
 * MWRASP Quantum Defense Dashboard JavaScript
 */

class MWRASPDashboard {
    constructor() {
        this.websocket = null;
        this.isConnected = false;
        this.charts = {};
        this.lastData = {};
        this.logBuffer = [];
        this.maxLogEntries = 100;
        
        // Initialize dashboard
        this.init();
    }
    
    async init() {
        console.log('Initializing MWRASP Dashboard...');
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initialize charts
        this.initializeCharts();
        
        // Connect WebSocket
        this.connectWebSocket();
        
        // Start periodic health checks
        this.startHealthMonitoring();
        
        // Load initial data
        await this.loadInitialData();
        
        this.log('Dashboard initialized', 'system');
    }
    
    setupEventListeners() {
        // Simulation buttons
        document.getElementById('simulateAttack').addEventListener('click', () => this.simulateQuantumAttack());
        document.getElementById('createToken').addEventListener('click', () => this.createCanaryToken());
        document.getElementById('fragmentData').addEventListener('click', () => this.fragmentTestData());
        document.getElementById('reconstructData').addEventListener('click', () => this.reconstructData());
        document.getElementById('triggerCoordination').addEventListener('click', () => this.triggerCoordination());
        document.getElementById('refreshAgents').addEventListener('click', () => this.refreshAgentStatus());
        
        // Log controls
        document.getElementById('clearLog').addEventListener('click', () => this.clearLog());
        
        // Modal controls
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        window.addEventListener('click', (e) => {
            if (e.target === document.getElementById('modal')) {
                this.closeModal();
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'l') {
                e.preventDefault();
                this.clearLog();
            }
        });
    }
    
    initializeCharts() {
        // Threat detection chart
        const threatCtx = document.getElementById('threatChart');
        if (threatCtx) {
            this.charts.threats = new Chart(threatCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Threat Level',
                        data: [],
                        borderColor: '#ff4444',
                        backgroundColor: 'rgba(255, 68, 68, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 4,
                            ticks: { color: '#cccccc' }
                        },
                        x: {
                            ticks: { color: '#cccccc' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#cccccc' }
                        }
                    }
                }
            });
        }
        
        // Fragment timeline chart
        const fragmentCtx = document.getElementById('fragmentTimeline');
        if (fragmentCtx) {
            this.charts.fragments = new Chart(fragmentCtx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Active Fragments',
                        data: [],
                        backgroundColor: 'rgba(0, 255, 136, 0.6)',
                        borderColor: '#00ff88',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#cccccc' }
                        },
                        x: {
                            ticks: { color: '#cccccc' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#cccccc' }
                        }
                    }
                }
            });
        }
        
        // Performance chart
        const perfCtx = document.getElementById('performanceChart');
        if (perfCtx) {
            this.charts.performance = new Chart(perfCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'Response Time (ms)',
                            data: [],
                            borderColor: '#00ffff',
                            backgroundColor: 'rgba(0, 255, 255, 0.1)',
                            yAxisID: 'y'
                        },
                        {
                            label: 'Active Agents',
                            data: [],
                            borderColor: '#00ff88',
                            backgroundColor: 'rgba(0, 255, 136, 0.1)',
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            ticks: { color: '#cccccc' }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            grid: { drawOnChartArea: false },
                            ticks: { color: '#cccccc' }
                        },
                        x: {
                            ticks: { color: '#cccccc' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#cccccc' }
                        }
                    }
                }
            });
        }
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                this.isConnected = true;
                this.updateConnectionStatus('online');
                this.log('WebSocket connected', 'system');
                
                // Subscribe to all event types
                this.sendWebSocketMessage({
                    type: 'subscribe',
                    subscriptions: ['threats', 'agents', 'fragments', 'system']
                });
            };
            
            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleWebSocketMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            this.websocket.onclose = () => {
                this.isConnected = false;
                this.updateConnectionStatus('offline');
                this.log('WebSocket disconnected', 'error');
                
                // Attempt reconnection after 3 seconds
                setTimeout(() => this.connectWebSocket(), 3000);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.log('WebSocket error occurred', 'error');
            };
            
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            this.updateConnectionStatus('error');
        }
    }
    
    handleWebSocketMessage(data) {
        const { type, event, timestamp, data: messageData } = data;
        
        switch (type) {
            case 'threats':
                this.handleThreatMessage(event, messageData);
                break;
            case 'agents':
                this.handleAgentMessage(event, messageData);
                break;
            case 'fragments':
                this.handleFragmentMessage(event, messageData);
                break;
            case 'system':
                this.handleSystemMessage(event, messageData);
                break;
            case 'alert':
                this.handleAlertMessage(event, messageData);
                break;
            default:
                console.log('Unknown message type:', data);
        }
        
        // Update last update time
        this.updateLastUpdateTime();
    }
    
    handleThreatMessage(event, data) {
        switch (event) {
            case 'new_threat':
                this.log(`New ${data.threat_level} threat detected: ${data.threat_id}`, 'threat');
                this.updateThreatChart(data);
                this.displayRecentThreat(data);
                break;
            case 'statistics_update':
                this.updateThreatStatistics(data);
                break;
        }
    }
    
    handleAgentMessage(event, data) {
        switch (event) {
            case 'status_change':
                this.log(`Agent status changed: ${data.active_agents} agents active`, 'agent');
                this.updateAgentDisplay(data);
                break;
            case 'coordination_executed':
                this.log(`Coordination executed: ${data.total_coordinations} total`, 'agent');
                this.updateCoordinationStats(data);
                break;
        }
    }
    
    handleFragmentMessage(event, data) {
        switch (event) {
            case 'fragment_update':
                this.log(`Fragments updated: ${data.total_fragments} total (${data.change > 0 ? '+' : ''}${data.change})`, 'fragment');
                this.updateFragmentDisplay(data);
                break;
        }
    }
    
    handleSystemMessage(event, data) {
        switch (event) {
            case 'status_update':
                this.updateSystemStats(data);
                break;
            case 'heartbeat':
                document.getElementById('connectedClients').textContent = data.connections || 0;
                break;
        }
    }
    
    handleAlertMessage(event, data) {
        this.log(`ALERT: ${data.message}`, 'error');
        this.showNotification(data.message, data.severity);
    }
    
    async loadInitialData() {
        try {
            // Load system stats
            const response = await fetch('/stats');
            if (response.ok) {
                const stats = await response.json();
                this.updateSystemStats(stats);
            }
        } catch (error) {
            console.error('Failed to load initial data:', error);
            this.log('Failed to load initial system data', 'error');
        }
    }
    
    updateSystemStats(stats) {
        // Update overview stats
        if (stats.system_uptime !== undefined) {
            document.getElementById('systemUptime').textContent = Math.round(stats.system_uptime);
        }
        
        if (stats.quantum_detector) {
            document.getElementById('totalThreats').textContent = stats.quantum_detector.total_threats_detected || 0;
            this.updateHealthIndicator('detectorHealth', 'healthy');
        }
        
        if (stats.temporal_fragmentation) {
            document.getElementById('activeFragments').textContent = stats.temporal_fragmentation.active_fragments || 0;
            document.getElementById('totalFragments').textContent = stats.temporal_fragmentation.total_fragments || 0;
            document.getElementById('fragmentGroups').textContent = stats.temporal_fragmentation.fragment_groups || 0;
            document.getElementById('cleanupStatus').textContent = stats.temporal_fragmentation.cleanup_running ? 'Yes' : 'No';
            this.updateHealthIndicator('fragmentationHealth', 'healthy');
        }
        
        if (stats.agent_coordination) {
            document.getElementById('activeAgents').textContent = stats.agent_coordination.coordination_stats?.active_agents || 0;
            this.updateAgentGrid(stats.agent_coordination.agents_by_role);
            this.updateCoordinationStats(stats.agent_coordination.coordination_stats);
            this.updateHealthIndicator('coordinatorHealth', stats.agent_coordination.system_running ? 'healthy' : 'error');
        }
    }
    
    updateThreatChart(threatData) {
        if (!this.charts.threats) return;
        
        const chart = this.charts.threats;
        const now = new Date().toLocaleTimeString();
        
        // Add new data point
        chart.data.labels.push(now);
        const threatLevel = this.getThreatLevelValue(threatData.threat_level);
        chart.data.datasets[0].data.push(threatLevel);
        
        // Keep only last 20 data points
        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        
        chart.update();
    }
    
    getThreatLevelValue(level) {
        const levels = { 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4 };
        return levels[level] || 0;
    }
    
    displayRecentThreat(threatData) {
        const threatsList = document.querySelector('.threats-list');
        
        // Remove "no data" message
        const noData = threatsList.querySelector('.no-data');
        if (noData) noData.remove();
        
        // Create threat item
        const threatItem = document.createElement('div');
        threatItem.className = `threat-item threat-level-${threatData.threat_level.toLowerCase()}`;
        threatItem.innerHTML = `
            <div><strong>${threatData.threat_level}</strong> - ${threatData.threat_id}</div>
            <div>Confidence: ${(threatData.confidence_score * 100).toFixed(1)}%</div>
            <div>Indicators: ${threatData.quantum_indicators.join(', ')}</div>
        `;
        
        threatsList.insertBefore(threatItem, threatsList.firstChild);
        
        // Keep only last 5 threats
        while (threatsList.children.length > 5) {
            threatsList.removeChild(threatsList.lastChild);
        }
    }
    
    updateAgentGrid(agentsByRole) {
        const agentGrid = document.getElementById('agentGrid');
        agentGrid.innerHTML = '';
        
        for (const [role, agents] of Object.entries(agentsByRole)) {
            agents.forEach(agent => {
                const agentCard = document.createElement('div');
                agentCard.className = `agent-card ${agent.status}`;
                agentCard.innerHTML = `
                    <div class="agent-role">${role}</div>
                    <div class="agent-status">${agent.status}</div>
                    <div class="agent-workload">${agent.workload}/${agent.max_workload}</div>
                `;
                agentGrid.appendChild(agentCard);
            });
        }
    }
    
    updateCoordinationStats(stats) {
        if (!stats) return;
        
        document.getElementById('totalCoordinations').textContent = stats.total_coordinations || 0;
        
        const successRate = stats.successful_defenses / Math.max(1, stats.total_coordinations) * 100;
        document.getElementById('successRate').textContent = `${successRate.toFixed(1)}%`;
        
        document.getElementById('avgResponseTime').textContent = `${Math.round(stats.average_response_time || 0)}ms`;
    }
    
    updateHealthIndicator(elementId, status) {
        const healthElement = document.getElementById(elementId);
        if (!healthElement) return;
        
        const dot = healthElement.querySelector('.health-dot');
        const text = healthElement.querySelector('span');
        
        dot.className = `health-dot ${status}`;
        text.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }
    
    updateConnectionStatus(status) {
        const statusDot = document.getElementById('systemStatus');
        const statusText = document.getElementById('systemStatusText');
        
        statusDot.className = `status-dot ${status}`;
        statusText.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        
        this.updateHealthIndicator('websocketHealth', status === 'online' ? 'healthy' : 'error');
    }
    
    updateLastUpdateTime() {
        const now = new Date().toLocaleTimeString();
        document.getElementById('lastUpdate').textContent = now;
    }
    
    log(message, type = 'system') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = { timestamp, message, type };
        
        this.logBuffer.push(logEntry);
        if (this.logBuffer.length > this.maxLogEntries) {
            this.logBuffer.shift();
        }
        
        this.renderLog();
    }
    
    renderLog() {
        const logContainer = document.getElementById('logContainer');
        const autoScroll = document.getElementById('autoScroll').checked;
        
        logContainer.innerHTML = '';
        
        this.logBuffer.forEach(entry => {
            const logDiv = document.createElement('div');
            logDiv.className = `log-entry ${entry.type} slide-in`;
            logDiv.innerHTML = `
                <span class="timestamp">[${entry.timestamp}]</span>
                <span class="message">${entry.message}</span>
            `;
            logContainer.appendChild(logDiv);
        });
        
        if (autoScroll) {
            logContainer.scrollTop = logContainer.scrollHeight;
        }
    }
    
    clearLog() {
        this.logBuffer = [];
        this.renderLog();
    }
    
    sendWebSocketMessage(message) {
        if (this.websocket && this.isConnected) {
            this.websocket.send(JSON.stringify(message));
        }
    }
    
    // API interaction methods
    async simulateQuantumAttack() {
        try {
            const response = await fetch('/simulate/quantum_attack?intensity=5', {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                this.log(`Quantum attack simulated: ${result.threats_detected} threats detected`, 'threat');
            }
        } catch (error) {
            this.log('Failed to simulate quantum attack', 'error');
        }
    }
    
    async createCanaryToken() {
        try {
            const response = await fetch('/quantum/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data_type: 'test_data' })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.log(`Canary token created: ${result.token_id}`, 'system');
            }
        } catch (error) {
            this.log('Failed to create canary token', 'error');
        }
    }
    
    async fragmentTestData() {
        try {
            const testData = `Sensitive test data ${Date.now()}`;
            const response = await fetch('/temporal/fragment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: testData })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.log(`Data fragmented: ${result.fragments_created} fragments created`, 'fragment');
            }
        } catch (error) {
            this.log('Failed to fragment data', 'error');
        }
    }
    
    async reconstructData() {
        // This would need a specific fragment ID to reconstruct
        this.log('Reconstruction requires specific fragment ID', 'system');
    }
    
    async triggerCoordination() {
        try {
            const response = await fetch('/agents/coordinate', {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                this.log('Agent coordination triggered manually', 'agent');
            }
        } catch (error) {
            this.log('Failed to trigger coordination', 'error');
        }
    }
    
    async refreshAgentStatus() {
        try {
            const response = await fetch('/agents/status');
            if (response.ok) {
                const status = await response.json();
                this.updateAgentGrid(status.agents_by_role);
                this.updateCoordinationStats(status.coordination_stats);
                this.log('Agent status refreshed', 'system');
            }
        } catch (error) {
            this.log('Failed to refresh agent status', 'error');
        }
    }
    
    startHealthMonitoring() {
        setInterval(() => {
            // Update system health indicators
            if (this.isConnected) {
                this.updateHealthIndicator('websocketHealth', 'healthy');
            } else {
                this.updateHealthIndicator('websocketHealth', 'error');
            }
        }, 5000); // Check every 5 seconds
    }
    
    showNotification(message, severity = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${severity} fade-in`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #00ffff;
            border-radius: 8px;
            color: white;
            z-index: 1001;
            max-width: 300px;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
    
    closeModal() {
        document.getElementById('modal').style.display = 'none';
    }
    
    showModal(title, content) {
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalBody').innerHTML = content;
        document.getElementById('modal').style.display = 'block';
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new MWRASPDashboard();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && window.dashboard) {
        // Reconnect WebSocket if needed
        if (!window.dashboard.isConnected) {
            window.dashboard.connectWebSocket();
        }
    }
});