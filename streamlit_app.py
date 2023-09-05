import openai 
import streamlit as st
import pandas as pd

# Define la función para calcular el ahorro total
def calcular_ahorro_total(consejos):
    ahorro_total = sum(consejo.get("ahorro_estimado", 0) for consejo in consejos)
    return ahorro_total

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

# Lista para almacenar los consejos y ahorros estimados
consejos_y_ahorros = []

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

    # Extraer y almacenar los consejos y ahorros estimados
    consejo_actual = msg.content
    ahorro_estimado = 0  # Deberás analizar el consejo para extraer el ahorro estimado, por ejemplo, usando expresiones regulares.
    consejos_y_ahorros.append({"consejo": consejo_actual, "ahorro_estimado": ahorro_estimado})

# Preguntar al usuario si desea ver una tabla con el ahorro total
if st.button("Ver tabla de ahorro total"):
    # Calcular el ahorro total
    ahorro_total = calcular_ahorro_total(consejos_y_ahorros)
    
    # Crear un DataFrame con los consejos y ahorros estimados
    df = pd.DataFrame(consejos_y_ahorros)
    
    # Mostrar la tabla con los consejos y ahorros estimados
    st.subheader("Tabla de ahorro total")
    st.dataframe(df)
    
    # Mostrar el ahorro total calculado
    st.info(f"Ahorro total estimado: ${ahorro_total}")
