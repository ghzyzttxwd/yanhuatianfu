# RikkaHub 运行层

本目录只保存 RikkaHub 的静态工作规则和助手提示词，**不保存动态正史**。动态事实始终实时读取仓库当前 HEAD。

## 一、导入 4 个 Skills
在 RikkaHub「Skills → 从 GitHub 导入」分别导入：

- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-core`
- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-planner`
- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-writer`
- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-reviewer`

## 二、只创建 1 个助手

助手名建议：`衍化天赋·总控写作`

- System Prompt：`rikka/assistants/master-system.md`
- Skills：启用全部 4 个 Skill
- GitHub：允许读写本仓库

总控助手内部按阶段执行：策划预检 → 正文写作 → 独立审核 → 自动修订 → 终验 → 只交付最终稿。

**作者不参与中间审核和返工。** 可自行解决的问题不得甩给作者。

## 三、统一设置
- RikkaHub Memory：关闭
- Global Memory：关闭
- Recent Chats Reference：关闭
- Lorebook：不承担正史
- 动态境界、资源、战力、章节、大纲不得写入 Skill

## 四、日常使用
作者通常只需要：

- `写下一章`：总控自行读取必要资料、写作、审核、返工，只返回最终正文。
- `继续` / `下一章`：视为上一章通过；先归档、同步动态资料并校验，再继续下一章。
- 直接指出剧情方向：总控按作者意见重做，不要求作者承担技术性查错。

归档后必须运行 `python scripts/validate_project.py`。