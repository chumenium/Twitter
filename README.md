# Twitter風アプリ

Djangoで作成されたTwitter風のソーシャルメディアアプリケーションです。

## 機能

- 📝 投稿の作成・編集・削除
- ❤️ いいね機能
- 🔖 ブックマーク機能
- 👤 ユーザープロフィール管理
- 🖼️ 画像投稿対応
- 📱 レスポンシブデザイン
- 🔐 ユーザー認証（allauth使用）

## 技術スタック

- **バックエンド**: Django 5.2.3
- **認証**: django-allauth
- **フロントエンド**: HTML5, CSS3, JavaScript
- **アイコン**: Font Awesome
- **フォント**: Inter

## セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/chumenium/Twitter.git
cd Twitter
```

### 2. 仮想環境の作成とアクティベート
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. データベースのマイグレーション
```bash
python manage.py migrate
```

### 5. スーパーユーザーの作成（オプション）
```bash
python manage.py createsuperuser
```

### 6. 開発サーバーの起動
```bash
python manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/` にアクセスしてください。

## 主な機能の説明

### 投稿機能
- テキストと画像を含む投稿の作成
- 投稿の編集・削除（自分の投稿のみ）
- 投稿の一覧表示（タイムライン）

### いいね機能
- 投稿へのいいね・いいね解除
- いいね数の表示

### ブックマーク機能
- 投稿のブックマーク・ブックマーク解除
- ブックマークした投稿の一覧表示

### ユーザー機能
- ユーザー登録・ログイン・ログアウト
- プロフィール編集
- マイページ表示

## プロジェクト構造

```
project4/
├── config/                 # プロジェクト設定
│   ├── settings.py        # Django設定
│   ├── urls.py           # メインURL設定
│   └── ...
├── microboard/            # メインアプリ
│   ├── models.py         # データモデル
│   ├── views.py          # ビュー
│   ├── urls.py           # アプリURL設定
│   ├── forms.py          # フォーム
│   └── templates/        # テンプレート
├── static/               # 静的ファイル
├── templates/            # グローバルテンプレート
└── manage.py            # Django管理スクリプト
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。 