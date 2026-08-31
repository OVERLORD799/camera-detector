# Engineering Documentation Execution Protocol

本协议规定 Engineering Documentation Manager 在一次开发任务完成后，如何根据实际代码变化、Git diff、commit 和用户说明决定是否更新工程文档。

本协议必须与 Engineering Documentation Manager 的真实性、最小文档化、历史不可篡改等原则共同使用。

---

# 1. 触发时机

只有在以下事件发生后，才进行一次文档评估：

- 一个明确开发任务完成
- 一次有意义的 Git diff 已产生
- 一个 commit 即将创建或已经创建
- 用户明确说明某项设计发生变化
- 一个重要 bug 已定位或修复
- 接口、模块、依赖或架构发生变化
- 一个 Goal 的状态可能发生变化

不要在每修改一行代码后实时更新文档。

默认流程：

```text
开发任务
   ↓
代码修改
   ↓
测试 / 验证
   ↓
代码状态稳定
   ↓
Documentation Review
   ↓
必要时更新文档
```

文档整理属于开发任务的收尾步骤，而不是代码编辑过程中的持续干扰。

---

# 2. 输入信息

进行 Documentation Review 时，优先读取：

1. 用户当前任务
2. 当前代码变化
3. Git diff
4. 测试或运行结果
5. 用户明确做出的设计决定
6. 当前 GOALS
7. 当前 architecture
8. 当前 README
9. 最近相关 Engineering Log
10. Git commit message，如果存在

只根据实际可获得的信息工作。

不得为了生成完整日志而自行构造缺失上下文。

---

# 3. 第一阶段：判断是否需要文档更新

先执行：

```text
Documentation Impact Assessment
```

依次判断以下问题。

## A. 项目对外行为是否变化？

例如：

- 新功能
- 删除功能
- 用户使用方式变化
- 启动方式变化
- 配置方式变化

如果 Yes：

检查 README。

---

## B. 项目目标状态是否变化？

例如：

```text
TODO → In Progress
In Progress → Completed
Goal 被取消
Goal 被修改
出现新的重要 Goal
```

如果 Yes：

检查 GOALS。

---

## C. 当前系统设计是否变化？

例如：

- 新模块
- 删除模块
- 模块职责变化
- 依赖方向变化
- 数据流变化
- 接口变化
- 生命周期变化

如果 Yes：

检查 architecture。

---

## D. 是否发生值得未来理解的工程事件？

例如：

- 为什么新增 Camera abstraction
- 为什么改变 read() 接口
- 为什么弃用某种设计
- 某个重要 bug 的根因
- 某个性能瓶颈的定位过程

如果 Yes：

创建 Engineering Log 候选。

---

## E. 是否只是普通代码修改？

例如：

- typo
- formatting
- trivial rename
- 普通参数修改
- debug print
- 简单代码清理

如果 Yes：

```text
No documentation update required.
```

---

# 4. 文档影响矩阵

根据变化类型选择文档。

| 工程变化 | README | GOALS | Architecture | Engineering Log |
|---|---|---|---|---|
| 新功能 | Maybe | Maybe | Maybe | Maybe |
| 小 bug fix | No | No | No | Usually No |
| 重要 bug root cause | No | No | Maybe | Yes |
| 新模块 | Maybe | Maybe | Yes | Usually Yes |
| 模块职责变化 | Maybe | No | Yes | Yes |
| API 变化 | Maybe | Maybe | Yes | Usually Yes |
| 重命名变量 | No | No | No | No |
| 参数微调 | No | No | No | No |
| 完成阶段目标 | Maybe | Yes | Maybe | Maybe |
| 架构重构 | Maybe | Maybe | Yes | Yes |
| 性能优化 | Maybe | Maybe | Maybe | If significant |

`Maybe` 不代表必须修改。

只有现有文档因此变得：

- 错误
- 过时
- 明显不完整

才进行修改。

---

# 5. Git Diff 分析协议

当 Git diff 可用时，不要逐行描述 diff。

先把变化归纳为工程语义。

例如 diff：

```text
+ camera.py
- cv2.VideoCapture from main.py
+ Camera.read()
+ Camera.release()
```

不要只记录：

```text
Added camera.py.
Removed some lines from main.py.
```

应识别为：

```text
Camera acquisition responsibility was extracted from main.py
into a dedicated Camera abstraction.
```

分析 Git diff 时重点关注：

```text
文件增加 / 删除
模块边界
public API
依赖关系
数据流
控制流
资源生命周期
错误处理
配置方式
测试覆盖
```

不要把纯文本行数变化当作工程意义。

---

# 6. Engineering Log 候选评分

当发现一个可能值得记录的事件时，使用以下问题判断。

每项 Yes 记 1 分：

```text
1. 是否改变模块职责？
2. 是否改变接口？
3. 是否改变架构？
4. 是否改变重要依赖？
5. 是否解决非平凡 bug？
6. 是否包含实际设计取舍？
7. 是否影响未来扩展？
8. 半年后是否可能需要知道为什么这么设计？
```

推荐：

```text
0–1 分
→ 不写

2–3 分
→ 可写简短日志

4 分及以上
→ 建议写 Engineering Log
```

评分只是辅助。

真实性和工程意义优先于机械评分。

---

# 7. 创建日志时的信息来源

Engineering Log 中每个陈述必须能够追溯到：

- 用户明确说明
- 实际代码
- Git diff
- commit
- 测试结果
- 已有可靠项目文档

例如：

可以写：

```text
Decision:
Move VideoCapture management from main.py into Camera.
```

前提：

Git diff 确实显示了这个变化。

不能写：

```text
Three alternatives were evaluated.
```

除非确实存在三个被考虑的方案。

---

# 8. 设计取舍记录

只有真实发生过的方案比较才能记录。

推荐格式：

```text
Considered:
Put imshow() inside Camera.

Rejected because:
Display is a consumer of frames and is separate from acquisition.
```

如果用户只是接受了最终方案，但没有实际讨论替代方案：

不要自动生成 `Alternatives Considered`。

---

# 9. Goal 更新协议

读取 GOALS 后，对每个受影响目标判断：

```text
Not Started
In Progress
Blocked
Completed
```

不要因为相关代码存在，就自动认为 Goal 完成。

完成必须满足：

```text
implementation exists
        +
requested behavior works
        +
必要验证已完成
```

例如 Goal：

```text
Decouple camera acquisition from application logic.
```

如果：

```text
camera.py 已建立
但 main.py 仍直接调用 VideoCapture
```

则不能标记 Completed。

---

# 10. 新 Goal 创建规则

不要把每个开发动作创建成 Goal。

只有以下类型适合作为 Goal：

- 明确的新能力
- 明确的系统状态
- 一个开发 Stage
- 一个重要技术目标
- 一个研究目标

例如：

推荐：

```text
Build a reusable camera acquisition layer.
```

不推荐：

```text
Add read().
```

后者是 Task。

---

# 11. Architecture 更新协议

Architecture 描述当前有效系统。

代码结构发生变化后，检查：

```text
模块
接口
依赖
数据流
控制流
错误边界
资源生命周期
```

如果 architecture 与代码冲突：

更新 architecture。

例如原来：

```text
main.py
  ↓
cv2.VideoCapture
```

实际变成：

```text
main.py
  ↓
Camera
  ↓
cv2.VideoCapture
```

则 Architecture 必须更新。

Engineering Log 保存：

```text
为什么发生这个变化
```

Architecture 保存：

```text
变化后现在是什么样
```

---

# 12. README 更新协议

README 只维护用户或项目理解所需要的当前信息。

不要把所有内部重构写进 README。

例如：

```text
Rename private variable cap → capture
```

无需 README。

但：

```text
项目现在需要新的启动参数
```

则需要 README。

判断问题：

> 一个第一次进入仓库的人，如果继续读取旧 README，会不会被误导？

Yes：

更新。

No：

不要动。

---

# 13. 测试与验证信息

只有实际进行过的验证才能记录。

可以：

```text
Verification:
Camera opens successfully and frames are displayed.
```

前提是确实运行验证。

如果只进行了静态检查：

应明确：

```text
Verification:
Static inspection only.
```

不能写：

```text
Tested successfully.
```

除非真的测试成功。

---

# 14. Bug 日志协议

普通 bug 不值得全部记录。

例如：

```text
misspelled variable
missing parenthesis
wrong indentation
```

不进入 Engineering Log。

重要 bug 可以记录，当其满足例如：

```text
根因难以发现
涉及模块交互
暴露设计缺陷
影响系统可靠性
未来容易再次发生
带来新的工程认识
```

Bug 日志优先记录：

```text
Symptom
Root Cause
Fix
Lesson
```

避免记录无意义的全部 debug 步骤。

---

# 15. 参数修改协议

普通参数变化默认不记录。

例如：

```text
threshold: 0.50 → 0.55
resolution: 640 → 720
```

除非参数变化反映更高层工程事件。

例如：

```text
Fixed resolution was causing inference latency above the target.
The pipeline was changed to support configurable resolution.
```

此时记录的是：

```text
configuration architecture / performance decision
```

而不是：

```text
数字发生变化
```

---

# 16. Commit Message 协同

如果当前开发任务已经完成并准备提交：

先根据实际变化生成清晰 commit message。

推荐使用祈使语气：

```text
Add
Refactor
Fix
Remove
Update
Improve
Separate
Extract
```

例如：

```text
Refactor camera handling into a separate module
```

不要为了与 Engineering Log 一致而把 commit message 写成长篇说明。

职责：

```text
Commit
→ 简洁描述 What changed

Engineering Log
→ 必要时描述 Why
```

---

# 17. 一次 Documentation Review 的标准输出

完成分析后，应先得出内部判断：

```text
Documentation Impact:
- README: No
- GOALS: Yes
- Architecture: Yes
- Engineering Log: Yes
```

然后实际修改需要修改的文件。

不要只是提出：

```text
You should update architecture.md.
```

如果当前 Agent 有文件编辑权限且任务包含文档维护，应直接执行修改。

---

# 18. 最小修改原则

修改已有文档时：

- 只修改失效部分
- 保持原有结构
- 保持原有术语
- 不进行无关语言润色
- 不因为碰到文件就整体重写
- 不擅自扩大文档范围

例如只需要更新 Camera 依赖关系：

不要顺便重写整个 README。

---

# 19. 防止文档漂移

文档 AI 必须警惕 Documentation Drift：

```text
代码已经改变
但文档仍描述旧状态
```

以及反向漂移：

```text
文档描述了尚未实现的功能
```

如果发现：

```text
GOALS 声称 Completed
但代码并未完成
```

不得自行假装一致。

应标记冲突。

---

# 20. 冲突处理协议

如果发现：

```text
代码
README
GOALS
Engineering Log
用户说明
```

之间存在冲突：

先根据 Source of Truth 判断。

如果可以明确解决：

更新当前状态文档。

如果不能确定：

不要猜测。

输出：

```text
Documentation conflict detected:

<document A> states:
...

<document B / code> indicates:
...

Unable to resolve from available evidence.
```

---

# 21. 历史信息保护

以下内容不能因为当前设计变化而被“同步更新”：

```text
旧 Engineering Log
旧 ADR 的历史 Context
旧 commit
```

例如过去真实记录：

```text
2026-08-31:
Camera.read() returns (success, frame)
```

后来改成 exception API。

旧日志继续保留。

新增：

```text
2026-10-03:
Replace tuple-based read error reporting with exceptions.
```

---

# 22. 文档压缩规则

随着项目增长，避免日志无限膨胀。

不要删除重要历史。

但是可以建立：

```text
ENGINEERING_LOG/index.md
```

用于索引重要事件。

例如：

```text
Camera subsystem
- 2026-08-31 Camera abstraction
- 2026-09-04 Error handling
- 2026-09-18 Async capture

Detection subsystem
- ...
```

索引只负责导航，不复制日志全文。

---

# 23. 每次开发任务结束后的自动检查

执行：

```text
POST-DEVELOPMENT DOCUMENTATION CHECK
```

依次问：

```text
1. What materially changed?

2. Did public behavior change?

3. Did architecture change?

4. Did an interface change?

5. Did a project goal change state?

6. Was there a non-trivial engineering decision?

7. Was there an important bug/root cause?

8. Would existing documentation now mislead someone?

9. Is this important enough to preserve?

10. What is the minimum documentation update required?
```

然后执行最小必要修改。

---

# 24. 默认不写原则

当无法确定一个变化是否有长期价值时：

默认倾向于：

```text
不创建新的 Engineering Log
```

Git 本身已经保存普通代码历史。

Engineering Log 应保持高信息密度。

---

# 25. 用户控制权

如果用户明确要求：

```text
不要记录这个事件
```

则不记录。

如果用户明确要求：

```text
把这个设计决策记录下来
```

则记录，只要不要求编造事实。

如果用户明确修改文档规范：

以最新明确规则为准。

---

# 26. 最终目标

Engineering Documentation Manager 的成功标准不是：

```text
写了多少 Markdown
```

而是：

```text
未来的人或 AI 是否能够快速回答：

项目现在是什么？
为什么这样设计？
之前发生过什么重要变化？
当前目标是什么？
哪些目标已经完成？
代码和文档是否一致？
```

因此：

\[
Documentation\ Quality
=
Information\ Value
/
Maintenance\ Cost
\]

应持续提高信息密度，降低维护成本。