# Clean Lecture Notes Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)](skills/clean-lecture-notes/SKILL.md)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-green)](https://agentskills.io)

Clean noisy lecture transcripts, meeting transcripts, class recordings, Feishu/Lark docs, and local ASR output into courseware-aligned study notes for Codex.

This repository packages a reusable **Codex skill** for transcript cleanup, lecture notes, study notes, Mermaid mindmaps, active recall, and optional Feishu/Lark writeback. It is designed for students, AI product managers, educators, course creators, and knowledge workers who want review-ready notes instead of raw ASR text.

## What It Does

- Cleans noisy transcripts without overwriting the source.
- Preserves examples, assignments, product names, numbers, and uncertainty.
- Aligns transcripts with courseware when slides or HTML notes are available.
- Produces learner-facing study notes with **core conclusions**, **active recall**, **project transfer**, and **Mermaid mindmaps**.
- Validates final notes so they do not become passive "the teacher said..." summaries.
- Supports optional Feishu/Lark workflows when your Codex environment has those tools installed.

## 中文快速上手

这个 Skill 用来把课堂录音转文字、飞书文档逐字稿、本地 ASR 文本、会议转写稿，清洗成可复习的学习笔记。

它特别适合：

- 清洗录音转文字
- 整理上课录音
- 把逐字稿和课件做成复习笔记
- 生成带思维导图、主动回忆问题、核心结论的中文课堂笔记
- 写回飞书或输出本地 Markdown

示例提示词：

```text
Use $clean-lecture-notes to clean this lecture transcript and generate courseware-aligned study notes.
```

```text
使用 $clean-lecture-notes 清洗这份课堂逐字稿，并结合课件整理成适合复习的中文学习笔记。
```

## Install

### Option 1: Copy the Skill into Codex

```bash
git clone https://github.com/ljim17502-hub/clean-lecture-notes-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R clean-lecture-notes-skill/skills/clean-lecture-notes "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex so it reloads skill metadata.

### Option 2: Use as a Skill-only Codex Plugin

This repository also includes `.codex-plugin/plugin.json`, so it can be distributed as a skill-only Codex plugin.

```bash
git clone https://github.com/ljim17502-hub/clean-lecture-notes-skill.git
```

Then install or load it using your Codex plugin workflow.

## Usage

Ask Codex naturally, or mention the skill explicitly:

```text
Use $clean-lecture-notes to clean this transcript. Preserve assignments and uncertain terms.
```

```text
Use $clean-lecture-notes to turn this Feishu/Lark transcript and courseware into review notes with a Mermaid mindmap.
```

```text
使用 $clean-lecture-notes，把这份录音转文字清洗成清洗稿，再生成学习者视角的复习笔记。
```

## Example

Input:

```text
Teacher: um today we talk about MCP, right, MCP lets the AI connect tools.
Teacher: and then, and then skill is different, skill is like the workflow.
Student: so if I already have MCP do I still need skills?
```

Output shape:

```markdown
## Core Conclusion

**MCP answers "what can the agent access"; Skills answer "how should the agent complete the task."**

## Active Recall

1. What problem does MCP solve?
2. What problem does a Skill solve?
3. Why do reusable workflows need validation?
```

See [`examples/`](examples/) for a privacy-safe mini input and output.

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
