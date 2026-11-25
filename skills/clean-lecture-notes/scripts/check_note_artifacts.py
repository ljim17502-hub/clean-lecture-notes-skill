#!/usr/bin/env python3
"""检查课堂笔记产物是否包含必需的复习笔记结构。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text()


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


AUDIT_SECTION = "资料来源与质量审计"
AUDIT_SOURCE_REFERENCE = r"(?:录音里|转写稿里|原稿里)(?:说|提到|出现|记录|写着)?"
SOURCE_NARRATION = r"(?:课程|课堂|录音|原文|原稿).{0,12}(?:讲了|说了|提到|展示|播放|出现|附带)"

OBSERVER_VOICE_PATTERNS: list[tuple[str, str]] = [
    (
        r"老师(?:说|讲|解释|播放|提到|提醒|展示|强调|安排|给出|认为|总结|让|列出|建议|测试|举例)?",
        "改成“我需要掌握的是...”或“关键判断是...”",
    ),
    (
        r"(?:这节课|本节课)(?:先|主要|继续|补充|讲了|介绍|讨论|围绕)?",
        "改成知识结构或复习目标，不写课程过程。",
    ),
    (
        r"(?:课堂里|课上)(?:说|讲|提到|展示|播放|解释|补充|安排|强调)?",
        "改成“这个案例说明...”或“实践时要注意...”。",
    ),
    (
        AUDIT_SOURCE_REFERENCE,
        "把来源过程放到资料审计，不放进正文叙述。",
    ),
    (
        r"(?:原始文件末尾|文件末尾(?:写着|附带|出现))",
        "直接整合为正文模块，不描述生成材料的位置。",
    ),
    (
        r"上课时(?:展示|播放|讲|提到|说)?",
        "改成案例结论、操作步骤或项目迁移项。",
    ),
    (
        r"(?:前面|后面|最后)(?:讲了|说了|介绍了|补充了|提到了)",
        "改成模块关系，例如“项目文档体系包括...”。",
    ),
    (
        SOURCE_NARRATION,
        "改成学习者结论，不写“谁/哪里讲了什么”。",
    ),
    (
        r"待确认",
        "最终学习笔记不设独立待确认；可推断术语直接归一化。",
    ),
]


def line_number_for(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def markdown_headings(text: str):
    fence = ""
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r" {0,3}(\x60{3,}|~{3,})(.*)", line)
        if fence:
            if (marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence)
                    and not marker[2].strip()):
                fence = ""
        elif marker:
            fence = marker[1]
        else:
            heading = re.match(r" {0,3}(#{1,6})[ \t]+(.*)", line)
            if heading:
                title = re.sub(r"[ \t]+#+[ \t]*$", "", heading[2]).strip()
                yield offset, offset + len(line), len(heading[1]), title
        offset += len(line)


def xml_headings(text: str):
    # Match Feishu heading blocks, including adjacent tags on a single line.
    blocks = re.compile(
        r"<!--.*?-->|<!\[CDATA\[.*?\]\]>|<h([1-6])(?:\s+[^<>]*)?>(.*?)</h\1\s*>",
        re.DOTALL | re.IGNORECASE,
    )
    for heading in blocks.finditer(text):
        if heading[1]:
            title = re.sub(r"<[^>]+>", "", heading[2]).strip()
            yield heading.start(), heading.end(), int(heading[1]), title


def audit_spans(text: str, *, xml: bool):
    headings = xml_headings(text) if xml else markdown_headings(text)
    start, audit_level = None, 0
    for position, end, level, title in headings:
        if start is not None and level <= audit_level:
            yield start, position
            start = None
        if start is None and title == AUDIT_SECTION:
            start, audit_level = end, level
    if start is not None:
        yield start, len(text)


def find_observer_voice_hits(text: str, *, xml: bool = False) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    spans = list(audit_spans(text, xml=xml))
    for pattern, hint in OBSERVER_VOICE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            value = match.group(0).strip()
            source_narration = pattern == AUDIT_SOURCE_REFERENCE or (
                pattern == SOURCE_NARRATION and value.startswith(("录音", "原文", "原稿"))
            )
            if source_narration and any(
                start <= match.start() and match.end() <= end for start, end in spans
            ):
                continue
            if value:
                hits.append((line_number_for(text, match.start()), value, hint))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="交付前校验本地课堂笔记 Markdown/XML 产物。",
    )
    parser.add_argument("paths", nargs="+", help="要检查的 Markdown/XML/文本产物")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="缺少学习笔记章节时仅报告警告。",
    )
    parser.add_argument(
        "--strict-whiteboard",
        action="store_true",
        help="产物中仍有空白飞书白板标记时判定失败。",
    )
    parser.add_argument(
        "--final-note",
        action="store_true",
        help="按最终学习笔记规则检查是否仍有旁观者视角表达。",
    )
    args = parser.parse_args()

    files = [Path(p) for p in args.paths]
    missing_files = [str(p) for p in files if not p.exists()]
    if missing_files:
        print("缺少文件：")
        for item in missing_files:
            print(f"  - {item}")
        return 2

    documents = [(path, read_text(path)) for path in files]
    text = "\n\n".join(content for _, content in documents)
    normalized = re.sub(r"\s+", " ", text)

    blank_whiteboard = "<whiteboard type=" + '"blank"' + "></whiteboard>"
    banned = [
        "TO" + "DO",
        "place" + "holder",
        "lark-whiteboard" + "-cli",
        "<DOC_" + "TOKEN>",
        "<MINUTE_" + "TOKEN>",
        "<BOARD_" + "TOKEN>",
    ]
    if args.strict_whiteboard:
        banned.append(blank_whiteboard)
    banned_hits = [item for item in banned if item in text]
    warnings = []
    if not args.strict_whiteboard and blank_whiteboard in text:
        warnings.append("仍有空白飞书白板标记；仅在填充白板前可接受。")

    categories = {
        "结构图或知识地图": [r"思维导图", r"知识地图", r"mindmap", r"知识图谱"],
        "使用路径": [r"使用方法", r"复习路径", r"可用时间", r"按时间"],
        "核心结论": [r"核心结论", r"必须.*结论", r"必须.*记住", r"key conclusions"],
        "主动回忆": [r"主动回忆", r"自测", r"复盘问题", r"闭卷"],
        "模型或模块": [r"认知模型", r"核心模块", r"章节", r"chapter"],
        "练习或话术": [r"面试话术", r"项目迁移", r"实操复盘", r"练习", r"实践"],
        "资料来源": [r"资料来源", r"原始资料", r"来源", r"\bsource\b", r"references?"],
        "重点加粗": [r"\*\*[^*\n]{2,}\*\*", r"<b>[^<]{2,}</b>", r"<strong>[^<]{2,}</strong>"],
    }

    missing_categories = [
        name for name, patterns in categories.items() if not has_any(normalized, patterns)
    ]

    broken_heading_patterns = [
        r"^#{1,6}\s*$",
        r"<h[1-6]>\s*</h[1-6]>",
        r"^#+\s*(待补|未命名|无标题)\s*$",
    ]
    broken_headings = []
    for pattern in broken_heading_patterns:
        broken_headings.extend(re.findall(pattern, text, re.MULTILINE))

    observer_voice_hits = []
    if args.final_note:
        line_offset = 0
        for path, content in documents:
            observer_voice_hits.extend(
                (number + line_offset, value, hint)
                for number, value, hint in find_observer_voice_hits(
                    content, xml=path.suffix.lower() == ".xml"
                )
            )
            line_offset += content.count("\n") + 2

    ok = (
        not banned_hits
        and not broken_headings
        and not observer_voice_hits
        and (not missing_categories or args.allow_partial)
    )

    if banned_hits:
        print("发现未处理占位标记：")
        for hit in banned_hits:
            print(f"  - {hit}")
    if broken_headings:
        print("发现异常标题：")
        for hit in broken_headings:
            print(f"  - {hit!r}")
    if missing_categories:
        label = "警告" if args.allow_partial else "缺少必需章节"
        print(f"{label}：")
        for name in missing_categories:
            print(f"  - {name}")
    if observer_voice_hits:
        print("发现旁观者视角表达（最终学习笔记需改为学习者结论/项目迁移视角）：")
        for line_no, value, hint in observer_voice_hits[:12]:
            print(f"  - L{line_no}: {value} -> {hint}")
        if len(observer_voice_hits) > 12:
            print(f"  - ... 另有 {len(observer_voice_hits) - 12} 处")
    if warnings:
        print("警告：")
        for warning in warnings:
            print(f"  - {warning}")

    if ok:
        print("课堂笔记产物校验通过。")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
