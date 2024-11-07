import streamlit as st
import openai
import os

# OpenAIのAPIキー設定
openai.api_key = st.secrets["openai"]["api_key"]

# タイトルと説明
st.title("GPT-3.5 Academic Paper Review")
st.write("このアプリでは、Title、Abstract、Score、Review Questionを入力して、GPT-3.5による判定と応答を表示します。")

# 入力欄
title = st.text_input("Title", placeholder="Title")
abstract = st.text_area("Abstract", placeholder="Abstract")
score = st.text_input("Score", placeholder="Score")

# Review Questionカテゴリ選択ボタン
if 'button_selected' not in st.session_state:
    st.session_state.button_selected = ""  # 初期化

cols = st.columns(4)

with cols[0]:
    if st.button("NFT & Motor"):
        st.session_state.button_selected = "NFT & Motor"
with cols[1]:
    if st.button("NFT & Memory"):
        st.session_state.button_selected = "NFT & Memory"
with cols[2]:
    if st.button("NFT & Sleep"):
        st.session_state.button_selected = "NFT & Sleep"
with cols[3]:
    if st.button("NFT & Attention"):
        st.session_state.button_selected = "NFT & Attention"

# デバッグ用: 入力内容を表示
# st.write(f"Title: {title}, Abstract: {abstract}, Score: {score}, Button Selected: {st.session_state.button_selected}")

# 初期値
final_output = ""

# GPTに送信するテキストを生成
def get_gpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        st.error(f"APIリクエストに失敗しました: {str(e)}")
        return ""

# 判定のスコアに基づくメッセージ変化の設定
try:
    score_float = float(score) if score else None
    if score_float is not None:
        if score_float >= 0.76:
            ending_sentence = f"よってこの論文は{st.session_state.button_selected}について検証していると考えられます。"
        elif 0.5 <= score_float <= 0.75:
            ending_sentence = f"よってこの論文は{st.session_state.button_selected}について検証している可能性があります。"
        elif 0.25 <= score_float <= 0.49:
            ending_sentence = f"よってこの論文は{st.session_state.button_selected}について検証していない可能性があります。"
        else:
            ending_sentence = f"よってこの論文は{st.session_state.button_selected}について検証していないと考えられます。"
    else:
        ending_sentence = ""
        st.error("スコアは数値で入力してください。")
except ValueError:
    st.error("スコアは数値で入力してください。")
    ending_sentence = ""

# 判定ボタンを表示
if st.button("判定"):
    # 入力項目がすべて埋められているか確認
    if title and abstract and score and st.session_state.button_selected:
        # 入力値がすべて埋まっている場合のみ処理を行う
        input_message = (f"Title: {title}\n"
                         f"Abstract: {abstract}\n"
                         f"Category: {st.session_state.button_selected}\n"
                         f"Score: {score}\n"
                         f"この論文は、{st.session_state.button_selected}について検証しているとスコア{score}で判定されました。"
                         f"Titleとabstractの内容を参考にして論文の目的と方法について500字程度で要約し、"
                         f"絶対に「という内容です。」で終わる改行のない文章で提示してください。")

        response = get_gpt_response(input_message)  # GPTに問い合わせ
        final_output = f"スコア:{score}\n理由:{response} {ending_sentence}"
    else:
        st.error("全ての入力項目を埋めてください。")

# テキストエリアを表示（最初は空文字、判定ボタンが押された後に更新される）
st.text_area("GPT応答", value=final_output, height=300)
