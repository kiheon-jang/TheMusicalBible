import asyncio
import aiohttp
import os
import sys
from dotenv import load_dotenv

load_dotenv()

async def test_runway():
    key = os.getenv("RUNWAY_API_KEY")
    if not key:
        print("Error: RUNWAY_API_KEY not found in .env")
        return

    # Try both dev and prod URLs if needed, but start with the one in code
    url = "https://api.dev.runwayml.com/v1/image_to_video"
    headers = {
        "Authorization": f"Bearer {key}",
        "X-Runway-Version": "2024-11-06",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gen3a_turbo", 
        "promptText": "A cinematic shot of a sunset over the ocean, volumetric fog, high-density cinematic.",
        "promptImage": [{"uri": "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=1280&auto=format&fit=crop", "position": "first"}], 
        "duration": 5, 
        "ratio": "1280:768",
        "motion": 7
    }
    
    print(f"Testing URL: {url}")
    print(f"Payload: {payload}")
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post(url, headers=headers, json=payload) as response:
            status = response.status
            text = await response.text()
            print(f"Status: {status}")
            print(f"Response: {text}")

if __name__ == "__main__":
    asyncio.run(test_runway())
