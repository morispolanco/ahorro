import openai 
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Obtener una clave de API de OpenAI](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot") 

# Define los prompts para proporcionar consejos de ahorro en cinco áreas diferentes
prompts = [
    "Proporcione un consejo diario específico y práctico para ahorrar dinero en alimentos. Incluya una explicación y el ahorro estimado para este consejo.",
    "Proporcione un consejo diario específico y práctico para ahorrar dinero en transporte. Incluya una explicación y el ahorro estimado para este consejo.",
    "Proporcione un consejo diario específico y práctico para ahorrar dinero en ocio. Incluya una explicación y el ahorro estimado para este consejo.",
    "Proporcione un consejo diario específico y práctico para ahorrar dinero en servicios públicos. Incluya una explicación y el ahorro estimado para este consejo.",
    "Proporcione un consejo diario específico y práctico para ahorrar dinero en compras. Incluya una explicación y el ahorro estimado para este consejo."
]

if "messages" not in st.session_state:
    # El asistente comienza la conversación con un mensaje de bienvenida
    st.session_state["messages"] = [{"role": "assistant", "content": "¡Hola! Estoy aquí para proporcionarte consejos diarios sobre cómo ahorrar dinero en diferentes áreas. ¿En cuál de las siguientes áreas te gustaría recibir un consejo: alimentos, transporte, ocio, servicios públicos o compras?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor, ingresa tu clave de API de OpenAI para continuar.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Agregar los prompts de consejos en función de la elección del usuario
    if "alimentos" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[0]})
    elif "transporte" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[1]})
    elif "ocio" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[2]})
    elif "servicios públicos" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[3]})
    elif "compras" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[4]})

    # La conversación continuará proporcionando consejos en la categoría elegida.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
