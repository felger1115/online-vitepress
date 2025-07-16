一个基于 VitePress 的在线 Markdown 编辑器集成，让你可以直接在浏览器中编写和发布文章。
后端使用Pyhton quart

## 特性
- 在线查看文档列表
- 在线编辑文档
- 在线新建文档
- 在线删除文档
- api获取文档
- 使用quart-cors运行跨域, (修改代码, 可自行配置), 建议跨域在网关解决, 而不是在这里

todo: 
- [ ] 动态的菜单 vitepress defineConfig

更多功能正在开发中...

# user API

## 认证

所有API端点都需要通过会话ID（Authid）进行身份验证，该会话ID应作为cookie或在请求头中的“x-Authid”提供。

## api

- get api/v1/docs-list
- post api/v1/docs
- get api/v1/docs/<name>
- delete api/v1/docs/<name>

# root API

## 认证

所有API端点都需要通过认证, 认证信息需要在请求头中的“secret”提供。
所有root API端点都需要通过“x-Authid”头中提供。

## api

- post root/api/build
