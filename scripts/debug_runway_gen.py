import aiohttp
import asyncio
import os
import sys

# Load env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_processor.config import Config

async def test_runway_gen():
    api_key = Config.RUNWAY_API_KEY
    url = "https://api.dev.runwayml.com/v1/image_to_video"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Runway-Version": "2024-11-06",
        "Content-Type": "application/json"
    }

    # Minimal payload for Gen3 Alpha Turbo
    payload = {
        "model": "gen3a_turbo",
        "promptText": "A cinematic shot of a futuristic city",
        "promptImage": [{"uri": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=1280&auto=format&fit=crop", "position": "first"}],
        "duration": 5,
        "ratio": "1280:768"
    }

    print("Sending request to Runway API...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=payload) as resp:
                print(f"Status: {resp.status}")
                text = await resp.text()
                print(f"Response: {text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_runway_gen())
