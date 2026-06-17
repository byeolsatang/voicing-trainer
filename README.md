# Rootless Voicing Trainer

ジャズピアノの**ルートレス・ヴォイシング**をMIDIキーボードで瞬時に弾けるようにする練習Webアプリ。

🎹 **公開URL**: https://voicing-trainer.vercel.app

## 特徴

- コードとフォームを出題 → MIDIキーボードで回答 → 即時判定
- Web MIDI API 使用（ビルド不要・フレームワークなし・静的HTML2ファイル）
- スマホの仮想鍵盤は1音ずつタップして必要音数で自動判定
- ダーク/ライトテーマ対応

## ヴォイシング一覧

### 7th（dom7）
| フォーム | 積み順（下から） |
|---------|----------------|
| A       | ♭7 → 9 → M3 → 13 |
| B       | M3 → 13 → ♭7 → 9  |

### maj7
| フォーム | 積み順（下から） |
|---------|----------------|
| A       | M3 → 5 → M7 → 9  |
| B       | M7 → 9 → M3 → 5  |

### m7
| フォーム | 積み順（下から） |
|---------|----------------|
| A       | m3 → 5 → ♭7 → 9  |
| B       | ♭7 → 9 → m3 → 5  |

### m7♭5
| フォーム | 積み順（下から） |
|---------|----------------|
| A       | m3 → ♭5 → ♭7 → ♭9（4声） |
| B       | ♭7 → m3 → ♭5（3声）       |

## ファイル構成

```
voicing-trainer/
├── index.html              # メイン画面（出題・MIDI判定・結果表示）
├── midi-setup-guide.html   # MIDIキーボード接続ガイド
└── .github/
    ├── workflows/
    │   └── ai-issue.yml    # Issue → Claude → 自動デプロイ ワークフロー
    └── scripts/
        └── implement.py    # Claude API 呼び出しスクリプト
```

## ローカルで開く

MIDIを使うためHTTPS（またはlocalhost）が必要です。

```bash
cd /Users/erikokoide/DEV/voicing-trainer
python3 -m http.server 8080
# → http://localhost:8080 を開く
```

## デプロイ

mainブランチにpushするとVercelが自動デプロイします。

```bash
git add -A
git commit -m "変更内容"
git push
```

## AI自動実装（GitHub Issue → 自動デプロイ）

GitHubのIssueに修正指示を書いて **"ai-fix" ラベル** を付けると、Claude APIが自動でコードを修正してデプロイします。

**セットアップ（初回のみ）**
1. GitHub リポジトリの Settings → Secrets → Actions に `ANTHROPIC_API_KEY` を登録
2. Issues タブで "ai-fix" ラベルを作成

**使い方**
1. Issueを作成して指示を書く（日本語OK）
2. "ai-fix" ラベルを付ける
3. ✅ コメントが来たらデプロイ完了

## 設計メモ

- **テーマ管理**: CSS変数 + `data-theme`属性 + `prefers-color-scheme` + localStorageキー`rvt-theme`
- 配色やボタンの挙動を変える際はこの仕組みを踏襲してください
