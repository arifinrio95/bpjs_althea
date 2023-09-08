import streamlit as st
import openai

openai.api_key = st.secrets['openai_apikey']
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

st.markdown("""
## Selamat Datang di Althea AI

### Deskripsi

Althea AI adalah asisten medis virtual yang berbasis kecerdasan buatan. Aplikasi ini dirancang untuk membantu Anda dengan pertanyaan atau kekhawatiran medis yang mungkin Anda miliki. Althea akan merespons pertanyaan Anda dan memandu Anda melalui serangkaian pertanyaan follow-up untuk memberikan informasi medis yang lebih spesifik dan akurat.
""")

st.sidebar.markdown("""
### Cara Menggunakan

1. **Masukkan Pertanyaan:** Tulis pertanyaan atau simptom medis Anda pada kotak teks yang disediakan.
2. **Tekan Enter:** Setelah menulis, tekan Enter.
3. **Baca Respon:** DokterAI akan merespons pertanyaan Anda dan mungkin akan memberikan pertanyaan follow-up untuk lebih memahami kondisi Anda.
4. **Jangan ragu untuk berinteraksi lebih lanjut:** Anda bisa melanjutkan dialog dengan menanggapi pertanyaan follow-up atau mengajukan pertanyaan baru.

### Catatan

- Aplikasi ini tidak menggantikan konsultasi medis profesional. Jika Anda mengalami gejala yang serius atau membutuhkan diagnosis medis, segera hubungi profesional medis.
- Semua informasi yang disediakan oleh DokterAI adalah berdasarkan sumber ilmiah yang tersedia hingga saat ini.
""")

st.write("Tulis keluhan / pertanyaan medis Anda di sini: ")
# Initialize DokterAI
bot = DokterAI(st.session_state.messages)

# Initialize Streamlit session state for text input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Placeholder for chat
chat_history_placeholder = st.empty()

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

# Text input
user_input = st.text_input("", value=st.session_state.user_input)

# Check if text_input is triggered
if st.session_state.get('prev_input') != user_input:
    st.session_state.prev_input = user_input
    if user_input:
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

        # Reset the user input
        st.session_state.user_input = ""
