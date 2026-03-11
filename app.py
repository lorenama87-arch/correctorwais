import streamlit as st

# 1. Configuración de seguridad básica
def check_password():
    """Devuelve True si el usuario introdujo la contraseña correcta."""
    def password_entered():
        if st.session_state["password"] == "MARITA2026": # <--- CAMBIA TU CONTRASEÑA AQUÍ
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # No guardar la contraseña en el estado
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Pantalla de inicio de sesión
        st.title("🔐 Acceso al Corrector WAIS-IV")
        st.text_input("Introduce la contraseña del proyecto", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Contraseña incorrecta
        st.text_input("Contraseña incorrecta. Inténtalo de nuevo", type="password", on_change=password_entered, key="password")
        st.error("😕 Acceso denegado")
        return False
    else:
        return True

# 2. Si el login es correcto, ejecutamos la App
if check_password():
    st.title("🧠 Calculadora de Puntuaciones WAIS-IV")
    st.sidebar.header("Datos del Sujeto")
    
    nombre = st.sidebar.text_input("ID / Iniciales")
    edad = st.sidebar.number_input("Edad (años)", min_value=16, max_value=90, value=25)
    
    st.write(f"### Introducción de Puntuaciones Directas (PD)")
    
    # Creamos columnas para organizar los subtests
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Comprensión Verbal (VCI)")
        semejanzas = st.number_input("Semejanzas", min_value=0, max_value=36)
        vocabulario = st.number_input("Vocabulario", min_value=0, max_value=57)
        informacion = st.number_input("Información", min_value=0, max_value=26)
        
    with col2:
        st.subheader("Razonamiento Perceptivo (PRI)")
        cubos = st.number_input("Cubos", min_value=0, max_value=66)
        matrices = st.number_input("Matrices", min_value=0, max_value=26)
        puzles = st.number_input("Puzles Visuales", min_value=0, max_value=26)

    # Botón para calcular
    if st.button("Calcular Puntuaciones Escalares"):
        # Aquí es donde programaremos la lógica de los baremos
        st.success("Cálculo realizado (Lógica de baremos pendiente de cargar)")
        
        # Ejemplo de cómo se vería un resultado
        st.metric(label="VCI Estimado", value="115", delta="Media Alta")
