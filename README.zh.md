# 🧠 arxiv-daily-mcp

> **用韩语、中文、日语或英语搜索 arXiv,并将论文保存到本地 Markdown 笔记库。**
> 一个将现有 CLI 脚本封装为 MCP 协议的开源工具。

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)

**🌍 选择语言:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 快速开始](#-快速开始) · [🛠 4 个工具](#-4-个工具) · [🎬 演示](#-演示) · [🆚 与其他 arXiv MCP 的区别](#-与其他-arxiv-mcp-的区别) · [🌐 多语言关键词](#-多语言关键词) · [🏗 架构](#-架构)

---

## ✨ 这是什么

一个将 CLI 脚本封装为 MCP 服务器的开源工具,让你可以从任何 LLM 客户端(Claude、Cursor、Cline 等)用自然语言调用它。

核心理念:

> **把你每天都在运行的 CLI 脚本封装进 MCP,这样你就可以用自然语言从任何 MCP 客户端调用它。**

如果你每天早上都要在终端里输入相同的 `curl` / `python` / `arxiv` 命令——这就是它作为 MCP 工具的样子。

## 🛠 4 个工具

| 工具 | 参数 | 说明 | 调用示例 |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | 今日 AI / 商科论文 | "今日 AI 论文" |
| `search_papers` | `keyword`, `max_results` | **多语言**关键词搜索 | "智能体 相关论文" |
| `save_paper_note` | `arxiv_id`, `note` | 保存到本地 `.md` 笔记库 | "把这个记下来" |
| `list_my_notes` | `keyword`, `limit` | 搜索 / 列出已保存笔记 | "显示我的笔记" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (全部)
- 返回: 今日新论文的 Markdown 卡片格式列表

### `search_papers(keyword, max_results=5)`

- `keyword`: 支持 🇰🇷 韩语、🇨🇳 中文、🇯🇵 日语、🇺🇸 英语
- 非英语关键词自动翻译为英语后用于 arXiv 搜索
- 返回: 包含翻译说明的 Markdown 卡片

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` 或完整 URL
- `note`: 你的注释(可选)
- 返回: 保存的文件路径(默认: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: 按标题/内容筛选(可选)
- 返回: 最近保存的笔记文件列表

## 🚀 快速开始

### 安装

```bash
pip install arxiv-daily-mcp
```

或从源码安装:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 注册到 MCP 客户端

#### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### Cursor / Cline

`.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### 其他 MCP 兼容客户端

使用标准 `stdio` 传输和 JSON-RPC 协议,适用于所有遵循 [MCP 规范](https://modelcontextprotocol.io) 的客户端。

**🌍 选择语言:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

## 🎬 演示

### 韩语关键词(自动翻译为英语)

```text
👤 에이전트 관련 논문 찾아줘  (查找智能体相关论文)

🤖 Claude:
🔍 '에이전트' 搜索结果 — 🇰🇷 한국어 → 英语: 'agent' (5 篇)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### 中文关键词

```text
👤 智能体 相关论文

🤖 Claude:
🔍 '智能体' 搜索结果 — 🇨🇳 中文 → 英语: 'agent' (5 篇)
```

### 日语关键词

```text
👤 エージェント 論文を探して  (查找智能体相关论文)

🤖 Claude:
🔍 'エージェント' 搜索结果 — 🇯🇵 日本語 → 英语: 'agent' (5 篇)
```

### 保存 + 检索

```text
👤 把第一篇记下来 — 多智能体安全很有意思

🤖 Claude:
✅ 已保存: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 显示我的笔记

🤖 Claude:
📚 我的 arXiv 笔记 (1 篇)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 与其他 arXiv MCP 的区别

GitHub 上已有 **466+ 个 arXiv MCP 仓库**(截至 2026-07-05)。最受欢迎的 `blazickjp/arxiv-mcp-server` (⭐ 2,933) 也很优秀,但它的目标用户群不同。

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (本项目) |
|---|---|---|---|
| **关键词语言** | 🇺🇸 仅英语 | 🇺🇸 仅英语 | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 种语言** |
| **输出格式** | JSON / 原始数据 | 仅文本 | **Markdown 卡片**(emoji + 列表) |
| **笔记归档** | ❌ | ❌ | ✅ **本地 `.md` 笔记库** |
| **笔记搜索** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **状态** | 活跃维护中 | 活跃维护中 | v0.1.0 (首发) |

### 共存的三个原因

1. **目标语言用户不同。** 2,933 星的领先者仅支持英语。本服务器将非英语研究者作为首要服务对象。
2. **输出形式不同。** 领先者返回原始 JSON / 数据表。本服务器返回**卡片式 Markdown**——在任意聊天界面中都能直接阅读。
3. **工作流不同。** 领先者是搜索-阅读工具。本服务器包含**归档**功能:用一句话把论文保存到本地 Markdown 笔记库,稍后用 `list_my_notes` 调出。

## 🌐 多语言关键词

翻译词典随包发布——**无 API 调用、无延迟、无速率限制**。

| 语言 | 关键词 |
|---|---|
| 🇰🇷 韩语 (28 个) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 中文 (23 个) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 日语 (24 个) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**检测算法:**

1. 若输入包含韩文字符(가-힣)→ 查询韩语词典
2. 否则若包含假名(ぁ-ヿ)→ 查询日语词典
3. 否则若包含汉字(一-鿿)→ 查询中文词典
4. 其余 → 英语(原样传递)

词典中未收录的关键词将原样传递给 arXiv,所以部分匹配时仍可直接搜索。

## 🏗 架构

```
┌─────────────────┐      stdio/JSON-RPC      ┌──────────────────────┐
│  LLM 客户端     │ ◀──────────────────────▶ │  arxiv-daily-mcp     │
│ (Claude/Cursor) │                          │  (FastMCP 服务器)    │
└─────────────────┘                          └──────────┬───────────┘
                                                        │ urllib
                                                        ▼
                                                 ┌──────────────┐
                                                 │  arXiv API   │
                                                 │  export.arxiv│
                                                 └──────────────┘
                                                        │
                                                        ▼ (save_paper_note)
                                                 ┌──────────────┐
                                                 │  ./memos/    │
                                                 │  *.md 笔记库 │
                                                 └──────────────┘
```

**关键设计决策:**

- **stdio 传输** — MCP 标准
- **FastMCP** — Anthropic 官方 Python SDK
- **仅使用 urllib** — 零外部 HTTP 依赖(可在任何极简 Python 环境中运行)
- **进程内翻译词典** — 无 LLM 调用,无速率限制,无逐词延迟
- **可配置 MEMO_DIR** — 通过环境变量配置,支持 Docker / 多用户

## 🧪 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行 MCP Inspector(浏览器 UI)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# 直接测试 stdio JSON-RPC
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### 翻译层单元测试

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 路线图

- [x] v0.1.0 — 4 个工具,stdio,多语言(75 个关键词)
- [ ] v0.2.0 — `weekly_summary` 工具(每周五摘要)
- [ ] v0.3.0 — 更多类别(cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — PyPI 发布
- [ ] v1.0.0 — HTTP 传输(远程访问)
- [ ] v1.1.0 — 更多语言(西班牙语、法语、德语、印地语)
- [ ] v2.0.0 — 笔记格式插件(Notion、Apple Notes、Bear)

## 🤝 贡献

欢迎提交 Issue 和 PR。特别欢迎以下贡献:

- 🌏 更多语言关键词(尤其是 cs.RO、q-fin、stat.ML)
- 📂 新的论文类别
- 📝 笔记格式选项(Notion API、Apple Notes、Bear)
- 🐛 带复现步骤的 bug 报告

## 📜 许可证

MIT

## 🙏 致谢

- 基于 [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 构建
- 论文数据来源:[arXiv.org](https://arxiv.org)(开放 API)
- 灵感来自 [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 参考合集

---

> 🌟 如果这个 MCP 帮你节省了几分钟研究时间,请给仓库点个 star——能帮助更多人发现它。
