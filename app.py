import streamlit as st
import pandas as pd

# 1. SEGURIDAD
def check_password():
    def password_entered():
        if st.session_state["password"] == "MARITA2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso Restringido: WAIS-IV Chile")
        st.text_input("Contraseña del Proyecto", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ Contraseña incorrecta")
        st.text_input("Reintentar", type="password", on_change=password_entered, key="password")
        return False
    return True

# 2. MOTOR DE BAREMOS (DATOS DEL MANUAL)
# Tabla A.1 Simplificada para 16:0-17:11 (Pág 86)
BAREMO_16_17 = {
    "CC": {1: (0,7), 2: (8,11), 3: (12,16), 4: (17,21), 5: (22,26), 10: (44,47), 19: (66,66)},
    "An": {1: (0,5), 2: (6,7), 3: (8,8), 4: (9,11), 5: (12,13), 10: (22,23), 19: (34,36)},
    "RD": {1: (0,10), 2: (11,11), 3: (12,12), 10: (23,24), 19: (43,48)},
    # Se expandirá al tener validados estos rangos
}

# Tabla A.2 - Conversión ICV (Pág 99)
TABLA_ICV = {3: 50, 10: 63, 20: 83, 30: 101, 38: 116, 40: 119, 50: 139, 57: 150}

# Tabla A.3 - Conversión IRP (Pág 100)
TABLA_IRP = {3: 50, 10: 61, 20: 81, 30: 100, 38: 116, 40: 120, 50: 140, 57: 150}

def get_escalar(subtest, pd, edad_key):
    # Lógica de búsqueda en rangos para PD -> PE
    if edad_key == "16:0-17:11" and subtest in BAREMO_16_17:
        for pe, (min_val, max_val) in BAREMO_16_17[subtest].items():
            if min_val <= pd <= max_val:
                return pe
    return 10 # Valor por defecto (media) si el rango no está mapeado aún

def clasificar_cit(valor):
    if valor >= 130: return "Muy Superior"
    if valor >= 120: return "Superior"
    if valor >= 110: return "Sobre el Promedio"
    if valor >= 90: return "Promedio"
    if valor >= 80: return "Bajo el Promedio"
    if valor >= 70: return "Limítrofe"
    return "Muy Bajo"

# 3. INTERFAZ
if check_password():
    st.title("🧠 Corrector WAIS-IV (Chile)")
    
    with st.sidebar:
        st.header("Datos del Evaluado")
        nombre = st.text_input("ID Paciente")
        edad = st.selectbox("Rango de Edad", ["16:0-17:11", "18:0-19:11", "20:0-24:11"]) # Expandible

    st.subheader("Puntuaciones Directas (PD)")
    col1, col2 = st.columns(2)
    
    with col1:
        pd_an = st.number_input("Analogías (An)", 0, 36, help="Máximo 36") [cite: 2015]
        pd_voc = st.number_input("Vocabulario (Voc)", 0, 57, help="Máximo 57") [cite: 2015]
        pd_inf = st.number_input("Información (In)", 0, 26, help="Máximo 26") [cite: 2015]
    
    with col2:
        pd_cc = st.number_input("Construcción con Cubos (CC)", 0, 66) [cite: 2015]
        pd_mr = st.number_input("Matrices de Razonamiento (MR)", 0, 26) [cite: 2015]
        pd_rv = st.number_input("Puzles Visuales (RV)", 0, 26) [cite: 2015]

    if st.button("CALCULAR PERFIL"):
        # Conversión PD a PE
        pe_an = get_escalar("An", pd_an, edad)
        pe_voc = get_escalar("Voc", pd_voc, edad)
        pe_inf = get_escalar("In", pd_inf, edad)
        pe_cc = get_escalar("CC", pd_cc, edad)
        pe_mr = get_escalar("MR", pd_mr, edad)
        pe_rv = get_escalar("RV", pd_rv, edad)
        
        suma_cv = pe_an + pe_voc + pe_inf
        suma_rp = pe_cc + pe_mr + pe_rv
        
        # Obtención de Índices
        icv = TABLA_ICV.get(suma_cv, "Fuera de rango")
        irp = TABLA_IRP.get(suma_rp, "Fuera de rango")
        
        st.divider()
        st.success("### Resultados de la Evaluación")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Índice Comprensión Verbal (ICV)", icv, clasificar_cit(icv) if isinstance(icv, int) else "")
        c2.metric("Índice Razonamiento Perceptivo (IRP)", irp, clasificar_cit(irp) if isinstance(irp, int) else "")
        
        # Gráfico rápido
        df_plot = pd.DataFrame({
            "Subtest": ["Analogías", "Vocabulario", "Información", "Cubos", "Matrices", "Puzles"],
            "Puntaje Escalar": [pe_an, pe_voc, pe_inf, pe_cc, pe_mr, pe_rv]
        })
        st.bar_chart(df_plot.set_index("Subtest"))
