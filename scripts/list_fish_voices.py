import aiohttp
import asyncio
import os
import sys

# Load env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_processor.config import Config

async def list_voices():
    # Found that /model (no v1) works or returns data
    url = "https://api.fish.audio/model" 
    
    headers = {
        "Authorization": f"Bearer {Config.FISH_AUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            print(f"GET /model Status: {resp.status}")
            if resp.status == 200:
                data = await resp.json()
                
                # Filter for Korean
                korean_voices = [
                    (m.get("_id"), m.get("title"), m.get("languages")) 
                    for m in data.get("items", []) 
                    if "ko" in m.get("languages", [])
                ]
                
                if korean_voices:
                    print(f"Found {len(korean_voices)} Korean voices:")
                    for vid, vtitle, vlang in korean_voices[:5]:
                        print(f"ID: {vid}, Title: {vtitle}, Langs: {vlang}")
                else:
                    print("No Korean voices found. Showing first 5 valid ANY:")
                    for m in data.get("items", [])[:5]:
                         print(f"ID: {m.get('_id')}, Title: {m.get('title')}, Langs: {m.get('languages')}")

if __name__ == "__main__":
    asyncio.run(list_voices())
