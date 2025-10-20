# Technical Specifications

## Component Specifications

### 1. PDF Text Extraction (`scripts/extract_pdf.py`)

**Purpose:** Extract raw text from PDF files

**Dependencies:**
```python
import pdfplumber
import sys
import json
from pathlib import Path
```

**Function Signature:**
```python
def extract_text_from_pdf(pdf_path: str, output_dir: str) -> dict:
    """
    Extract text from PDF and save to working directory
    
    Args:
        pdf_path: Path to input PDF
        output_dir: Working directory for this book
    
    Returns:
        {
            'success': bool,
            'output_file': str,
            'page_count': int,
            'char_count': int,
            'warnings': list
        }
    """
```

**Implementation Notes:**
- Use `pdfplumber.open()` for best results
- Extract page by page, track page numbers
- Save as `extracted_v1.txt` in working dir
- Handle corrupted PDFs gracefully
- Return metadata about extraction

**Example Usage:**
```bash
python scripts/extract_pdf.py input/time_machine.pdf working/time_machine
```

---

### 2. Text Cleaning (`scripts/clean_text.py`)

**Purpose:** Fix OCR errors and normalize text

**Dependencies:**
```python
import re
import sys
from pathlib import Path
```

**Common OCR Fixes:**
```python
OCR_FIXES = {
    # Common character substitutions
    'rn': 'm',      # "rn" often read as "m"
    'vv': 'w',      # "vv" often read as "w"
    'l1': 'll',     # "l1" often read as "ll"
    'cl': 'd',      # "cl" often read as "d"
}

# Context-aware fixes (need regex)
def fix_zero_o(text):
    # Replace "0" with "O" only in words, not numbers
    return re.sub(r'(?<=[a-zA-Z])0(?=[a-zA-Z])', 'O', text)
```

**Cleaning Steps:**
1. Remove Gutenberg license text
2. Fix common OCR errors
3. Normalize quotes (" " to " ")
4. Normalize dashes (-- to —)
5. Remove page numbers (pattern: `\n\d+\n`)
6. Remove headers/footers (if detectable)
7. Normalize whitespace (multiple newlines → double newline)
8. Fix broken words at line breaks

**Function Signature:**
```python
def clean_text(input_file: str, output_file: str, fixes: dict = OCR_FIXES) -> dict:
    """
    Clean extracted text
    
    Returns:
        {
            'success': bool,
            'fixes_applied': int,
            'char_count_before': int,
            'char_count_after': int,
            'warnings': list
        }
    """
```

---

### 3. Structure Analysis (`scripts/analyze_structure.py`)

**Purpose:** Use AI to identify chapters, characters, dialogue

**Dependencies:**
```python
import anthropic
import json
import sys
from pathlib import Path
from lib.ai_client import AIClient
```

**AI Prompts:**

**Chapter Detection Prompt:**
```
You are analyzing a classic novel for an ESL learning platform.

Task: Identify all chapters in this text.

Common chapter patterns:
- "Chapter I", "CHAPTER 1", "I.", "1"
- Roman numerals (I, II, III, IV, V, etc.)
- Arabic numerals (1, 2, 3, etc.)
- May or may not have chapter titles

Important:
- Some books use unusual formatting
- Check for "Part I", "Book I" style divisions too
- Note if chapters have titles vs just numbers

Text to analyze:
{first_10000_chars}

Output as JSON:
{
  "chapters": [
    {
      "number": 1,
      "title": null or "Chapter Title",
      "starts_at_line": 5,
      "pattern_used": "Chapter I"
    }
  ],
  "total_chapters": 16,
  "chapter_pattern": "Roman numerals without titles",
  "confidence": 0.95
}
```

**Character Identification Prompt:**
```
You are analyzing dialogue and character mentions in a novel.

Task: Identify all named characters who speak or are referenced significantly.

For each character provide:
- Primary name (how they're most often called)
- Aliases (other names/pronouns used)
- Brief description (gender, age, role)
- First appearance (approximate chapter)

Look for:
- Dialogue attribution ("said X", "X replied")
- Direct address ("Listen, X")
- Third-person reference ("X did...")

Ignore:
- Generic references ("a man", "someone")
- Background characters with <3 mentions
- Place names

Text to analyze:
{chapter_chunks}

Output as JSON:
{
  "characters": [
    {
      "name": "Time Traveller",
      "aliases": ["the Traveller", "he", "the inventor"],
      "description": "Protagonist, inventor, middle-aged British man",
      "first_chapter": 1,
      "estimated_dialogue_percentage": 45,
      "voice_suggestion": "male_british_mature"
    }
  ],
  "confidence": 0.88
}
```

**Function Signature:**
```python
def analyze_structure(text_file: str, output_dir: str) -> dict:
    """
    Analyze book structure using AI
    
    Returns:
        {
            'success': bool,
            'structure_file': str,  # path to structure.json
            'review_file': str,     # path to review.json
            'confidence': float,
            'ready_for_review': bool
        }
    """
```

**Output Format (structure.json):**
```json
{
  "book": {
    "title": "The Time Machine",
    "author": "H.G. Wells",
    "year": 1895,
    "total_words": 35000,
    "total_chapters": 16,
    "gutenberg_id": 35
  },
  "chapters": [
    {
      "number": 1,
      "title": null,
      "starts_at_line": 5,
      "ends_at_line": 423,
      "word_count": 2847,
      "has_dialogue": true
    }
  ],
  "characters": [
    {
      "name": "Time Traveller",
      "aliases": ["the Traveller", "he"],
      "description": "Protagonist inventor, aged around 40",
      "first_chapter": 1,
      "voice_type": "male_british_mature",
      "dialogue_percentage": 45,
      "elevenlabs_voice_id": null  # filled in later
    }
  ],
  "processed_at": "2025-01-15T10:30:00Z",
  "processing_notes": []
}
```

---

### 4. Review System (`scripts/review_outputs.py`)

**Purpose:** AI double-checks its own work and flags issues

**Validation Checks:**

1. **Chapter Continuity:**
   - Do line numbers make sense?
   - Are there gaps in chapter sequence?
   - Do chapter word counts seem reasonable?

2. **Character Consistency:**
   - Are aliases properly linked?
   - Do descriptions match usage in text?
   - Are there unnamed speakers?

3. **Text Quality:**
   - Spot-check random passages for errors
   - Check for remaining OCR artifacts
   - Verify dialogue attribution

**Output Format (review.json):**
```json
{
  "overall_confidence": 0.92,
  "ready_for_production": false,
  "warnings": [
    {
      "type": "chapter_length",
      "severity": "low",
      "message": "Chapter 7 is very long (8,234 words) - may actually be two chapters",
      "location": "chapter 7",
      "suggested_action": "Manual review of chapter break at line 4,582"
    },
    {
      "type": "character_unclear",
      "severity": "medium",
      "message": "Character 'Weena' - gender unclear from text",
      "location": "chapter 5",
      "suggested_action": "Confirm gender for voice assignment"
    }
  ],
  "passed_checks": [
    "All chapters identified",
    "No OCR artifacts detected",
    "Dialogue properly attributed",
    "Character list complete"
  ],
  "failed_checks": [
    "One potential missing chapter break"
  ]
}
```

---

### 5. Scene Generation (`scripts/generate_scenes.py`)

**Purpose:** Identify key scenes for illustration

**AI Prompt:**
```
Analyze [BOOK_TITLE] by [AUTHOR] and identify 10-12 key scenes for illustration.

Criteria:
- Visually interesting (action, distinctive setting, character interaction)
- Spread across the narrative arc (beginning, middle, end)
- Iconic moments that readers remember
- Can be illustrated without major spoilers
- Represent different moods/settings

For each scene provide:
- Chapter number
- Scene description (2-3 sentences, focusing on visual elements)
- Characters present
- Setting details (time of day, location, atmosphere)
- Mood (tense, peaceful, mysterious, etc.)
- Style notes for artist

Output as JSON.
```

**Output Format (scenes.json):**
```json
{
  "scenes": [
    {
      "id": 1,
      "chapter": 1,
      "description": "Victorian parlor with fireplace, Time Traveller demonstrating small time machine model to skeptical friends seated in leather armchairs, warm evening lighting, intellectual atmosphere",
      "characters": ["Time Traveller", "Filby", "others"],
      "setting": "Time Traveller's parlor, evening",
      "mood": "curious, skeptical",
      "style_notes": "Victorian interior, realistic, warm lighting, emphasis on faces showing disbelief",
      "image_prompt": null  # filled in by image gen script
    }
  ]
}
```

---

### 6. Audio Generation (`scripts/generate_audio.py`)

**Purpose:** Generate narration using ElevenLabs API

**Dependencies:**
```python
import elevenlabs
from elevenlabs import VoiceSettings
import json
from pathlib import Path
```

**Voice Assignment Strategy:**

```python
VOICE_PROFILES = {
    'narrator_primary': {
        'voice_id': 'voice_id_adam',
        'settings': {
            'stability': 0.75,
            'similarity_boost': 0.75,
            'style': 0.5
        },
        'description': 'Warm, authoritative narrator'
    },
    'male_british_mature': {
        'voice_id': 'voice_id_brian',
        'settings': {...},
        'description': 'Middle-aged British male'
    },
    # etc.
}
```

**Process:**

1. **Voice Assignment:**
   - Narrator: Consistent across all books
   - Characters: Assigned based on character.voice_type
   - Test 30-second sample of each

2. **Text Chunking:**
   - Break by chapters
   - Further chunk at sentence boundaries if >5000 chars
   - Preserve paragraph breaks

3. **Generation:**
   - Call ElevenLabs API per chunk
   - Use appropriate voice ID
   - Save audio files as chapter_XX.mp3

4. **Timestamp Generation:**
   - Track word-level timestamps
   - Needed for text highlighting sync
   - Save as timestamps.json

**Function Signature:**
```python
def generate_audio(
    structure_file: str,
    text_file: str,
    output_dir: str,
    voices: dict
) -> dict:
    """
    Generate audio narration
    
    Returns:
        {
            'success': bool,
            'audio_files': list,  # paths to MP3s
            'timestamp_file': str,
            'total_duration_seconds': float,
            'cost_usd': float,
            'characters_used': int
        }
    """
```

**Timestamp Format:**
```json
{
  "chapter_01": {
    "audio_file": "chapter_01.mp3",
    "duration_seconds": 543.2,
    "words": [
      {
        "word": "The",
        "start_time": 0.0,
        "end_time": 0.15,
        "confidence": 0.98
      }
    ]
  }
}
```

---

### 7. Image Generation (`scripts/generate_images.py`)

**Purpose:** Generate scene illustrations via ComfyUI

**Dependencies:**
```python
import requests
import json
import time
from pathlib import Path
```

**ComfyUI Integration:**

```python
def generate_image(scene: dict, workflow_path: str) -> str:
    """
    Generate image using ComfyUI API
    
    Args:
        scene: Scene dict from scenes.json
        workflow_path: Path to ComfyUI workflow JSON
    
    Returns:
        Path to generated image
    """
    
    # Load workflow template
    with open(workflow_path) as f:
        workflow = json.load(f)
    
    # Inject prompt
    workflow['nodes']['prompt']['inputs']['text'] = scene['image_prompt']
    workflow['nodes']['style']['inputs']['text'] = 'Victorian illustration, detailed, classic literature'
    
    # Queue workflow
    response = requests.post('http://localhost:8188/prompt', json={
        'prompt': workflow
    })
    
    # Poll for completion
    # Download result
    # Return path
```

**Image Style:**
- Victorian illustrations for 19th century books
- Pulp magazine style for early 20th century
- Consistent style within each book
- High resolution (1024x1024 minimum)

---

### 8. Deployment (`scripts/deploy.py`)

**Purpose:** Upload content and update database

**Steps:**

1. **Upload Audio Files:**
   ```python
   from google.cloud import storage
   
   def upload_audio(book_id: str, audio_dir: str):
       bucket = storage_client.bucket('compel-classics')
       for audio_file in Path(audio_dir).glob('*.mp3'):
           blob = bucket.blob(f'audio/{book_id}/{audio_file.name}')
           blob.upload_from_filename(audio_file)
   ```

2. **Upload Images:**
   ```python
   def upload_images(book_id: str, images_dir: str):
       bucket = storage_client.bucket('compel-classics')
       for image_file in Path(images_dir).glob('*.png'):
           blob = bucket.blob(f'images/{book_id}/{image_file.name}')
           blob.upload_from_filename(image_file)
   ```

3. **Insert Database Records:**
   ```sql
   -- books table
   INSERT INTO books (id, title, author, word_count, public_domain_status, 
                      gutenberg_id, published_year, processed_at)
   VALUES (...);
   
   -- chapters table
   INSERT INTO chapters (id, book_id, chapter_number, title, text_content,
                         word_count, audio_url, duration_seconds)
   VALUES (...);
   
   -- scenes table
   INSERT INTO scenes (id, chapter_id, scene_number, image_url, description)
   VALUES (...);
   
   -- character_voices table
   INSERT INTO character_voices (id, book_id, character_name, 
                                  elevenlabs_voice_id, description)
   VALUES (...);
   
   -- words table (for definitions)
   INSERT INTO words (id, book_id, word, definition, difficulty_level,
                      frequency, sample_sentences)
   VALUES (...);
   ```

4. **Update Book Status:**
   ```python
   update_book_state(book_id, 'DEPLOYED')
   ```

---

## Shared Utilities (`lib/`)

### AI Client (`lib/ai_client.py`)

```python
class AIClient:
    def __init__(self, provider='anthropic', config=None):
        self.provider = provider
        self.config = config
        
        if provider == 'anthropic':
            import anthropic
            self.client = anthropic.Anthropic(api_key=config['api_key'])
        # Add other providers as needed
    
    def analyze_text(self, prompt: str, text: str, max_tokens: int = 4000) -> dict:
        """Send text to AI for analysis"""
        
    def validate_json(self, response: str) -> dict:
        """Parse and validate JSON response"""
        
    def retry_on_error(self, func, max_attempts=3):
        """Retry failed API calls"""
```

### Text Cleaning (`lib/cleaning.py`)

```python
def fix_ocr_errors(text: str, fixes: dict) -> str:
    """Apply OCR error fixes"""

def normalize_whitespace(text: str) -> str:
    """Clean up spacing"""

def remove_gutenberg_license(text: str) -> str:
    """Remove Project Gutenberg legal text"""

def detect_encoding(file_path: str) -> str:
    """Detect file encoding"""
```

### Issue Tracking (`lib/tracking.py`)

```python
class IssueTracker:
    def __init__(self, db_path='pipeline.db'):
        self.db = sqlite3.connect(db_path)
    
    def log_issue(self, book_id, step, issue_type, description):
        """Record a new issue"""
    
    def get_recent_issues(self, limit=10):
        """Get unresolved issues"""
    
    def resolve_issue(self, issue_id, resolution_notes):
        """Mark issue as resolved"""
    
    def get_issue_patterns(self):
        """Analyze common issue types"""
```

### Validators (`lib/validators.py`)

```python
def validate_chapter_structure(chapters: list) -> list:
    """Check for gaps, overlaps, oddities"""

def validate_character_list(characters: list) -> list:
    """Check for consistency"""

def validate_text_quality(text: str) -> list:
    """Check for remaining OCR errors"""
```

---

## Database Schema

```sql
-- State tracking
CREATE TABLE books (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    state TEXT NOT NULL,
    current_step TEXT,
    progress_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    cost_usd REAL DEFAULT 0,
    notes TEXT
);

-- Issue tracking
CREATE TABLE issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id TEXT NOT NULL,
    step TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    description TEXT,
    severity TEXT DEFAULT 'medium',
    resolved BOOLEAN DEFAULT 0,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Processing log
CREATE TABLE processing_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id TEXT NOT NULL,
    step TEXT NOT NULL,
    status TEXT NOT NULL,  -- success, failure, warning
    message TEXT,
    duration_seconds REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);
```

---

## Configuration Template

See `config.example.py` for full configuration.

Key sections:
- Local AI credentials
- ElevenLabs API setup
- ComfyUI connection
- Cloud storage paths
- Database credentials
- Voice ID mappings

---

## Error Handling

All scripts should:
1. Log to `pipeline.log`
2. Record issues in database
3. Return structured error info
4. Fail gracefully with cleanup
5. Provide actionable error messages

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
```

---

## Testing

Each script should have basic tests:

```python
# tests/test_extract_pdf.py
def test_extract_basic_pdf():
    result = extract_text_from_pdf('tests/fixtures/sample.pdf', 'tests/output')
    assert result['success'] == True
    assert result['page_count'] > 0
```

Run with: `pytest tests/`