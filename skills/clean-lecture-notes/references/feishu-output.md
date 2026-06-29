# 飞书输出工作流

当用户希望将清洗稿或学习笔记写入飞书时，使用本参考。

## 必需技能路由

- 飞书操作前先读取 `lark-shared`，以遵守认证、身份和权限规则。
- 读取和写入飞书 docx 时，使用 `lark-doc`。
- 搜索、上传、下载妙记或读取元数据时，使用 `lark-minutes`。
- 从妙记获取逐字稿、总结、待办和章节时，使用 `lark-vc` 的 `vc +notes`。
- 编辑已有白板，或创建复杂且非空的白板时，使用 `lark-whiteboard`。

## 输入路由

| 用户输入 | 路由 |
|---|---|
| 本地音频或视频 | 通过云空间上传，创建妙记，然后用 `vc +notes` 拉取笔记产物 |
| 飞书妙记 URL | 提取 `minute_token`，用 `vc +notes` 拉取产物 |
| 飞书 docx 逐字稿 URL | 使用 `docs +fetch` 拉取 |
| 本地逐字稿 | 直接读取本地文件 |
| 课件 URL | 浏览或拉取来源，并将其作为笔记主干 |

## 写入默认值

- 默认新建飞书文档。
- 除非用户明确要求，不要覆盖源逐字稿。
- 条件允许时，保留清洗稿、笔记正文和图示的本地中间文件。
- 对长笔记，先创建骨架，再分块追加或插入章节。

## 飞书文档结构

推荐输出顺序：

1. 标题。
2. 目标提示。
3. 思维导图或知识地图。最终学习笔记中，`思维导图` 必须是 Mermaid flowchart 或等价可视化白板。
4. 导图较密时，添加快速索引。
5. 复习路径。
6. 核心结论。
7. 主动回忆问题。
8. 核心笔记模块。
9. 练习、项目迁移或面试迁移。
10. 质量审计和资料来源。

## 白板和 Mermaid 检查

- 最终文档中不要留下空白白板。
- 对内嵌 Mermaid 导图，写入前先确认 Mermaid 文本语法基本合理，优先使用 `flowchart TD` 或 `flowchart LR`。
- 对已有白板，在工具允许时，写入后导出图片或查询节点。
- 最终学习笔记的 `思维导图` 章节不能只保留 `pre/code` 纯文本树状图；如果需要文本辅助说明，放在图后。
- 如果白板写入失败，改用内嵌 Mermaid，不要留下空白块或纯文本树状图。
- 写入后拉取 `思维导图` 章节，确认存在 `whiteboard type="mermaid"` 或等价 Mermaid 内容。
- 下载白板缩略图或导出图时，确认图片非空且主体文字可读。

## 清洗稿和学习笔记边界

- 清洗稿可以保留课堂顺序、说话人、待确认和回查线索。
- 最终学习笔记必须改成学习者复习视角，不写成旁听记录。
- 最终学习笔记不输出独立 `待确认` 章节；无法确认且影响事实的内容放入质量审计。

## 校验命令

按需使用以下命令族：

```bash
lark-cli docs +fetch --api-version v2 --doc "<doc>" --scope outline --max-depth 3 --as user
lark-cli docs +fetch --api-version v2 --doc "<doc>" --scope keyword --keyword "主动回忆|资料来源|最终判断" --as user
lark-cli docs +fetch --api-version v2 --doc "<doc>" --scope keyword --keyword "思维导图" --as user
lark-cli whiteboard +query --whiteboard-token "<token>" --output_as image --output ./verify.png --as user
```

## 最终报告

报告以下内容：

- 飞书文档 URL。
- 源文档是否保持不变。
- 本地中间文件保存位置。
- 已执行的校验检查。
- 任何限制，例如无法访问课件，或逐字稿术语存在歧义。
