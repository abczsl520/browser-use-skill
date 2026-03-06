"""
Browser-Use 通用模板
安装: pip install browser-use playwright langchain-openai && playwright install chromium
用法: source ~/browser-use-env/bin/activate && python3 template.py
"""
import asyncio
from browser_use import Agent, ChatOpenAI, BrowserSession, BrowserProfile

# === 配置区（使用前必须填写） ===
API_KEY = "<YOUR_API_KEY>"        # 你的 OpenAI 兼容 API key
BASE_URL = "<YOUR_BASE_URL>"      # API 地址，如 https://api.openai.com/v1
MODEL = "gpt-4o-mini"             # 模型名

TASK = "打开 https://www.baidu.com，搜索'你的关键词'，返回第一条结果"

# 模式A: 内置Chromium
# profile = BrowserProfile(headless=False, user_data_dir="~/.browser-use/default-profile")

# 模式B: 连接真Chrome (推荐，需先启动: Chrome --remote-debugging-port=9222)
profile = BrowserProfile(cdp_url="http://127.0.0.1:9222")

USE_VISION = True   # 复杂页面开True
MAX_STEPS = 20      # 最大操作步数
# === 配置区结束 ===

async def main():
    llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=BASE_URL)
    session = BrowserSession(browser_profile=profile)

    agent = Agent(
        task=TASK,
        llm=llm,
        browser_session=session,
        use_vision=USE_VISION,
        max_steps=MAX_STEPS,
    )

    result = await agent.run()
    print("=== 结果 ===")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
