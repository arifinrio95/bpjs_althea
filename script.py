import streamlit as st
import openai

class DokterAI:
    def __init__(self, messages):
        self.messages = messages

    def get_reply(self, question):
        self.messages.append({"role": "user", "content": question + """
            Jika saya memberikan pernyataan selain symptomps, balas dengan normal.
            Jika saya memberikan symptomps, berikan satu follow-up pertanyaan satu-persatu secara kreatif,
            misal dari kebiasaan, riwayat, dan lainnya sampai kamu bisa mendiagnosa penyakit saya dengan pasti.
            Jangan mendiagnosa jika kesimpulannya belum pasti. Setelah mendiagnosis,
            sertakan sumber jurnal ilmiah atau paper yang mendukung beserta kutipannya yang related."""})

        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=self.messages
        )

        answer = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": answer})

        return answer

st.title("DokterAI")

# Initialize session state if not already initialized
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Saya adalah DokterAI, dokter virtual Anda. Saya siap membantu Anda dengan pertanyaan medis Anda."}
    ]

# Initialize DokterAI with existing session messages
bot = DokterAI(st.session_state.messages)

# Create a placeholder for displaying conversation
chat_history_placeholder = st.empty()

# Update the chat history
chat_str = ""
for message in bot.messages:
    role, content = message["role"], message["content"]
    if role == "user":
        chat_str += f"User: {content}\n"
    elif role == "assistant":
        chat_str += f"DokterAI: {content}\n"
chat_history_placeholder.text(chat_str)

# Create a text input for user input
user_input = st.text_input("Tulis pertanyaan medis Anda di sini:")

# Create a button for sending the question
if st.button("Kirim"):
    # Get a reply from the bot
    response = bot.get_reply(user_input)

    # Update the chat history
    chat_str = ""
    for message in bot.messages:
        role, content = message["role"], message["content"]
        if role == "user":
            chat_str += f"User: {content}\n"
        elif role == "assistant":
            chat_str += f"DokterAI: {content}\n"
    chat_history_placeholder.text(chat_str)
