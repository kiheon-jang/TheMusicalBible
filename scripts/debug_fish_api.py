import aiohttp
import asyncio
import os
import sys

# Load env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_processor.config import Config

async def debug_fish():
    token = Config.FISH_AUDIO_API_KEY
    if not token:
        print("❌ No API Key found in Config")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Check Profile/Balance (if endpoint exists/traceable)
    # Common endpoints: /v1/users/me, /v1/wallet, /user
    print("--- 1. Checking Auth ---")
    async with aiohttp.ClientSession() as session:
        balance_url = "https://api.fish.audio/v1/user/profile" # Guessing based on common patterns or docs
        # Or /v1/wallet
        try:
             async with session.get("https://api.fish.audio/v1/wallet", headers=headers) as resp:
                 if resp.status == 200:
                     print(f"✅ Wallet Check: {await resp.json()}")
                 else:
                     print(f"⚠️ Wallet Check Failed: {resp.status}")
                     # Try generic /model to proof key works generally
                     async with session.get("https://api.fish.audio/model", headers=headers) as m_resp:
                         print(f"Model List Status: {m_resp.status} (Key works if 200)")
        except Exception as e:
            print(f"Auth Check Error: {e}")

    # 2. Test Generation Variations
    print("\n--- 2. Testing Generations ---")
    
    # IDs we found earlier
    test_ids = [
        "728f6ff2240d49308e8137ffe66008e2", # ElevenLabs Adam (System?)
        "26ff45fab722431c85eea2536e5c5197", # Idea Vilarino
    ]
    
    url = "https://api.fish.audio/v1/tts"
    
    async with aiohttp.ClientSession() as session:
        for ref_id in test_ids:
            print(f"\nTesting Reference ID: {ref_id}")
            
            # Variant A: Standard 'reference_id'
            payload_a = {
                "text": "Hello, this is a debug test.",
                "reference_id": ref_id,
                "format": "mp3"
            }
            try:
                async with session.post(url, headers=headers, json=payload_a) as resp:
                    if resp.status == 200:
                        print(f"✅ Variant A (reference_id) SUCCESS! Content-Type: {resp.headers.get('Content-Type')}")
                        return # Found valid config
                    else:
                        print(f"❌ Variant A Failed: {resp.status} - {await resp.text()}")
            except Exception as e: print(f"Error: {e}")

            # Variant B: 'model_id' (Some models use this field instead)
            payload_b = {
                "text": "Hello, this is a debug test.",
                "model_id": ref_id, # Trying same ID as model_id
                "format": "mp3"
            }
            try:
                async with session.post(url, headers=headers, json=payload_b) as resp:
                    if resp.status == 200:
                        print(f"✅ Variant B (model_id) SUCCESS!")
                        return
                    else:
                        print(f"❌ Variant B Failed: {resp.status} - {await resp.text()}")
            except Exception as e: print(f"Error: {e}")
            
        # Variant C: No ID (Default?)
        print("\nTesting NO ID (Default)")
        payload_c = {
            "text": "Hello, this is a debug test.",
            "format": "mp3"
        }
        try:
             async with session.post(url, headers=headers, json=payload_c) as resp:
                if resp.status == 200:
                    print(f"✅ Variant C (No ID) SUCCESS!")
                else:
                    print(f"❌ Variant C Failed: {resp.status} - {await resp.text()}")
        except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_fish())
