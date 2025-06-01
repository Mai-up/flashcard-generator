# flashcard-generator

日本語の語彙学習用フラッシュカードを自動生成できる Streamlit アプリです。  
CSVを読み込んで複数枚のカードを一括作成することもできます。

## 🔧 機能

- 上の語と下の語を入力 → A4横サイズのPDFを生成
- 長い語も自動的に文字サイズ調整
- 語ペアをCSVで一括入力可能

## 🖥 使用方法

1. 必要なライブラリをインストール（`requirements.txt`参照）
2. ターミナルで以下を実行：

```bash
streamlit run flashcard_final_streamlit_autofit.py
```

3. アプリ画面に沿って語を入力 → PDFをダウンロード

## 📁 必要ファイル

- `flashcard_final_streamlit_autofit.py`（メインアプリ）
- `NotoSerifJP-Regular.ttf`（PDF出力用フォント）

## 📜 ライセンス

このプロジェクトは MIT License のもとで公開されています。
