## 使用方式

### 方法一：使用UV管理包

1. 下载uv

   ```
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. 下载[node.js](https://nodejs.org/zh-cn)

3. 进入根目录

4. 输入以下指令

   ```
   uv sync
   cd frontend
   npm install
   ```

5. 点击根目录下的`start_uv.bat`

### 方法二：用本地python

1. 确保python的版本为3.9
2. 下载[node.js](https://nodejs.org/zh-cn)

2. 输入以下命令

   ```
   pip install -r requirements.txt
   cd frontend
   npm install
   ```

3. 点击根目录下的`start.bat`

## 开发模式（前后端分离）：

终端1：启动后端

  cd backend && python main.py

终端2：启动前端开发服务器

  cd frontend && npm run serve

前端通过代理访问后端 API

## Agent API配置

运行一次后端后，会生成一个`backend\config\config.toml`文件，在该文件中配置`api_key`和`base_url`后重新运行后端即可