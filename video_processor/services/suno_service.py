import aiohttp
import asyncio
from ..config import Config

class SunoService:
    def __init__(self):
        self.api_url = Config.SUNO_API_URL

    async def generate_music(self, prompt: str, lyrics: str, title: str):
        """
        Attempts to generate music via the wrapper.
        If Config.MANUAL_SUNO_MODE is True or wrapper fails, returns a specific status to trigger manual intervention.
        """
        if Config.MANUAL_SUNO_MODE:
             return {"status": "manual_required", "message": "Manual mode is active."}

        # Try automatic generation
        try:
            async with aiohttp.ClientSession() as session:
                # Schema: CustomModeGenerateParam
                # prompt: lyrics
                # tags: style of music
                # title: song title
                # mv: model version
                payload = {
                    "prompt": lyrics,
                    "tags": prompt, 
                    "title": title,
                    "mv": "chirp-v3-5",
                    "negative_tags": ""
                }
                async with session.post(f"{self.api_url}/generate", json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"status": "started", "task_id": data.get("id")} # Adjust based on actual wrapper response
                    else:
                        error_text = await response.text()
                        print(f"Suno Wrapper Error: {error_text}")
                        return {"status": "manual_required", "message": f"Wrapper API failed: {error_text}"}
        except Exception as e:
            print(f"Suno Connection Error: {e}")
            return {"status": "manual_required", "message": f"Connection failed: {e}"}

    async def check_status(self, task_id: str):
        # Implementation to poll for status from wrapper
        pass
