# 🧠 arxiv-daily-mcp

> **arXiv를 한국어, 중국어, 일본어로 검색하고, 로컬 Markdown 보관함에 저장하세요.**
> 기존 CLI 스크립트를 MCP로 감싼 오픈소스.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![한국어](https://img.shields.io/badge/README-한국어-red)](README.ko.md)
[![中文](https://img.shields.io/badge/README-中文-yellow)](README.zh.md)
[![日本語](https://img.shields.io/badge/README-日本語-green)](README.ja.md)

[🚀 빠른 시작](#-빠른-시작) · [🛠 도구 4개](#-도구-4개) · [🎬 데모](#-데모) · [🆚 다른 arXiv MCP와 비교](#-다른-arxiv-mcp와-차이점) · [🌐 다국어 키워드](#-다국어-키워드) · [🏗 아키텍처](#-아키텍처)

---

## ✨ 이게 뭔가요

CLI 스크립트를 MCP 서버로 감싸서, LLM 클라이언트(Claude, Cursor, Cline 등)에서 자연어로 호출할 수 있게 한 것입니다.

핵심 아이디어:

> **매일 실행하던 CLI 스크립트를 MCP로 감싸서, 자연어로 호출하세요.**

매일 아침 같은 `curl` / `python` 명령을 터미널에 치고 있었다면, 그게 MCP 도구로 어떻게 보이는지 보여줍니다.

## 🛠 도구 4개

| 도구 | 인자 | 설명 | 사용 예시 |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | 오늘의 AI/비즈니스 논문 | "오늘 AI 논문 알려줘" |
| `search_papers` | `keyword`, `max_results` | **다국어** 키워드 검색 | "에이전트 관련 논문" |
| `save_paper_note` | `arxiv_id`, `note` | 로컬 `.md` 보관함에 저장 | "이거 메모해줘" |
| `list_my_notes` | `keyword`, `limit` | 저장한 노트 검색/조회 | "내 메모 보여줘" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (전체)
- 반환: 오늘 제출된 논문의 Markdown 카드뉴스

### `search_papers(keyword, max_results=5)`

- `keyword`: 🇰🇷 한국어, 🇨🇳 중국어, 🇯🇵 일본어, 🇺🇸 영어 모두 가능
- 비영어 키워드는 자동으로 영어로 번역되어 arXiv 검색
- 반환: 번역 정보가 포함된 Markdown 카드뉴스

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` 또는 전체 URL
- `note`: 내 코멘트 (선택)
- 반환: 저장된 파일 경로 (기본: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: 제목/내용 필터 (선택)
- 반환: 최근 저장된 노트 파일 목록

## 🚀 빠른 시작

### 설치

```bash
pip install arxiv-daily-mcp
```

또는 소스에서:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### MCP 클라이언트에 등록

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

#### 다른 MCP 호환 클라이언트

표준 `stdio` transport와 JSON-RPC를 사용하므로 [MCP 스펙](https://modelcontextprotocol.io)을 따르는 모든 클라이언트에서 작동합니다.

## 🎬 데모

### 한국어 키워드 (영어로 자동 번역)

```text
👤 에이전트 관련 논문 찾아줘

🤖 Claude:
🔍 '에이전트' 검색 결과 — 🇰🇷 한국어 → 영어: 'agent' (5편)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### 중국어 키워드

```text
👤 智能体 相关论文

🤖 Claude:
🔍 '智能体' 검색 결과 — 🇨🇳 中文 → 영어: 'agent' (5편)
```

### 일본어 키워드

```text
👤 エージェント 論文を探して

🤖 Claude:
🔍 'エージェント' 검색 결과 — 🇯🇵 日本語 → 영어: 'agent' (5편)
```

### 저장 + 조회

```text
👤 첫 번째 논문 메모해줘 — 멀티에이전트 보안 흥미롭다

🤖 Claude:
✅ 저장 완료: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 내 메모 보여줘

🤖 Claude:
📚 내 arXiv 노트 (1개)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 다른 arXiv MCP와 차이점

GitHub에는 466개 이상의 arXiv MCP 저장소가 있습니다 (2026-07-05 기준). 가장 유명한 `blazickjp/arxiv-mcp-server` (⭐ 2,933)도 훌륭하지만, 다른 청중을 대상으로 만들어졌습니다.

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (이 프로젝트) |
|---|---|---|---|
| **키워드 언어** | 🇺🇸 영어만 | 🇺🇸 영어만 | 🇰🇷🇨🇳🇯🇵🇺🇸 **4개 언어** |
| **출력 형식** | JSON / raw 데이터 | 텍스트만 | **Markdown 카드뉴스** (이모지 + 글머리) |
| **노트 보관** | ❌ | ❌ | ✅ **로컬 `.md` 보관함** |
| **노트 검색** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **상태** | 활발히 유지보수 | 활발히 유지보수 | v0.1.0 (출시) |

### 공존할 수 있는 세 가지 이유

1. **다른 언어 청중.** 1위 프로젝트는 영어 전용입니다. 이 서버는 비영어권 연구자를 1순위로 설계했습니다.
2. **다른 출력 형태.** 1위는 raw JSON을 반환합니다. 이 서버는 **카드뉴스 Markdown**을 반환하여, 어떤 채팅 UI에서도 바로 읽을 수 있습니다.
3. **다른 워크플로우.** 1위는 검색-읽기 도구입니다. 이 서버는 **보관** 기능이 포함되어 있어, 한 문장으로 논문을 로컬 Markdown 보관함에 저장하고 나중에 `list_my_notes`로 다시 찾을 수 있습니다.

## 🌐 다국어 키워드

번역 사전은 패키지에 포함되어 있어 — **API 호출 없음, 지연 없음, 요청 제한 없음**.

| 언어 | 키워드 |
|---|---|
| 🇰🇷 한국어 (28개) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 中文 (23개) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 日本語 (24개) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**감지 알고리즘:**

1. 입력에 한글(가-힣)이 포함되면 → 한국어 사전 조회
2. 아니고 가나(ぁ-ヿ)가 포함되면 → 일본어 사전 조회
3. 아니고 한자(一-鿿)가 포함되면 → 중국어 사전 조회
4. 그 외 → 영어 (그대로 전달)

사전에 없는 키워드는 그대로 전달되므로, 일부만 매칭되어도 arXiv를 직접 검색합니다.

## 🏗 아키텍처

```
┌─────────────────┐      stdio/JSON-RPC      ┌──────────────────────┐
│  LLM 클라이언트  │ ◀──────────────────────▶ │  arxiv-daily-mcp     │
│ (Claude/Cursor) │                          │  (FastMCP 서버)      │
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
                                                 │  *.md 보관함 │
                                                 └──────────────┘
```

**핵심 설계 선택:**

- **stdio transport** — MCP 표준
- **FastMCP** — Anthropic 공식 Python SDK
- **urllib only** — 외부 HTTP 의존성 0개 (최소 Python 환경에서 작동)
- **사전 내장 번역** — LLM 호출 없음, 요청 제한 없음, 키워드별 지연 없음
- **MEMO_DIR 환경변수화** — Docker / 다중 사용자 대응

## 🧪 개발

```bash
# 개발 의존성 설치
pip install -e ".[dev]"

# MCP Inspector 실행 (브라우저 UI)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# stdio JSON-RPC 직접 테스트
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### 번역 레이어 단위 테스트

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 로드맵

- [x] v0.1.0 — 도구 4개, stdio, 다국어 (75개 키워드)
- [ ] v0.2.0 — `weekly_summary` 도구 (금요일 주간 다이제스트)
- [ ] v0.3.0 — 카테고리 확장 (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — PyPI 배포
- [ ] v1.0.0 — HTTP transport (원격 접근)
- [ ] v1.1.0 — 더 많은 언어 (스페인어, 프랑스어, 독일어, 힌디)
- [ ] v2.0.0 — 노트 포맷 플러그인 (Notion, Apple Notes, Bear)

## 🤝 기여

이슈와 PR 환영. 특히 다음이 유용합니다:

- 🌏 더 많은 언어 키워드 (특히 cs.RO, q-fin, stat.ML)
- 📂 새로운 논문 카테고리
- 📝 노트 포맷 옵션 (Notion API, Apple Notes, Bear)
- 🐛 재현 단계가 있는 버그 리포트

## 📜 라이선스

MIT

## 🙏 크레딧

- [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)로 제작
- 논문 데이터 출처: [arXiv.org](https://arxiv.org) (오픈 API)
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 레퍼런스 컬렉션에서 영감

---

> 🌟 이 MCP가 연구 워크플로우에서 몇 분을 절약해줬다면, 저장소에 별표를 눌러주세요 — 다른 사람들이 찾는 데 도움이 됩니다.
