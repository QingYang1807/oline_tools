// HTML代码示例
const htmlExamples = {
    basic: `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>基础页面示例</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 { color: #333; }
        p { color: #666; }
        .highlight { 
            background: #f0f8ff; 
            padding: 10px; 
            border-radius: 5px; 
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>欢迎使用HTML预览工具</h1>
    <p>这是一个基础的HTML页面示例。</p>
    <div class="highlight">
        <p>这个工具可以帮助您快速预览HTML代码效果。</p>
    </div>
    <p>您可以在左侧编辑器中修改代码，右侧会实时显示效果。</p>
</body>
</html>`,

    card: `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>卡片布局示例</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h3 {
            color: #333;
            margin-top: 0;
        }
        .card p {
            color: #666;
            line-height: 1.6;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>卡片布局示例</h1>
        <div class="card-grid">
            <div class="card">
                <h3>卡片标题 1</h3>
                <p>这是第一张卡片的内容。卡片布局是现代网页设计中常用的元素。</p>
            </div>
            <div class="card">
                <h3>卡片标题 2</h3>
                <p>这是第二张卡片的内容。使用CSS Grid可以轻松创建响应式卡片布局。</p>
            </div>
            <div class="card">
                <h3>卡片标题 3</h3>
                <p>这是第三张卡片的内容。悬停效果让卡片更加生动有趣。</p>
            </div>
        </div>
    </div>
</body>
</html>`,

    form: `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>表单示例</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .form-container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #5a67d8;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>联系我们</h2>
        <form>
            <div class="form-group">
                <label for="name">姓名：</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">邮箱：</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="subject">主题：</label>
                <select id="subject" name="subject">
                    <option value="">请选择主题</option>
                    <option value="general">一般咨询</option>
                    <option value="support">技术支持</option>
                    <option value="feedback">意见反馈</option>
                </select>
            </div>
            <div class="form-group">
                <label for="message">消息：</label>
                <textarea id="message" name="message" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn">发送消息</button>
        </form>
    </div>
</body>
</html>`
};

// 加载示例代码的函数
function loadExample(type) {
    if (htmlExamples[type]) {
        const htmlCode = document.getElementById('htmlCode');
        htmlCode.value = htmlExamples[type];
        updatePreview();
        updateCharCount();
        setStatus(`已加载${type}示例`);
    }
}