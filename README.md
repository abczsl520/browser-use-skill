# 🌐 Browser-Use Skill for OpenClaw

> **Stop fighting with snapshot→act loops.** Let AI handle complex browser automation end-to-end.

[![ClawHub](https://img.shields.io/badge/ClawHub-browser--use-blue)](https://clawhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## The Problem

OpenClaw's built-in browser tool works great for simple tasks — take a screenshot, click a button. But for **multi-step workflows** (login → navigate → fill form → submit), it falls apart:

- 🔄 Endless snapshot→act loops, often clicking the wrong element
- 💥 Breaks on dynamic pages (popups, redirects, lazy loading)
- 🚫 Gets detected by anti-bot systems

## The Solution

This skill integrates [Browser-Use](https://github.com/browser-use/browser-use) — an AI browser agent that **sees the page like a human** and completes entire workflows autonomously.

```
You: "Log into Reddit and post this article"
Browser-Use: ✅ Opens login page → types credentials → handles CAPTCHA wait → 
             navigates to submit → fills title & body → clicks Post → Done.
```

## When to Use What

| Scenario | Built-in Tool | Browser-Use |
|----------|:---:|:---:|
| Screenshot / check a page | ✅ Free & fast | ❌ Overkill |
| Click one button | ✅ | ❌ |
| 5+ step workflow (login→fill→submit) | ❌ Breaks easily | ✅ |
| Anti-detection needed (real Chrome) | ❌ | ✅ |
| Batch/repeat operations | ❌ | ✅ |

## Install

```bash
clawhub install browser-use
```

Or manually: copy the `browser-use/` folder to `~/.openclaw/skills/`

## Setup (One-Time)

```bash
python3 -m venv ~/browser-use-env
source ~/browser-use-env/bin/activate
pip install browser-use playwright langchain-openai
playwright install chromium
```

## Two Modes

### Mode A: Built-in Chromium (Simple)
Works out of the box. Some sites may detect automation.

### Mode B: Connect to Real Chrome (Recommended) ✅
Uses your actual Chrome browser — **zero detection**. Sites see a real human browser.

```bash
# Quit Chrome first, then relaunch with debugging:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
```

## Quick Example

```python
import asyncio
from browser_use import Agent, ChatOpenAI, Browser

async def main():
    llm = ChatOpenAI(model="gpt-4o-mini", api_key="YOUR_KEY", base_url="https://api.openai.com/v1")
    browser = Browser(cdp_url="http://127.0.0.1:9222")  # Real Chrome
    
    agent = Agent(
        task="""
        1. Go to https://news.ycombinator.com
        2. Extract the top 5 story titles and URLs
        3. Return them as a list
        """,
        llm=llm, browser=browser, use_vision=True, max_steps=15,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Features

- 🎯 **Smart task routing** — Knows when to use Browser-Use vs built-in tool
- 🔐 **Sensitive data handling** — Passwords never sent to LLM (placeholder substitution)
- 🛡️ **Anti-detection** — Connect to real Chrome via CDP, undetectable
- 📝 **Task writing guide** — Prompting best practices for reliable automation
- 🔧 **Failure recovery** — Decision tree for CAPTCHA, timeouts, anti-spam
- ⚡ **Flash mode** — Skip reasoning for simple tasks, 2x faster

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `use_vision` | AI sees screenshots | `True` |
| `max_steps` | Max actions | `100` |
| `sensitive_data` | Password placeholders | `None` |
| `flash_mode` | Skip thinking (faster) | `False` |
| `fallback_llm` | Backup LLM on failure | `None` |
| `allowed_domains` | Restrict navigation | `None` |

## LLM Compatibility

| LLM | Works | Notes |
|-----|:---:|-------|
| GPT-4o / 4o-mini | ✅ | Best compatibility |
| Claude | ✅ | Works well |
| Gemini | ❌ | Structured output incompatible |

## Links

- [Browser-Use Documentation](https://docs.browser-use.com)
- [Browser-Use GitHub](https://github.com/browser-use/browser-use) (38k+ ⭐)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub Skills](https://clawhub.com)

## License

MIT
