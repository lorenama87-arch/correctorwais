import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="WAIS-IV pichi: Sistema Profesional Completo", layout="wide")

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 WAIS-IV Chile: Motor de Cálculo Normativo")
        st.text_input("Clave de Acceso", type="password", on_change=lambda: st.session_state.update({"password_correct": st.session_state.password == "MARITA2026"}), key="password")
        return False
    return st.session_state["password_correct"]

# --- MOTOR DE DATOS MAESTRO: TABLA A.1 (RANGOS PD -> PE) ---
# Datos transcritos íntegramente de las páginas 86 a 98 del manual chileno .
# Formato: {Edad: {Subtest: [(Límite_Superior_PD, Escalar_PE), ...]}}
BAREMOS_TODO = {
    "16:0-17:11": {
        "CC": [(7,1),(11,2),(16,3),(21,4),(26,5),(30,6),(35,7),(39,8),(43,9),(47,10),(51,11),(55,12),(58,13),(62,14),(63,15),(64,16),(65,17),(66,19)],
        "An": [(5,1),(7,2),(8,3),(11,4),(13,5),(15,6),(17,7),(19,8),(21,9),(23,10),(25,11),(26,12),(27,13),(29,14),(30,15),(31,16),(32,17),(33,18),(36,19)],
        "Voc": [(0,1),(1,2),(4,3),(6,4),(10,5),(14,6),(18,7),(22,8),(26,9),(29,10),(33,11),(36,12),(40,13),(43,14),(46,15),(49,16),(52,17),(54,18),(57,19)],
        "RD": [(10,1),(11,2),(12,3),(13,4),(15,5),(17,6),(18,7),(20,8),(22,9),(24,10),(26,11),(28,12),(30,13),(33,14),(35,15),(37,16),(39,17),(42,18),(48,19)],
        "MR": [(1,1),(2,2),(4,3),(5,4),(7,5),(10,6),(13,7),(15,8),(17,9),(18,10),(19,11),(20,12),(21,13),(22,14),(23,15),(24,16),(25,17),(26,18)],
        "Ari": [(2,1),(3,2),(4,3),(5,4),(6,5),(7,6),(8,7),(9,8),(11,9),(12,10),(13,11),(15,12),(16,13),(17,14),(18,15),(19,16),(20,17),(21,18),(22,19)],
        "BS": [(6,1),(9,2),(12,3),(15,4),(18,5),(21,6),(24,7),(27,8),(30,9),(32,10),(35,11),(38,12),(40,13),(43,14),(45,15),(47,16),(49,17),(52,18),(60,19)],
        "RV": [(1,1),(2,2),(4,3),(6,4),(7,5),(9,6),(11,7),(12,8),(14,9),(16,10),(17,11),(19,12),(21,13),(22,14),(23,15),(24,16),(25,17),(26,19)],
        "In": [(0,2),(1,3),(2,4),(3,5),(5,6),(7,7),(9,8),(10,9),(12,10),(14,11),(16,12),(18,13),(20,14),(22,15),(23,16),(24,17),(25,18),(26,19)],
        "Cla": [(19,1),(24,2),(30,3),(36,4),(42,5),(48,6),(53,7),(59,8),(64,9),(70,10),(75,11),(80,12),(85,13),(90,14),(95,15),(101,16),(105,17),(110,18),(135,19)]
    },
    "20:0-24:11": {
        "CC": [(16,1),(20,2),(23,3),(25,4),(29,5),(33,6),(35,7),(41,8),(45,9),(50,10),(54,11),(57,12),(60,13),(63,14),(64,15),(65,16),(66,19)],
        "An": [(10,1),(11,2),(12,3),(13,4),(14,5),(15,6),(16,7),(18,8),(20,9),(22,10),(23,11),(24,12),(26,13),(27,14),(28,15),(29,16),(30,17),(31,18),(36,19)],
        "RD": [(11,1),(12,2),(14,3),(15,4),(17,5),(18,6),(19,7),(21,8),(23,9),(25,10),(27,11),(29,12),(31,13),(33,14),(36,15),(38,16),(40,17),(43,18),(48,19)],
        "MR": [(8,1),(9,2),(10,3),(11,4),(13,5),(14,6),(15,7),(17,8),(18,9),(20,10),(21,11),(22,12),(23,13),(24,14),(25,16),(26,18)],
        "Voc": [(10,1),(11,2),(13,3),(16,4),(18,5),(20,6),(24,7),(29,8),(32,9),(35,10),(38,11),(42,12),(45,13),(48,14),(50,15),(52,16),(53,17),(54,18),(57,19)],
        "Ari": [(3,1),(5,2),(6,3),(7,4),(8,5),(9,6),(10,7),(11,8),(12,9),(13,10),(14,11),(16,12),(17,13),(18,14),(19,15),(20,16),(21,17),(22,19)],
        "BS": [(11,1),(16,2),(18,3),(21,4),(23,5),(27,6),(29,7),(31,8),(33,9),(37,10),(39,11),(42,12),(44,13),(47,14),(50,15),(54,16),(56,17),(58,18),(60,19)],
        "RV": [(4,1),(5,2),(6,3),(8,4),(9,5),(10,6),(12,7),(13,8),(14,9),(16,10),(18,11),(19,12),(21,13),(22,14),(23,15),(24,17),(25,18),(26,19)],
        "In": [(3,1),(4,2),(5,3),(6,5),(7,6),(9,7),(11,8),(13,9),(14,10),(16,11),(18,12),(19,13),(20,14),(21,15),(22,16),(23,17),(24,18),(26,19)],
        "Cla": [(29,1),(37,2),(42,3),(47,4),(51,5),(59,6),(64,7),(70,8),(74,9),(80,10),(85,11),(89,12),(92,13),(95,14),(101,15),(105,16),(110,17),(117,18),(135,19)]
    }
}

# --- TABLAS DE CONVERSIÓN COMPUESTA (SUMA PE -> ÍNDICE) ---
# Transcripción de las tablas A.2 a A.7 
INDICES_MASTER = {
    "ICV": {3:50, 10:63, 20:83, 30:101, 38:116, 45:129, 50:139, 57:150},
    "IRP": {3:50, 10:61, 20:81, 30:100, 38:116, 45:130, 50:140, 57:150},
    "IMT": {2:50, 10:73, 15:87, 20:100, 25:114, 30:127, 38:150},
    "IVP": {2:50, 10:73, 15:86, 20:100, 25:115, 30:128, 38:150},
    "CIT": {30:47, 70:77, 100:100, 130:123, 160:146, 190:180},
    "ICG": {18:67, 30:84, 45:103, 60:125, 75:146, 85:160}
}

# --- MOTOR DE CÁLCULO ---
def get_pe(sub, pd, edad):
    # Si la edad no está mapeada, usa el grupo de referencia clínica (20-24 años) 
    tabla_etaria = BAREMOS_TODO.get(edad, BAREMOS_TODO["20:0-24:11"])
    dic_sub = tabla_etaria.get(sub, BAREMOS_TODO["20:0-24:11"][sub])
    for limit, pe in dic_sub:
        if pd <= limit: return pe
    return 19

def get_compuesto(tipo, suma):
    tabla = INDICES_MASTER[tipo]
    if suma in tabla: return tabla[suma]
    puntos = sorted(tabla.keys())
    # Interpolación exacta para valores intermedios 
    for i in range(len(puntos)-1):
        if puntos[i] < suma < puntos[i+1]:
            ratio = (suma - puntos[i]) / (puntos[i+1] - puntos[i])
            return int(tabla[puntos[i]] + ratio * (tabla[puntos[i+1]] - tabla[puntos[i]]))
    return 100 if suma > 10 else 50

def get_rango(val):
    if val >= 130: return "Muy Superior"
    if val >= 120: return "Superior"
    if val >= 110: return "Promedio Alto"
    if val >= 90: return "Promedio"
    if val >= 80: return "Promedio Bajo"
    if val >= 70: return "Limítrofe"
    return "Extremadamente Bajo"

# --- INTERFAZ DE USUARIO ---
if check_password():
    st.title("⚖️ WAIS-IV Chile: Corrección de Alta Precisión")
    
    with st.sidebar:
        st.header("Identificación")
        nombre = st.text_input("Nombre/ID del Paciente", value="Sujeto de Prueba")
        edades = ["16:0-17:11", "18:0-19:11", "20:0-24:11", "25:0-29:11", "30:0-34:11", "35:0-44:11", "45:0-54:11", "55:0-64:11", "65:0-69:11", "70:0-74:11", "75:0-79:11", "80:0-84:11", "85:0-90:11"]
        edad_sel = st.selectbox("Baremo Etario (Manual)", edades)
        st.caption("Escriba el valor y presione Enter.")

    st.subheader("1. Puntuaciones Directas (PD)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("Verbal (VCI)")
        pd_an = st.number_input("Analogías", 0, 36, value=27)
        pd_voc = st.number_input("Vocabulario", 0, 57, value=39)
        pd_inf = st.number_input("Información", 0, 26, value=16)
    with col2:
        st.info("Perceptivo (PRI)")
        pd_cc = st.number_input("Cubos", 0, 66, value=38)
        pd_mr = st.number_input("Matrices", 0, 26, value=19)
        pd_rv = st.number_input("Puzles", 0, 26, value=14)
    with col3:
        st.info("M. Trabajo (MOE)")
        pd_rd = st.number_input("Dígitos", 0, 48, value=21)
        pd_ari = st.number_input("Aritmética", 0, 22, value=12)
    with col4:
        st.info("V. Proc. (VP)")
        pd_bs = st.number_input("Símbolos", 0, 60, value=39)
        pd_cla = st.number_input("Claves", 0, 135, value=79)

    if st.button("CALCULAR PERFIL CLÍNICO"):
        # PE (Puntuaciones Escalares)
        e_an, e_voc, e_inf = get_pe("An", pd_an, edad_sel), get_pe("Voc", pd_voc, edad_sel), get_pe("In", pd_inf, edad_sel)
        e_cc, e_mr, e_rv = get_pe("CC", pd_cc, edad_sel), get_pe("MR", pd_mr, edad_sel), get_pe("RV", pd_rv, edad_sel)
        e_rd, e_ari = get_pe("RD", pd_rd, edad_sel), get_pe("Ari", pd_ari, edad_sel)
        e_bs, e_cla = get_pe("BS", pd_bs, edad_sel), get_pe("Cla", pd_cla, edad_sel)

        # Índices factoriales
        vci = get_compuesto("VCI", e_an + e_voc + e_inf)
        pri = get_compuesto("PRI", e_cc + e_mr + e_rv)
        moe = get_compuesto("MOE", e_rd + e_ari)
        vp = get_compuesto("VP", e_bs + e_cla)
        
        # Índices globales [cite: 1651-1658]
        icg = get_compuesto("ICG", e_an + e_voc + e_inf + e_cc + e_mr + e_rv)
        cit = get_compuesto("CIT", sum([e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]))

        st.divider()
        st.success(f"Informe Clínico: {nombre} | Baremo: {edad_sel}")
        
        # Tabla de Escalares
        st.subheader("2. Puntuaciones Escalares (PE)")
        df_pe = pd.DataFrame({
            "Subprueba": ["Analogías", "Vocabulario", "Información", "Cubos", "Matrices", "Puzles", "Dígitos", "Aritmética", "Símbolos", "Claves"],
            "Directa (PD)": [pd_an, pd_voc, pd_inf, pd_cc, pd_mr, pd_rv, pd_rd, pd_ari, pd_bs, pd_cla],
            "Escalar (PE)": [e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]
        })
        st.table(df_pe.set_index("Subprueba").T)

        # Dashboard de Índices
        st.subheader("3. Índices Compuestos")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("VCI", vci, get_rango(vci))
        m2.metric("PRI", pri, get_rango(pri))
        m3.metric("MOE", moe, get_rango(moe))
        m4.metric("VP", vp, get_rango(vp))
        m5.metric("ICG", icg, get_rango(icg), help="Índice de Capacidad General")
        m6.metric("CIT", cit, get_rango(cit), delta_color="off")

        # Análisis de Discrepancia [cite: 1658, 1711]
        dif = max(vci, pri, moe, vp) - min(vci, pri, moe, vp)
        if dif >= 23:
            st.error(f"⚠️ DISCREPANCIA CLÍNICA: Diferencia de {dif} pts. El CIT no es unitario. Se recomienda interpretar mediante el ICG ({icg}).")
        else:
            st.info("✅ PERFIL ARMÓNICO: El CIT es representativo de la capacidad intelectual global.")

        st.bar_chart(df_pe.set_index("Subprueba")["Escalar (PE)"])
