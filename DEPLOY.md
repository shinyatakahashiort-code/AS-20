# AS-20アンケートシステム デプロイ手順書

## 📋 必要なもの

1. GitHubアカウント
2. Streamlit Cloudアカウント（GitHubアカウントで無料登録可能）

---

## 🚀 デプロイ手順（完全ガイド）

### ステップ1: GitHubリポジトリの作成

1. **GitHubにログイン**
   - https://github.com にアクセス
   - アカウントがない場合は新規作成

2. **新しいリポジトリを作成**
   - 右上の「+」→「New repository」をクリック
   - リポジトリ名: `as20-survey`（または任意の名前）
   - 説明: `視覚のQOL調査 AS-20 アンケートシステム`
   - Public（公開）を選択
   - 「Create repository」をクリック

3. **ファイルをアップロード**
   - 「uploading an existing file」をクリック
   - 以下のファイルをドラッグ&ドロップ:
     - `app.py`
     - `requirements.txt`
     - `README.md`
     - `.gitignore`
   - コミットメッセージ: `Initial commit`
   - 「Commit changes」をクリック

---

### ステップ2: Streamlit Cloudでデプロイ

1. **Streamlit Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - 「Sign up」または「Sign in」をクリック
   - 「Continue with GitHub」を選択

2. **新しいアプリを作成**
   - ダッシュボードで「New app」をクリック
   - または直接: https://share.streamlit.io/deploy

3. **アプリの設定**
   - **Repository**: `あなたのユーザー名/as20-survey`を選択
   - **Branch**: `main` または `master`
   - **Main file path**: `app.py`
   - **App URL**: カスタムURLを設定可能（例: `as20-survey`）

4. **デプロイ開始**
   - 「Deploy!」ボタンをクリック
   - 数分待つと、アプリが公開されます

5. **公開URLを取得**
   - デプロイ完了後、URLが表示されます
   - 例: `https://あなたのユーザー名-as20-survey.streamlit.app`

---

## ✅ デプロイ確認

デプロイが成功すると、以下が表示されます：
- ✅ アプリのタイトル: 「視覚のQOL調査 AS-20」
- ✅ 氏名・患者ID入力フィールド
- ✅ 20項目の質問
- ✅ 送信ボタン

---

## 🔧 トラブルシューティング

### エラー: ModuleNotFoundError

**原因**: `requirements.txt`に必要なパッケージが記載されていない

**解決策**:
1. GitHubリポジトリの`requirements.txt`を確認
2. 不足しているパッケージを追加
3. Streamlit Cloudで「Reboot」をクリック

### エラー: アプリが起動しない

**原因**: `app.py`にエラーがある

**解決策**:
1. Streamlit Cloudのログを確認
2. エラーメッセージを確認して修正
3. GitHubにプッシュすると自動的に再デプロイ

### データが保存されない

**原因**: Streamlit Cloudは一時ストレージのみ

**解決策**:
- 永続的なデータ保存が必要な場合は、以下を検討:
  - Google Sheets API
  - Firebase
  - PostgreSQL（Streamlit Cloudは無料でサポート）

---

## 📝 アプリの更新方法

1. **ローカルでファイルを編集**
2. **GitHubにプッシュ**
   ```bash
   git add .
   git commit -m "更新内容"
   git push
   ```
3. **自動再デプロイ**
   - Streamlit Cloudが自動的に検出して再デプロイ
   - 数分後に変更が反映されます

---

## 🌐 URLの共有

デプロイ後、以下のURLを患者さんに共有できます：
```
https://あなたのユーザー名-as20-survey.streamlit.app
```

このURLをブックマークやQRコードにして配布可能です。

---

## 💡 ヒント

### カスタムドメインの設定
Streamlit Cloudの設定で独自ドメインを設定できます。

### アクセス制限
パスワード認証を追加する場合は、`streamlit-authenticator`パッケージの使用を検討してください。

### データのバックアップ
定期的に`survey_data`フォルダをダウンロードしてバックアップすることを推奨します。

---

## 📞 サポート

問題が発生した場合:
1. Streamlit公式ドキュメント: https://docs.streamlit.io
2. Streamlit Community: https://discuss.streamlit.io
3. GitHub Issues: リポジトリのIssuesタブ

---

## ✨ デプロイ完了！

おめでとうございます！AS-20アンケートシステムがオンラインで利用可能になりました。

URLを共有して、患者さんにアンケートに回答してもらいましょう！
