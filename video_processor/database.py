from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from .config import Config
from datetime import datetime

engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Scripture(Base):
    __tablename__ = "scripture"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String)
    chapter = Column(Integer)
    verse = Column(Integer)
    korean_text = Column(Text)
    character_main = Column(String)
    emotion_primary = Column(String)
    
    # Levels
    fear_level = Column(Float, default=0.0)
    resolve_level = Column(Float, default=0.0)
    confusion_level = Column(Float, default=0.0)

    # Status
    status = Column(String, default="pending") # pending, processing_phase1, waiting_for_suno, completed
    
    # Phase 1
    phase1_shot_type = Column(String)
    phase1_location = Column(String)
    phase1_runway_prompt = Column(Text)
    phase1_duration = Column(Integer, default=8)

    # Phase 2
    phase2_character_state = Column(Text)
    phase2_hedra_prompt = Column(Text)
    phase2_duration = Column(Integer, default=10)

    # Phase 3 (Suno & Lyrics)
    phase3_vocal_lyrics = Column(Text)
    phase3_suno_prompt = Column(Text)
    phase3_visual_climax = Column(Text)
    phase3_duration = Column(Integer, default=12)
    suno_url = Column(Text) # The URL for the generated music (from wrapper or manual input)

    # Media URLs (Results)
    fish_url = Column(Text)
    hedra_url = Column(Text)
    runway_url = Column(Text)
    final_video_path = Column(Text)
    
    # Metadata
    fish_emotion_tags = Column(String)
    runway_seed = Column(String)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BookOrder(Base):
    __tablename__ = "book_order"

    id = Column(Integer, primary_key=True, index=True)
    book_number = Column(Integer, unique=True, nullable=False)
    book_name_korean = Column(String, unique=True, nullable=False)
    book_name_english = Column(String, nullable=False)
    testament = Column(String, nullable=False)
    chapter_count = Column(Integer, nullable=False)
    verse_count = Column(Integer, nullable=False)

class StoryUnit(Base):
    __tablename__ = "story_units"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    verses_range = Column(String, nullable=False)  # e.g., "1:1-5"
    title = Column(String, nullable=False)         # e.g., "Creation of the World"
    verse_count = Column(Integer, nullable=False)
    
    # Narrative Fields
    key_theme = Column(Text)
    story_arc = Column(Text)
    
    # 3-Phase Structure (Stored at Story Unit Level now, NOT Verse level)
    # Phase 1
    phase1_shot_type = Column(String)
    phase1_location = Column(String)
    phase1_runway_prompt = Column(Text)
    
    # Phase 2
    phase2_hedra_prompt = Column(Text)
    phase2_character_state = Column(Text)
    
    # Phase 3
    phase3_suno_prompt = Column(Text)
    phase3_vocal_lyrics = Column(Text)
    phase3_visual_climax = Column(Text)
    suno_url = Column(Text)

    # Results
    fish_url = Column(Text)
    hedra_url = Column(Text)
    runway_url = Column(Text)
    final_video_path = Column(Text)
    
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    scenes = relationship("StoryScene", back_populates="unit", cascade="all, delete-orphan")

class StoryScene(Base):
    __tablename__ = "story_scenes"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("story_units.id"))
    
    sequence_order = Column(Integer) # 1, 2, 3...
    
    # The Visual Director's instructions
    visual_prompt = Column(Text) 
    phase_type = Column(String) # 'context', 'tension', 'aria'
    
    # Generated Asset
    video_path = Column(String, nullable=True)
    
    unit = relationship("StoryUnit", back_populates="scenes")

class VerseToStory(Base):
    __tablename__ = "verse_to_story"
    
    id = Column(Integer, primary_key=True, index=True)
    story_unit_id = Column(Integer, nullable=False) # ForeignKey added in logic or properly
    scripture_id = Column(Integer, nullable=False)
    order_in_story = Column(Integer)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
