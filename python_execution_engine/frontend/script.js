// Python代码执行引擎前端脚本
class PythonExecutionEngine {
    constructor() {
        this.serverUrl = 'http://101.42.23.49/api';
        this.editor = null;
        this.currentTemplate = '';
        this.init();
    }

    init() {
        this.initEditor();
        this.bindEvents();
        this.checkServerStatus();
        this.loadPackages();
    }

    // 初始化代码编辑器
    initEditor() {
        this.editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
            mode: 'python',
            theme: 'default',
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            lineWrapping: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            foldGutter: true,
            gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
            extraKeys: {
                'Ctrl-Enter': () => this.executeCode(),
                'F5': () => this.executeCode(),
                'Ctrl-/': 'toggleComment',
                'Ctrl-A': 'selectAll'
            }
        });

        // 设置编辑器大小
        this.editor.setSize('100%', '100%');
    }

    // 绑定事件
    bindEvents() {
        // 运行按钮
        document.getElementById('runBtn').addEventListener('click', () => this.executeCode());
        
        // 清空按钮
        document.getElementById('clearBtn').addEventListener('click', () => this.clearCode());
        
        // 清空结果按钮
        document.getElementById('clearResultBtn').addEventListener('click', () => this.clearResult());
        
        // 复制结果按钮
        document.getElementById('copyResultBtn').addEventListener('click', () => this.copyResult());
        
        // 主题切换
        document.getElementById('themeSelect').addEventListener('change', (e) => {
            this.editor.setOption('theme', e.target.value);
        });
        
        // 模板相关按钮
        document.getElementById('showTemplatesBtn').addEventListener('click', () => this.showTemplates());
        document.getElementById('showPackagesBtn').addEventListener('click', () => this.showPackages());
        document.getElementById('showHelpBtn').addEventListener('click', () => this.showHelp());
        
        // 模态框关闭
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.target.closest('.modal').style.display = 'none';
            });
        });
        
        // 点击模态框外部关闭
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
        
        // 模板分类切换
        document.querySelectorAll('.template-category').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const category = e.target.dataset.category;
                this.switchTemplateCategory(category);
            });
        });
        
        // 使用模板按钮
        document.getElementById('useTemplateBtn').addEventListener('click', () => {
            this.useTemplate();
        });
    }

    // 检查服务器状态
    async checkServerStatus() {
        try {
            const response = await fetch(`${this.serverUrl}/health`);
            if (response.ok) {
                const data = await response.json();
                this.updateServerStatus(true, data);
            } else {
                this.updateServerStatus(false, null);
            }
        } catch (error) {
            this.updateServerStatus(false, null);
        }
    }

    // 更新服务器状态显示
    updateServerStatus(isOnline, data) {
        const statusElement = document.getElementById('serverStatus');
        if (isOnline) {
            statusElement.innerHTML = '<i class="fas fa-circle" style="color: #4CAF50;"></i> 服务器在线';
            statusElement.className = 'server-status online';
        } else {
            statusElement.innerHTML = '<i class="fas fa-circle" style="color: #f44336;"></i> 服务器离线';
            statusElement.className = 'server-status offline';
        }
    }

    // 执行Python代码
    async executeCode() {
        const code = this.editor.getValue().trim();
        if (!code) {
            this.showResult('error', '请输入要执行的Python代码');
            return;
        }

        this.showLoading(true);
        this.clearResult();

        try {
            const response = await fetch(`${this.serverUrl}/execute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });

            const result = await response.json();
            this.showLoading(false);

            if (result.success) {
                this.showResult('success', result.output, result);
            } else {
                this.showResult('error', result.error, result);
            }

            // 更新执行信息
            this.updateExecutionInfo(result);

        } catch (error) {
            this.showLoading(false);
            this.showResult('error', `网络错误: ${error.message}`);
        }
    }

    // 显示执行结果
    showResult(type, content, result = null) {
        const resultOutput = document.getElementById('resultOutput');
        
        // 清除欢迎消息
        const welcomeMsg = resultOutput.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        const resultDiv = document.createElement('div');
        resultDiv.className = `result-item ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        const header = document.createElement('div');
        header.className = 'result-header';
        header.innerHTML = `
            <span class="result-type">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                ${type === 'success' ? '执行成功' : '执行失败'}
            </span>
            <span class="result-time">${timestamp}</span>
        `;
        
        const body = document.createElement('div');
        body.className = 'result-body';
        body.textContent = content;
        
        resultDiv.appendChild(header);
        resultDiv.appendChild(body);
        
        resultOutput.appendChild(resultDiv);
        resultOutput.scrollTop = resultOutput.scrollHeight;

        // 如果有安装信息，显示出来
        if (result && result.install_message && result.install_message !== '无需安装包') {
            this.showInstallInfo(result.install_message);
        }
    }

    // 显示安装信息
    showInstallInfo(message) {
        const resultOutput = document.getElementById('resultOutput');
        const installDiv = document.createElement('div');
        installDiv.className = 'result-item info';
        
        const header = document.createElement('div');
        header.className = 'result-header';
        header.innerHTML = `
            <span class="result-type">
                <i class="fas fa-download"></i>
                包安装信息
            </span>
        `;
        
        const body = document.createElement('div');
        body.className = 'result-body';
        body.textContent = message;
        
        installDiv.appendChild(header);
        installDiv.appendChild(body);
        
        resultOutput.appendChild(installDiv);
    }

    // 更新执行信息
    updateExecutionInfo(result) {
        const execTime = document.getElementById('executionTime');
        const importsInfo = document.getElementById('importsInfo');
        
        if (result.execution_time) {
            execTime.innerHTML = `<i class="fas fa-clock"></i> 执行时间: ${result.execution_time}秒`;
        }
        
        if (result.imports_used && result.imports_used.length > 0) {
            importsInfo.innerHTML = `<i class="fas fa-download"></i> 导入包: ${result.imports_used.join(', ')}`;
        } else {
            importsInfo.innerHTML = `<i class="fas fa-download"></i> 导入包: 无`;
        }
    }

    // 显示/隐藏加载动画
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    // 清空代码
    clearCode() {
        if (confirm('确定要清空代码吗？')) {
            this.editor.setValue('');
            this.editor.focus();
        }
    }

    // 清空结果
    clearResult() {
        const resultOutput = document.getElementById('resultOutput');
        resultOutput.innerHTML = `
            <div class="welcome-message">
                <i class="fas fa-info-circle"></i>
                <p>点击"运行代码"按钮开始执行Python代码</p>
                <p>支持自动安装常用Python包，如numpy、pandas、matplotlib等</p>
            </div>
        `;
        
        // 清空执行信息
        document.getElementById('executionTime').innerHTML = '<i class="fas fa-clock"></i> 执行时间: --';
        document.getElementById('importsInfo').innerHTML = '<i class="fas fa-download"></i> 导入包: --';
    }

    // 复制结果
    copyResult() {
        const resultOutput = document.getElementById('resultOutput');
        const text = resultOutput.innerText;
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showToast('结果已复制到剪贴板', 'success');
            });
        } else {
            // 降级方案
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('结果已复制到剪贴板', 'success');
        }
    }

    // 显示模板
    showTemplates() {
        document.getElementById('templatesModal').style.display = 'block';
    }

    // 显示支持的包
    showPackages() {
        document.getElementById('packagesModal').style.display = 'block';
    }

    // 显示帮助
    showHelp() {
        document.getElementById('helpModal').style.display = 'block';
    }

    // 切换模板分类
    switchTemplateCategory(category) {
        // 更新按钮状态
        document.querySelectorAll('.template-category').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');
        
        // 更新内容显示
        document.querySelectorAll('.template-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`template${category.charAt(0).toUpperCase() + category.slice(1)}`).classList.add('active');
    }

    // 使用模板
    useTemplate() {
        const activeSection = document.querySelector('.template-section.active');
        const codeElement = activeSection.querySelector('code');
        const code = codeElement.textContent;
        
        this.editor.setValue(code);
        document.getElementById('templatesModal').style.display = 'none';
        this.editor.focus();
        
        this.showToast('模板已加载到编辑器', 'success');
    }

    // 加载支持的包列表
    async loadPackages() {
        try {
            const response = await fetch(`${this.serverUrl}/packages`);
            if (response.ok) {
                const data = await response.json();
                this.displayPackages(data.allowed_packages);
            }
        } catch (error) {
            console.error('加载包列表失败:', error);
        }
    }

    // 显示支持的包
    displayPackages(packages) {
        const packagesGrid = document.getElementById('packagesGrid');
        packagesGrid.innerHTML = '';
        
        // 按类别分组
        const categories = {
            '数据处理': ['numpy', 'pandas', 'scipy'],
            '可视化': ['matplotlib', 'seaborn', 'plotly', 'bokeh'],
            '机器学习': ['sklearn', 'tensorflow', 'torch', 'keras', 'xgboost', 'lightgbm'],
            '网络请求': ['requests', 'beautifulsoup4', 'lxml'],
            '图像处理': ['pillow', 'opencv-python'],
            'Web框架': ['flask', 'django', 'fastapi'],
            '数据库': ['sqlalchemy', 'pymongo'],
            '其他': ['jupyter', 'ipython', 'sympy', 'pytest', 'unittest']
        };
        
        Object.entries(categories).forEach(([category, categoryPackages]) => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'package-category';
            
            const categoryHeader = document.createElement('h4');
            categoryHeader.textContent = category;
            categoryDiv.appendChild(categoryHeader);
            
            const packagesList = document.createElement('div');
            packagesList.className = 'packages-list';
            
            categoryPackages.forEach(pkg => {
                if (packages.includes(pkg)) {
                    const packageDiv = document.createElement('div');
                    packageDiv.className = 'package-item';
                    packageDiv.textContent = pkg;
                    packagesList.appendChild(packageDiv);
                }
            });
            
            categoryDiv.appendChild(packagesList);
            packagesGrid.appendChild(categoryDiv);
        });
    }

    // 显示提示消息
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // 显示动画
        setTimeout(() => toast.classList.add('show'), 100);
        
        // 自动隐藏
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new PythonExecutionEngine();
});

// 键盘快捷键
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter 或 F5 执行代码
    if ((e.ctrlKey && e.key === 'Enter') || e.key === 'F5') {
        e.preventDefault();
        if (window.pythonEngine) {
            window.pythonEngine.executeCode();
        }
    }
});