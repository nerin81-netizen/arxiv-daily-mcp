# 🧠 arxiv-daily-mcp

> **एक MCP सर्वर जो तुम्हारे arXiv वर्कफ्लो को नैचुरल टूल्स में बदल देता है।**
> arXiv पर 🇰🇷 कोरियन, 🇨🇳 चाइनीज़, 🇯🇵 जापानीज़ या 🇺🇸 इंग्लिश में सर्च करो — और सब कुछ अपने लोकल Markdown vault में सेव करो।

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/arxiv-daily-mcp)](https://github.com/nerin81-netizen/arxiv-daily-mcp/stargazers)

**🌍 अपनी भाषा में पढ़ें:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · **हिन्दी** · [العربية](README.ar.md)

[🚀 क्विक स्टार्ट](#-क्विक-स्टार्ट) · [🛠 टूल्स](#-टूल्स-4) · [🎬 डेमो](#-डेमो) · [🆚 दूसरे arXiv MCPs से अलग](#-दूसरे-arxiv-mcps-से-अलग) · [🏗 आर्किटेक्चर](#-आर्किटेक्चर) · [🧪 डेवलपमेंट](#-डेवलपमेंट) · [🌐 मल्टीलींगुअल](#-मल्टीलींगुअल-कीवर्ड्स)

---

## ✨ ये क्या है?

एक सिंपल MCP सर्वर जो एक useful arXiv workflow को LLM-callable टूल्स में बदल देता है। कोर आइडिया:

> **वो CLI स्क्रिप्ट जो तुम रोज़ चलाते हो, उसे MCP में wrap करो ताकि किसी भी MCP क्लाइंट से नैचुरल लैंग्वेज में invoke कर सको।**

अगर तुमने कभी हर सुबह terminal में same `curl` / `python` / `arxiv` query टाइप की है — ये MCP tool के रूप में वैसा ही दिखता है।

## 🛠 टूल्स (4)

| टूल | आर्ग्स | डिस्क्रिप्शन | उदाहरण |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | आज के AI / business पेपर्स | "आज के papers दिखाओ" |
| `search_papers` | `keyword`, `max_results` | **मल्टीलींगुअल** keyword सर्च | "agents पर papers" / "agent 论文" / "エージェント 論文" |
| `save_paper_note` | `arxiv_id`, `note` | `.md` vault में paper सेव करो | "ये paper सेव करो" |
| `list_my_notes` | `keyword`, `limit` | सेव किए गए notes सर्च/लिस्ट करो | "मेरे notes दिखाओ" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (सब)
- रिटर्न: आज के papers की Markdown card-news लिस्ट

### `search_papers(keyword, max_results=5)`

- `keyword`: कोई भी text 🇰🇷 कोरियन, 🇨🇳 चाइनीज़, 🇯🇵 जापानीज़ या 🇺🇸 इंग्लिश में
- Non-English keywords को automatically English में translate करके arXiv पर सर्च करता है
- रिटर्न: translation note के साथ Markdown card-news

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` या full URL `https://arxiv.org/abs/2507.01234`
- `note`: तुम्हारा commentary (optional)
- रिटर्न: सेव किए गए file का path (default: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: title / content से filter (optional)
- रिटर्न: हाल ही में सेव किए गए note files की लिस्ट

## 🚀 क्विक स्टार्ट

### इंस्टॉलेशन

```bash
pip install arxiv-daily-mcp
```

या source से:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### अपने MCP क्लाइंट में रजिस्टर करो

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

`.cursor/mcp.json` या workspace settings:

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### कोई भी MCP-compatible क्लाइंट

ये सर्वर standard `stdio` transport use करता है और 4 tools को JSON-RPC के through expose करता है — ये किसी भी client के साथ काम करता है जो [MCP spec](https://modelcontextprotocol.io) को follow करता है।

## 🎬 डेमो

### कोरियन keyword (English में auto-translate)

```text
👤 agents पर papers ढूंढो

🤖 Claude:
🔍 'agents' के results — 🇰🇷 कोरियन → English: 'agent' (5 papers)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### चाइनीज़ keyword

```text
👤 智能体 相关论文

🤖 Claude:
🔍 '智能体' के results — 🇨🇳 चाइनीज़ → English: 'agent' (5 papers)
```

### जापानीज़ keyword

```text
👤 エージェント 論文を探して

🤖 Claude:
🔍 'エージェント' के results — 🇯🇵 जापानीज़ → English: 'agent' (5 papers)
```

### सेव + retrieve

```text
👤 पहला paper सेव करो — multi-agent security interesting है

🤖 Claude:
✅ सेव हो गया: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 मेरे notes दिखाओ

🤖 Claude:
📚 मेरे arXiv notes (1)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 दूसरे arXiv MCPs से अलग

GitHub पर **466+ arXiv MCP repositories** हैं (2026-07-05 तक)। सबसे popular, `blazickjp/arxiv-mcp-server`, excellent है — लेकिन different audience के लिए बना है।

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (ये) |
|---|---|---|---|
| **Keyword languages** | 🇺🇸 सिर्फ English | 🇺🇸 सिर्फ English | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 languages** |
| **Output format** | JSON / raw data | सिर्फ text | **Markdown card-news** (emoji + bullets) |
| **Note archive** | ❌ | ❌ | ✅ **Local `.md` vault** |
| **Note search** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **Status** | Maintained | Maintained | Active (v0.1.0) |

### तीन reasons जो coexist कर सकते हैं

1. **Different language audience.** 2,933-star leader सिर्फ English-only है। ये सर्वर non-English researchers के लिए पहले designed है।
2. **Different output shape.** Leader raw JSON / data tables return करता है। ये सर्वर **card-news Markdown** return करता है — जो किसी भी chat UI में directly readable है।
3. **Different workflow.** Leader search-and-read है। ये सर्वर **archival** include करता है: एक sentence में paper को अपने local Markdown vault में सेव करो, फिर बाद में `list_my_notes` से recall करो।

## 🌐 मल्टीलींगुअल कीवर्ड्स

Translation dictionary package के साथ आता है — **no API call, no latency, no rate limit**।

| Language | Keywords |
|---|---|
| 🇰🇷 कोरियन (28) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 चाइनीज़ (23) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 जापानीज़ (24) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**Detection algorithm:**

1. अगर input में Hangul (가-힣) है → कोरियन lookup
2. नहीं तो अगर Kana (ぁ-ヿ) है → जापानीज़ lookup
3. नहीं तो अगर CJK ideographs (一-鿿) हैं → चाइनीज़ lookup
4. नहीं तो → English (जैसा है वैसा pass)

Unknown keywords जैसी हैं वैसी ही pass होती हैं — तो partial match अभी भी arXiv पर directly सर्च करता है।

## 🏗 आर्किटेक्चर

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
- **FastMCP** — Anthropic का official Python SDK
- **sirf urllib** — zero external HTTP dependencies (किसी भी minimal Python environment में काम करता है)
- **In-process translation dictionary** — no LLM call, no rate limit, no per-keyword latency
- **Configurable MEMO_DIR** — Docker / multi-user setups के लिए env var से set करो

## 🧪 डेवलपमेंट

```bash
# dev dependencies install करो
pip install -e ".[dev]"

# MCP Inspector चलाओ (browser UI)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# stdio JSON-RPC directly test करो
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### Translation layer का unit test

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 रोडमैप

- [x] v0.1.0 — 4 tools, stdio, multilingual (75 keywords)
- [ ] v0.2.0 — `weekly_summary` tool (Friday digest)
- [ ] v0.3.0 — More categories (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — PyPI release
- [ ] v1.0.0 — HTTP transport (remote access)
- [ ] v1.1.0 — More languages (Spanish, French, German, Hindi)
- [ ] v2.0.0 — Note format plugins (Notion, Apple Notes, Bear)

## 🤝 कंट्रीब्यूट करो

Issues और PRs welcome हैं। विशेष रूप से useful:

- 🌏 More language keywords (खासकर cs.RO, q-fin, stat.ML में)
- 📂 New paper categories
- 📝 Note format options (Notion API, Apple Notes, Bear)
- 🐛 Bug reports with reproduction steps

## 📜 लाइसेंस

MIT

## 🙏 क्रेडिट्स

- [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) के साथ built
- Paper data [arXiv.org](https://arxiv.org) से (open API)
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) reference collection से inspired

---

> 🌟 अगर इस MCP ने तुम्हारे research workflow में कुछ minutes बचाए, तो repo को star करने के बारे में सोचो — ये दूसरों को इसे ढूंढने में help करता है।
