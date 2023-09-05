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

# Define los elementos y ahorros estimados en cada categoría
elementos_y_ahorros = {
    "alimentos": [
        {"elemento": "Comer en casa en lugar de restaurantes", "ahorro_estimado": 50},
        {"elemento": "Comprar alimentos a granel", "ahorro_estimado": 20},
        {"elemento": "Planificar comidas con anticipación", "ahorro_estimado": 30}
    ],
    "transporte": [
        {"elemento": "Usar transporte público en lugar de auto", "ahorro_estimado": 40},
        {"elemento": "Caminar o andar en bicicleta cuando sea posible", "ahorro_estimado": 20},
        {"elemento": "Compartir viajes con amigos o colegas", "ahorro_estimado": 25}
    ],
    "ocio": [
        {"elemento": "Optar por actividades gratuitas o de bajo costo", "ahorro_estimado": 30},
        {"elemento": "Reducir la suscripción a servicios de transmisión", "ahorro_estimado": 15},
        {"elemento": "Buscar ofertas y descuentos en entretenimiento", "ahorro_estimado": 20}
    ],
    "servicios públicos": [
        {"elemento": "Reducir el consumo de electricidad apagando luces y dispositivos", "ahorro_estimado": 40},
        {"elemento": "Aislar ventanas y puertas para mejorar la eficiencia energética", "ahorro_estimado": 25},
        {"elemento": "Programar el termostato para un uso eficiente de la calefacción y refrigeración", "ahorro_estimado": 35}
    ],
    "compras": [
        {"elemento": "Comparar precios antes de realizar compras grandes", "ahorro_estimado": 50},
        {"elemento": "Utilizar cupones y descuentos en línea", "ahorro_estimado": 20},
        {"elemento": "Comprar productos genéricos en lugar de marcas de lujo", "ahorro_estimado": 30}
    ]
}

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
        consejos = elementos_y_ahorros["alimentos"]
    elif "transporte" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[1]})
        consejos = elementos_y_ahorros["transporte"]
    elif "ocio" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[2]})
        consejos = elementos_y_ahorros["ocio"]
    elif "servicios públicos" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[3]})
        consejos = elementos_y_ahorros["servicios públicos"]
    elif "compras" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": prompts[4]})
        consejos = elementos_y_ahorros["compras"]

    # La conversación continuará proporcionando consejos en la categoría elegida.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)

    # Mostrar los consejos y ahorros estimados con la opción de revelar el ahorro al hacer clic en un botón
    for consejo in consejos:
        if st.button(f"Revelar ahorro para '{consejo['elemento']}'"):
            st.info(f"Ahorro estimado para '{consejo['elemento']}': ${consejo['ahorro_estimado']}")

# Mostrar el ahorro total calculado
if st.button("Calcular ahorro total"):
    ahorro_total = sum(consejo.get("ahorro_estimado", 0) for consejo in consejos)
        st.info(f"Ahorro total estimado en esta categoría: ${ahorro_total}")

# Calcular el ahorro total en todas las categorías
ahorro_total_total = sum(sum(consejo.get("ahorro_estimado", 0) for consejo in consejos) for consejos in elementos_y_ahorros.values())

# Mostrar el ahorro total en todas las categorías
if st.button("Calcular ahorro total en todas las categorías"):
    st.info(f"Ahorro total estimado en todas las categorías: ${ahorro_total_total}")

