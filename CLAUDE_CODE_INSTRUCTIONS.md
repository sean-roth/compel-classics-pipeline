# Instructions for Claude Code

## Overview

You are building a local-first content pipeline that processes classic sci-fi novels into interactive ESL learning materials. The system prioritizes **free local processing** before calling expensive APIs.

## Your Mission

Build the 8 core scripts in the `scripts/` directory plus shared utilities in `lib/`. Follow the specifications in `SPECIFICATIONS.md` exactly.

## Getting Started

1. **Read the docs first:**
   - `README.md` - Understand the big picture
   - `SPECIFICATIONS.md` - Detailed technical specs for each component
   - This file - Your specific instructions

2. **Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp config.example.py config.py
   # Edit config.py with real values
   ```

3. **Create folder structure:**
   ```bash
   mkdir -p input working output archive logs scripts lib tests
   ```

## Build Order

### Phase 1: Foundation (Start Here)

1. **`lib/tracking.py`** - Issue tracking system
   - Create SQLite database
   - Implement IssueTracker class
   - Add methods to log, retrieve, resolve issues

2. **`lib/cleaning.py`** - Text cleaning utilities
   - OCR error fixes
   - Whitespace normalization
   - Gutenberg license removal

3. **`lib/ai_client.py`** - AI interface
   - Anthropic API wrapper
   - JSON parsing and validation
   - Retry logic for failed calls

4. **`lib/validators.py`** - Quality checks
   - Chapter structure validation
   - Character consistency checks
   - Text quality checks

### Phase 2: Core Processing

5. **`scripts/extract_pdf.py`** - PDF extraction
   - Use pdfplumber
   - Save to working/{book}/extracted_v1.txt
   - Return metadata

6. **`scripts/clean_text.py`** - Text cleaning
   - Apply OCR fixes from lib/cleaning.py
   - Save to working/{book}/cleaned.txt
   - Track fixes applied

7. **`scripts/analyze_structure.py`** - Structure analysis
   - Call AI to identify chapters, characters
   - Save to working/{book}/structure.json
   - Use prompts from SPECIFICATIONS.md

8. **`scripts/review_outputs.py`** - Quality review
   - AI double-checks its work
   - Flag issues for human review
   - Save to working/{book}/review.json

### Phase 3: Content Generation

9. **`scripts/generate_scenes.py`** - Scene identification
   - AI selects 10-12 key scenes
   - Create image prompts
   - Save to working/{book}/scenes.json

10. **`scripts/generate_audio.py`** - Audio generation
    - Call ElevenLabs API
    - Generate per-chapter audio
    - Create timestamp mappings
    - Save to output/{book}/audio/

11. **`scripts/generate_images.py`** - Image generation
    - Call ComfyUI API
    - Generate scene illustrations
    - Save to output/{book}/images/

### Phase 4: Deployment

12. **`scripts/deploy.py`** - Deploy to web app
    - Upload to Cloud Storage
    - Insert database records
    - Update book status

## Important Guidelines

### Error Handling

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    # Your code
    pass
except Exception as e:
    logger.error(f"Error in processing: {e}", exc_info=True)
    # Log to issue tracker
    tracker.log_issue(book_id, step, 'error', str(e))
    raise
```

### Configuration

```python
from config import CONFIG

# Access config like:
api_key = CONFIG['LOCAL_AI']['api_key']
voices = CONFIG['ELEVENLABS']['voices']
```

### Progress Reporting

```python
from tqdm import tqdm

for item in tqdm(items, desc="Processing chapters"):
    # Your code
    pass
```

### File Paths

```python
from pathlib import Path

# Always use Path for cross-platform compatibility
working_dir = Path('working') / book_id
working_dir.mkdir(parents=True, exist_ok=True)

output_file = working_dir / 'structure.json'
```

## Testing

Create tests in `tests/` directory:

```python
# tests/test_extract_pdf.py
import pytest
from scripts.extract_pdf import extract_text_from_pdf

def test_extract_basic():
    result = extract_text_from_pdf(
        'tests/fixtures/sample.pdf',
        'tests/output'
    )
    assert result['success'] == True
```

Run with: `pytest tests/ -v`

## CLI Interface

Use `click` for user-friendly CLIs:

```python
import click

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', default='working', help='Output directory')
def extract(pdf_path, output):
    """Extract text from PDF"""
    click.echo(f"Extracting {pdf_path}...")
    result = extract_text_from_pdf(pdf_path, output)
    
    if result['success']:
        click.secho(f"✓ Success! {result['page_count']} pages", fg='green')
    else:
        click.secho(f"✗ Failed: {result['error']}", fg='red')

if __name__ == '__main__':
    extract()
```

## Code Quality

- **Format with black:** `black scripts/ lib/`
- **Lint with flake8:** `flake8 scripts/ lib/`
- **Type hints:** Use them for function signatures
- **Docstrings:** Every function needs a docstring
- **Comments:** Explain *why*, not *what*

## Common Pitfalls to Avoid

1. **Don't hardcode paths** - Use `config.py` and `Path()`
2. **Don't skip error handling** - Always log and track issues
3. **Don't ignore the specs** - Follow `SPECIFICATIONS.md` exactly
4. **Don't commit secrets** - Check `.gitignore` is working
5. **Don't call APIs unnecessarily** - Check if output already exists

## When You're Stuck

1. Check `SPECIFICATIONS.md` for details
2. Look at the example code in this file
3. Check the logs: `tail -f logs/pipeline.log`
4. Check the database: `sqlite3 pipeline.db "SELECT * FROM issues"`

## Success Criteria

You're done when:

1. ✅ All 8 scripts are implemented
2. ✅ All 4 lib utilities are implemented
3. ✅ Basic tests pass
4. ✅ Can process The Time Machine end-to-end
5. ✅ Human review workflow is clear
6. ✅ Costs are tracked accurately
7. ✅ Issues are logged properly
8. ✅ Code is clean and documented

## First Task

**Start with `lib/tracking.py`** - This is the foundation. Get the issue tracking system working first so you can log problems as you build the rest.

Good luck! Remember: local processing first, expensive APIs last.
