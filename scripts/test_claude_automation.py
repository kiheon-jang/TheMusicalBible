import asyncio
import json
import os
import sys

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.services.claude_service import ClaudeService

async def test_automation():
    service = ClaudeService()
    
    scripture_text = """
    1 태초에 하나님이 천지를 창조하시니라
    2 땅이 혼돈하고 공허하며 흑암이 깊음 위에 있고 하나님의 영은 수면 위에 운행하시니라
    3 하나님이 이르시되 빛이 있으라 하시니 빛이 있었고
    4 빛이 하나님이 보시기에 좋았더라 하나님이 빛과 어둠을 나누사
    5 하나님이 빛을 낮이라 부르시고 어둠을 밤이라 부르시니라 저녁이 되고 아침이 되니 이는 첫째 날이니라
    """
    
    context = {
        "book_name": "창세기",
        "chapter": 1,
        "verse": "1-5"
    }
    
    print("--- Testing Claude Automation Logic ---")
    playbook = await service.generate_production_playbook(scripture_text, context)
    
    print("\n[Playbook Result]")
    print(json.dumps(playbook, indent=2, ensure_ascii=False))
    
    print("\n--- Validation ---")
    style = playbook.get("musical_style", "")
    lyrics = playbook.get("lyrics", "")
    
    print(f"Musical Style: {style}")
    
    # Check Voice DB & Genre DB Integration
    if "Deep Male Baritone" in style or "God-like Voice" in style:
        print("✅ Voice DB (GOD) correctly identified.")
    else:
        print("❌ Voice DB identification failed or missing.")
        
    if "Epic Orchestral" in style or "Cinematic" in style:
        print("✅ Genre DB (EPIC) correctly identified.")
    else:
        print("❌ Genre DB identification failed or missing.")
        
    if "[End]" in lyrics:
        print("✅ Lyrics structure contains [End] tag.")
    else:
        print("❌ Lyrics structure missing [End] tag.")
        
    if any(char.isdigit() for char in lyrics if char not in ['[', ']']):
        # Numbers are okay in [Verse 1] or [Intro] if Claude adds them, 
        # but the prompt asks to remove numbers from scripture text.
        # Let's check for verse numbers like 1, 2, 3 in the text itself.
        print("⚠️ Warning: Numbers found in lyrics content. Claude might not have cleaned them perfectly.")
    else:
        print("✅ Numbers cleaned from lyrics.")

if __name__ == "__main__":
    asyncio.run(test_automation())
