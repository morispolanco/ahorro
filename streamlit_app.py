import openai 
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Obtener una clave de API de OpenAI](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot") 

# Define el prompt sin mostrarlo al usuario
ahorro_prompt = "Proporcione cinco consejos diarios específicos y prácticos para ahorrar dinero en alimentos, transporte, ocio, servicios públicos y compras. Incluya explicaciones y ahorros estimados para cada consejo, discuta su efectividad y beneficios financieros a largo plazo. Asegúrese de que los consejos sean realistas, ampliamente aplicables y promuevan ahorros sostenibles."

if "messages" not in st.session_state:
    # El asistente comienza la conversación con un mensaje de bienvenida
    st.session_state["messages"] = [{"role": "assistant", "content": "¡Hola! Estoy aquí para ayudarte con consejos de ahorro en tu vida diaria. ¿En qué área específica te gustaría recibir consejos hoy?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor, ingresa tu clave de API de OpenAI para continuar.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Agregar el prompt de ahorro en cada interacción para que el modelo lo use internamente
    st.session_state.messages.append({"role": "assistant", "content": ahorro_prompt})
    
    # La conversación continuará utilizando el prompt de ahorro sin mostrarlo al usuario.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
