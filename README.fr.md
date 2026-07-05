# 🧠 arxiv-daily-mcp

> **Un serveur MCP qui transforme ton workflow arXiv en outils naturels.**
> Cherche des papers en 🇰🇷 coréen, 🇨🇳 chinois, 🇯🇵 japonais ou 🇺🇸 anglais — et sauvegarde tout dans ta voûte Markdown locale.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/arxiv-daily-mcp)](https://github.com/nerin81-netizen/arxiv-daily-mcp/stargazers)

**🌍 Lis dans ta langue :** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · **Français** · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 Démarrage rapide](#-démarrage-rapide) · [🛠 Outils](#-outils-4) · [🎬 Démo](#-démo) · [🆚 vs autres MCPs arXiv](#-vs-autres-mcps-arxiv) · [🏗 Architecture](#-architecture) · [🧪 Développement](#-développement) · [🌐 Multilingue](#-mots-clés-multilingues)

---

## ✨ C'est quoi ça ?

Un serveur MCP simple qui transforme un workflow arXiv utile en outils que ton LLM peut utiliser. L'idée centrale :

> **Prends ce script CLI que tu lances tous les matins et emballe-le dans MCP pour pouvoir l'invoquer en langage naturel depuis n'importe quel client MCP.**

Si t'as déjà tapé la même requête `curl` / `python` / `arxiv` dans ton terminal tous les matins — voilà à quoi ça ressemble comme outil MCP.

## 🛠 Outils (4)

| Outil | Args | Description | Exemple |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | Papers du jour (AI / business) | "Donne-moi les papers d'aujourd'hui" |
| `search_papers` | `keyword`, `max_results` | Recherche **multilingue** | "papers sur les agents" / "agent 论文" / "エージェント 論文" |
| `save_paper_note` | `arxiv_id`, `note` | Sauvegarde un paper dans ta voûte `.md` | "Sauvegarde ce paper" |
| `list_my_notes` | `keyword`, `limit` | Cherche / liste tes notes sauvegardées | "Montre-moi mes notes" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (tout)
- Renvoie : liste des papers du jour en format Markdown card-news

### `search_papers(keyword, max_results=5)`

- `keyword`: n'importe quel texte en 🇰🇷 coréen, 🇨🇳 chinois, 🇯🇵 japonais ou 🇺🇸 anglais
- Traduit automatiquement les keywords non-anglais en anglais pour chercher sur arXiv
- Renvoie : Markdown card-news avec note de traduction

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` ou URL complète `https://arxiv.org/abs/2507.01234`
- `note`: ton commentaire (optionnel)
- Renvoie : chemin du fichier sauvegardé (défaut : `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: filtre par titre / contenu (optionnel)
- Renvoie : liste des fichiers de notes sauvegardées récemment

## 🚀 Démarrage rapide

### Installation

```bash
pip install arxiv-daily-mcp
```

Ou depuis le source :

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Enregistre dans ton client MCP

#### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` :

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

`.cursor/mcp.json` ou settings du workspace :

```json
{
  "mcpServers": {
    "arxiv-daily": {
      "command": "arxiv-daily-mcp"
    }
  }
}
```

#### N'importe quel client compatible MCP

Ce serveur utilise le transport standard `stdio` et expose 4 outils via JSON-RPC — ça marche avec n'importe quel client qui suit le [spec MCP](https://modelcontextprotocol.io).

## 🎬 Démo

### Keyword en coréen (auto-traduite en anglais)

```text
👤 Cherche des papers sur les agents

🤖 Claude :
🔍 Résultats pour 'agents' — 🇰🇷 coréen → anglais : 'agent' (5 papers)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### Keyword en chinois

```text
👤 智能体 相关论文

🤖 Claude :
🔍 Résultats pour '智能体' — 🇨🇳 chinois → anglais : 'agent' (5 papers)
```

### Keyword en japonais

```text
👤 エージェント 論文を探して

🤖 Claude :
🔍 Résultats pour 'エージェント' — 🇯🇵 japonais → anglais : 'agent' (5 papers)
```

### Sauvegarder + récupérer

```text
👤 Sauvegarde le premier paper — sécurité multi-agents intéressante

🤖 Claude :
✅ Sauvegardé : `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 Montre-moi mes notes

🤖 Claude :
📚 Mes notes arXiv (1)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 vs autres MCPs arXiv

GitHub a **466+ dépôts MCP arXiv** (au 2026-07-05). Le plus populaire, `blazickjp/arxiv-mcp-server`, est excellent — mais fait pour une autre audience.

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (celui-ci) |
|---|---|---|---|
| **Keywords en langues** | 🇺🇸 Anglais seulement | 🇺🇸 Anglais seulement | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 langues** |
| **Format de sortie** | JSON / données brutes | Texte seulement | **Markdown card-news** (emoji + bullets) |
| **Archive de notes** | ❌ | ❌ | ✅ **Voûte `.md` locale** |
| **Recherche de notes** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **Statut** | Maintenu | Maintenu | Actif (v0.1.0) |

### Trois raisons pour lesquelles il peut coexister

1. **Audience de langues différente.** Le leader à 2,933 étoiles est anglais seulement. Ce serveur est conçu pour les chercheurs non-anglophones d'abord.
2. **Forme de sortie différente.** Le leader renvoie du JSON brut / des tables de données. Ce serveur renvoie du **Markdown card-news** — lisible directement dans n'importe quelle UI de chat.
3. **Workflow différent.** Le leader est chercher-et-lire. Ce serveur inclut l'**archivage** : sauvegarde un paper dans ta voûte Markdown locale avec une phrase, puis `list_my_notes` pour le récupérer.

## 🌐 Mots-clés multilingues

Le dictionnaire de traduction vient avec le package — **pas d'API call, pas de latence, pas de rate limit**.

| Langue | Keywords |
|---|---|
| 🇰🇷 Coréen (28) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 Chinois (23) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 Japonais (24) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**Algorithme de détection :**

1. Si l'input contient du Hangul (가-힣) → recherche en coréen
2. Sinon s'il contient du Kana (ぁ-ヿ) → recherche en japonais
3. Sinon s'il contient des idéogrammes CJK (一-鿿) → recherche en chinois
4. Sinon → anglais (passé tel quel)

Les keywords inconnues sont passées telles quelles — donc un partial match cherche quand même directement sur arXiv.

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

**Choix de design clés :**

- **stdio transport** — standard MCP
- **FastMCP** — SDK Python officiel d'Anthropic
- **urllib seulement** — zéro dépendances HTTP externes (marche dans n'importe quel environnement Python minimal)
- **Dictionnaire de traduction in-process** — pas d'appel LLM, pas de rate limit, pas de latence par keyword
- **MEMO_DIR configurable** — défini via env var pour setups Docker / multi-utilisateur

## 🧪 Développement

```bash
# Installe les dépendances de dev
pip install -e ".[dev]"

# Lance MCP Inspector (UI de browser)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# Teste stdio JSON-RPC directement
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### Test unitaire de la couche de traduction

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 Roadmap

- [x] v0.1.0 — 4 outils, stdio, multilingue (75 keywords)
- [ ] v0.2.0 — outil `weekly_summary` (digest du vendredi)
- [ ] v0.3.0 — Plus de catégories (cs.RO, cs.CV, q-fin.ST)
- [ ] v0.4.0 — Release PyPI
- [ ] v1.0.0 — Transport HTTP (accès distant)
- [ ] v1.1.0 — Plus de langues (espagnol, français, allemand, hindi)
- [ ] v2.0.0 — Plugins de format de notes (Notion, Apple Notes, Bear)

## 🤝 Contribuer

Issues et PRs bienvenus. Particulièrement utile :

- 🌏 Plus de keywords de langues (surtout en cs.RO, q-fin, stat.ML)
- 📂 Nouvelles catégories de papers
- 📝 Options de format de notes (Notion API, Apple Notes, Bear)
- 🐛 Bug reports avec étapes de reproduction

## 📜 Licence

MIT

## 🙏 Crédits

- Construit avec [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Données de papers de [arXiv.org](https://arxiv.org) (API ouverte)
- Inspiré par la collection de référence [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

---

> 🌟 Si ce MCP t'a fait gagner quelques minutes dans ton workflow de recherche, pense à mettre une étoile au repo — ça aide d'autres à le trouver.
