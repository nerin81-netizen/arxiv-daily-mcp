# 🧠 arxiv-daily-mcp

> **سيرفر MCP بيحول شغلك على arXiv لأدوات طبيعية.**
> دور على papers بـ 🇰🇷 كوري، 🇨🇳 صيني، 🇯🇵 ياباني أو 🇺🇸 إنجليزي — واحفظ كل حاجة في vault الـ Markdown المحلي عندك.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/arxiv-daily-mcp)](https://github.com/nerin81-netizen/arxiv-daily-mcp/stargazers)

**🌍 اقرأ بلغتك:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · **العربية**

[🚀 البداية السريعة](#-البداية-السريعة) · [🛠 الأدوات](#-الأدوات-4) · [🎬 العرض](#-العرض) · [🆚 مقارنة مع MCPs تانية](#-مقارنة-مع-mcps-تانية) · [🏗 البنية](#-البنية) · [🧪 التطوير](#-التطوير) · [🌐 متعدد اللغات](#-keywords-متعددة-اللغات)

---

## ✨ إيه ده؟

سيرفر MCP بسيط بيحول workflow مفيد على arXiv لأدوات يقدر الـ LLM بتاعك يستخدمها. الفكرة الأساسية:

> **خد الـ CLI script اللي بتشتغله كل يوم، ولفه في MCP عشان تقدر تستدعيه باللغة الطبيعية من أي MCP client.**

لو يومياً كتبت نفس الـ `curl` / `python` / `arxiv` query في الـ terminal كل الصبح — ده شكله كأداة MCP.

## 🛠 الأدوات (4)

| الأداة | المعاملات | الوصف | مثال |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | Papers النهاردة (AI / business) | "وريني papers النهاردة" |
| `search_papers` | `keyword`, `max_results` | بحث **متعدد اللغات** | "papers عن agents" / "agent 论文" / "エージェント 論文" |
| `save_paper_note` | `arxiv_id`, `note` | احفظ paper في vault الـ `.md` بتاعك | "احفظ الـ paper ده" |
| `list_my_notes` | `keyword`, `limit` | دور / اعرض.notes المحفوظة | "وريني notes بتاعتي" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (كل حاجة)
- بيرجع: ليسة papers النهاردة بصيغة Markdown card-news

### `search_papers(keyword, max_results=5)`

- `keyword`: أي text بـ 🇰🇷 كوري، 🇨🇳 صيني، 🇯🇵 ياباني أو 🇺🇸 إنجليزي
- بيترجم keywords مش إنجليزي لإنجليزي تلقائياً عشان يبحث على arXiv
- بيرجع: Markdown card-news مع ملاحظة الترجمة

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` أو الـ URL كامل `https://arxiv.org/abs/2507.01234`
- `note`: تعليقك (اختياري)
- بيرجع: path الملف المحفوظ (افتراضي: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: فلتر بالعنوان / المحتوى (اختياري)
- بيرجع: ليسة ملفات notes محفوظة مؤخراً

## 🚀 البداية السريعة

### التثبيت

```bash
pip install arxiv-daily-mcp
```

أو من الـ source:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### سجّل في MCP client بتاعك

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

`.cursor/mcp.json` أو إعدادات الـ workspace:

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### أي MCP-compatible client

السيرفر ده بيستخدم stdio transport القياسي وبيعرض 4 أدوات عن طريق JSON-RPC — بيشتغل مع أي client بيتبع [MCP spec](https://modelcontextprotocol.io).

## 🎬 العرض

### Keyword كوري (بيترجم لإنجليزي تلقائياً)

```text
👤 دورلي على papers عن agents

🤖 Claude:
🔍 نتائج 'agents' — 🇰🇷 كوري → إنجليزي: 'agent' (5 papers)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### Keyword صيني

```text
👤 智能体 相关论文

🤖 Claude:
🔍 نتائج '智能体' — 🇨🇳 صيني → إنجليزي: 'agent' (5 papers)
```

### Keyword ياباني

```text
👤 エージェント 論文を探して

🤖 Claude:
🔍 نتائج 'エージェント' — 🇯🇵 ياباني → إنجليزي: 'agent' (5 papers)
```

### حفظ + استرجاع

```text
👤 احفظ أول paper — multi-agent security مهم

🤖 Claude:
✅ محفوظ: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 وريني notes بتاعتي

🤖 Claude:
📚 الـ arXiv notes بتاعتي (1)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 مقارنة مع MCPs تانية

GitHub فيه **466+ repositories MCP لـ arXiv** (حتى 2026-07-05). الأشهر، `blazickjp/arxiv-mcp-server`، ممتاز — لكن مصمم لجمهور تاني.

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (ده) |
|---|---|---|---|
| **لغات الـ keywords** | 🇺🇸 إنجليزي بس | 🇺🇸 إنجليزي بس | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 لغات** |
| **صيغة المخرج** | JSON / بيانات خام | نص بس | **Markdown card-news** (emoji + bullets) |
| **أرشيف الـ notes** | ❌ | ❌ | ✅ **Vault `.md` محلي** |
| **بحث الـ notes** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **الحالة** | بيتم صيانته | بيتم صيانته | نشط (v0.1.0) |

### 3 أسباب ليه ممكن يتعايشوا

1. **جمهور لغات مختلف.** الـ leader بـ 2,933 نجمة إنجليزي بس. السيرفر ده مصمم للباحثين مش الناطقين بالإنجليزي الأول.
2. **شكل مخرج مختلف.** الـ leader بيرجع JSON خام / جداول بيانات. السيرفر ده بيرجع **Markdown card-news** — يقرا مباشرة في أي chat UI.
3. **Workflow مختلف.** الـ leader هو ابحث-واقرأ. السيرفر ده فيه **أرشفة**: احفظ paper في vault الـ Markdown المحلي بتاعك بجملة واحدة، وبعدين `list_my_notes` عشان ترجعله.

## 🌐 Keywords متعددة اللغات

قاموس الترجمة بيجي مع الـ package — **مفيش API call، مفيش تأخير، مفيش rate limit**.

| اللغة | Keywords |
|---|---|
| 🇰🇷 كوري (28) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 صيني (23) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 ياباني (24) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**خوارزمية الكشف:**

1. لو الـ input فيه Hangul (가-힣) → بحث كوري
2. ولا فيه Kana (ぁ-ヿ) → بحث ياباني
3. ولا فيه CJK ideographs (一-鿿) → بحث صيني
4. ولا → إنجليزي (بيعدي زي ما هو)

الـ keywords مش معروفه بتعدي زي ما هي — فالـ partial match لسه بيدور على arXiv مباشرة.

## 🏗 البنية

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

**اختيارات التصميم الرئيسية:**

- **stdio transport** — قياسي MCP
- **FastMCP** — الـ Python SDK الرسمي من Anthropic
- **urllib بس** — صفر اعتماديات HTTP خارجية (بيشتغل في أي بيئة Python بسيطة)
- **قاموس ترجمة داخل العملية** — مفيش LLM call، مفيش rate limit، مفيش تأخير لكل keyword
- **MEMO_DIR قابل للتخصيص** — اتعمل بـ env var لـ Docker / multi-user setups

## 🧪 التطوير

```bash
# ثبّت dev dependencies
pip install -e ".[dev]"

# شغل MCP Inspector (browser UI)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# اختبر stdio JSON-RPC مباشرة
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### Unit test لطبقة الترجمة

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 خارطة الطريق

- [x] v0.1.0 — 4 أدوات، stdio، متعدد اللغات (75 keywords)
- [ ] v0.2.0 — أداة `weekly_summary` (هضمة الجمعة)
- [ ] v0.3.0 — تصنيفات أكتر (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — إصدار PyPI
- [ ] v1.0.0 — HTTP transport (وصول عن بُعد)
- [ ] v1.1.0 — لغات أكتر (Spanish, French, German, Hindi)
- [ ] v2.0.0 — plugins صيغة الـ notes (Notion, Apple Notes, Bear)

## 🤝 المساهمة

Issues و PRs مرحب بيها. المفيد خصوصاً:

- 🌏 keywords لغات أكتر (خصوصاً في cs.RO, q-fin, stat.ML)
- 📂 تصنيفات papers جديدة
- 📝 خيارات صيغة الـ notes (Notion API, Apple Notes, Bear)
- 🐛 Bug reports مع خطوات إعادة الإنتاج

## 📜 الترخيص

MIT

## 🙏 الفضل

- مبني بـ [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- بيانات الـ papers من [arXiv.org](https://arxiv.org) (open API)
- مستوحى من مجموعة المرجعية [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

---

> 🌟 لو الـ MCP ده وفرلك كام دقايق في workflow البحث بتاعك، فكر إنك تعمل نجمة للـ repo — ده بيساعد ناس تانية تلاقيه.
