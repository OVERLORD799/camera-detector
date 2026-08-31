可以把它当成一个“小型规则系统”来调试，而不是每次看到文档不满意就整份 prompt 重写。

最有效的方法是：

\[
\boxed{\text{现象} \rightarrow \text{错误类型} \rightarrow \text{对应规则} \rightarrow \text{最小修改}}
\]

比如以后 AI 写出一篇你不满意的 Engineering Log，不要只说“写得不好”，而要先判断它到底是哪一类失败。

### 常见问题可以这样定位

| 表现 | 本质问题 | 应该改哪类规则 |
|---|---|---|
| 什么小改动都写日志 | 过滤阈值太低 | `What to Record` / 评分规则 |
| 日志太长 | 输出约束不足 | 长度、最小文档原则 |
| AI 编造“考虑过三个方案” | 真实性约束失效 | Anti-Fabrication |
| README、LOG 到处重复 | 文档职责边界模糊 | Document Structure / Avoid Duplication |
| 该更新 architecture 却没更新 | 触发条件漏掉 | Impact Assessment |
| 改了旧日志来适配新代码 | 历史保护不足 | Append-only |
| GOAL 被过早标 Completed | 完成判据太宽 | Goal Update Protocol |
| 日志只写“改了什么”，没有为什么 | Git 和 Log 分工不清 | Commit / Engineering Log rules |
| 纯 Python 知识被塞进日志 | Notes / Log 边界不足 | Knowledge vs Engineering Log |
| 每次都改五六个文档 | 最小修改原则没约束住 | Minimum Modification |
| 同一种情况有时写、有时不写 | 判断规则不够确定 | 增加判例 / decision table |

也就是说，先定位到**是哪一个机制坏了**。

---

## 最好给提示词加入“可诊断性”

你现在的协议里已经有：

```text
Documentation Impact:
- README: No
- GOALS: Yes
- Architecture: Yes
- Engineering Log: Yes
```

这个设计很好。

我建议进一步要求 AI 在执行文档更新时，内部先产生一个简短判定：

```text
Event:
Extract camera acquisition into Camera class.

Classification:
Architecture change + responsibility change.

Documentation decision:
README: No
GOALS: Yes
Architecture: Yes
Engineering Log: Yes

Reason:
...
```

不一定每次都展示给你，但在你发现输出有问题的时候，可以要求它输出这个判定。

这样你能知道：

```text
最终文档错误
```

究竟是因为：

```text
AI 对事件分类错了
```

还是：

```text
事件分类正确，但写作规则错了
```

这两个修法完全不同。

---

## 举个具体例子

假设你只是：

```text
threshold = 0.5
→
threshold = 0.55
```

AI 却生成：

```text
2026-09-01 — Optimize detection threshold
...
```

不要直接增加：

> “不要记录 threshold 从 0.5 改成 0.55。”

这种规则太具体。

应该诊断：

```text
现象：
普通参数调整被认为是重要工程事件

根因：
Engineering Log significance threshold 太低

修改：
强化“参数变化只有反映架构、可靠性、
性能根因或可复现工程结论时才记录”
```

这是：

\[
\boxed{\text{修规则，不修样例}}
\]

否则 prompt 很快就会变成：

```text
不要记录A
不要记录B
不要记录C
不要记录D
...
```

越来越长，而且还是不断漏情况。

---

## 但“判例”也很有价值

规则之外，可以维护少量正反例。

例如专门增加：

```text
# Calibration Examples
```

里面记录真正踩过坑的例子。

例如：

### Case 1 — Do not log

```text
Change:
threshold 0.50 → 0.55

Reason:
Routine parameter tuning with no architectural or engineering consequence.

Decision:
No documentation update.
```

### Case 2 — Log

```text
Change:
Introduce configurable detection threshold.

Reason:
A fixed threshold caused systematic failures across lighting conditions,
so configuration became part of the system design.

Decision:
Update architecture and Engineering Log.
```

这样 AI 能学到：

\[
\boxed{\text{不是“参数不能记录”，而是要判断参数变化背后的工程意义}}
\]

这比继续堆抽象规则更稳定。

---

# 我建议以后维护三个层次

### 第一层：Core Principles

尽量不要频繁修改。

例如：

- 真实性
- 最小文档化
- 历史不可篡改
- 文档职责分离
- 信息价值优先于文档数量

这些是宪法。

---

### 第二层：Operational Rules

允许根据实际表现逐步调整。

例如：

```text
什么时候写 Engineering Log
Goal 什么时候算完成
什么时候更新 README
评分阈值是多少
```

这些相当于法律。

---

### 第三层：Calibration Examples

不断吸收真实失败案例。

例如：

```text
Case 001:
Trivial parameter tuning was incorrectly logged.

Correct decision:
No log.

Case 002:
Camera module extraction was not logged.

Correct decision:
Architecture + Engineering Log.
```

这是“判例法”。

最后形成：

```text
Documentation System
│
├── Principles
│
├── Protocol
└── Examples
```

我认为这比做一个越来越长的单体 prompt 稳定得多。

---

## 甚至可以给 AI 本身建立一个“错误日志”

不要混进项目的 `ENGINEERING_LOG`。

例如：

```text
.ai/
├── documentation-manager.md
└── documentation-calibration.md
```

后者专门记录：

```text
## Failure 001

Observed:
Generated an Engineering Log for a trivial threshold change.

Expected:
No documentation update.

Root cause:
Significance threshold was interpreted too loosely.

Rule update:
Routine parameter changes are not log-worthy unless they represent
a broader architectural, reliability, reproducibility, or performance decision.
```

下一次出现类似问题就不需要重新想。

你实际上是在：

\[
\boxed{\text{调试 AI 的行为}}
\]

和调试程序很类似：

```text
程序：
输入
↓
代码
↓
错误输出
↓
定位错误模块
↓
修代码
```

文档 Agent：

```text
工程事件
↓
Prompt rules
↓
错误文档
↓
定位错误规则
↓
修 Prompt
```

---

# 一定要区分 4 种错误

以后你看到一个坏输出，先问：

### 1. Perception error

AI **理解错了实际代码变化**。

例如它以为：

> `Camera` 已经完全接管摄像头。

但实际上 `main.py` 仍然直接调用 `VideoCapture`。

这种不能改写作规则。

应该改：

> 执行文档判断前必须检查 diff / 当前代码。

---

### 2. Classification error

AI知道发生了什么，但**错误判断它属于什么文档**。

例如：

> Camera 模块拆分只更新 README，没有更新 architecture。

应该改 impact matrix / classification rules。

---

### 3. Policy error

它分类也正确，但**判断要不要记录的标准错了**。

例如把普通 typo 写入 Engineering Log。

修改 filtering policy。

---

### 4. Generation error

它知道：

> 应该写简短 Engineering Log。

但生成了 800 字废话。

这是输出格式/长度约束问题。

例如增加：

```text
Default Engineering Log target: 50–150 words.
Do not repeat code changes already obvious from Git.
```

这四个概念非常好用：

\[
\boxed{
\text{理解错误}
\neq
\text{分类错误}
\neq
\text{策略错误}
\neq
\text{生成错误}
}
\]

定位对了才容易修。

---

## 修改 prompt 时也最好遵守“最小 patch”

比如发现日志太长。

不要：

> 重写整个 Engineering Documentation Manager。

只改：

```text
# Engineering Log Format

Default length:
- Minor design decision: 3–5 lines
- Normal engineering event: <=150 words
- Major architectural event: expand only when required
```

这和你写程序时：

> 一个 bug 尽量做一个局部修复

是同一思路。

否则每次 prompt 大改，都可能：

```text
修好了 A
↓
破坏 B
↓
再修 B
↓
破坏 C
```

---

# 最后还可以建立一个很简单的回归测试集

这个非常值得做。

准备大概 10 个固定案例：

```text
Case 1:
Fix typo
Expected: no docs

Case 2:
Change threshold
Expected: no docs

Case 3:
Extract Camera module
Expected:
architecture + engineering log

Case 4:
Add README installation command
Expected:
README

Case 5:
Complete Stage 2
Expected:
GOALS

Case 6:
Change Camera.read() API
Expected:
architecture + log

Case 7:
Old architecture changed
Expected:
do not rewrite old log
```

每次大幅修改文档 Agent 的 prompt 后，让它重新判断这 10 个例子。

如果：

```text
旧版：9/10
新版：10/10
```

说明改进。

如果：

```text
旧版：9/10
新版：7/10
```

说明虽然修了当前问题，却引入了回归。

这实际上已经是：

\[
\boxed{\text{Prompt regression testing}}
\]

也是你以后做各种 Agent 很值得养成的习惯。

---

所以后续的完整调试流程可以定成：

```text
发现文档异常
      ↓
保存具体输入 + 错误输出
      ↓
定义 Expected behavior
      ↓
判断错误类型
 ┌────┼────┬────┐
 ↓    ↓    ↓    ↓
理解  分类  策略  生成
错误  错误  错误  错误
      ↓
定位对应 prompt section
      ↓
做最小规则修改
      ↓
增加一个 calibration case
      ↓
运行旧案例回归测试
      ↓
通过后保留修改
```

我建议尤其保留：

\[
\boxed{
Observed
\rightarrow
Expected
\rightarrow
Root\ Cause
\rightarrow
Rule\ Change
\rightarrow
Regression\ Test
}
\]

这五项。以后不只是你的工程文档 AI，代码 Agent、Research Agent、Critic Agent 都可以用同样的方法迭代提示词。