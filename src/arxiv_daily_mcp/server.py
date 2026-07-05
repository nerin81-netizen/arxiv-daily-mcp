"""arXiv Daily MCP Server

Provides tools to:
- get_today_papers: 오늘 올라온 AI/비즈니스 논문 목록
- search_papers: 키워드로 arXiv 논문 검색
- save_paper_note: 논문을 내 Obsidian 메모장에 저장

Transport: stdio (Anthropic MCP 표준)
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── 상수 ──────────────────────────────────────────────
NS = {"a": "http://www.w3.org/2005/Atom"}
KST = timezone(timedelta(hours=9))
ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "arxiv-daily-mcp/0.1.0 (https://github.com/nerin81-netizen/arxiv-daily-mcp)"
MEMO_DIR = Path("/opt/data/memos")

CATEGORIES = {
    "ai": "cat:cs.AI OR cat:cs.CL OR cat:cs.LG",
    "business": "cat:econ.GN OR cat:q-fin",
    "all": "cat:cs.AI OR cat:cs.CL OR cat:cs.LG OR cat:cs.CV OR cat:cs.RO OR cat:econ.GN",
}

# ── 다국어 키워드 매핑 (5/1 v0.2 추가) ────────────────
# arXiv 초록/제목은 주로 영어. 사용자 입력을 영어로 번역해 검색 정확도↑
LANG_KEYWORDS = {
    # 한국어 → 영어
    "에이전트": "agent",
    "인공지능": "artificial intelligence",
    "머신러닝": "machine learning",
    "딥러닝": "deep learning",
    "자연어처리": "natural language processing",
    "컴퓨터비전": "computer vision",
    "강화학습": "reinforcement learning",
    "생성형": "generative",
    "변압기": "transformer",
    "확산모델": "diffusion model",
    "검색증강": "retrieval-augmented",
    "멀티모달": "multimodal",
    "로보틱스": "robotics",
    "추천시스템": "recommender system",
    "그래프신경망": "graph neural network",
    "파운데이션모델": "foundation model",
    "거대언어모델": "large language model",
    "프롬프트": "prompt",
    "미세조정": "fine-tuning",
    "정렬": "alignment",
    "안전성": "safety",
    "환각": "hallucination",
    "추론": "reasoning",
    "계획": "planning",
    "도구사용": "tool use",
    "메모리": "memory",
    "체인": "chain",
    # 중국어 → 영어 (간체/번체 모두)
    "智能体": "agent",
    "人工智能": "artificial intelligence",
    "机器学习": "machine learning",
    "深度学习": "deep learning",
    "自然语言处理": "natural language processing",
    "计算机视觉": "computer vision",
    "强化学习": "reinforcement learning",
    "生成式": "generative",
    "变压器": "transformer",
    "扩散模型": "diffusion model",
    "多模态": "multimodal",
    "机器人": "robotics",
    "推荐系统": "recommender system",
    "图神经网络": "graph neural network",
    "基础模型": "foundation model",
    "大语言模型": "large language model",
    "提示": "prompt",
    "微调": "fine-tuning",
    "对齐": "alignment",
    "推理": "reasoning",
    "工具使用": "tool use",
    "链": "chain",
    "代理": "agent",
    # 일본어 → 영어
    "エージェント": "agent",
    "人工知能": "artificial intelligence",
    "機械学習": "machine learning",
    "深層学習": "deep learning",
    "自然言語処理": "natural language processing",
    "コンピュータビジョン": "computer vision",
    "強化学習": "reinforcement learning",
    "生成": "generative",
    "変圧器": "transformer",
    "拡散モデル": "diffusion model",
    "検索拡張": "retrieval-augmented",
    "マルチモーダル": "multimodal",
    "ロボット": "robotics",
    "推薦システム": "recommender system",
    "グラフニューラルネットワーク": "graph neural network",
    "基盤モデル": "foundation model",
    "大規模言語モデル": "large language model",
    "プロンプト": "prompt",
    "微調整": "fine-tuning",
    "アライメント": "alignment",
    "推論": "reasoning",
    "計画": "planning",
    "ツール使用": "tool use",
    "記憶": "memory",
    "幻覚": "hallucination",
}


def _translate_keyword(keyword: str) -> tuple[str, str]:
    """사용자 키워드를 영어로 번역 + 매칭된 언어 반환.

    Returns:
        (translated_keyword, detected_lang) — lang는 "ko"|"zh"|"ja"|"en"
    """
    kw = keyword.strip()
    kw_lower = kw.lower()

    # 한국어 감지 (한글 유니코드 범위)
    has_korean = any("\uac00" <= c <= "\ud7a3" for c in kw)
    # 중국어 간체/번체 (CJK)
    has_cjk = any("\u4e00" <= c <= "\u9fff" for c in kw)
    # 일본어 가나
    has_kana = any("\u3040" <= c <= "\u30ff" for c in kw)

    if has_korean:
        return LANG_KEYWORDS.get(kw, kw), "ko"
    if has_kana:
        return LANG_KEYWORDS.get(kw, kw), "ja"
    if has_cjk:
        # 중국어: 한자 단독으로는 ko/ja와 구분 어려움 → ko/ja 매칭 안 되면 zh
        for cjk_kw, en in LANG_KEYWORDS.items():
            if cjk_kw in kw and any("\u4e00" <= c <= "\u9fff" for c in cjk_kw):
                return en, "zh"
        return kw, "zh"
    return kw, "en"

# ── FastMCP 서버 ─────────────────────────────────────
mcp = FastMCP(
    "arxiv-daily",
    instructions=(
        "arXiv 논문 검색/조회 MCP 서버. "
        "카톡에서 '오늘 AI 논문 알려줘', 'agent 관련 논문 찾아줘', '이거 메모해줘' 같은 자연어 요청에 응답합니다."
    ),
)


# ── 내부 헬퍼 ─────────────────────────────────────────
def _fetch_arxiv(query: str, max_results: int = 5) -> list[dict]:
    """arXiv API 호출 → 파싱된 paper dict 리스트 반환."""
    params = {
        "search_query": query,
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            root = ET.parse(resp).getroot()
    except Exception as e:
        raise RuntimeError(f"arXiv API 호출 실패: {e}") from e

    papers: list[dict] = []
    for entry in root.findall("a:entry", NS):
        # 철회된 논문 제외
        summary_el = entry.find("a:summary", NS)
        summary = (summary_el.text or "").strip()
        if "withdrawn" in summary.lower() or "retracted" in summary.lower():
            continue

        title = (entry.find("a:title", NS).text or "").strip().replace("\n", " ")
        arxiv_id_el = entry.find("a:id", NS)
        arxiv_id = (arxiv_id_el.text or "").strip().split("/abs/")[-1]
        published = (entry.find("a:published", NS).text or "")[:10]
        authors = ", ".join(
            (a.find("a:name", NS).text or "")
            for a in entry.findall("a:author", NS)[:3]
        )
        categories = ", ".join(
            c.get("term", "") for c in entry.findall("a:category", NS)
        )

        papers.append(
            {
                "id": arxiv_id,
                "title": title,
                "authors": authors,
                "published": published,
                "categories": categories,
                "summary": summary[:300],
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}",
            }
        )
    return papers


def _format_paper(p: dict, index: int | None = None) -> str:
    """paper dict → 마크다운 한 줄."""
    prefix = f"{index}. " if index is not None else "📄 "
    return (
        f"{prefix}**{p['title'][:90]}**\n"
        f"   👥 {p['authors'][:60]}\n"
        f"   📅 {p['published']} | 🏷️ {p['categories'][:50]}\n"
        f"   🔗 {p['url']}"
    )


# ── MCP Tools ─────────────────────────────────────────
@mcp.tool()
async def get_today_papers(category: str = "ai", max_results: int = 5) -> str:
    """오늘 arXiv에 올라온 AI/ML 또는 비즈니스 분야 논문을 반환합니다.

    Args:
        category: "ai" (cs.AI+cs.CL+cs.LG) | "business" (econ.GN+q-fin) | "all" (전체)
        max_results: 최대 결과 수 (기본 5, 최대 20)

    Returns:
        마크다운 형식 논문 목록
    """
    category = category.lower()
    if category not in CATEGORIES:
        return (
            f"❌ 알 수 없는 category: {category}\n"
            f"   가능한 값: {', '.join(CATEGORIES.keys())}"
        )
    max_results = max(1, min(max_results, 20))

    try:
        papers = _fetch_arxiv(CATEGORIES[category], max_results)
    except RuntimeError as e:
        return f"❌ {e}"

    if not papers:
        return f"📭 오늘({category}) 새 논문이 없습니다."

    today = datetime.now(KST).strftime("%Y-%m-%d")
    header = f"📚 **오늘의 arXiv 논문 — {today}** ({category})\n총 {len(papers)}편\n"
    body = "\n\n".join(_format_paper(p, i + 1) for i, p in enumerate(papers))
    return f"{header}\n{body}"


@mcp.tool()
async def search_papers(keyword: str, max_results: int = 5) -> str:
    """키워드로 arXiv 논문을 검색합니다 (한/영/중/일 4개 언어 자동 번역).

    Args:
        keyword: 검색 키워드 (예: 'agent', '에이전트', '智能体', 'エージェント')
        max_results: 최대 결과 수 (기본 5, 최대 20)

    Returns:
        마크다운 형식 검색 결과
    """
    if not keyword.strip():
        return "❌ keyword는 비어 있을 수 없습니다."
    max_results = max(1, min(max_results, 20))

    # 다국어 → 영어 번역
    translated, lang = _translate_keyword(keyword)
    lang_label = {"ko": "🇰🇷 한국어", "zh": "🇨🇳 中文", "ja": "🇯🇵 日本語", "en": "🇺🇸 English"}.get(lang, lang)

    try:
        papers = _fetch_arxiv(f"all:{translated}", max_results)
    except RuntimeError as e:
        return f"❌ {e}"

    if not papers:
        # 번역된 키워드 + 원본 모두 표시
        if translated != keyword:
            return f"🔍 '{keyword}' (번역: '{translated}') 검색 결과가 없습니다."
        return f"🔍 '{keyword}' 검색 결과가 없습니다."

    if translated != keyword:
        header = f"🔍 **'{keyword}' 검색 결과** — {lang_label} → 영어: '{translated}' ({len(papers)}편)"
    else:
        header = f"🔍 **'{keyword}' 검색 결과** — {len(papers)}편"
    body = "\n\n".join(_format_paper(p, i + 1) for i, p in enumerate(papers))
    return f"{header}\n\n{body}"


@mcp.tool()
async def save_paper_note(arxiv_id: str, note: str = "") -> str:
    """arXiv 논문을 내 Obsidian 메모장에 저장합니다 (마크다운 .md 파일).

    Args:
        arxiv_id: arXiv ID (예: '2507.01234' 또는 'https://arxiv.org/abs/2507.01234')
        note: 내 코멘트 (선택)

    Returns:
        저장된 파일 경로
    """
    # URL → ID 정규화
    arxiv_id = arxiv_id.strip()
    if "arxiv.org/abs/" in arxiv_id:
        arxiv_id = arxiv_id.split("/abs/")[-1].split("v")[0]
    arxiv_id = arxiv_id.replace("/", "_")

    try:
        # 메타데이터 조회
        papers = _fetch_arxiv(f"id:{arxiv_id}", 1)
    except RuntimeError as e:
        return f"❌ {e}"

    if not papers:
        return f"❌ arXiv ID '{arxiv_id}'를 찾을 수 없습니다."

    p = papers[0]
    today = datetime.now(KST).strftime("%Y-%m-%d")
    MEMO_DIR.mkdir(parents=True, exist_ok=True)
    out = MEMO_DIR / f"{today}_arxiv_{arxiv_id}.md"

    content = f"""# {p['title']}

📅 저장: {today}
🔗 arXiv: {p['url']}
📄 PDF: {p['pdf']}

## 메타데이터
- **ID**: {arxiv_id}
- **발행일**: {p['published']}
- **저자**: {p['authors']}
- **카테고리**: {p['categories']}

## 초록
{p['summary']}

## 내 코멘트
{note or '_(작성 예정)_'}

---
*Saved by arxiv-daily-mcp*
"""
    out.write_text(content, encoding="utf-8")
    return f"✅ 저장 완료: `{out}`"


@mcp.tool()
async def list_my_notes(keyword: str = "", limit: int = 10) -> str:
    """내가 저장한 arXiv 노트 목록을 조회합니다.

    Args:
        keyword: 제목/내용 필터링 (선택)
        limit: 최대 결과 수 (기본 10)

    Returns:
        저장된 노트 파일 목록
    """
    if not MEMO_DIR.exists():
        return "📭 저장된 노트가 없습니다."

    files = sorted(MEMO_DIR.glob("*_arxiv_*.md"), reverse=True)
    if keyword:
        kw = keyword.lower()
        files = [f for f in files if kw in f.read_text(encoding="utf-8", errors="ignore").lower()]

    if not files:
        return f"🔍 '{keyword}' 매칭 노트 없음"

    files = files[:limit]
    lines = [f"📚 **내 arXiv 노트** ({len(files)}개)\n"]
    for f in files:
        # 첫 줄(제목) 추출
        first_line = f.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0].lstrip("# ").strip()
        lines.append(f"  · `{f.name}` — {first_line[:60]}")
    return "\n".join(lines)


# ── 진입점 ───────────────────────────────────────────
def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
