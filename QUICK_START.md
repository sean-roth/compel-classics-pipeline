# Quick Start for Sean

## What Just Happened

I created a complete GitHub repository with everything Claude Code needs to build your content pipeline. Here's what's in there:

### Documentation
- **README.md** - Big picture overview
- **SPECIFICATIONS.md** - Detailed technical specs for every component
- **CLAUDE_CODE_INSTRUCTIONS.md** - Step-by-step instructions for Claude Code

### Configuration
- **config.example.py** - Template with all settings
- **requirements.txt** - All Python dependencies
- **.gitignore** - Protects secrets and generated content

## Next Steps

### 1. Clone the repo to your local server

```bash
cd /path/to/your/server
git clone https://github.com/sean-roth/compel-classics-pipeline.git
cd compel-classics-pipeline
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure

```bash
cp config.example.py config.py
# Edit config.py with your actual:
# - Anthropic API key (for local AI)
# - ElevenLabs API key (when ready)
# - Paths to your 14TB drive
# - etc.
```

### 4. Create folder structure

```bash
mkdir -p input working output archive logs scripts lib tests
```

### 5. Download The Time Machine

```bash
cd input
wget https://www.gutenberg.org/files/35/35-0.txt -O time_machine.txt
# Or use the PDF: wget https://www.gutenberg.org/files/35/35-pdf.pdf -O time_machine.pdf
```

### 6. Hand it to Claude Code

Open this project in your IDE with Claude Code and say:

```
"Read CLAUDE_CODE_INSTRUCTIONS.md and start building the pipeline. 
Begin with lib/tracking.py as instructed."
```

## What Claude Code Will Build

Claude Code will create 8 scripts in `scripts/`:

1. **extract_pdf.py** - Pull text from PDFs
2. **clean_text.py** - Fix OCR errors
3. **analyze_structure.py** - Find chapters, characters (uses AI)
4. **review_outputs.py** - Quality check (uses AI)
5. **generate_scenes.py** - Pick scenes for images (uses AI)
6. **generate_audio.py** - Create narration (uses ElevenLabs)
7. **generate_images.py** - Generate illustrations (uses ComfyUI)
8. **deploy.py** - Upload to web app

Plus 4 utilities in `lib/`:
- `tracking.py` - Issue tracking database
- `cleaning.py` - Text cleaning functions
- `ai_client.py` - Interface to local AI
- `validators.py` - Quality checks

## The Workflow (Once Built)

### Day 1 (Friday night):
```bash
python scripts/extract_pdf.py input/time_machine.pdf
python scripts/clean_text.py working/time_machine
python scripts/analyze_structure.py working/time_machine
# ^ These run overnight, cost nothing
```

### Day 2 (Saturday morning):
```bash
python scripts/review_outputs.py working/time_machine
# Look at working/time_machine/review.json
# Fix any flagged issues
# When satisfied: touch working/time_machine/approved.flag
```

### Day 2 (Saturday afternoon):
```bash
python scripts/generate_scenes.py working/time_machine
python scripts/generate_audio.py working/time_machine  # Costs ~$38
python scripts/generate_images.py working/time_machine  # Costs ~$7
# ^ These run in background
```

### Day 3 (Sunday):
```bash
python scripts/deploy.py output/time_machine
# Uploads to Cloud Storage + updates PostgreSQL
```

**Total cost: ~$45**
**Your time: ~2.5 hours**

## Key Features

### Free Local Processing
- Text extraction and cleaning runs locally (no API costs)
- AI analysis uses your local assistant (cheap/free)
- Only call expensive APIs when data is perfect

### Human Quality Gate
- AI flags issues for you to review
- You approve before spending money
- No surprises, no wasted API calls

### Issue Tracking
- Every problem is logged in SQLite database
- System learns from mistakes
- Improves with each book

### Version Control
- Every processing step is saved
- Can rollback to any version
- 14TB storage = keep everything

## Architecture

```
Local Processing (FREE)
  ├─ Extract PDF
  ├─ Clean text  
  ├─ Analyze structure (local AI)
  └─ Review & flag issues
         ↓
Human Approval (30 mins)
         ↓
Cloud APIs (COSTS $$$)
  ├─ Generate audio (ElevenLabs)
  ├─ Generate images (ComfyUI)
  └─ Deploy to web app
```

## What Gets Created

For The Time Machine, you'll get:

```
output/time_machine/
├── audio/
│   ├── chapter_01.mp3
│   ├── chapter_02.mp3
│   └── ... (16 chapters)
│   └── timestamps.json
├── images/
│   ├── scene_01.png
│   ├── scene_02.png
│   └── ... (10-12 scenes)
├── manifest.json
└── metadata.json
```

Plus database records in your web app's PostgreSQL:
- `books` table entry
- 16 `chapters` table entries  
- 10+ `scenes` table entries
- 5+ `character_voices` table entries
- ~2,500 `words` table entries

## Cost Breakdown

### Per Book (The Time Machine):
- ElevenLabs: ~$38 (192k characters)
- Images: ~$7 (10 scenes)
- **Total: ~$45**

### Time Investment:
- **Your time:** ~2.5 hours (spread over 3 days)
- **Machine time:** ~30 hours (mostly automated)

### Scale:
- **Book #1:** ~15 hours human time (learning)
- **Book #2:** ~10 hours (refinement)
- **Book #10:** ~6-8 hours (mostly automated)

## Troubleshooting

If things break:

```bash
# Check logs
tail -f logs/pipeline.log

# Check issues database
sqlite3 pipeline.db "SELECT * FROM issues ORDER BY created_at DESC LIMIT 10"

# Re-run a step
python scripts/analyze_structure.py working/time_machine --force
```

## When Ready to Scale

Once The Time Machine works:

1. Document lessons learned
2. Update cleaning rules based on issues
3. Process 2-3 more books
4. Build batch processing
5. Eventually: near-full automation

## The Big Picture

This isn't just a script - it's a **content factory** that:
- ✅ Processes public domain classics
- ✅ Converts them to interactive learning materials
- ✅ Minimizes costs through local processing
- ✅ Learns and improves over time
- ✅ Scales to dozens of books

All without a content team, just you and AI.

## Repository

https://github.com/sean-roth/compel-classics-pipeline

## Support

Claude Code has everything it needs in:
- `SPECIFICATIONS.md` - Technical details
- `CLAUDE_CODE_INSTRUCTIONS.md` - Build instructions

If you hit issues, the documentation should have answers.

---

**Ready to start?** Hand it to Claude Code and let it build! 🚀