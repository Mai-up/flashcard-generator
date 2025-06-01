
import streamlit as st
from fpdf import FPDF
import io
import pandas as pd

# フォントサイズを自動調整する関数
def fit_text(pdf, text, max_width, initial_font_size):
    font_size = initial_font_size
    while font_size > 10:
        pdf.set_font("Noto", size=font_size)
        if pdf.get_string_width(text) <= max_width:
            break
        font_size -= 1
    return font_size

# PDF作成関数（文字サイズ調整・中央配置対応）
def create_flashcard_pdf(pairs):
    pdf = FPDF(orientation="L", format="A4")
    pdf.add_font("Noto", "", "NotoSerifJP-Regular.ttf", uni=True)

    page_width = 297
    page_height = 210
    margin = 20
    max_width = page_width - margin * 2

    for top_text, bottom_text in pairs:
        if not top_text or not bottom_text:
            continue

        pdf.add_page()

        # 上の語
        top_font_size = fit_text(pdf, top_text, max_width, 100)
        pdf.set_font("Noto", size=top_font_size)
        top_w = pdf.get_string_width(top_text)
        top_x = (page_width - top_w) / 2
        top_y = (page_height / 2 - top_font_size * 0.6) / 2
        pdf.set_xy(top_x, top_y)
        pdf.cell(top_w, top_font_size * 0.6, txt=top_text)

        # 中央の線
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.5)
        pdf.line(0, page_height / 2, page_width, page_height / 2)

        # 下の語
        bottom_font_size = fit_text(pdf, bottom_text, max_width, 100)
        pdf.set_font("Noto", size=bottom_font_size)
        bottom_w = pdf.get_string_width(bottom_text)
        bottom_x = (page_width - bottom_w) / 2
        bottom_y = page_height / 2 + (page_height / 2 - bottom_font_size * 0.6) / 2
        pdf.set_xy(bottom_x, bottom_y)
        pdf.cell(bottom_w, bottom_font_size * 0.6, txt=bottom_text)

    pdf_output = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_output)

# Streamlit UI
st.title("フラッシュカード自動作成ツール")
st.caption("言葉をペアで入力すると、印刷用のPDFが作れます。")

tab1, tab2, tab3 = st.tabs(["1枚だけ作成", "10枚まで作成", "もっと作成"])

with tab1:
    st.subheader("1枚だけ作成")
    col1, col2 = st.columns(2)
    with col1:
        top_text = st.text_input("上の語（例：はしる）")
    with col2:
        bottom_text = st.text_input("下の語（例：はしって）")

    if st.button("PDFを作成", key="btn_single"):
        if top_text and bottom_text:
            pdf_file = create_flashcard_pdf([(top_text, bottom_text)])
            st.download_button("PDFをダウンロード", data=pdf_file, file_name="flashcard.pdf", mime="application/pdf")
        else:
            st.warning("上の語と下の語を両方入力してください")

with tab2:
    st.subheader("10枚まで作成")
    pairs = []
    for i in range(10):
        col1, col2 = st.columns(2)
        with col1:
            front = st.text_input(f"{i+1}枚目・上の語", key=f"front_{i}")
        with col2:
            back = st.text_input(f"{i+1}枚目・下の語", key=f"back_{i}")
        pairs.append((front.strip(), back.strip()))

    if st.button("PDFを出力する", key="btn_multi"):
        valid_pairs = [pair for pair in pairs if pair[0] and pair[1]]
        incomplete_pairs = [pair for pair in pairs if (pair[0] and not pair[1]) or (not pair[0] and pair[1])]

        if incomplete_pairs:
            st.warning("ペアで記入されていない行があります")

        if valid_pairs:
            pdf_file = create_flashcard_pdf(valid_pairs)
            st.download_button("PDFをダウンロード", data=pdf_file, file_name="flashcards.pdf", mime="application/pdf")
        else:
            st.warning("少なくとも1組の語を入力してください")

with tab3:
    st.subheader("もっと作成")
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください（列名：上の語, 下の語）", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "上の語" in df.columns and "下の語" in df.columns:
            pairs = list(zip(df["上の語"].fillna(""), df["下の語"].fillna("")))
            if len(pairs) > 0:
                st.success(f"{len(pairs)} ペアを読み込みました")
                pdf_file = create_flashcard_pdf(pairs)
                st.download_button("PDFをダウンロード", data=pdf_file, file_name="flashcards_from_csv.pdf", mime="application/pdf")
            else:
                st.warning("語彙が空です。CSVの中身を確認してください。")
        else:
            st.error("CSVの列名は '上の語' と '下の語' にしてください。")

# フッター
st.markdown("""
<div style='margin-top: 100px; text-align: center; font-size: 12px;'>
    © 2025 Mai Ichimoto. Released under the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT License</a>
</div>
""", unsafe_allow_html=True)
