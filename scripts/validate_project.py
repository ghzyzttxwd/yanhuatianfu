#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg: str):
    errors.append(msg)

manifest_path = ROOT / "SOURCE_MANIFEST.md"
state_path = ROOT / "工作稿/当前续写工作状态.md"

for path in [manifest_path, state_path]:
    if not path.exists():
        fail(f"缺少必需文件: {path.relative_to(ROOT)}")

if errors:
    for e in errors:
        print(f"FAIL: {e}")
    sys.exit(1)

manifest = manifest_path.read_text(encoding="utf-8")
state = state_path.read_text(encoding="utf-8")

# 1. Manifest 中引用的 Markdown 文件必须存在。
for ref in sorted(set(re.findall(r"`([^`]+\.md)`", manifest))):
    if "/" in ref or ref == "SOURCE_MANIFEST.md":
        if not (ROOT / ref).exists():
            fail(f"Manifest 引用了不存在的文件: {ref}")

# 2. 当前 HEAD 不允许残留已废弃的迁移/原文分片资料。
for rel in [
    "migration_payload",
    "正文/S0原文字符分片",
    "正文/原文分片",
    "迁移完成说明_非正文资料.md",
]:
    if (ROOT / rel).exists():
        fail(f"发现应从当前 HEAD 清除的残留: {rel}")

# 3. 以实际正文文件名计算最新已归档章节。
chapters = []
for p in (ROOT / "正文").glob("*.md"):
    m = re.match(r"^(\d+)_", p.name)
    if m:
        chapters.append(int(m.group(1)))
if not chapters:
    fail("正文目录中没有可识别的正式章节文件")
    latest = None
else:
    latest = max(chapters)

# 4. 当前状态与 Manifest 的下一章必须一致，且等于最新正文 + 1。
state_match = re.search(r"当前下一章[：:]\s*\**第?(\d+)", state)
manifest_match = re.search(r"当前直接创作目标[：:]\s*\**第(\d+)章", manifest)

if not state_match:
    fail("无法从当前续写工作状态解析‘当前下一章’")
if not manifest_match:
    fail("无法从 SOURCE_MANIFEST 解析‘当前直接创作目标’")

if state_match and manifest_match:
    state_next = int(state_match.group(1))
    manifest_next = int(manifest_match.group(1))
    if state_next != manifest_next:
        fail(f"下一章不一致: 当前状态={state_next}, Manifest={manifest_next}")
    if latest is not None and state_next != latest + 1:
        fail(f"下一章与实际正文不连续: 最新正文={latest}, 下一章={state_next}")

    # 5. 下一章必须被且仅被一个‘当前版’动态大纲覆盖。
    covering = []
    for p in (ROOT / "动态大纲").glob("*当前版.md"):
        m = re.match(r"^(\d+)-(\d+)章", p.name)
        if m and int(m.group(1)) <= state_next <= int(m.group(2)):
            covering.append(p.name)
    if len(covering) != 1:
        fail(f"下一章 {state_next} 应被且仅被一个当前版动态大纲覆盖，实际: {covering}")

# 6. README 不得维护动态章节进度，避免形成第二事实源。
readme = (ROOT / "README.md").read_text(encoding="utf-8")
if re.search(r"当前(?:下一章|进度).*\d+", readme):
    fail("README 中发现动态章节进度；动态状态只能由 Manifest/当前状态维护")

# 7. RikkaHub 运行层必须完整；Skill 必须有 frontmatter，且不能硬编码动态章节事实。
rikka_required = [
    "rikka/README.md",
    "rikka/skills/novel-core/SKILL.md",
    "rikka/skills/novel-planner/SKILL.md",
    "rikka/skills/novel-writer/SKILL.md",
    "rikka/skills/novel-reviewer/SKILL.md",
    "rikka/assistants/planner-system.md",
    "rikka/assistants/writer-system.md",
    "rikka/assistants/reviewer-system.md",
]
for rel in rikka_required:
    if not (ROOT / rel).exists():
        fail(f"缺少RikkaHub运行层文件: {rel}")

for skill_path in (ROOT / "rikka/skills").glob("*/SKILL.md"):
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or not re.search(r"^name:\s*\S+", text, re.M) or not re.search(r"^description:\s*.+", text, re.M):
        fail(f"Skill frontmatter 不完整: {skill_path.relative_to(ROOT)}")
    if re.search(r"当前(?:下一章|直接创作目标)[^\n]*\d+|第\d+章《", text):
        fail(f"Skill 中发现动态章节事实硬编码: {skill_path.relative_to(ROOT)}")

if errors:
    for e in errors:
        print(f"FAIL: {e}")
    sys.exit(1)

print("PASS: 项目资料入口、章节连续性、动态大纲覆盖、残留清理与RikkaHub运行层检查均通过")
