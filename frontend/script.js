// 全局变量
let currentMode = 'idea'; // 'idea' 或 'references'
let conversationId = null;
let isLoading = false;

// API配置
const API_BASE_URL = 'http://localhost:5000';

// DOM 元素
const outputArea = document.querySelector('.output-area');
const inputArea = document.querySelector('textarea');
const sendButton = document.querySelector('button');

// 文件上传相关
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
let selectedFiles = new Map();

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 显示模式选择提示
    addSystemMessage('请选择输入模式：\n1. 输入具体研究想法\n2. 输入相关文献');
    
    // 添加模式选择按钮
    const modeButtons = document.createElement('div');
    modeButtons.className = 'mode-buttons';
    modeButtons.innerHTML = `
        <button onclick="selectMode('idea')">研究想法</button>
        <button onclick="selectMode('references')">相关文献</button>
    `;
    outputArea.appendChild(modeButtons);

    // 测试后端连接
    testBackendConnection();
});

// 测试后端连接
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: 'test' })
        });
        
        if (response.ok) {
            addSystemMessage('系统已就绪');
        } else {
            addSystemMessage('后端服务器连接失败，请确保服务器已启动');
        }
    } catch (error) {
        console.error('Backend connection test failed:', error);
        addSystemMessage('无法连接到后端服务器，请检查：\n1. 后端服务器是否已启动\n2. 端口 5000 是否被占用\n3. 防火墙设置是否允许连接');
    }
}

// 选择输入模式
function selectMode(mode) {
    currentMode = mode;
    const modeButtons = document.querySelector('.mode-buttons');
    if (modeButtons) {
        modeButtons.remove();
    }
    
    if (mode === 'idea') {
        addSystemMessage('请输入您的研究想法，包括：\n- 研究主题\n- 研究目标\n- 预期贡献');
    } else {
        addSystemMessage('请输入相关文献，每篇文献请包含：\n- 标题\n- 作者\n- 摘要\n- 关键发现');
    }
}

// 设置加载状态
function setLoading(loading) {
    isLoading = loading;
    sendButton.disabled = loading;
    inputArea.disabled = loading;
    fileInput.disabled = loading;
    
    if (loading) {
        sendButton.innerHTML = '<div class="loading-spinner"></div>';
        addSystemMessage('正在处理您的请求，请稍候...');
    } else {
        sendButton.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>';
    }
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 添加文件到列表
function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.innerHTML = `
        <span class="file-name">${file.name}</span>
        <span class="file-size">${formatFileSize(file.size)}</span>
        <span class="remove-file" onclick="removeFile('${file.name}')">×</span>
    `;
    fileList.appendChild(fileItem);
    selectedFiles.set(file.name, file);
}

// 移除文件
function removeFile(fileName) {
    selectedFiles.delete(fileName);
    updateFileList();
}

// 更新文件列表显示
function updateFileList() {
    fileList.innerHTML = '';
    selectedFiles.forEach((file) => addFileToList(file));
}

// 处理文件选择
fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    files.forEach(file => {
        if (!selectedFiles.has(file.name)) {
            addFileToList(file);
        }
    });
});

// 修改发送消息函数，添加文件分析结果显示
sendButton.addEventListener('click', async () => {
    if (isLoading) return;
    
    const message = inputArea.value.trim();
    if (!message && selectedFiles.size === 0) {
        addSystemMessage('请输入消息或上传文件');
        return;
    }

    setLoading(true);

    // 创建FormData对象
    const formData = new FormData();
    formData.append('message', message);
    formData.append('mode', currentMode);
    if (conversationId) {
        formData.append('conversationId', conversationId);
    }

    // 添加文件
    selectedFiles.forEach((file) => {
        formData.append('files', file);
    });

    try {
        // 显示用户输入
        addMessage(message, 'right', 'student');
        inputArea.value = '';

        // 发送到后端
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30秒超时

        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.conversationId) {
            conversationId = data.conversationId;
        }

        // 显示文件分析结果
        if (data.fileAnalysis && data.fileAnalysis.files) {
            data.fileAnalysis.files.forEach(file => {
                if (file.analysis && file.analysis.status === 'success') {
                    addSystemMessage(`文件 "${file.filename}" 分析结果：`);
                    addMessage(file.analysis.summary, 'left', 'system');
                } else if (file.error) {
                    addSystemMessage(`文件 "${file.filename}" 处理失败：${file.error}`);
                }
            });
        }

        // 显示系统响应
        if (data.analysis) {
            addSystemMessage('分析结果：');
            addMessage(data.analysis, 'left', 'system');
        }

        // 显示教授反馈
        if (data.professorFeedback) {
            addMessage(data.professorFeedback, 'left', 'professor');
        }

        // 显示研究顾问反馈
        if (data.researchFeedback) {
            addMessage(data.researchFeedback, 'left', 'research');
        }

        // 清空文件列表
        selectedFiles.clear();
        updateFileList();

    } catch (error) {
        console.error('Error:', error);
        if (error.name === 'AbortError') {
            addSystemMessage('请求超时，请重试');
        } else if (error.message.includes('Failed to fetch')) {
            addSystemMessage('无法连接到后端服务器，请确保服务器已启动');
        } else {
            addSystemMessage(`发生错误：${error.message}`);
        }
    } finally {
        setLoading(false);
    }
});

// 添加消息到聊天界面
function addMessage(content, position, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${position}`;
    
    const avatar = document.createElement('div');
    avatar.className = `avatar ${type}`;
    
    // 添加SVG图标
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', '2');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    
    // 根据角色类型设置不同的图标
    if (type === 'professor') {
        // 教授图标：眼镜和书本
        svg.innerHTML = `
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            <circle cx="8" cy="7" r="1"/>
            <circle cx="16" cy="7" r="1"/>
        `;
    } else if (type === 'research') {
        // 研究顾问图标：放大镜和图表
        svg.innerHTML = `
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            <line x1="8" y1="11" x2="14" y2="11"/>
            <line x1="11" y1="8" x2="11" y2="14"/>
        `;
    } else {
        // 博士生图标：毕业帽和笔
        svg.innerHTML = `
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M6 10.6V16a6 3 0 0 0 12 0v-5.4"/>
            <line x1="12" y1="22" x2="12" y2="16"/>
        `;
    }
    
    avatar.appendChild(svg);
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    outputArea.appendChild(messageDiv);
    outputArea.scrollTop = outputArea.scrollHeight;
}

// 添加系统消息
function addSystemMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    outputArea.appendChild(messageDiv);
    outputArea.scrollTop = outputArea.scrollHeight;
}

// 支持按Enter发送消息
inputArea.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendButton.click();
    }
}); 