# 🧠 arxiv-daily-mcp

> **Un servidor MCP que convierte tu flujo de arXiv en herramientas naturales.**
> Buscá papers en 🇰🇷 coreano, 🇨🇳 chino, 🇯🇵 japonés o 🇺🇸 inglés — y guardá todo en tu bóveda Markdown local.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/arxiv-daily-mcp)](https://github.com/nerin81-netizen/arxiv-daily-mcp/stargazers)

**🌍 Leé en tu idioma:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · **Español** · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 Inicio rápido](#-inicio-rápido) · [🛠 Herramientas](#-herramientas-4) · [🎬 Demo](#-demo) · [🆚 vs otros MCPs de arXiv](#-vs-otros-mcps-de-arxiv) · [🏗 Arquitectura](#-arquitectura) · [🧪 Desarrollo](#-desarrollo) · [🌐 Multilingüe](#-keywords-multilingües)

---

## ✨ ¿Qué es esto?

Un servidor MCP simple que convierte un flujo útil de arXiv en herramientas que tu LLM puede usar. La idea central:

> **Tomá ese script CLI que usás todos los días y envolvélo en MCP para poder invocarlo con lenguaje natural desde cualquier cliente MCP.**

Si alguna vez te encontraste tipeando la misma consulta `curl` / `python` / `arxiv` en la terminal todas las mañanas — esto es cómo se ve como herramienta MCP.

## 🛠 Herramientas (4)

| Herramienta | Args | Descripción | Ejemplo |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | Papers de hoy (AI / negocios) | "Dame los papers de hoy" |
| `search_papers` | `keyword`, `max_results` | Búsqueda **multilingüe** | "papers sobre agentes" / "agent 论文" / "エージェント 論文" |
| `save_paper_note` | `arxiv_id`, `note` | Guardá un paper en tu bóveda `.md` | "Guardá este paper" |
| `list_my_notes` | `keyword`, `limit` | Buscá / listá tus notas guardadas | "Mostrame mis notas" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (todo)
- Devuelve: lista de papers de hoy en formato Markdown card-news

### `search_papers(keyword, max_results=5)`

- `keyword`: cualquier texto en 🇰🇷 coreano, 🇨🇳 chino, 🇯🇵 japonés o 🇺🇸 inglés
- Traduce automáticamente keywords no-inglesas a inglés para buscar en arXiv
- Devuelve: Markdown card-news con nota de traducción

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` o URL completa `https://arxiv.org/abs/2507.01234`
- `note`: tu comentario (opcional)
- Devuelve: path del archivo guardado (default: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: filtro por título / contenido (opcional)
- Devuelve: lista de archivos de notas guardadas recientemente

## 🚀 Inicio rápido

### Instalación

```bash
pip install arxiv-daily-mcp
```

O desde el source:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Registrá en tu cliente MCP

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

`.cursor/mcp.json` o settings del workspace:

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### Cualquier cliente compatible con MCP

Este servidor usa el transporte estándar `stdio` y expone 4 herramientas via JSON-RPC — funciona con cualquier cliente que siga el [spec MCP](https://modelcontextprotocol.io).

## 🎬 Demo

### Keyword en coreano (auto-traducida a inglés)

```text
👤 Buscá papers sobre agentes

🤖 Claude:
🔍 Resultados para 'agentes' — 🇰🇷 coreano → inglés: 'agent' (5 papers)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### Keyword en chino

```text
👤 智能体 相关论文

🤖 Claude:
🔍 Resultados para '智能体' — 🇨🇳 chino → inglés: 'agent' (5 papers)
```

### Keyword en japonés

```text
👤 エージェント 論文を探して

🤖 Claude:
🔍 Resultados para 'エージェント' — 🇯🇵 japonés → inglés: 'agent' (5 papers)
```

### Guardar + recuperar

```text
👤 Guardá el primer paper — seguridad multi-agente interesante

🤖 Claude:
✅ Guardado: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 Mostrame mis notas

🤖 Claude:
📚 Mis notas de arXiv (1)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 vs otros MCPs de arXiv

GitHub tiene **466+ repositorios MCP de arXiv** (al 2026-07-05). El más popular, `blazickjp/arxiv-mcp-server`, es excelente — pero hecho para otra audiencia.

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (este) |
|---|---|---|---|
| **Keywords en idiomas** | 🇺🇸 Solo inglés | 🇺🇸 Solo inglés | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 idiomas** |
| **Formato de salida** | JSON / datos raw | Solo texto | **Markdown card-news** (emoji + bullets) |
| **Archivo de notas** | ❌ | ❌ | ✅ **Bóveda `.md` local** |
| **Búsqueda de notas** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **Estado** | Mantenido | Mantenido | Activo (v0.1.0) |

### Tres razones por las que puede coexistir

1. **Audiencia de idiomas diferente.** El líder de 2,933 estrellas es solo inglés. Este servidor está diseñado para investigadores no-angloparlantes primero.
2. **Forma de salida diferente.** El líder devuelve JSON raw / tablas de datos. Este servidor devuelve **Markdown card-news** — legible directamente en cualquier UI de chat.
3. **Flujo de trabajo diferente.** El líder es buscar-y-leer. Este servidor incluye **archivado**: guardá un paper en tu bóveda Markdown local con una oración, después `list_my_notes` para recuperarlo.

## 🌐 Keywords multilingües

El diccionario de traducción viene con el paquete — **sin API call, sin latencia, sin rate limit**.

| Idioma | Keywords |
|---|---|
| 🇰🇷 Coreano (28) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 Chino (23) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 Japonés (24) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**Algoritmo de detección:**

1. Si el input contiene Hangul (가-힣) → búsqueda en coreano
2. Sino contiene Kana (ぁ-ヿ) → búsqueda en japonés
3. Sino contiene ideogramas CJK (一-鿿) → búsqueda en chino
4. Sino → inglés (pasado sin cambios)

Keywords desconocidas se pasan tal cual — así que un partial match todavía busca directamente en arXiv.

## 🏗 Arquitectura

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

**Decisiones de diseño clave:**

- **stdio transport** — estándar MCP
- **FastMCP** — SDK oficial de Python de Anthropic
- **solo urllib** — cero dependencias HTTP externas (funciona en cualquier entorno Python mínimo)
- **Diccionario de traducción in-process** — sin LLM call, sin rate limit, sin latencia por keyword
- **MEMO_DIR configurable** — seteá via env var para setups Docker / multi-usuario

## 🧪 Desarrollo

```bash
# Instalá dependencias de dev
pip install -e ".[dev]"

# Corré MCP Inspector (UI de browser)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# Testeá stdio JSON-RPC directamente
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### Unit test de la capa de traducción

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 Roadmap

- [x] v0.1.0 — 4 herramientas, stdio, multilingüe (75 keywords)
- [ ] v0.2.0 — herramienta `weekly_summary` (digest del viernes)
- [ ] v0.3.0 — Más categorías (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — Release en PyPI
- [ ] v1.0.0 — Transporte HTTP (acceso remoto)
- [ ] v1.1.0 — Más idiomas (español, francés, alemán, hindi)
- [ ] v2.0.0 — Plugins de formato de notas (Notion, Apple Notes, Bear)

## 🤝 Contribuir

Issues y PRs bienvenidos. Particularmente útil:

- 🌏 Más keywords de idiomas (especialmente en cs.RO, q-fin, stat.ML)
- 📂 Nuevas categorías de papers
- 📝 Opciones de formato de notas (Notion API, Apple Notes, Bear)
- 🐛 Bug reports con pasos de reproducción

## 📜 Licencia

MIT

## 🙏 Créditos

- Construido con [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Datos de papers de [arXiv.org](https://arxiv.org) (API abierta)
- Inspirado en la colección de referencia [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

---

> 🌟 Si este MCP te ahorró unos minutos en tu flujo de investigación, considerá darle una estrella al repo — ayuda a otros a encontrarlo.
