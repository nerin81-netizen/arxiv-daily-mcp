# 🧠 arxiv-daily-mcp

> **arXiv を韓国語、中国語、日本語、英語で検索し、ローカルの Markdown ノート庫に保存しましょう。**
> 既存の CLI スクリプトを MCP にラップしたオープンソース。

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)

**🌍 言語を選ぶ:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 クイックスタート](#-クイックスタート) · [🛠 ツール 4 個](#-ツール-4-個) · [🎬 デモ](#-デモ) · [🆚 他の arXiv MCP との違い](#-他の-arxiv-mcp-との違い) · [🌐 多言語キーワード](#-多言語キーワード) · [🏗 アーキテクチャ](#-アーキテクチャ)

---

## ✨ これは何?

CLI スクリプトを MCP サーバーとしてラップし、LLM クライアント(Claude、Cursor、Cline など)から自然言語で呼び出せるようにしたオープンソースです。

核心となるアイデア:

> **毎日実行している CLI スクリプトを MCP でラップして、自然言語で呼び出せるようにする。**

毎朝ターミナルに同じ `curl` / `python` / `arxiv` コマンドを入力しているなら、それが MCP ツールとしてどのように見えるかを示しています。

## 🛠 ツール 4 個

| ツール | 引数 | 説明 | 使用例 |
|---|---|---|---|
| `get_today_papers` | `category`, `max_results` | 今日の AI / ビジネス論文 | "今日の AI 論文を教えて" |
| `search_papers` | `keyword`, `max_results` | **多言語**キーワード検索 | "エージェント 論文を探して" |
| `save_paper_note` | `arxiv_id`, `note` | ローカル `.md` ノート庫に保存 | "これをメモして" |
| `list_my_notes` | `keyword`, `limit` | 保存したノートの検索/一覧 | "マイメモを見せて" |

### `get_today_papers(category, max_results=5)`

- `category`: `"ai"` (cs.AI+cs.CL+cs.LG) · `"business"` (econ.GN+q-fin) · `"all"` (全て)
- 戻り値: 今日の投稿論文の Markdown カードニュース一覧

### `search_papers(keyword, max_results=5)`

- `keyword`: 🇰🇷 韓国語、🇨🇳 中国語、🇯🇵 日本語、🇺🇸 英語すべて対応
- 英語以外のキーワードは自動的に英語に翻訳され、arXiv 検索に使用
- 戻り値: 翻訳情報を含む Markdown カード

### `save_paper_note(arxiv_id, note="")`

- `arxiv_id`: `"2507.01234"` または完全な URL
- `note`: あなたのコメント(オプション)
- 戻り値: 保存されたファイルパス(デフォルト: `~/memos/YYYY-MM-DD_arxiv_<id>.md`)

### `list_my_notes(keyword="", limit=10)`

- `keyword`: タイトル/内容でフィルタ(オプション)
- 戻り値: 最近保存されたノートファイル一覧

## 🚀 クイックスタート

### インストール

```bash
pip install arxiv-daily-mcp
```

またはソースから:

```bash
git clone https://github.com/nerin81-netizen/arxiv-daily-mcp
cd arxiv-daily-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### MCP クライアントに登録

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

#### その他の MCP 対応クライアント

標準の `stdio` トランスポートと JSON-RPC を使用するため、[MCP 仕様](https://modelcontextprotocol.io) に従うすべてのクライアントで動作します。

**🌍 言語を選ぶ:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

## 🎬 デモ

### 韓国語キーワード(自動的に英語に翻訳)

```text
👤 에이전트 관련 논문 찾아줘  (エージェント関連の論文を探して)

🤖 Claude:
🔍 '에이전트' 検索結果 — 🇰🇷 한국어 → 英語: 'agent' (5 件)

1. **Distributed Attacks in Persistent-State AI Control**
   👥 Josh Hills, Ida Caspary, Asa Cooper Stickland
   📅 2026-07-02 | 🏷️ cs.AI
   🔗 https://arxiv.org/abs/2607.02514v1
```

### 中国語キーワード

```text
👤 智能体 相关论文  (エージェント関連の論文)

🤖 Claude:
🔍 '智能体' 検索結果 — 🇨🇳 中文 → 英語: 'agent' (5 件)
```

### 日本語キーワード

```text
👤 エージェント 論文を探して

🤖 Claude:
🔍 'エージェント' 検索結果 — 🇯🇵 日本語 → 英語: 'agent' (5 件)
```

### 保存 + 検索

```text
👤 最初の論文をメモして — マルチエージェント セキュリティが面白い

🤖 Claude:
✅ 保存完了: `~/memos/2026-07-06_arxiv_2607.02514.md`

👤 マイメモを見せて

🤖 Claude:
📚 マイ arXiv ノート (1 件)
  · `2026-07-06_arxiv_2607.02514.md` — Distributed Attacks in Persistent-State AI Control
```

## 🆚 他の arXiv MCP との違い

GitHub には **466 件以上の arXiv MCP リポジトリ**があります(2026-07-05 時点)。最も人気のある `blazickjp/arxiv-mcp-server` (⭐ 2,933) も優れていますが、対象ユーザーは異なります。

| | `blazickjp/arxiv-mcp-server` ⭐ 2,933 | `mcp-simple-arxiv` ⭐ 198 | `arxiv-daily-mcp` (本プロジェクト) |
|---|---|---|---|
| **キーワード言語** | 🇺🇸 英語のみ | 🇺🇸 英語のみ | 🇰🇷🇨🇳🇯🇵🇺🇸 **4 言語** |
| **出力形式** | JSON / 生データ | テキストのみ | **Markdown カードニュース**(絵文字 + 箇条書き) |
| **ノート保存** | ❌ | ❌ | ✅ **ローカル `.md` ノート庫** |
| **ノート検索** | ❌ | ❌ | ✅ `list_my_notes(keyword=…)` |
| **状態** | 活発に保守中 | 活発に保守中 | v0.1.0 (初回リリース) |

### 共存できる 3 つの理由

1. **対象言語ユーザーが異なる。** 2,933 スターのリーダーは英語専用です。本サーバーは非英語圏の研究者を最優先で設計しました。
2. **出力形式が異なる。** リーダーは生 JSON / データテーブルを返します。本サーバーは**カードニュース Markdown**を返すため、あらゆるチャット UI で直接読めます。
3. **ワークフローが異なる。** リーダーは検索-閲覧ツールです。本サーバーは**アーカイブ**機能を含み、一言で論文をローカル Markdown ノート庫に保存し、後で `list_my_notes` で呼び出せます。

## 🌐 多言語キーワード

翻訳辞書はパッケージに同梱——**API 呼び出しなし、遅延なし、レート制限なし**。

| 言語 | キーワード |
|---|---|
| 🇰🇷 韓国語 (28 個) | 에이전트, 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 강화학습, 생성형, 변압기, 확산모델, 검색증강, 멀티모달, 로보틱스, 추천시스템, 그래프신경망, 파운데이션모델, 거대언어모델, 프롬프트, 미세조정, 정렬, 안전성, 환각, 추론, 계획, 도구사용, 메모리, 체인, … |
| 🇨🇳 中国語 (23 個) | 智能体, 人工智能, 机器学习, 深度学习, 自然语言处理, 计算机视觉, 强化学习, 生成式, 变压器, 扩散模型, 多模态, 机器人, 推荐系统, 图神经网络, 基础模型, 大语言模型, 提示, 微调, 对齐, 推理, 工具使用, 链, 代理 |
| 🇯🇵 日本語 (24 個) | エージェント, 人工知能, 機械学習, 深層学習, 自然言語処理, コンピュータビジョン, 強化学習, 生成, 変圧器, 拡散モデル, 検索拡張, マルチモーダル, ロボット, 推薦システム, グラフニューラルネットワーク, 基盤モデル, 大規模言語モデル, プロンプト, 微調整, アライメント, 推論, 計画, ツール使用, 記憶, 幻覚 |

**検出アルゴリズム:**

1. 入力にハングル(가-힣)が含まれていれば → 韓国語辞書を参照
2. そうでなくカナ(ぁ-ヿ)が含まれていれば → 日本語辞書を参照
3. そうでなく漢字(一-鿿)が含まれていれば → 中国語辞書を参照
4. その他 → 英語(そのまま渡す)

辞書にないキーワードはそのまま渡されるため、部分一致でも arXiv を直接検索します。

## 🏗 アーキテクチャ

```
┌─────────────────┐      stdio/JSON-RPC      ┌──────────────────────┐
│  LLM クライアント │ ◀──────────────────────▶ │  arxiv-daily-mcp     │
│ (Claude/Cursor) │                          │  (FastMCP サーバー)  │
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
                                                 │  *.md ノート庫│
                                                 └──────────────┘
```

**主要な設計判断:**

- **stdio トランスポート** — MCP 標準
- **FastMCP** — Anthropic 公式 Python SDK
- **urllib のみ** — 外部 HTTP 依存ゼロ(最小限の Python 環境で動作)
- **プロセス内翻訳辞書** — LLM 呼び出しなし、レート制限なし、キーワードごとの遅延なし
- **MEMO_DIR の環境変数化** — Docker / マルチユーザー対応

## 🧪 開発

```bash
# 開発依存をインストール
pip install -e ".[dev]"

# MCP Inspector を実行(ブラウザ UI)
npx @modelcontextprotocol/inspector arxiv-daily-mcp

# stdio JSON-RPC を直接テスト
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | arxiv-daily-mcp
```

### 翻訳レイヤーのユニットテスト

```python
from arxiv_daily_mcp.server import _translate_keyword

assert _translate_keyword("에이전트") == ("agent", "ko")
assert _translate_keyword("智能体") == ("agent", "zh")
assert _translate_keyword("エージェント") == ("agent", "ja")
assert _translate_keyword("agent") == ("agent", "en")
```

## 🌍 ロードマップ

- [x] v0.1.0 — 4 ツール、stdio、多言語(75 キーワード)
- [ ] v0.2.0 — `weekly_summary` ツール(金曜ダイジェスト)
- [ ] v0.3.0 — カテゴリの拡張(cs.RO、cs.CV、q-fin.ST)
- [ ] v0.4.0 — PyPI リリース
- [ ] v1.0.0 — HTTP トランスポート(リモートアクセス)
- [ ] v1.1.0 — より多くの言語(スペイン語、フランス語、ドイツ語、ヒンディー語)
- [ ] v2.0.0 — ノート形式プラグイン(Notion、Apple Notes、Bear)

## 🤝 コントリビュート

Issue と PR を歓迎します。特に以下の貢献が有用です:

- 🌏 より多くの言語キーワード(特に cs.RO、q-fin、stat.ML)
- 📂 新しい論文カテゴリ
- 📝 ノート形式オプション(Notion API、Apple Notes、Bear)
- 🐛 再現手順付きのバグレポート

## 📜 ライセンス

MIT

## 🙏 クレジット

- [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) で構築
- 論文データ提供元: [arXiv.org](https://arxiv.org)(オープン API)
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) リファレンス集からインスピレーション

---

> 🌟 この MCP があなたの研究ワークフローで数分を節約できたら、リポジトリにスターを付けてください——他の人が見つける助けになります。
