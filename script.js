class QRCodeReader {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.resultSection = document.getElementById('resultSection');
        this.previewImage = document.getElementById('previewImage');
        this.resultText = document.getElementById('resultText');
        this.copyBtn = document.getElementById('copyBtn');
        this.openLinkBtn = document.getElementById('openLinkBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupClipboardPaste();
        this.setupDragAndDrop();
    }

    setupEventListeners() {
        // 文件上传按钮
        this.uploadBtn.addEventListener('click', () => {
            this.fileInput.click();
        });

        // 文件选择
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFile(e.target.files[0]);
            }
        });

        // 复制按钮
        this.copyBtn.addEventListener('click', () => {
            this.copyToClipboard();
        });

        // 打开链接按钮
        this.openLinkBtn.addEventListener('click', () => {
            this.openLink();
        });

        // 清除按钮
        this.clearBtn.addEventListener('click', () => {
            this.clearAll();
        });
    }

    setupClipboardPaste() {
        // 监听全局粘贴事件
        document.addEventListener('paste', (e) => {
            e.preventDefault();
            this.handlePaste(e);
        });

        // 监听键盘快捷键
        document.addEventListener('keydown', (e) => {
            // Ctrl+V (Windows/Linux) 或 Cmd+V (Mac)
            if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
                // 让默认的paste事件处理
                return;
            }
        });
    }

    setupDragAndDrop() {
        // 拖拽进入
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });

        // 拖拽离开
        this.uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
        });

        // 拖拽放下
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        });
    }

    async handlePaste(e) {
        const items = e.clipboardData.items;
        
        for (let item of items) {
            if (item.type.indexOf('image') !== -1) {
                const file = item.getAsFile();
                if (file) {
                    this.handleFile(file);
                    break;
                }
            }
        }
    }

    async handleFile(file) {
        // 验证文件类型
        if (!file.type.startsWith('image/')) {
            this.showError('请选择图片文件');
            return;
        }

        // 验证文件大小 (最大10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('文件大小不能超过10MB');
            return;
        }

        this.hideError();
        this.showLoading();

        try {
            // 读取文件
            const imageData = await this.readFileAsImageData(file);
            
            // 显示预览
            this.showPreview(file);
            
            // 解析二维码
            const result = await this.decodeQRCode(imageData);
            
            if (result) {
                this.showResult(result);
            } else {
                this.showError('未检测到二维码，请确保图片中包含清晰的二维码');
            }
        } catch (error) {
            console.error('处理文件时出错:', error);
            this.showError('处理图片时出错，请重试');
        } finally {
            this.hideLoading();
        }
    }

    readFileAsImageData(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    canvas.width = img.width;
                    canvas.height = img.height;
                    ctx.drawImage(img, 0, 0);
                    
                    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                    resolve(imageData);
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    async decodeQRCode(imageData) {
        try {
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            return code ? code.data : null;
        } catch (error) {
            console.error('解析二维码时出错:', error);
            return null;
        }
    }

    showPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.previewImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    showResult(result) {
        this.resultText.value = result;
        this.resultSection.style.display = 'block';
        
        // 检查是否为URL
        if (this.isValidUrl(result)) {
            this.openLinkBtn.style.display = 'inline-block';
        } else {
            this.openLinkBtn.style.display = 'none';
        }
        
        // 滚动到结果区域
        this.resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    async copyToClipboard() {
        try {
            await navigator.clipboard.writeText(this.resultText.value);
            this.showSuccess('内容已复制到剪贴板');
        } catch (error) {
            // 降级方案
            this.resultText.select();
            document.execCommand('copy');
            this.showSuccess('内容已复制到剪贴板');
        }
    }

    openLink() {
        const url = this.resultText.value;
        if (this.isValidUrl(url)) {
            window.open(url, '_blank');
        }
    }

    clearAll() {
        this.resultSection.style.display = 'none';
        this.fileInput.value = '';
        this.resultText.value = '';
        this.previewImage.src = '';
        this.hideError();
        this.hideLoading();
    }

    showLoading() {
        this.uploadArea.classList.add('loading');
    }

    hideLoading() {
        this.uploadArea.classList.remove('loading');
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.style.display = 'block';
        setTimeout(() => {
            this.errorMessage.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }

    hideError() {
        this.errorMessage.style.display = 'none';
    }

    showSuccess(message) {
        // 创建临时成功提示
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <div class="success-content">
                <span class="success-icon">✅</span>
                <span>${message}</span>
            </div>
        `;
        
        // 添加样式
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 15px;
            color: #155724;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(successDiv);
        
        // 3秒后自动移除
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new QRCodeReader();
});

// 添加一些额外的键盘快捷键
document.addEventListener('keydown', (e) => {
    // ESC 键清除所有内容
    if (e.key === 'Escape') {
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            clearBtn.click();
        }
    }
    
    // Enter 键打开链接（如果当前焦点在结果区域）
    if (e.key === 'Enter' && e.target.id === 'resultText') {
        const openLinkBtn = document.getElementById('openLinkBtn');
        if (openLinkBtn && openLinkBtn.style.display !== 'none') {
            openLinkBtn.click();
        }
    }
});