import aiohttp
import asyncio
import os
import sys

# Load env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_processor.config import Config

async def test_claude():
    api_key = Config.CLAUDE_API_KEY
    url = "https://api.anthropic.com/v1/messages"
    
    # Models to try
    models = [
        "claude-3-5-sonnet-20240620",
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        for model in models:
            print(f"Testing model: {model}...")
            payload = {
                "model": model,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            
            try:
                async with session.post(url, headers=headers, json=payload) as resp:
                    print(f"Status: {resp.status}")
                    if resp.status == 200:
                        print(f"✅ SUCCESS with {model}")
                        print(await resp.json())
                        return
                    else:
                        print(f"❌ FAILED: {await resp.text()}")
            except Exception as e:
                print(f"Error: {e}")
            print("-" * 20)

if __name__ == "__main__":
    asyncio.run(test_claude())
