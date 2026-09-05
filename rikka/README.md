# RikkaHub 运行层

本目录只保存 RikkaHub 的静态工作规则和助手提示词，**不保存动态正史**。动态事实始终实时读取仓库当前 HEAD。

## 一、导入 4 个 Skills
在 RikkaHub「Skills → 从 GitHub 导入」分别导入：

- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-core`
- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-planner`
- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-writer`
- `https://github.com/ghzyzttxwd/yanhuatianfu/tree/main/rikka/skills/novel-reviewer`

## 二、创建 3 个助手

### 总策划
- System Prompt：`rikka/assistants/planner-system.md`
- Skills：`novel-core` + `novel-planner`
- GitHub：允许读写本仓库

### 正文写手
- System Prompt：`rikka/assistants/writer-system.md`
- Skills：`novel-core` + `novel-writer`
- GitHub：只读本仓库

### 独立审核员
- System Prompt：`rikka/assistants/reviewer-system.md`
- Skills：`novel-core` + `novel-reviewer`
- GitHub：只读本仓库

## 三、三个助手统一设置
- RikkaHub Memory：关闭
- Global Memory：关闭
- Recent Chats Reference：关闭
- Lorebook：暂不承担正史
- 动态境界、资源、战力、章节、大纲不得写入 Skill

## 四、正式流程
总策划定章纲 → 写手写草稿 → 审核员独立审核 → 修改 → 作者确认定稿 → 总策划归档正文并同步动态资料 → 运行 `python scripts/validate_project.py`。
