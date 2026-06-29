#!/usr/bin/env python3
"""Regression tests for lecture-note artifact validation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check_note_artifacts.py")


VALID_FINAL_NOTE = """# AI PM 学习笔记

## 思维导图

```mermaid
flowchart TD
  A["AI PM"] --> B["MCP"]
  A --> C["Skill"]
```

## 复习路径

5 分钟先看核心结论，20 分钟补齐模块。

## 核心结论

**我需要掌握的是 MCP 的接入判断和 Skill 的复用边界。**

## 主动回忆自测

- MCP 适合解决什么问题？

## 核心模块

### 模块一：MCP

**关键判断是先确认工具边界，再设计接入路径。**

## 项目迁移清单

- 可迁移到项目里的是工具接入检查表。

## 面试话术

**面试可表达为：我会先拆清数据、工具和权限边界。**

## 资料来源与质量审计

- 来源：清洗稿、课件。
"""


class CheckNoteArtifactsTest(unittest.TestCase):
    def run_checker(self, content: str, *args: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "artifact.md"
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), *args, str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_final_note_rejects_observer_voice_synonyms(self) -> None:
        observer_note = VALID_FINAL_NOTE.replace(
            "**关键判断是先确认工具边界，再设计接入路径。**",
            "课上说 MCP 可以连接工具，老师提到后面讲项目文档。",
        )

        result = self.run_checker(observer_note, "--final-note")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("旁观者视角", result.stdout)
        self.assertIn("课上说", result.stdout)

    def test_final_note_accepts_learner_voice(self) -> None:
        result = self.run_checker(VALID_FINAL_NOTE, "--final-note")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_clean_transcript_can_keep_teacher_and_pending(self) -> None:
        transcript = "老师提到这里待确认，后面需要按课件再核对。"

        result = self.run_checker(transcript, "--allow-partial")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
