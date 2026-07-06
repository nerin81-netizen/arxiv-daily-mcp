# 🧠 arxiv-daily-mcp

> **A Model Context Protocol (MCP) server that wraps an arXiv CLI workflow.**
> Search arXiv in 🇰🇷 Korean, 🇨🇳 Chinese, 🇯🇵 Japanese, or 🇺🇸 English — and save findings to a local Markdown vault.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/arxiv-daily-mcp)](https://github.com/nerin81-netizen/arxiv-daily-mcp/stargazers)

**🌍 Read in your language:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 Quickstart](#-quickstart) · [🛠 Tools](#-tools-4) · [🎬 Demo](#-demo) · [🆚 vs other arXiv MCPs](#-how-it-differs-from-existing-arxiv-mcps) · [🏗 Architecture](#-architecture) · [🧪 Development](#-development) · [🌐 Multilingual](#-multilingual-keywords)

---

## ✨ What this is

A simple MCP server that exposes a useful arXiv workflow as LLM-callable tools. The core idea:

> **Take a CLI script that you already run every day, and wrap it in MCP so you can invoke it with natural language from any MCP client.**

If you've ever found yourself typing the same `curl` / `python` / `arxiv` query into a terminal every morning — this is what that looks like as an MCP tool.

## 🛠 Tools (4)

| Tool | Args | Description | Example prompt |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | Today's AI / business papers | "오늘 AI 논문 알려줘" |
| `search_papers` | `keyword`, `max_results` | **Multilingual** keyword search | "에이전트 관련 논문" / "智能体 论文" / "エージェント 論文" |
| `save_paper_note` | `arxiv_id`, `note` | Save a paper to local `.md` vault | "이거 메모해줘" |
| `list_my_notes` | `keyword`, `limit` | Search / list saved notes | "내 메모 보여줘" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (전체)
- Returns: Markdown card-news list of today's submissions

### `search_papers(keyword, max_results=5)`

- `keyword`: any text in 🇰🇷 Korean, 🇨🇳 Chinese, 🇯🇵 Japanese, or 🇺🇸 English
- Auto-translates non-English keywords to English for arXiv search
- Returns: Markdown card-news of results, with translation note

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` or full URL `https://arxiv.org/abs/2507.01234`
- `note`: your commentary (optional)
- Returns: path to saved file (default: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: filter by title / content (optional)
- Returns: list of recently saved note files

## 🚀 Quickstart

### Install

```bash
pip install arxiv-daily-mcp
```

Or from source:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Register with your MCP client

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

`.cursor/mcp.json` or workspace settings:

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### Any MCP-compatible client

This server uses the standard `stdio` transport and exposes 4 tools via JSON-RPC — it works with any client that follows the [MCP spec](https://modelcontextprotocol.io).

## 🎬 Demo

### Korean keyword (auto-translated to English)

```text
👤 에이전트 관련 논문 찾아줘

🤖 Claude:
🔍 '에이전트' 검색 결과 — 🇰🇷 한국어 → 영어: 'agent' (5편)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### Chinese keyword

```text
👤 智能体 相关论文

🤖 Claude:
🔍 '智能体' 검색 결과 — 🇨🇳 中文 → 영어: 'agent' (5편)
```

### Japanese keyword

```text
👤 エージェント 論文を探して

🤖 Claude:
🔍 'エージェント' 검색 결과 — 🇯🇵 日本語 → 영어: 'agent' (5편)
```

### Save + retrieve

```text
👤 첫 번째 논문 메모해줘 — 멀티에이전트 보안 흥미롭다

🤖 Claude:
✅ 저장 완료: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 내 메모 보여줘

🤖 Claude:
📚 내 arXiv 노트 (1개)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 How it differs from existing arXiv MCPs

GitHub has **466+ arXiv MCP repositories** (as of 2026-07-05). The most popular, `blazickjp/arxiv-mcp-server`, is excellent — but built for a different audience.

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (this) |
|---|---|---|---|
| **Keyword languages** | 🇺🇸 English only | 🇺🇸 English only | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 languages** |
| **Output format** | JSON / raw data | Text only | **Markdown card-news** (emoji + bullets) |
| **Note archive** | ❌ | ❌ | ✅ **Local `.md` vault** |
| **Note search** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **Status** | Maintained | Maintained | Active (v0.1.0) |

### Three reasons it can coexist

1. **Different language audience.** The 2,933-star leader is English-only. This server is designed for non-English researchers first.
2. **Different output shape.** The leader returns raw JSON / data tables. This server returns **card-news Markdown** — readable directly inside any chat UI.
3. **Different workflow.** The leader is search-and-read. This server includes **archival**: save a paper to your local Markdown vault with one sentence, then `list_my_notes` to recall it later.

## 🌐 Multilingual keywords

The translation dictionary ships with the package — **no API call, no latency, no rate limit**.

| Language | Keywords |
|---|---|
| 🇰🇷 Korean (28) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 Chinese (23) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 Japanese (24) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**Detection algorithm:**

1. If the input contains Hangul (가-힣) → Korean lookup
2. Else if it contains Kana (ぁ-ヿ) → Japanese lookup
3. Else if it contains CJK ideographs (一-鿿) → Chinese lookup
4. Else → English (passed through unchanged)

Unknown keywords are passed through as-is — so a partial match still searches arXiv directly.

## 🏗 Architecture

```
┌─────────────────┐      stdio/JSON-RPC      ┌──────────────────────┐
│  LLM Client     │ ◀──────────────────────▶ │  arxiv-daily-mcp     │
│  (Claude/Cursor) │                          │  (FastMCP server)    │
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
                                                 │  *.md vault  │
                                                 └──────────────┘
```

**Key design choices:**

- **stdio transport** — MCP standard
- **FastMCP** — Anthropic's official Python SDK
- **urllib only** — zero external HTTP dependencies (works in any minimal Python environment)
- **In-process translation dictionary** — no LLM call, no rate limit, no per-keyword latency
- **Configurable MEMO_DIR** — set via env var for Docker / multi-user setups

## 🧪 Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run MCP Inspector (browser UI)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# Test stdio JSON-RPC directly
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### Unit test the translation layer

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 Roadmap

- [x] v0.1.0 — 4 tools, stdio, multilingual (75 keywords)
- [ ] v0.2.0 — `weekly_summary` tool (Friday digest)
- [ ] v0.3.0 — More categories (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — PyPI release
- [ ] v1.0.0 — HTTP transport (remote access)
- [ ] v1.1.0 — More languages (Spanish, French, German, Hindi)
- [ ] v2.0.0 — Note format plugins (Notion, Apple Notes, Bear)

## 🤝 Contributing

Issues and PRs welcome. Particularly useful:

- 🌏 More language keywords (especially in cs.RO, q-fin, stat.ML)
- 📂 New paper categories
- 📝 Note format options (Notion API, Apple Notes, Bear)
- 🐛 Bug reports with reproduction steps

## 📜 License

MIT

## 🙏 Credits

- Built with [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Paper data from [arXiv.org](https://arxiv.org) (open API)
- Inspired by the [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) reference collection

---

> 🌟 If this MCP saved you a few minutes of research workflow, consider starring the repo — it helps others find it.
