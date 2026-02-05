import logging
import aiohttp
import asyncio
import os
import requests
import base64
from typing import Dict, Any
from lumaai import LumaAI  # V2 SDK
from ..config import Config

logger = logging.getLogger(__name__)

class ExternalApiService:
    def __init__(self):
        self.fish_api_key = Config.FISH_AUDIO_API_KEY
        self.hedra_api_key = Config.HEDRA_API_KEY
        self.runway_api_key = Config.RUNWAY_API_KEY
        self.luma_api_key = Config.LUMA_API_KEY
        
        # Initialize Luma Client if key exists
        self.luma_client = LumaAI(auth_token=self.luma_api_key) if self.luma_api_key else None

    async def _upload_to_temp_host(self, file_path: str) -> str:
        """
        Uploads local file to tmpfiles.org to get a public URL for Luma API.
        Returns the DIRECT download URL (e.g., https://tmpfiles.org/dl/...).
        """
        url = "https://tmpfiles.org/api/v1/upload"
        try:
            data = aiohttp.FormData()
            data.add_field('file', open(file_path, 'rb'), filename=os.path.basename(file_path))
            
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        resp_json = await response.json()
                        raw_url = resp_json['data']['url']
                        # Convert to direct link: https://tmpfiles.org/123/img.png -> https://tmpfiles.org/dl/123/img.png
                        direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                        logger.info(f"Uploaded temp asset: {direct_url}")
                        return direct_url
                    else:
                        logger.error(f"Temp upload failed: {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"Temp upload error: {e}")
            return None

    async def generate_video_luma(self, prompt: str, image_url: str = None, end_image_url: str = None) -> str:
        """
        Generate video using Luma Dream Machine API (Raw HTTP).
        Uses tmpfiles.org to bypass local file restriction.
        Target: Ray-2 (1080p).
        Supports: Start Image (frame0) AND End Image (frame1) for Interpolation.
        """
        if not self.luma_api_key:
            logger.error("Luma API Key missing!")
            return None

        logger.info(f"Generating Video via Luma (Raw API): {prompt[:50]}...")
        
        # 1. Handle Start Image
        final_image_url = image_url
        if image_url and not image_url.startswith("http"):
            if os.path.exists(image_url):
                 logger.info(f"Uploading Start Image to temp host...")
                 final_image_url = await self._upload_to_temp_host(image_url)
        
        # 2. Handle End Image (For Interpolation)
        final_end_image_url = end_image_url
        if end_image_url and not end_image_url.startswith("http"):
            if os.path.exists(end_image_url):
                 logger.info(f"Uploading End Image to temp host...")
                 final_end_image_url = await self._upload_to_temp_host(end_image_url)

        url = "https://api.lumalabs.ai/dream-machine/v1/generations"
        headers = {
            "Authorization": f"Bearer {self.luma_api_key}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "model": "ray-2"
        }
        
        payload["keyframes"] = {}
        
        if final_image_url:
            payload["keyframes"]["frame0"] = {
                "type": "image",
                "url": final_image_url
            }
            logger.info(f" - Set Start Keyframe: {final_image_url}")

        if final_end_image_url:
            payload["keyframes"]["frame1"] = {
                "type": "image",
                "url": final_end_image_url
            }
            logger.info(f" - Set End Keyframe: {final_end_image_url}")
            
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                # 1. Create Generation
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status != 201 and response.status != 200:
                        err_text = await response.text()
                        logger.error(f"Luma Create Failed ({response.status}): {err_text}")
                        return None
                    
                    data = await response.json()
                    gen_id = data.get("id")
                    logger.info(f"Luma Generation Started: {gen_id}")
                
                # 2. Poll for Completion
                poll_url = f"{url}/{gen_id}"
                
                for _ in range(60): # Poll for ~5 mins (60 * 5s)
                    await asyncio.sleep(5)
                    async with session.get(poll_url, headers=headers) as resp:
                        if resp.status != 200:
                             logger.warning(f"Luma Poll Error: {resp.status}")
                             continue
                        
                        status_data = await resp.json()
                        state = status_data.get("state")
                        
                        if state == "completed":
                            assets = status_data.get("assets", {})
                            video_url = assets.get("video")
                            logger.info(f"Luma Generation Completed: {video_url}")
                            
                            if not video_url: return None
                            
                            filename = f"luma_{gen_id}.mp4"
                            path = await self.download_file(video_url, filename)
                            return path
                            
                        elif state == "failed":
                            logger.error(f"Luma Generation Failed: {status_data.get('failure_reason')}")
                            return None
                        else:
                            logger.info(f"Luma Status: {state}...")
                            
                logger.error("Luma Timeout")
                return None

        except Exception as e:
            logger.error(f"Luma API Error: {e}")
            return None

    async def download_file(self, url: str, filename: str) -> str:

        """Downloads a file from a URL to TEMP_DIR."""
        if not url: return None
        if not url.startswith("http"): return url # Assume local path

        # Auto-extract Suno MP3 from Share Link
        if "suno.com/s/" in url:
            try:
                import re
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.get(url) as page_resp:
                        if page_resp.status == 200:
                            html = await page_resp.text()
                            match = re.search(r'(https://cdn[0-9]*\.suno\.ai/[^"]+\.mp3)', html)
                            if match:
                                url = match.group(1)
                                logger.info(f"Resolved Suno Share Link to: {url}")
            except Exception as e:
                logger.error(f"Failed to resolve Suno link: {e}")

        filepath = os.path.join(Config.TEMP_DIR, filename)
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(filepath, "wb") as f:
                            f.write(await response.read())
                        return filepath
                    else:
                        logger.error(f"Download Failed: {url} -> {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Download Error: {e}")
            return None

    async def generate_model_audio(self, text: str) -> str:
        """Generation using standard model if reference fails."""
        # This is a placeholder if we find a model-based endpoint
        pass

    async def generate_audio_fish(self, text: str, reference_id: str = "728f6ff2240d49308e8137ffe66008e2") -> str:
        """
        Generates TTS audio via Fish Audio API.
        Attempts to use the provided reference_id as 'model_id'.
        """
        url = "https://api.fish.audio/v1/tts"
        headers = {
            "Authorization": f"Bearer {self.fish_key}",
            "Content-Type": "application/json"
        }
        
        # FIX: Use 'model_id' instead of 'reference_id' based on debug result
        payload = {
            "text": text,
            "model_id": reference_id,
            "format": "mp3",
            "mp3_bitrate": 128
        }
        
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        content = await response.read()
                        filename = f"fish_{hash(text)}.mp3"
                        filepath = os.path.join(Config.TEMP_DIR, filename)
                        with open(filepath, "wb") as f:
                            f.write(content)
                        return filepath
                    else:
                        error_text = await response.text()
                        logger.error(f"Fish Audio Error: {error_text}")
                        # If failed, try without ID (Default)
                        if "model_id" in payload:
                            del payload["model_id"]
                            async with session.post(url, headers=headers, json=payload) as resp2:
                                if resp2.status == 200:
                                    logger.info("Fish Audio: Used default model as fallback.")
                                    content = await resp2.read()
                                    with open(filepath, "wb") as f: f.write(content)
                                    return filepath
                        
                        return "tests/assets/dummy_voice.mp3"
        except Exception as e:
            logger.error(f"Fish Audio Connection Error: {e}")
            return "tests/assets/dummy_voice.mp3"


    async def generate_video_hedra(self, text: str, audio_path: str, image_url: str) -> str:
        """
        Generates Lip-Sync Video via Hedra API.
        Uses multipart/form-data to upload local audio file directly.
        """
        url = "https://api.hedra.ai/v1/portrait" 
        headers = {
            "X-API-KEY": self.hedra_key
            # Content-Type is auto-set by FormData
        }
        
        # Prepare Multipart Data
        data = aiohttp.FormData()
        data.add_field('avatar_image', image_url)
        data.add_field('aspect_ratio', '16:9')
        # Add Audio File
        if audio_path and os.path.exists(audio_path):
            data.add_field('audio', open(audio_path, 'rb'), filename=os.path.basename(audio_path), content_type='audio/mpeg')
        else:
            logger.error("Hedra: Audio path invalid")
            return None
        
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        resp_data = await response.json()
                        job_id = resp_data.get("job_id")
                        return job_id 
                    else:
                        logger.error(f"Hedra Error: {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"Hedra Connection Error: {e}")
            return None

    async def generate_video_runway(self, prompt: str, image_url: str = None, seed: int = None) -> str:
        """
        Generates Video via Runway Gen-3 Alpha Turbo (API).
        Incorporates Forced Cinematic Keywords and Seed Management.
        """
        url = "https://api.dev.runwayml.com/v1/image_to_video"
        headers = {
            "Authorization": f"Bearer {self.runway_key}",
            "X-Runway-Version": "2024-11-06",
            "Content-Type": "application/json"
        }
        
        # EXPERT MODE: Forced Cinematic Technical Language (Prompt Density)
        forced_tags = (
            "Cinematic volumetric fog, Ray-traced reflections, Physical camera simulation, "
            "120fps slow-motion interpolation, 8K RAW footage, high-contrast chiaroscuro, "
            "volumetric god-rays, massive scale, global illumination, unreal engine 5.4 render quality."
        )
        
        # Blockbuster Enhancement: Use user-provided image or a thematic 'Primordial Void' fallback
        # This prevents the 'Globe' issue and fits the Genesis theme.
        if image_url and not image_url.startswith("http"):
            # Assume local file -> Convert to Base64 Data URI
            try:
                import base64
                import mimetypes
                
                if os.path.exists(image_url):
                    mime_type, _ = mimetypes.guess_type(image_url)
                    if not mime_type: mime_type = "image/png"
                    
                    with open(image_url, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        image_url = f"data:{mime_type};base64,{encoded_string}"
                        logger.info(f"Converted local image to Base64: {len(image_url)} chars")
                else:
                    logger.warning(f"Local image file not found: {image_url}")
                    image_url = None
            except Exception as e:
                logger.error(f"Failed to encode local image: {e}")
                image_url = None

        base_image = image_url or "https://images.unsplash.com/photo-1464802686167-b939a6910659?q=80&w=1280&auto=format&fit=crop"
        
        full_prompt = f"{prompt}, {forced_tags}"
        
        payload = {
            "model": "gen3a_turbo", 
            "promptText": full_prompt,
            "promptImage": [{"uri": base_image, "position": "first"}], 
            "duration": 10, 
            "ratio": "1280:768",
            "motion": 5 # Reduce motion slightly for 10s stability
        }
        
        if seed:
            payload["seed"] = seed
        
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                # 1. Trigger Generation
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        logger.error(f"Runway Trigger Error: {await response.text()}")
                        return "tests/assets/phase1.mp4" # Fallback
                    
                    data = await response.json()
                    task_id = data.get("id")
                    logger.info(f"Runway Task Started: {task_id}")

                # 2. Poll for Completion
                # 2. Poll for Completion
                poll_url = f"https://api.dev.runwayml.com/v1/tasks/{task_id}"
                for _ in range(150): # Wait up to 300s (5m)
                    await asyncio.sleep(2)
                    async with session.get(poll_url, headers=headers) as resp:
                        if resp.status != 200: continue
                        task_data = await resp.json()
                        status = task_data.get("status")
                        
                        if status == "SUCCEEDED":
                            # Download
                            video_url = task_data.get("output", [None])[0]
                            if video_url:
                                return await self.download_file(video_url, f"runway_{task_id}.mp4")
                        elif status == "FAILED":
                             logger.error(f"Runway Task Failed: {task_data}")
                             return "tests/assets/phase1.mp4"
                
                logger.error("Runway Timeout")
                return "tests/assets/phase1.mp4"

        except Exception as e:
            logger.error(f"Runway Error: {e}")
            return "tests/assets/phase1.mp4"


