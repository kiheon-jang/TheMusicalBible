import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from video_processor.services.claude_service import ClaudeService

async def debug():
    claude = ClaudeService()
    text = "태초에 하나님이 천지를 창조하시니라 땅이 혼돈하고 공허하며 흑암이 깊음 위에 있고 하나님의 신은 수면에 운행하시니라 하나님이 가라사대 빛이 있으라 하시매 빛이 있었고 그 빛이 하나님의 보시기에 좋았더라 하나님이 빛과 어두움을 나누사 빛을 낮이라 칭하시고 어두움을 밤이라 칭하시니라 저녁이 되며 아침이 되니 이는 첫째 날이니라"
    context = {"book_name": "Genesis", "chapter": 1, "verse": 1}
    
    print("--- Requesting Playbook ---")
    playbook = await claude.generate_production_playbook(text, context)
    
    import json
    print("\n--- Final Parsed Playbook ---")
    print(json.dumps(playbook, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(debug())
