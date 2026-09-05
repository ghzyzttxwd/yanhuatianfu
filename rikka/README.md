# RikkaHub 运行层

本项目在 RikkaHub **只创建 2 个助手**。项目内部仍有“策划 / 写作 / 审核”三种功能，但策划和写作合并到同一个主助手。

## 1. 导入 4 个 Skills（只导一次）

- `rikka/skills/novel-core`
- `rikka/skills/novel-planner`
- `rikka/skills/novel-writer`
- `rikka/skills/novel-reviewer`

动态正史不放进 Skill；始终实时读取 GitHub 当前 HEAD。

## 2. 创建两个助手

### 主助手：`衍化天赋·策划正文`
- System Prompt：`rikka/assistants/main-system.md`
- Skills：`novel-core` + `novel-planner` + `novel-writer`
- GitHub：读写
- 职责：策划、写正文、按审核意见修改、审核通过后归档与同步资料

### 审核助手：`衍化天赋·独立审核`
- System Prompt：`rikka/assistants/reviewer-system.md`
- Skills：`novel-core` + `novel-reviewer`
- GitHub：需要读取全仓库；写入权限只用于 `工作稿/审核结果.md`，提示词禁止修改任何正式资料
- 职责：独立审核并给出 PASS/FAIL

## 3. 两个助手统一设置
- Memory：关闭
- Global Memory：关闭
- Recent Chats Reference：关闭
- Lorebook：不承担正史

## 4. 每章固定流程

1. 对主助手说：`写下一章`。
   - 主助手写完并保存 `工作稿/待审核正文.md`。
2. 切到审核助手说：`审核`。
   - 审核助手自己读待审核稿和仓库。
   - 第一行只给 `通过` 或 `不通过`，并同步写 `工作稿/审核结果.md`。
3. 如果 `不通过`：回主助手说 `按审核结果修改`，然后再去审核。
4. 如果 `通过`：作者不用检查技术错误，也不用处理资料。下次回主助手说 `下一章/继续`，主助手会先验证 PASS 对应同一 revision，再自动归档上一章、同步资料、跑校验，然后写下一章。

## 5. 防错机制

每版待审核稿都有 revision（如 `277-r1`、`277-r2`）。审核 PASS 只对同一 revision 有效。正文一改，旧 PASS 自动作废，避免错版归档。

作者只负责创作取舍和最终喜好，不负责战力、设定、连续性、资源、伏笔、人物 OOC 或 AI 味查错。