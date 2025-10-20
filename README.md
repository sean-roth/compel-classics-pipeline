# Compel Classics Pipeline 📚

> Local-first content pipeline for transforming classic sci-fi novels into interactive ESL learning materials

## Overview

This system processes public domain novels (starting with The Time Machine) into structured, narrated, illustrated content for the Compel English ESL platform. It emphasizes **local processing** (free iteration) before calling **expensive APIs** (only when data is perfect).

## Philosophy

- **Local server = Free experimentation zone** - Iterate without API costs
- **Human = Quality gate** - Approve before spending money  
- **AI = Processing assistant** - Structure identification, not creative decisions
- **Version everything** - Track every iteration on 14TB storage

## Quick Start

```bash
# Clone and setup
git clone https://github.com/sean-roth/compel-classics-pipeline.git
cd compel-classics-pipeline
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Configure
cp config.example.py config.py
# Edit config.py with your API keys and paths

# Process a book
python process_book.py input/time_machine.pdf

# Review results
python review.py working/time_machine

# Generate final content (costs money!)
python generate_content.py working/time_machine --approve

# Deploy to web app
python deploy.py output/time_machine
```

## System Requirements

- Python 3.11+
- 32GB RAM (for PDF processing)
- Large storage (14TB recommended for backups)
- Local AI assistant (Anthropic API or local LLM)
- Internet for final API calls (ElevenLabs, image generation)

## Pipeline Stages

### Stage 1: Local Processing (FREE)

1. **Extract** - Pull text from PDF (`extract_pdf.py`)
2. **Clean** - Fix OCR errors, normalize text (`clean_text.py`)
3. **Analyze** - Identify chapters, characters, scenes (`analyze_structure.py`)
4. **Review** - Flag issues for human review (`review_outputs.py`)

### Stage 2: Human QA Gate (30 mins)

5. **Approve** - Human reviews and fixes flagged issues

### Stage 3: Cloud APIs (COSTS $$$)

6. **Audio** - Generate narration via ElevenLabs (`generate_audio.py`)
7. **Images** - Create scene illustrations via ComfyUI (`generate_images.py`)

### Stage 4: Deploy

8. **Package** - Upload to Cloud Storage and PostgreSQL (`deploy.py`)

## Project Structure

```
compel-classics-pipeline/
├── input/                  # Raw PDFs from Gutenberg
├── working/                # Active processing
│   └── {book_name}/
│       ├── raw.pdf
│       ├── extracted_v1.txt
│       ├── cleaned.txt
│       ├── structure.json
│       ├── review.json
│       └── approved.flag
├── output/                 # Finalized content
│   └── {book_name}/
│       ├── audio/
│       │   ├── chapter_01.mp3
│       │   └── timestamps.json
│       ├── images/
│       │   └── scene_01.png
│       └── manifest.json
├── archive/                # Backups (on 14TB drive)
├── scripts/                # Processing scripts
│   ├── extract_pdf.py
│   ├── clean_text.py
│   ├── analyze_structure.py
│   ├── generate_scenes.py
│   ├── generate_audio.py
│   ├── generate_images.py
│   └── deploy.py
├── lib/                    # Shared utilities
│   ├── ai_client.py       # Local AI interface
│   ├── cleaning.py        # Text cleaning functions
│   ├── tracking.py        # Issue tracking system
│   └── validators.py      # Quality checks
├── config.py               # Configuration (gitignored)
├── requirements.txt
└── README.md
```

## Processing States

Each book moves through these states:

1. **INGESTED** - PDF downloaded
2. **EXTRACTED** - Text pulled from PDF
3. **CLEANED** - OCR errors fixed
4. **ANALYZED** - Structure identified  
5. **FLAGGED** - Issues found, needs human
6. **APPROVED** - Human says it's good
7. **GENERATING** - Calling expensive APIs
8. **COMPLETED** - Ready for deployment
9. **DEPLOYED** - Live on web app

Tracked in SQLite: `pipeline.db`

## Time Estimates

### First Book (The Time Machine):
- **Day 1**: Download PDF, start processing (runs overnight)
- **Day 2**: Review flagged issues (30 mins), approve, generate content (runs 4-5 hours)
- **Day 3**: Review generated content (1 hour), deploy (30 mins)

**Your time:** ~2.5 hours  
**Machine time:** ~30 hours  
**Cost:** ~$45 (ElevenLabs + images)

### Subsequent Books:
- **Your time:** ~1-2 hours (known issues documented)
- **Cost:** $35-60 depending on length

## Cost Breakdown

- **ElevenLabs**: ~$0.20 per 1,000 characters
  - Time Machine (~35k words = 192k chars) = ~$38
- **Image Generation**: ~$0.50-1.00 per image
  - 10 scenes = ~$5-10
- **Total per book:** $40-50 average

## Configuration

See `config.example.py` for full configuration template.

Key settings:
- Local AI credentials (Anthropic or local LLM)
- ElevenLabs API key and voice preferences
- ComfyUI/image generation setup
- Cloud storage paths
- Database credentials

## Issue Tracking

The system tracks problems for continuous improvement:

```sql
-- pipeline.db
CREATE TABLE issues (
    id INTEGER PRIMARY KEY,
    book_id TEXT,
    step TEXT,
    issue_type TEXT,
    description TEXT,
    resolved BOOLEAN,
    resolution_notes TEXT,
    created_at TIMESTAMP
);
```

**Issue Types:**
- `ocr_error` - Text extraction problems
- `structure_fail` - Missed chapters/characters  
- `voice_mismatch` - Wrong voice for character
- `audio_quality` - Pronunciation, pacing issues
- `image_fail` - Image doesn't match scene

Every run reviews last 10 issues and adapts prompts accordingly.

## First Book: The Time Machine

**Why this book:**
- Short (35,000 words)
- Well-known story
- Clean Gutenberg text
- Limited characters (~6 main)
- Good test case

**Download:**
https://www.gutenberg.org/ebooks/35

**Expected output:**
- 16 chapters
- ~3 hours of audio narration  
- 10-12 scene illustrations
- ~2,500 vocabulary words
- Cost: ~$40

## Development Roadmap

### Phase 1: Core Pipeline (Current)
- [x] Repository setup
- [ ] PDF extraction script
- [ ] Text cleaning script  
- [ ] Structure analysis (with local AI)
- [ ] Review/approval system
- [ ] Audio generation (ElevenLabs)
- [ ] Image generation (ComfyUI)
- [ ] Deployment script

### Phase 2: The Time Machine
- [ ] Process full book
- [ ] Document all issues found
- [ ] Generate audio and images
- [ ] Deploy to web app

### Phase 3: Automation
- [ ] Improve cleaning based on learned patterns
- [ ] Better chapter detection
- [ ] Automated voice assignment
- [ ] Batch processing support

### Phase 4: Scale
- [ ] Process 10 more classics
- [ ] Build library catalog
- [ ] Quality metrics dashboard

## Documentation

See `/docs` for detailed specifications:
- `ARCHITECTURE.md` - System design and data flow
- `SPECIFICATIONS.md` - Technical specs for each component  
- `API_REFERENCE.md` - How to call ElevenLabs, image gen, etc.
- `PROMPTS.md` - Tested AI prompts for structure analysis
- `TROUBLESHOOTING.md` - Common issues and solutions

## Contributing

This is a private project. Claude Code will be the primary developer.

## License

Proprietary - All rights reserved

---

**Built for:** Compel English ESL Platform  
**Purpose:** Transform classic sci-fi into interactive learning materials  
**Tagline:** Literature breeds literacy