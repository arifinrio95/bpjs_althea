import streamlit as st

# Custom CSS to limit the width of the output
st.markdown("""
<style>
    .output {
        max-width: 600px;
        word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

class DokterAI:
    def __init__(self, messages):
        self.messages = messages

    def get_reply(self, question):
        prompt = """Jika saya memberikan pernyataan selain symptomps, balas dengan normal.
                    Jika saya memberikan symptomps: berikan satu follow-up pertanyaan satu-persatu secara kreatif misal dari kebiasaan, riwayat,
                    dan lainnya sampai kamu bisa mendiagnosa penyakit saya dengan pasti,
                    jangan mendiagnosa jika kesimpulannya belum pasti.
                    Setelah mendiagnosis, sertakan sumber jurnal ilmiah atau paper yang mendukung beserta kutipannya yang related."""

        self.messages.append({"role": "user", "content": question})
        self.messages.append({"role": "system", "content": prompt})

        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=self.messages
        )
        answer = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": answer})

        return answer

# Initialize Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Saya adalah DokterAI, dokter virtual Anda. Saya siap membantu Anda dengan pertanyaan medis Anda."}
    ]

# Initialize DokterAI
bot = DokterAI(st.session_state.messages)

# Placeholder for chat
chat_history_placeholder = st.empty()

# Update the chat history
chat_str = "<div class='output'>"
for message in bot.messages:
    role, content = message["role"], message["content"]
    if role == "user":
        # Only display the user's input, not the entire prompt
        chat_str += f"<p><strong>User:</strong> {content.split('. ')[0]}</p>"
    elif role == "assistant":
        chat_str += f"<p><strong>DokterAI:</strong> {content}</p>"
chat_str += "</div>"
chat_history_placeholder.markdown(chat_str, unsafe_allow_html=True)

# Text input and button
user_input = st.text_input("Tulis pertanyaan medis Anda di sini:")
if st.button("Kirim"):
    response = bot.get_reply(user_input)

    # Update the chat history
    chat_str = "<div class='output'>"
    for message in bot.messages:
        role, content = message["role"], message["content"]
        if role == "user":
            chat_str += f"<p><strong>User:</strong> {content.split('. ')[0]}</p>"
        elif role == "assistant":
            chat_str += f"<p><strong>DokterAI:</strong> {content}</p>"
    chat_str += "</div>"
    chat_history_placeholder.markdown(chat_str, unsafe_allow_html=True)
