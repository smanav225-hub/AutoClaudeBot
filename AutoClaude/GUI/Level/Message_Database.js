/**
 * Data Management Modal
 * Standalone JavaScript for data management functionality
 * 
 * Usage in level.html:
 * 1. Add: <script src="dataManagement.js"></script>
 * 2. Add button: <button onclick="openDataManagement()" class="btn-data">📊 Data</button>
 */

(function () {
    'use strict';

    let statsRetryTimer = null;

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function waitForBackendReady(maxRetries = 8, delayMs = 1000) {
        for (let i = 0; i < maxRetries; i++) {
            try {
                const resp = await fetch(`${window.location.origin}/api/servers`);
                if (resp.ok) return true;
            } catch (e) {
                // ignore and retry
            }
            await sleep(delayMs);
        }
        return false;
    }

    // Create and inject modal styles
    const styles = `
        .data-mgmt-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }

        .data-mgmt-overlay.show {
            opacity: 1;
            visibility: visible;
        }

        .data-mgmt-modal {
            background-color: #2a2c31;
            border-radius: 12px;
            padding: 24px;
            width: 95%;
            max-width: 420px;
            max-height: 75vh;
            overflow-y: auto;
            border: 1px solid #3f4147;
            position: relative;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            animation: dataMgmtSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        @keyframes dataMgmtSlideIn {
            from {
                transform: translateY(-30px) scale(0.95);
                opacity: 0;
            }
            to {
                transform: translateY(0) scale(1);
                opacity: 1;
            }
        }

        .data-mgmt-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid #3f4147;
        }

        .data-mgmt-title {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
        }

        .data-mgmt-title h2 {
            font-size: 18px;
            font-weight: 700;
            margin: 0;
            color: #ffffff;
        }

        .data-mgmt-back {
            background: none;
            border: none;
            color: #b5bac1;
            cursor: pointer;
            font-size: 20px;
            padding: 4px 8px;
            transition: color 0.2s;
            margin-right: 8px;
        }

        .data-mgmt-back:hover {
            color: #ffffff;
        }

        .data-mgmt-close {
            background: none;
            border: none;
            color: #b5bac1;
            cursor: pointer;
            font-size: 24px;
            padding: 0;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: color 0.2s;
        }

        .data-mgmt-close:hover {
            color: #ffffff;
        }

        .data-mgmt-content {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .data-mgmt-section {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .data-mgmt-label {
            font-size: 11px;
            font-weight: 700;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .data-mgmt-btn {
            background-color: #1e1f22;
            border: 1px solid #3f4147;
            border-radius: 6px;
            padding: 12px 16px;
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-family: inherit;
        }

        .data-mgmt-btn:hover {
            background-color: #313339;
            border-color: #5865f2;
        }

        .data-mgmt-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .data-mgmt-btn-primary {
            background-color: #5865f2;
            border-color: #5865f2;
            color: #ffffff;
        }

        .data-mgmt-btn-primary:hover {
            background-color: #4752c4;
        }

        .data-mgmt-btn-secondary {
            background-color: #4e5058;
            border-color: #4e5058;
        }

        .data-mgmt-btn-secondary:hover {
            background-color: #5a5d62;
        }

        .data-mgmt-status-box {
            background-color: #1e1f22;
            border: 1px solid #3f4147;
            border-left: 3px solid #6b7280;
            border-radius: 6px;
            padding: 12px;
            font-size: 12px;
            color: #b5bac1;
            transition: border-color 0.3s;
        }

        .data-mgmt-status-box.downloading {
            border-left-color: #5865f2;
        }

        .data-mgmt-status-box.completed {
            border-left-color: #10b981;
        }

        .data-mgmt-status-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .data-mgmt-status-text {
            color: #ffffff;
        }

        .data-mgmt-status-icon {
            font-size: 14px;
        }

        .data-mgmt-progress-bar {
            width: 100%;
            height: 6px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 8px;
        }

        .data-mgmt-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #5865f2, #7289da);
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 3px;
        }

        .data-mgmt-progress-text {
            font-size: 11px;
            color: #9ca3af;
            margin-top: 6px;
            text-align: center;
        }

        .data-mgmt-stat-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            font-size: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .data-mgmt-stat-item:last-child {
            border-bottom: none;
        }

        .data-mgmt-stat-label {
            color: #b5bac1;
        }

        .data-mgmt-stat-value {
            color: #ffffff;
            font-weight: 600;
        }

        .data-mgmt-stat-value.active {
            color: #10b981;
        }

        .data-mgmt-modal::-webkit-scrollbar {
            width: 8px;
        }

        .data-mgmt-modal::-webkit-scrollbar-track {
            background: transparent;
        }

        .data-mgmt-modal::-webkit-scrollbar-thumb {
            background: #4a4d52;
            border-radius: 4px;
        }

        .data-mgmt-modal::-webkit-scrollbar-thumb:hover {
            background: #5a5d62;
        }
    `;

    // Inject styles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Create modal HTML
    const modalHTML = `
        <div id="dataManagementOverlay" class="data-mgmt-overlay">
            <div class="data-mgmt-modal">
                <!-- Header -->
                <div class="data-mgmt-header">
                    <div class="data-mgmt-title">
                        <button class="data-mgmt-back" onclick="closeDataManagement()" title="Back">←</button>
                        <span style="font-size: 18px;">📊</span>
                        <h2>Data Management</h2>
                    </div>
                    <button class="data-mgmt-close" onclick="closeDataManagement()" title="Close">✕</button>
                </div>

                <!-- Content -->
                <div class="data-mgmt-content">
                    <!-- Message History Section -->
                    <div class="data-mgmt-section">
                        <label class="data-mgmt-label">📥 Message History</label>
                        <button class="data-mgmt-btn data-mgmt-btn-primary" id="downloadBtn" onclick="downloadMessages()">
                            <span>⬇️</span> Download All Previous Messages
                        </button>
                    </div>

                    <!-- Status Section -->
                    <div class="data-mgmt-section">
                        <label class="data-mgmt-label">Status</label>
                        <div class="data-mgmt-status-box" id="statusBox">
                            <div class="data-mgmt-status-header">
                                <span>Status: <span class="data-mgmt-status-text" id="statusText">Idle</span></span>
                                <span class="data-mgmt-status-icon" id="statusIcon">⭕</span>
                            </div>
                            <div class="data-mgmt-progress-bar">
                                <div class="data-mgmt-progress-fill" id="progressFill"></div>
                            </div>
                            <div class="data-mgmt-progress-text">
                                <span id="progressText">Ready to download</span>
                            </div>
                        </div>
                    </div>

                    <!-- Tracking Status -->
                    <div class="data-mgmt-section">
                        <label class="data-mgmt-label">🔄 Tracking Status</label>
                        <div style="background-color: #1e1f22; border: 1px solid #3f4147; border-radius: 6px; padding: 12px;">
                            <div class="data-mgmt-stat-item">
                                <span class="data-mgmt-stat-label">Status:</span>
                                <span class="data-mgmt-stat-value active">ACTIVE ✅</span>
                            </div>
                            <div class="data-mgmt-stat-item">
                                <span class="data-mgmt-stat-label">Messages today:</span>
                                <span class="data-mgmt-stat-value" id="messagestoday">0</span>
                            </div>
                            <div class="data-mgmt-stat-item">
                                <span class="data-mgmt-stat-label">Last updated:</span>
                                <span class="data-mgmt-stat-value" id="lastupdated">Never</span>
                            </div>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="data-mgmt-section">
                        <button class="data-mgmt-btn data-mgmt-btn-secondary" onclick="refreshStats()">
                            <span>🔄</span> Refresh Stats
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Insert modal into page when DOM is ready
    function initModal() {
        if (document.body) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            const btn = document.getElementById('downloadBtn');
            if (btn) {
                btn.innerHTML = '<span>&#x2B07;&#xFE0F;</span> Update/Add Previous Messages';
            }
        } else {
            setTimeout(initModal, 100);
        }
    }

    // Open Data Management Modal
    window.openDataManagement = function () {
        const overlay = document.getElementById('dataManagementOverlay');
        if (overlay) {
            overlay.classList.add('show');
            document.body.style.overflow = 'hidden';
            refreshStats(true);
        }
    };

    // Close Data Management Modal
    window.closeDataManagement = function () {
        const overlay = document.getElementById('dataManagementOverlay');
        if (overlay) {
            overlay.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    };

    // Download Messages
    window.downloadMessages = async function () {
        const urlParams = new URLSearchParams(window.location.search);
        const guildId = urlParams.get('guild_id');
        if (!guildId) { alert("Guild ID missing"); return; }

        const statusBox = document.getElementById('statusBox');
        const statusText = document.getElementById('statusText');
        const statusIcon = document.getElementById('statusIcon');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const btn = document.getElementById('downloadBtn');

        btn.disabled = true;
        statusBox.classList.remove('idle');
        statusBox.classList.add('downloading');
        statusText.textContent = 'Starting...';
        statusIcon.textContent = '⏳';
        progressFill.style.width = '0%';
        progressText.textContent = 'Initiating request...';

        try {
            const ready = await waitForBackendReady();
            if (!ready) {
                throw new Error('Backend is still starting, please try again in a moment.');
            }
            // 1. Start Background Task
            const startResp = await fetch(`${window.location.origin}/api/messages/download/${guildId}`);
            if (!startResp.ok) {
                throw new Error(`Server error (${startResp.status})`);
            }
            const startData = await startResp.json();

            if (!startData.success) {
                if (startData.error && startData.error.includes("progress")) {
                    // Already running, just poll
                } else {
                    throw new Error(startData.error || 'Failed to start');
                }
            }

            // 2. Poll Status
            const poll = setInterval(async () => {
                try {
                    const statusResp = await fetch(`${window.location.origin}/api/messages/download/status/${guildId}`);
                    if (!statusResp.ok) {
                        throw new Error(`Server error (${statusResp.status})`);
                    }
                    const statusData = await statusResp.json();

                    if (statusData.success && statusData.status) {
                        const s = statusData.status;

                        if (s === 'downloading' || s === 'starting') {
                            statusText.textContent = 'Downloading';
                            progressText.textContent = statusData.progress_text || `Downloaded ${statusData.total || 0} messages...`;
                            // Fake progress bar movement or estimate
                            progressFill.style.width = '50%';
                        } else if (s === 'completed') {
                            clearInterval(poll);
                            progressFill.style.width = '100%';
                            statusText.textContent = 'Exporting...';
                            statusBox.classList.remove('downloading');
                            statusBox.classList.add('completed');
                            statusText.textContent = 'Completed';
                            statusIcon.textContent = 'âœ…';
                            const total = statusData.total || 0;
                            progressText.textContent = `${total.toLocaleString()} messages updated`;
                            btn.disabled = false;
                            return;

                            // 3. Export File
                            const exportResp = await fetch(`${window.location.origin}/api/messages/export/${guildId}`);
                            const exportData = await exportResp.json();

                            if (exportData.success) {
                                statusBox.classList.remove('downloading');
                                statusBox.classList.add('completed');
                                statusText.textContent = 'Completed';
                                statusIcon.textContent = '✅';
                                progressText.textContent = `${exportData.count} messages saved`;

                                const link = document.createElement('a');
                                link.href = exportData.download_url;
                                link.download = exportData.download_url.split('/').pop();
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                            } else {
                                throw new Error(exportData.error || 'Export failed');
                            }
                            btn.disabled = false;
                        } else if (s === 'error') {
                            clearInterval(poll);
                            throw new Error(statusData.error || 'Loading. Please wait for 1-2 minutes.');
                        }
                    } else if (statusData && statusData.error) {
                        clearInterval(poll);
                        throw new Error(statusData.error);
                    }
                } catch (err) {
                    console.error("Poll error", err);
                    clearInterval(poll);
                    statusBox.classList.remove('downloading');
                    statusText.textContent = 'Error';
                    progressText.textContent = err && err.message ? err.message : "Connection lost";
                    btn.disabled = false;
                }
            }, 2000); // Poll every 2s

        } catch (error) {
            console.error(error);
            statusBox.classList.remove('downloading');
            statusText.textContent = 'Error';
            statusIcon.textContent = '❌';
            progressText.textContent = error && error.message ? error.message : "Connection lost";
            btn.disabled = false;
        }
    };

    // Refresh Stats
    window.refreshStats = async function (isInit = false) {
        const messagestoday = document.getElementById('messagestoday');
        const lastupdated = document.getElementById('lastupdated');

        const urlParams = new URLSearchParams(window.location.search);
        const guildId = urlParams.get('guild_id');
        if (!guildId) return;

        messagestoday.textContent = isInit ? "Starting..." : "Loading...";

        try {
            const response = await fetch(`${window.location.origin}/api/stats/messages-today/${guildId}`);
            if (!response.ok) {
                throw new Error(`Server error (${response.status})`);
            }
            const data = await response.json();
            if (data.success) {
                messagestoday.textContent = data.count.toLocaleString();
            } else {
                throw new Error(data.error || 'Failed to load stats');
            }
        } catch (e) {
            console.error("Stats error", e);
            messagestoday.textContent = "Starting...";
            if (!statsRetryTimer) {
                statsRetryTimer = setTimeout(() => {
                    statsRetryTimer = null;
                    refreshStats(false);
                }, 1500);
            }
        }

        const now = new Date();
        lastupdated.textContent = now.toLocaleTimeString();
    };

    // Close on overlay click
    document.addEventListener('click', function (event) {
        const overlay = document.getElementById('dataManagementOverlay');
        if (overlay && event.target === overlay) {
            closeDataManagement();
        }
    });

    // Close on ESC key
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeDataManagement();
        }
    });

    // Initialize modal when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initModal);
    } else {
        initModal();
    }
})();
