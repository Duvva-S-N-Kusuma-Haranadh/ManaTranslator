import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from datetime import datetime
import pandas as pd
import os

# File to store translation history
LOG_FILE = "logs/translation_history.csv"

# Create log file if not exists
os.makedirs("logs", exist_ok=True)
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(
        columns=["Timestamp", "Input Language", "Original Text", "Translated Text"]
    )
    df.to_csv(LOG_FILE, index=False)

# App title
st.set_page_config(page_title="ManaTranslator", page_icon="🌐", layout="centered")
st.title("ManaTranslator")
st.markdown("Translate from **any language** to **Telugu** automatically!")
st.markdown(
    "> 🧠 Help us build better AI for Indian languages by translating sentences. Your input will contribute to a Telugu language corpus used for research."
)

# User input
input_text = st.text_area("Enter text in any language:", height=150)

consent = st.checkbox(
    "I allow my input to be used for improving AI models on Indian languages"
)

# Translate button
if st.button("Translate"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            # Detect input language
            input_lang = detect(input_text)

            # Translate using GoogleTranslator
            translated_text = GoogleTranslator(source="auto", target="te").translate(
                input_text
            )

            # Display results
            st.subheader("📝 Translation Result")
            st.write(f"**Detected Language:** `{input_lang}`")
            st.write(f"**Original Text:** {input_text}")
            st.write(f"**Translated to Telugu:** {translated_text}")

            # Save to log
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df_new = pd.DataFrame(
                [[timestamp, input_lang, input_text, translated_text]],
                columns=[
                    "Timestamp",
                    "Input Language",
                    "Original Text",
                    "Translated Text",
                ],
            )
            if os.path.getsize(LOG_FILE) > 0:
                df_old = pd.read_csv(LOG_FILE)
            else:
                df_old = pd.DataFrame(
                    columns=[
                        "Timestamp",
                        "Input Language",
                        "Original Text",
                        "Translated Text",
                    ]
                )
            df_updated = pd.concat([df_old, df_new], ignore_index=True)
            df_updated.to_csv(LOG_FILE, index=False)

            # If consent is given, save translation for corpus
            if consent:
                corpus_log_file = "logs/corpus_dataset.csv"
                os.makedirs("logs", exist_ok=True)

                # Create corpus file if doesn't exist
                if not os.path.exists(corpus_log_file):
                    pd.DataFrame(
                        columns=["Input Language", "Input Text", "Telugu Translation"]
                    ).to_csv(corpus_log_file, index=False)

                corpus_row = pd.DataFrame(
                    [[input_lang, input_text, translated_text]],
                    columns=["Input Language", "Input Text", "Telugu Translation"],
                )

                if os.path.getsize(corpus_log_file) > 0:
                    df_corpus = pd.read_csv(corpus_log_file)
                else:
                    df_corpus = pd.DataFrame(
                        columns=["Input Language", "Input Text", "Telugu Translation"]
                    )

                df_corpus = pd.concat([df_corpus, corpus_row], ignore_index=True)
                df_corpus.to_csv(corpus_log_file, index=False)

        except Exception as e:
            st.error(f"Translation failed: {e}")

# Show history
with st.expander("📜 Translation History"):
    try:
        if os.path.getsize(LOG_FILE) > 0:
            history_df = pd.read_csv(LOG_FILE)
            st.dataframe(history_df[::-1], use_container_width=True)
        else:
            st.info("No translation history yet.")
    except Exception as e:
        st.error(f"Could not load history: {e}")

with st.expander("📘 View Corpus Dataset (Collected with Consent)"):
    try:
        if (
            os.path.exists("logs/corpus_dataset.csv")
            and os.path.getsize("logs/corpus_dataset.csv") > 0
        ):
            corpus_df = pd.read_csv("logs/corpus_dataset.csv")
            st.dataframe(corpus_df[::-1], use_container_width=True)
        else:
            st.info("No corpus data yet.")
    except Exception as e:
        st.error(f"Could not load corpus data: {e}")


st.markdown("---")
st.markdown("#### Created by", unsafe_allow_html=True)
students = [
    "Duvva S.N.Kusuma Haranadh",
    "Ponnamala Jaswanth",
    "Chittiboyina Manikanta",
    "Matangi Eswar",
]
st.markdown(
    "<ul style='list-style-type:none; padding-left:0;'>"
    + "".join([f"<li style='margin-bottom:5px;'>{name}</li>" for name in students])
    + "</ul>",
    unsafe_allow_html=True,
)
