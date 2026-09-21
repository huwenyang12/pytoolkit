# pytoolkit

Python自动化工具库，用于整理和复用日常开发、RPA 和自动化项目中的通用能力。

## 功能

- 飞书通知
  - 文本消息
  - 图片消息
- 企业微信通知
  - 文本消息
  - 图片消息
- 日志
  - 控制台彩色输出
  - 按日期生成日志文件
- 截图
  - Windows 桌面截图
- 录屏
  - 基于 FFmpeg 的桌面录屏
- 浏览器
  - 启动 Chrome 远程调试模式
- 通用工具
  - JSON 配置读取
  - 重试装饰器

## 项目结构

```text
pytoolkit/
├── bin/                  # 第三方工具
├── feishu.py             # 飞书通知
├── wecom.py              # 企业微信通知
├── log.py                # 日志封装
├── screenshot.py         # 桌面截图
├── screen_recorder.py    # 桌面录屏
├── start_browser.py      # Chrome 调试模式启动
├── utils.py              # 通用工具
├── config.example.json   # 配置模板
└── requirements.txt      # Python 依赖
```
