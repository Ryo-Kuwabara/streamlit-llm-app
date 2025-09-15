from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
# llmインスタンスはAPIキー取得後に初期化するため、ここでは定義しない

import os

st.title("テストアプリ: 専門家アプリ")

st.write("##### 動作モード1: 健康の専門家")
st.write("入力フォームに質問を入力し、「実行」ボタンを押すことで健康の専門家のアドバイスが受けれます")
st.write("##### 動作モード2: 大学受験の専門家")
st.write("入力フォームに質問を入力し、「実行」ボタンを押すことで大学受験の専門家のアドバイスが受けられます")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["健康の専門家", "大学受験の専門家"]
)

st.divider()

if selected_item == "健康の専門家":
    input_message = st.text_input(label="健康に関するお悩みを入力ください")
else:
    input_message = st.text_input(label="大学受験に関するお悩みを入力ください")

if st.button("実行") and input_message:
    st.divider()
    # OpenAI APIキーを環境変数から取得
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")
        st.stop()
    # LangChainのOpenAIラッパーを初期化（APIキーが存在する場合のみ）
    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7)
    # モードごとにプロンプトを分岐
    if selected_item == "健康の専門家":
        prompt = f"あなたは健康の専門家です。次の悩みに専門的なアドバイスを日本語でください: {input_message}"
    else:
        prompt = f"あなたは大学受験の専門家です。次の悩みに専門的なアドバイスを日本語でください: {input_message}"
    # LLMでアドバイス生成
    with st.spinner("アドバイス生成中..."):
        try:
            advice = llm.invoke(prompt)
            # 結果表示
            st.write("### アドバイス")
            st.write(advice.content if hasattr(advice, "content") else advice)
        except Exception as e:
            st.error(f"アドバイス生成中にエラーが発生しました: {e}")