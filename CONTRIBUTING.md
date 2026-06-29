# Contributing

Thanks for improving `clean-lecture-notes`.

## What belongs here

- Better transcript-cleaning heuristics.
- Study-note structures that help learners review, recall, and transfer ideas.
- Feishu/Lark, Markdown, Mermaid, or local-file workflow improvements.
- Validation improvements for note quality and safety.

## What does not belong here

- Real classroom transcripts, private Feishu/Lark URLs, tokens, API keys, or `.env` values.
- Vendor-specific credentials or private course materials.
- Large generated artifacts that are not needed to use or test the skill.

## Validation

Run these checks before opening a pull request:

```bash
python3 /Users/wujihang/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/clean-lecture-notes
python3 -m unittest discover -s skills/clean-lecture-notes/scripts -p '*_test.py'
find . -name "__pycache__" -o -name "*.pyc"
```

If your local Codex install is not at `/Users/wujihang/.codex`, replace the first command with the path to your own `quick_validate.py`.

Also run a secret scan before publishing. At minimum, check for private document URLs, access tokens, bearer tokens, application secrets, API keys, and unfinished template markers.
