# Clean Lecture Notes Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)](skills/clean-lecture-notes/SKILL.md)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-green)](https://agentskills.io)

Turn a noisy lecture transcript into a clean transcript and study notes you can review. This Codex skill preserves assignments, numbers, and uncertainty, then organizes the material into conclusions, recall questions, and a Mermaid mindmap.

**先看效果 / Preview without installing:** [Noisy transcript 原稿](examples/noisy-transcript.md) → [Cleaned transcript 清洗稿](examples/cleaned-transcript.md) → [Study notes 复习笔记](examples/study-notes-outline.md). The synthetic sample keeps the assignment to find and test **three** skills. No Feishu account or real class recording is needed for this example.

[Install in Codex](#install) · [Try the sample prompt](#try-the-sample-in-codex)

## What It Does

- Cleans noisy transcripts without overwriting the source.
- Preserves examples, assignments, product names, numbers, and uncertainty.
- Aligns transcripts with courseware when slides or HTML notes are available.
- Produces learner-facing study notes with **core conclusions**, **active recall**, **project transfer**, and **Mermaid mindmaps**.
- Validates final notes so they do not become passive "the teacher said..." summaries.
- Supports optional Feishu/Lark workflows when your Codex environment has those tools installed.

## 中文快速上手

已有课堂逐字稿时，可以直接生成两个 Markdown 文件：清洗稿和复习笔记，保留原稿、作业和关键数字。飞书是可选项；如果手上只有音视频，需要先用环境里可用的工具转录。

## Install

### Option 1: Copy the Skill into Codex

```bash
git clone https://github.com/ljim17502-hub/clean-lecture-notes-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R clean-lecture-notes-skill/skills/clean-lecture-notes "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex so it reloads skill metadata, then open the cloned `clean-lecture-notes-skill` folder as your workspace.

### Option 2: Use as a Skill-only Codex Plugin

This repository also includes `.codex-plugin/plugin.json`, so it can be distributed as a skill-only Codex plugin.

```bash
git clone https://github.com/ljim17502-hub/clean-lecture-notes-skill.git
```

Then install or load it using your Codex plugin workflow.

## Try the sample in Codex

After installing, open this repository in Codex and paste:

```text
Use $clean-lecture-notes on examples/noisy-transcript.md.
Create a cleaned transcript and study notes as new local Markdown files.
Keep the source unchanged, preserve the three-skill assignment, and do not use Feishu/Lark.
```

```text
使用 $clean-lecture-notes 处理 examples/noisy-transcript.md。
新建本地 Markdown 清洗稿和复习笔记，保留原稿和「找三个 Skill」的作业，不使用飞书。
```

Compare your result with the [checked-in examples](examples/). Wording may vary; check that the source is unchanged and that the assignment is still present.

## Repository Layout

```text
.
├── .codex-plugin/plugin.json
├── skills/
│   └── clean-lecture-notes/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       │   ├── transcript-cleaning.md
│       │   ├── study-note-workflow.md
│       │   ├── feishu-output.md
│       │   └── quality-checklist.md
│       └── scripts/
│           ├── check_note_artifacts.py
│           └── check_note_artifacts_test.py
└── examples/
```

## Validation

Validate the skill metadata:

```bash
python3 /path/to/quick_validate.py skills/clean-lecture-notes
```

Run the included tests:

```bash
python3 -m unittest discover -s skills/clean-lecture-notes/scripts -p '*_test.py'
```

Run a local note artifact check:

```bash
python3 skills/clean-lecture-notes/scripts/check_note_artifacts.py --final-note examples/study-notes-outline.md
```

## Privacy and Safety

- Do not commit real transcripts, private Feishu/Lark URLs, access tokens, API keys, or `.env` files.
- The examples in this repo are synthetic and privacy-safe.
- The skill defaults to creating new outputs instead of overwriting source transcripts.
- Feishu/Lark support is optional and depends on your local Codex tooling.

## Keywords

`codex skill`, `agent skills`, `lecture notes`, `transcript cleanup`, `meeting transcript`, `study notes`, `Feishu`, `Lark`, `Mermaid mindmap`, `AI product manager`, `Markdown`, `ASR cleanup`, `courseware notes`

## License

MIT
