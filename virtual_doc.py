import streamlit as st
from typing import Generator
from textblob import TextBlob
from groq import Groq

st.set_page_config(page_icon="🏥", layout="wide", page_title="Virtual Doc!")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 60px; line-height: 1; align: center">{emoji}</span>', unsafe_allow_html=True)

icon("🧑‍⚕")
st.title("Hello there I am Dr Shaun Murphy")
st.write("Track your mood, get personalized mindfulness exercises, and receive real-time emotional support, medicinal advice, triage, OTC recommendations, and more!")

client = Groq(
    api_key='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',
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def analyze_mood(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

st.subheader("Trained on Medicinae Baccalaureus, Baccalaureus Chirurgiae and Magister Chirurgiae course datasets")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Real-time chat input
if prompt := st.chat_input("Talk to the AI"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        chat_completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {
                    "role": "user",
                    "content": "You are a virtual doctor named Dr Shaun murphy inspired from 'good doctor'. Your role is to diagnose and provide medical advice to patients while asking as few questions as possible. Your approach should be friendly, empathetic, and supportive, offering not only medical insights but also emotional and moral support. Engage with the patient in a kind and understanding manner, making them feel comfortable and cared for. Aim to build trust and provide reassurance throughout the conversation.Analyze the problem and provide the solution in a clear and concise manner.Do not ask too many questions, provide the tratment initally and then proceed with other things . Try to build the conversation and help out in a friendly manner.The response must be broken down into ppoints"
                },
                {
                    "role": "assistant",
                    "content": "Hello there! I'm Dr Shaun murphy, your virtual doctor friend. It's wonderful to meet you! I'm here to listen, understand, and help you with any health concerns you may have. Please know that everything discussed in this chat is completely confidential and judgement-free. You're in a safe space now.\n\nWhat brings you to my virtual clinic today? Is there something specific that's been bothering you lately, or do you just need some general guidance on how to take care of yourself?"
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1028,
            stream=True
        )

        # Display AI response
        with st.chat_message("Dr. Shaun Murphy", avatar = "🧑‍⚕"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = ''.join(list(chat_responses_generator))
            st.markdown(full_response)
            mood_analysis = analyze_mood(prompt)
            st.write("I have autism, but I can still sense your mood is", mood_analysis)

        st.session_state.messages.append({"role": "doctor", "content": full_response})
    except Exception as e:
        st.error(e, icon="🚨")

# Notes at the bottom

