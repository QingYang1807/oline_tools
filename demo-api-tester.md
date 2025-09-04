# 🔌 接口请求工具演示

## 🎯 工具概述

这是一个简易的接口请求工具，类似 Postman 的功能，使用 fetch API 实现 GET/POST 等多种请求方法。无需打开 Postman 就能测试接口！

## 🚀 快速开始

### 1. 访问工具
- 打开浏览器访问：`http://localhost:8080/tools/api-tester.html`
- 或者从首页点击"🔌 接口请求工具"卡片

### 2. 基本功能演示

#### GET 请求测试
1. 选择请求方法：`GET`
2. 输入测试 URL：`https://httpbin.org/get`
3. 点击"发送请求"
4. 查看响应结果

#### POST 请求测试
1. 选择请求方法：`POST`
2. 输入测试 URL：`https://httpbin.org/post`
3. 在 JSON 标签页输入：
```json
{
  "name": "测试用户",
  "message": "Hello World"
}
```
4. 点击"发送请求"
5. 查看响应结果

### 3. 高级功能

#### 自定义请求头
- 添加 `Authorization: Bearer your-token`
- 添加 `X-Custom-Header: custom-value`

#### 多种请求体格式
- **JSON**: 结构化数据
- **Form Data**: 表单数据
- **Raw**: 原始文本

#### 请求历史
- 自动保存每次请求
- 点击历史记录快速重试
- 支持清空历史

## 🧪 测试用例

### 测试接口列表

| 接口 | 方法 | 说明 |
|------|------|------|
| `https://httpbin.org/get` | GET | 获取请求信息 |
| `https://httpbin.org/post` | POST | 提交数据 |
| `https://httpbin.org/put` | PUT | 更新数据 |
| `https://httpbin.org/delete` | DELETE | 删除数据 |
| `https://httpbin.org/status/404` | GET | 测试错误状态 |
| `https://jsonplaceholder.typicode.com/users/1` | GET | 获取用户信息 |

### 常用测试数据

#### JSON 格式
```json
{
  "title": "测试标题",
  "body": "测试内容",
  "userId": 1
}
```

#### Form Data 格式
```
title=测试标题
body=测试内容
userId=1
```

## ✨ 特色功能

1. **响应式设计**: 支持桌面、平板、手机
2. **主题适配**: 自动适配明暗主题
3. **实时验证**: JSON 格式自动验证
4. **性能监控**: 显示请求响应时间
5. **错误处理**: 友好的错误提示
6. **本地存储**: 请求历史自动保存

## 🔧 使用技巧

1. **快速测试**: 使用 httpbin.org 等测试服务
2. **历史管理**: 利用历史记录功能
3. **请求头**: 合理设置 Content-Type
4. **错误排查**: 查看响应头信息
5. **性能评估**: 观察响应时间

## 🌟 适用场景

- **前端开发**: 测试后端 API 接口
- **后端开发**: 验证接口功能
- **测试人员**: 接口功能测试
- **学习研究**: 了解 HTTP 协议
- **快速调试**: 临时测试接口

## 🎉 开始使用

现在就可以开始使用这个工具了！访问 `http://localhost:8080/tools/api-tester.html` 体验便捷的接口测试功能。

---

**提示**: 工具已预置了一些测试数据，可以直接点击"发送请求"进行测试！