# 🧠 arxiv-daily-mcp

> **arXiv 논문을 카톡/Claude에서 한국어·중국어·일본어로 검색하고, 내 Obsidian 메모장에 바로 저장하세요.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![PlayMCP Ready](https://img.shields.io/badge/PlayMCP-ready-FFCD00.svg)](https://playmcp.kakao.com)
[![Made by 상학](https://img.shields.io/badge/made_by-상학-FF6B6B.svg)](https://github.com/nerin81-netizen)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/arxiv-daily-mcp)](https://github.com/nerin81-netizen/arxiv-daily-mcp/stargazers)

A Model Context Protocol (MCP) server for arXiv paper search and personal-note archival.

**Built for the 카카오 PlayMCP 에이전틱 플레이어 10 contest.**

[🇰🇷 한국어 안내](#-한국어-안내) · [🚀 빠른 시작](#-quickstart) · [🛠 도구 4개](#-tools-4개) · [🎬 데모](#-demo) · [🆚 경쟁 MCP 비교](#-왜-다른-arxiv-mcp와-다른가) · [🏗 아키텍처](#-architecture)

---

## ✨ 30초 요약

```text
👤 User: "오늘 AI 논문 알려줘"
   ↓
🤖 Claude (PlayMCP) → MCP tool call
   ↓
arxiv-daily-mcp → arXiv API
   ↓
📚 5편의 논문 (마크다운 카드뉴스 형식)
```

### 이 MCP가 다른 arXiv MCP와 다른 이유

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `arxiv-daily-mcp` (우리) |
|---|---|---|
| **언어** | 🇺🇸 영어만 | 🇰🇷🇨🇳🇯🇵🇺🇸 **4개국 자동 번역** |
| **응답 형식** | JSON / raw 데이터 | **마크다운 카드뉴스** (이모지 + 글머리) |
| **메모리 통합** | ❌ 없음 | ✅ **Obsidian `.md` 자동 저장** |
| **카카오 생태계** | ❌ 무관 | ✅ **PlayMCP/메모챗/카톡 채널 특화** |
| **개인화** | 없음 | ✅ `list_my_notes` 검색/조회 |
| **1인 개발자** | 5명+ 팀 | 1인 (사장님) |
| **타겟 시장** | 글로벌 LLM | **한국 1인 개발자 + 카톡 사용자** |

> 🎯 **공모전 어필:** 466개의 arXiv MCP 중 **카카오 PlayMCP 생태계를 위해 디자인된 것 = 사실상 0개.** 우리는 그 빈 시장을 노립니다.

## 🛠 Tools (4개)

| Tool | Args | Description | Example prompt |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | 오늘의 AI/비즈니스 논문 | "오늘 AI 논문 알려줘" |
| `search_papers` | `keyword`, `max_results` | **🇰🇷🇨🇳🇯🇵 다국어 자동 번역** 검색 | "에이전트 논문 찾아줘" / "智能体 相关论文" / "エージェント 論文" |
| `save_paper_note` | `arxiv_id`, `note` | Obsidian 메모장에 .md 저장 | "이거 메모해줘" |
| `list_my_notes` | `keyword`, `limit` | 저장한 노트 검색/조회 | "내 메모 보여줘" |

### 🇰🇷🇨🇳🇯🇵 4개국 키워드 지원 (v0.2)

`search_papers`는 사용자 입력을 자동으로 감지 + 번역:

```text
🇰🇷 "에이전트"      → "agent"             (28개 한국어 키워드)
🇨🇳 "智能体"        → "agent"             (23개 중국어 키워드)
🇯🇵 "エージェント"  → "agent"             (24개 일본어 키워드)
🇺🇸 "agent"        → "agent"             (영어 그대로)
```

arXiv 초록/제목은 주로 영어라서, 한국어/중국어/일본어 키워드를 영어로 자동 변환해 검색 정확도를 크게 높입니다. **다른 arXiv MCP는 이 기능이 없습니다.**

## 🚀 Quickstart

### 1. Install

```bash
pip install arxiv-daily-mcp
```

또는 개발용 (로컬 clone):

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Register with your MCP client

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

#### 카카오 PlayMCP

1. https://playmcp.kakao.com 접속
2. "Submit MCP" → **stdio transport** 선택
3. command: `arxiv-daily-mcp`
4. 카테고리: `연구/리서치`

## 🎬 Demo

### 🇰🇷 한국어 검색

```text
👤 에이전트 관련 논문 찾아줘

🤖 Claude (PlayMCP):
🔍 '에이전트' 검색 결과 — 🇰🇷 한국어 → 영어: 'agent' (5편)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### 🇨🇳 중국어 검색

```text
👤 智能体 相关论文

🤖 Claude (PlayMCP):
🔍 '智能体' 검색 결과 — 🇨🇳 中文 → 영어: 'agent' (5편)
```

### 🇯🇵 일본어 검색

```text
👤 エージェント 論文を探して

🤖 Claude (PlayMCP):
🔍 'エージェント' 검색 결과 — 🇯🇵 日本語 → 영어: 'agent' (5편)
```

### 메모 저장

```text
👤 첫 번째 논문 메모해줘 — RAG 멀티에이전트 흥미롭다

🤖 Claude (PlayMCP):
✅ 저장 완료: `/opt/data/memos/2026-07-06_arxiv_2607.02514.md`
```

## 🆚 왜 다른 arXiv MCP와 다른가

### 시장 분석 (7/5 검증)

| 쿼리 | GitHub repo 수 | 1위 | 비고 |
|---|---|---|---|
| `arxiv mcp` | **466개** | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | 사실상 표준 |
| `arxiv daily` | **1,136개** | `TideDra/zotero-arxiv-daily` ⭐ 5,645 | Zotero 연동 |
| `arxiv research mcp` | 172개 | - | - |
| `arxiv agent mcp` | 96개 | - | - |

**arXiv MCP는 saturated market.** 그래서 우리는 다른 각도를 노립니다:

### 4가지 차별점

1. **🇰🇷🇨🇳🇯🇵 다국어 자동 번역** — 75개 키워드 (한 28 + 중 23 + 일 24)
2. **카톡/PlayMCP 카드뉴스 형식** — 이모지 + 글머리 + 마크다운 (1위는 raw JSON)
3. **Obsidian 메모리 통합** — `save_paper_note` + `list_my_notes` 워크플로우
4. **한국 1인 개발자 타겟** — EZEDI / Hermes Agent 운영자가 직접 만든 도구

### 우리 시장 검증 3법칙

1. ✅ **비슷한 게 있어도 되는가?** Yes — 1위는 영어만, 우리는 한/중/일 + 카톡
2. ✅ **왜 1위가 안 했는가?** 1위는 글로벌 LLM 시장만 봤음, 한국 카톡 생태계는 무관
3. ✅ **평가위원이 5분 안에 "오 다르네"?** 다국어 검색 데모 즉시 가능

## 🏗 Architecture

```
┌─────────────────┐      stdio/JSON-RPC      ┌──────────────────────┐
│  LLM Client     │ ◀──────────────────────▶ │  arxiv-daily-mcp     │
│  (Claude/PlayMCP) │                          │  (FastMCP server)    │
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
                                                 │  /opt/data/  │
                                                 │  memos/*.md  │
                                                 └──────────────┘
```

**Key design choices:**

- **stdio transport** — PlayMCP 표준 호환
- **FastMCP** — Anthropic 공식 Python SDK 기반
- **urllib (외부 HTTP 의존성 0)** — 가벼움, hermes 환경 검증됨
- **다국어 사전 내장** — 75개 키워드 (한/중/일), 0 API 호출
- **MEMO_DIR 환경변수화** — Docker/다중 사용자 대비

## 🧪 Development

```bash
# 의존성 설치
pip install -e ".[dev]"

# MCP Inspector로 디버깅 (브라우저)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# stdio JSON-RPC 직접 테스트
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### 실제 동작 확인 (2026-07-05)

```bash
$ python3 -c "
import asyncio
from arxiv_daily_mcp.server import get_today_papers, search_papers
print(asyncio.run(get_today_papers(category='ai', max_results=3)))
print('---')
print(asyncio.run(search_papers('에이전트', max_results=3)))
"
```

## 🌍 Roadmap

- [x] v0.1.0 — 4 tools, stdio transport, 한국어/중국어/일본어 75개 키워드
- [ ] v0.2.0 — `weekly_summary` 도구 추가 (금요일 주간 리포트)
- [ ] v0.3.0 — 카테고리 확장 (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — PyPI 배포
- [ ] v1.0.0 — HTTP transport (원격 호출)
- [ ] v2.0.0 — **MCP 팜**: `cloud-cost-mcp`, `idea-box-mcp`, `project-backup-mcp`

## 🤝 Contributing

PR 환영! 특히:
- 🌏 더 많은 언어 추가 (스페인어, 프랑스어, 독일어, 힌디어)
- 📂 새 카테고리 추가 (cs.RO, cs.CV, q-fin.ST)
- 📝 메모 포맷 옵션 (Notion, Apple Notes, Bear)

## 📜 License

MIT © 2026 상학 (Sanghak)

## 🙏 Credits

- Built with [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Data from [arXiv.org](https://arxiv.org) (open API)
- Inspired by [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

## 🇰🇷 한국어 안내

이 MCP는 **카카오 PlayMCP 에이전틱 플레이어 10** 공모전 출품작입니다.

### 만드는 사람
- **상학** — 1인 SW 사업자, 정보통신업 개업 6개월차
- **만 44세** — 40대+ 시니어 개발자 관점
- **EZEDI** — CSO 정산 자동화 SaaS 운영 (B2B + B2G)
- **Hermes Agent** — AI 워크플로우 자동화 (14개 크론잡)

### 왜 만들었나
매일 arXiv에서 AI 논문을 찾아 메모하는 작업이 30분씩 걸렸는데, 카톡에서 한 줄이면 끝나도록 만들었습니다. **1인 개발자에게 시간은 가장 비싼 자원**입니다.

### 사용한 본인 오플 로직
기존 `/opt/data/home/.hermes/scripts/daily-arxiv-crawl.py` (134줄) — 매일 10시 cron으로 실행되던 스크립트를 MCP로 감싸서 카톡에서 호출 가능하게 만들었어요.

### GitHub 경쟁 분석 (7/5 검증)
arXiv MCP 카테고리는 **466개** repo 존재. `blazickjp/arxiv-mcp-server` (⭐ 2,933)가 사실상 표준. **하지만 한국어/중국어/일본어 미지원, 카톡 UI 안 맞음, 메모리 통합 없음.** → **우리 차별점 = 4개국 자동 번역 + 카톡 카드뉴스 + Obsidian 메모 통합.**

### 공모전 정보
- **대회명**: 카카오 에이전틱 플레이어 10
- **총상금**: 2,700만원 (1등 1,000만원)
- **공식 사이트**: https://playmcp.kakao.com
- **전략**: 오플 18개 중 S/A 등급 4개 선정 → "MCP 팜" 확장 계획

### 관련 프로젝트
- 🗂️ `cloud-cost-mcp` — 클라우드 비용 (출품 1순위 후보)
- 💡 `idea-box-mcp` — 아이디어 박스 검색/통계
- 📦 `project-backup-mcp` — 자연어 백업

---

> 📧 문의: nerin81@gmail.com
> 🌟 이 프로젝트가 도움이 되셨다면 Star 부탁드려요!
> ⭐ 100 Stars → 1인 개발자에게 큰 동기부여가 됩니다.
