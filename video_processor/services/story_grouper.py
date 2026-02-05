import logging
from typing import List
from sqlalchemy.orm import Session
from ..database import Scripture, StoryUnit, VerseToStory, BookOrder
from ..services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

class StoryGrouper:
    def __init__(self, db: Session):
        self.db = db
        self.claude = ClaudeService()

    async def create_next_story_unit(self) -> StoryUnit:
        """
        1. Finds the next 'ungrouped' verses in Biblical order.
        2. Selects a chunk (e.g., 5-10 verses).
        3. Asks Claude to define the best 'Story Unit' boundary (where the scene ends).
        4. Creates a StoryUnit record and links verses.
        """
        # 1. Find first verse not in any story
        # We need a way to check if verse is linked. 
        # Left Join VerseToStory where story_id is null?
        # Efficient query: Get 10 pending verses sorted by order.
        
        # Or simplistic: Get top 20 verses from 'Scripture' table that don't have a mapping.
        # This requires a subquery or checking IDs.
        
        # Let's assume Scripture status 'pending' means not processed.
        # But we need a new status 'grouped'? 
        # Or just use the existence of VerseToStory.
        
        # Let's clean up logic: Scripture Status = 'pending' -> 'grouped' -> ...
        
        # Get next 15 pending verses (e.g. Genesis 1:1-15)
        # We really need BookOrder sorting here.
        
        from sqlalchemy import text
        
        # Raw SQL might be easier for complex join/sort, ORM for safety
        # "Select s.* from Scripture s join BookOrder b ... where status='pending' limit 20"
        
        pending_verses = (
            self.db.query(Scripture)
            .join(BookOrder, Scripture.book_name == BookOrder.book_name_korean)
            .filter(Scripture.status == 'pending')
            .order_by(BookOrder.book_number, Scripture.chapter, Scripture.verse)
            .limit(15)
            .all()
        )
        
        if not pending_verses:
            logger.info("No pending verses to group.")
            return None

        # Format for Claude
        verses_text = "\n".join([f"[{v.id}] {v.book_name} {v.chapter}:{v.verse} - {v.korean_text}" for v in pending_verses])
        
        # Ask Claude to Group
        # "Look at these verses. Decide where the first coherant story/scene ends. 
        # Return the IDs of verses included, a Title, and a Summary."
        
        # PROMPT LOGIC (Simplified for MVP)
        # ... call self.claude.group_verses(...)
        
        # MOCK LOGIC for Speed: Group first 5 verses, or by paragraph breaks?
        # Let's just group 3-5 verses as a unit for now to test the pipeline flow.
        
        selected_verses = pending_verses[:4] # Group 4 verses
        first = selected_verses[0]
        last = selected_verses[-1]
        range_str = f"{first.chapter}:{first.verse}-{last.verse}"
        
        title = f"{first.book_name} - {range_str}" # Placeholder title
        
        # Create StoryUnit
        new_unit = StoryUnit(
            book_name=first.book_name,
            verses_range=range_str,
            title=title,
            verse_count=len(selected_verses),
            status="pending"
        )
        self.db.add(new_unit)
        self.db.commit() # Commit to get ID
        
        # Link Verses
        for i, v in enumerate(selected_verses):
            link = VerseToStory(
                story_unit_id=new_unit.id,
                scripture_id=v.id,
                order_in_story=i+1
            )
            self.db.add(link)
            v.status = "grouped" # Mark as grouped so we don't pick them again
        
        self.db.commit()
        logger.info(f"Created Story Unit: {new_unit.title} (ID: {new_unit.id})")
        return new_unit
