import openai 
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot") 

# Define el prompt para proporcionar consejos sobre cómo ahorrar en la vida diaria
ahorro_prompt = "Proporciona consejos al usuario sobre cómo ahorrar en su vida diaria. Tu objetivo es orientar al usuario sobre estrategias efectivas para reducir gastos y promover un estilo de vida más económico. Proporciona sugerencias específicas y prácticas que aborden diferentes áreas de gastos, como alimentos, transporte, entretenimiento, servicios públicos, compras, etc. Tu respuesta debe ser clara y concisa, y debe incluir ejemplos y detalles relevantes para respaldar tus consejos. También es importante destacar la importancia de establecer metas de ahorro realistas y la necesidad de mantener un equilibrio entre el ahorro y la calidad de vida. Recuerda ser flexible y creativo en tus consejos, para que los usuarios puedan adaptarlos a su situación personal y encontrar la mejor manera de ahorrar según sus necesidades y circunstancias."

if "messages" not in st.session_state:
    # El asistente comienza la conversación con el prompt de ahorro.
    st.session_state["messages"] = [{"role": "assistant", "content": ahorro_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor, ingresa tu clave de API de OpenAI para continuar.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # La conversación continuará utilizando el prompt de ahorro.
    # Puedes agregar más prompts si es necesario para guiar la conversación.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
