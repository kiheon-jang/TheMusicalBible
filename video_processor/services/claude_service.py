import json
import logging
from typing import Dict, Any
import aiohttp
from ..config import Config

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        self.api_key = Config.CLAUDE_API_KEY
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-haiku-20240307"

    async def generate_production_playbook(self, scripture_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        V5 Architecture: Multi-Stage Expert Review System.
        Phase 1: Draft Generation
        Phase 2: Step-by-Step Expert Refinement (Theologian -> Maestro -> Visual)
        """
        # Phase 1: Generate Draft
        draft_json = await self._generate_initial_draft(scripture_text, context)
        if not draft_json: return self._get_fallback_playbook(scripture_text)
        
        # Phase 2: Expert Review & Refinement
        refined_json = await self._refine_playbook(draft_json, scripture_text)
        return refined_json

    async def _generate_initial_draft(self, scripture_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are the 'TMB Creative Executive Team'. Generate a DRAFT Production Playbook.\n"
            "Use your 4 Personas (Theologian, Playwright, Maestro, Visual Architect) to create a solid base.\n"
            "Keep the output structure strict JSON.\n"
            # ... (Abbreviated for brevity, reuse previous prompt basics)
            "CRITICAL: OUTPUT ONLY VALID JSON."
        )
        # Using the simplified draft prompt to save tokens, the review phase will add depth.
        user_content = f"Scripture: {scripture_text}\nContext: {context}"
        
        return await self._call_claude(system_prompt, user_content)

    async def _refine_playbook(self, draft: Dict[str, Any], scripture_text: str) -> Dict[str, Any]:
        """
        The 'Step-by-Step' Review Phase.
        The AI assumes the role of a 'Total Executive Director' reviewing the draft.
        """
        refinement_prompt = (
            "You are the 'Total Executive Producer' reviewing a draft for the Mega-Hit Musical 'TMB'.\n"
            "Your goal: Elevate this draft from 'Good' to 'Word-Class Masterpiece'.\n"
            "\n"
            "Perform a Step-by-Step Review:\n"
            "1. [Theologian Check]: Are there any doctrinal errors? (e.g. Is 'Fruit' mistaken for 'Apple'?)\n"
            "2. [Maestro Check]: Is the music direction TRENDY enough? Does it specifically mention instruments and BPM? If vague, FIX IT.\n"
            "3. [Visual Check]: Are the cinematic keywords (65mm, Anamorphic, Volumetric) present? If not, INJECT THEM.\n"
            "\n"
            "INPUT: Draft JSON\n"
            "OUTPUT: FINAL POLISHED JSON (Must maintain exact structure, but with upgraded content)."
        )
        
        user_content = f"Original Scripture: {scripture_text}\nDraft Playbook: {json.dumps(draft, ensure_ascii=False)}"
        
        refined_data = await self._call_claude(refinement_prompt, user_content)
        return refined_data if refined_data else draft

    async def _call_claude(self, system: str, user: str) -> Dict[str, Any]:
        """Helper to call Claude API"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": 2000,
            "system": system,
            "messages": [{"role": "user", "content": user}]
        }
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        logger.error(f"Claude API Error: {await response.text()}")
                        return None
                    data = await response.json()
                    return self._parse_json_response(data['content'][0]['text'])
        except Exception:
            logger.exception("Claude Call Failed")
            return None

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        try:
            # Common fix for Claude: It sometimes puts newlines in strings
            # which standard json.loads doesn't like.
            # But more robustly, we find the first '{' and last '}'
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = text[start:end]
                # If Claude included raw newlines in a string, we might need to escape them 
                # or use a more lenient parser. For now, let's try strict and fallback.
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to replace literal newlines within string values (heuristic)
                    # This is risky but sometimes necessary for Haiku
                    json_str_fixed = json_str.replace('\n', '\\n')
                    # Actually, a better way is to check if it's just the lyrics having newlines
                    # For now, let's try manually fixing the most common issue: newlines in the "lyrics" field
                    return json.loads(json_str, strict=False)
            return json.loads(text, strict=False)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from Claude response")
            return {}

    def _get_fallback_playbook(self, text: str) -> Dict[str, Any]:
        """Fallback if API fails"""
        return {
            "production_notes": "Fallback Mode",
            "musical_style": "Cinematic Orchestral",
            "title": "Genesis Fallback",
            "lyrics": text,
            "scenes": [
                {
                    "sequence": 1,
                    "phase": "context",
                    "visual_prompt": "Cinematic wide shot of ancient biblical landscape, atmospheric lighting, 8k",
                    "duration_estimate": 10
                },
                {
                    "sequence": 2,
                    "phase": "aria",
                    "visual_prompt": "Epic light breaking through darkness, particles floating, divine atmosphere",
                    "duration_estimate": 10
                }
            ]
        }
