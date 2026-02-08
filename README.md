# Photo Date Writer

JPGファイルのEXIFから撮影日時を読み取り、画像の右下に日付を印字するシンプルなツールです。

## 機能

- JPGファイルのEXIFデータから撮影日時を自動取得
- 画像右下に「YYYY/MM/DD」形式で日付を印字
- 半透明の黒背景で可読性を確保
- 元の画像品質を保持（JPEG品質95）

## 必要要件

- Python 3.x
- Pillow ライブラリ

## インストール

```bash
# 1. 仮想環境を作成（初回のみ）
python3 -m venv venv

# 2. 仮想環境をアクティベート（毎回必要）
source venv/bin/activate

# 3. 必要なライブラリをインストール（初回のみ）
pip install -r requirements.txt
```

## 使い方

**重要**: プログラムを実行する前に、毎回仮想環境をアクティベートする必要があります。

```bash
# 仮想環境をアクティベート（毎回必要）
source venv/bin/activate

# プログラムを実行
python main.py <入力ファイル.jpg> <出力ファイル.jpg>

# 作業終了後、仮想環境を無効化（オプション）
deactivate
```

### 例

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# 単一ファイルを処理
python main.py input.jpg output.jpg

# samples ディレクトリの画像を処理
python main.py samples/photo.jpg samples/output.jpg
```

## 仕様

- **フォントサイズ**: 32px
- **フォント色**: 白
- **背景**: 半透明の黒（透明度50%）
- **位置**: 右下（マージン20px）
- **日付フォーマット**: YYYY/MM/DD

## 注意事項

- EXIFデータが存在しないJPGファイルは処理できません
- 入力ファイルはJPEG形式である必要があります
- 出力ファイルは常にJPEG形式で保存されます

## ライセンス

MIT License

## 今後の拡張予定

- バッチ処理（複数ファイル・ディレクトリ対応）
- 日付フォーマットのカスタマイズ
- フォント・色・位置の設定
- より詳細なエラーハンドリング
