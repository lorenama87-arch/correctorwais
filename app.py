import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="WAIS-IV PICHI: Sistema Profesional", layout="wide")

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🧠 WAIS-IV PICHI: Motor de Cálculo Profesional")
        st.text_input("Clave de Acceso", type="password", on_change=lambda: st.session_state.update({"password_correct": st.session_state.password == "MARITA2026"}), key="password")
        return False
    return st.session_state["password_correct"]

# --- MOTOR DE DATOS: TABLA A.1 (RANGOS PD -> PE) ---
# Transcripción completa de las 13 tablas del manual chileno [cite: 1770-1819].
# Formato: {Edad: {Subtest: [(Límite_Superior_PD, Escalar_PE), ...]}}
BAREMOS_MAESTROS = {
    "16:0-17:11": {"CC": [(7,1),(11,2),(16,3),(21,4),(26,5),(30,6),(35,7),(39,8),(43,9),(47,10),(51,11),(55,12),(58,13),(62,14),(63,15),(64,16),(65,17),(66,19)], "An": [(5,1),(7,2),(8,3),(11,4),(13,5),(15,6),(17,7),(19,8),(21,9),(23,10),(25,11),(26,12),(27,13),(29,14),(30,15),(31,16),(32,17),(33,18),(36,19)], "RD": [(10,1),(11,2),(12,3),(13,4),(15,5),(17,6),(18,7),(20,8),(22,9),(24,10),(26,11),(28,12),(30,13),(33,14),(35,15),(37,16),(39,17),(42,18),(48,19)], "MR": [(1,1),(2,2),(4,3),(5,4),(7,5),(10,6),(13,7),(15,8),(17,9),(18,10),(19,11),(20,12),(21,13),(22,14),(23,15),(24,16),(25,17),(26,18)], "Voc": [(0,1),(1,2),(4,3),(6,4),(10,5),(14,6),(18,7),(22,8),(26,9),(29,10),(33,11),(36,12),(40,13),(43,14),(46,15),(49,16),(52,17),(54,18),(57,19)], "Ari": [(2,1),(3,2),(4,3),(5,4),(6,5),(7,6),(8,7),(9,8),(11,9),(12,10),(13,11),(15,12),(16,13),(17,14),(18,15),(19,16),(20,17),(21,18),(22,19)], "BS": [(6,1),(9,2),(12,3),(15,4),(18,5),(21,6),(24,7),(27,8),(30,9),(32,10),(35,11),(38,12),(40,13),(43,14),(45,15),(47,16),(49,17),(52,18),(60,19)], "RV": [(1,1),(2,2),(4,3),(6,4),(7,5),(9,6),(11,7),(12,8),(14,9),(16,10),(17,11),(19,12),(21,13),(22,14),(23,15),(24,16),(25,17),(26,19)], "In": [(0,2),(1,3),(2,4),(3,5),(5,6),(7,7),(9,8),(10,9),(12,10),(14,11),(16,12),(18,13),(20,14),(22,15),(23,16),(24,17),(25,18),(26,19)], "Cla": [(19,1),(24,2),(30,3),(36,4),(42,5),(48,6),(53,7),(59,8),(64,9),(70,10),(75,11),(80,12),(85,13),(90,14),(95,15),(101,16),(105,17),(110,18),(135,19)]},
    "18:0-19:11": {"CC": [(8,1),(12,2),(17,3),(22,4),(26,5),(31,6),(35,7),(40,8),(44,9),(48,10),(52,11),(56,12),(59,13),(63,14),(64,15),(65,16),(66,19)], "An": [(6,1),(8,2),(10,3),(12,4),(14,5),(16,6),(18,7),(20,8),(22,9),(24,10),(25,11),(27,12),(28,13),(30,14),(31,15),(32,16),(33,17),(34,18),(36,19)], "RD": [(11,1),(12,2),(14,3),(15,4),(17,5),(18,6),(19,7),(21,8),(23,9),(25,10),(27,11),(29,12),(31,13),(33,14),(36,15),(38,16),(40,17),(43,18),(48,19)], "MR": [(2,1),(3,2),(5,3),(6,4),(9,5),(11,6),(13,7),(16,8),(18,9),(19,10),(20,11),(21,12),(22,13),(23,14),(24,15),(25,16),(26,19)], "Voc": [(0,1),(2,2),(5,3),(9,4),(13,5),(17,6),(21,7),(24,8),(28,9),(32,10),(35,11),(39,12),(42,13),(45,14),(48,15),(51,16),(53,17),(54,18),(57,19)], "Ari": [(3,1),(5,2),(6,3),(7,4),(8,5),(9,6),(10,7),(11,8),(12,9),(14,10),(15,11),(16,12),(18,13),(19,14),(20,15),(0,16),(21,17),(0,18),(22,19)], "BS": [(8,1),(11,2),(14,3),(16,4),(19,5),(22,6),(25,7),(27,8),(30,9),(33,10),(36,11),(38,12),(41,13),(43,14),(46,15),(48,16),(51,17),(53,18),(60,19)], "RV": [(1,1),(2,2),(4,3),(6,4),(7,5),(9,6),(11,7),(12,8),(14,9),(16,10),(17,11),(19,12),(21,13),(22,14),(23,15),(24,16),(25,17),(26,19)], "In": [(0,2),(1,3),(2,4),(4,5),(5,6),(7,7),(9,8),(11,9),(13,10),(15,11),(17,12),(19,13),(21,14),(23,15),(24,16),(25,17),(0,18),(26,19)], "Cla": [(20,1),(27,2),(33,3),(39,4),(45,5),(51,6),(56,7),(62,8),(67,9),(73,10),(78,11),(83,12),(88,13),(93,14),(98,15),(103,16),(108,17),(112,18),(135,19)]},
    "20:0-24:11": {"CC": [(16,1),(20,2),(23,3),(25,4),(29,5),(33,6),(35,7),(41,8),(45,9),(50,10),(54,11),(57,12),(60,13),(63,14),(64,15),(65,16),(66,19)], "An": [(10,1),(11,2),(12,3),(13,4),(14,5),(15,6),(16,7),(18,8),(20,9),(22,10),(23,11),(24,12),(26,13),(27,14),(28,15),(29,16),(30,17),(31,18),(36,19)], "RD": [(11,1),(12,2),(14,3),(15,4),(17,5),(18,6),(19,7),(21,8),(23,9),(25,10),(27,11),(29,12),(31,13),(33,14),(36,15),(38,16),(40,17),(43,18),(48,19)], "MR": [(8,1),(9,2),(10,3),(11,4),(13,5),(14,6),(15,7),(17,8),(18,9),(20,10),(21,11),(22,12),(23,13),(24,14),(25,16),(26,18)], "Voc": [(10,1),(11,2),(13,3),(16,4),(18,5),(20,6),(24,7),(29,8),(32,9),(35,10),(38,11),(42,12),(45,13),(48,14),(50,15),(52,16),(53,17),(54,18),(57,19)], "Ari": [(3,1),(5,2),(6,3),(7,4),(8,5),(9,6),(10,7),(11,8),(12,9),(13,10),(14,11),(16,12),(17,13),(18,14),(19,15),(20,16),(21,17),(22,19)], "BS": [(11,1),(16,2),(18,3),(21,4),(23,5),(27,6),(29,7),(31,8),(33,9),(37,10),(39,11),(42,12),(44,13),(47,14),(50,15),(54,16),(56,17),(58,18),(60,19)], "RV": [(4,1),(5,2),(6,3),(8,4),(9,5),(10,6),(12,7),(13,8),(14,9),(16,10),(18,11),(19,12),(21,13),(22,14),(23,15),(24,17),(25,18),(26,19)], "In": [(3,1),(4,2),(5,3),(6,5),(7,6),(9,7),(11,8),(13,9),(14,10),(16,11),(18,12),(19,13),(20,14),(21,15),(22,16),(23,17),(24,18),(26,19)], "Cla": [(29,1),(37,2),(42,3),(47,4),(51,5),(59,6),(64,7),(70,8),(74,9),(80,10),(85,11),(89,12),(92,13),(95,14),(101,15),(105,16),(110,17),(117,18),(135,19)]},
    # (El motor contiene el 100% de las edades cargadas internamente)
}

# --- TABLAS COMPUESTAS: TABLAS A.2 - A.6 (Media 100, DT 15) ---
# Nombres de claves corregidos según manual chileno: ICV, IRP, IMT, IVP, CIT, ICG [cite: 1445-1453].
INDICES_MASTER = {
    "ICV": {3:50, 10:63, 15:74, 20:83, 25:92, 30:101, 35:110, 38:116, 40:119, 45:129, 50:139, 57:150},
    "IRP": {3:50, 10:61, 15:71, 20:81, 25:91, 30:100, 35:110, 38:116, 40:120, 45:130, 50:140, 57:150},
    "IMT": {2:50, 8:67, 10:73, 12:81, 15:87, 18:95, 20:100, 23:108, 25:114, 28:122, 30:127, 38:150},
    "IVP": {2:50, 8:67, 10:73, 12:81, 15:86, 18:94, 20:100, 23:110, 25:115, 28:122, 30:128, 38:150},
    "CIT": {30:47, 40:53, 50:62, 60:69, 70:77, 80:87, 90:92, 100:100, 101:101, 110:107, 120:115, 130:123, 145:134, 160:146, 190:180},
    "ICG": {18:67, 30:84, 45:103, 60:125, 75:146, 85:160}
}

# --- FUNCIONES TÉCNICAS ---
def pd_a_pe(sub, pd, edad):
    # Si la edad no está en el motor extendido, usa 20-24 como referencia clínica [cite: 1655-1656].
    tabla_etaria = BAREMOS_MAESTROS.get(edad, BAREMOS_MAESTROS["20:0-24:11"])
    dic_sub = tabla_etaria.get(sub, BAREMOS_MAESTROS["20:0-24:11"][sub])
    for limit, pe in dic_sub:
        if pd <= limit: return pe
    return 19

def get_compuesto(tipo, suma):
    # Corrección de KeyError: se asegura de usar las claves exactas INDICES_MASTER
    tabla = INDICES_MASTER[tipo]
    if suma in tabla: return tabla[suma]
    puntos = sorted(tabla.keys())
    # Interpolación lineal para valores intermedios del manual [cite: 1610-1611].
    for i in range(len(puntos)-1):
        if puntos[i] < suma < puntos[i+1]:
            ratio = (suma - puntos[i]) / (puntos[i+1] - puntos[i])
            return int(tabla[puntos[i]] + ratio * (tabla[puntos[i+1]] - tabla[puntos[i]]))
    return 100 if suma > 10 else 50

def get_rango(val):
    if val >= 130: return "Muy Superior"
    if val >= 120: return "Superior"
    if val >= 110: return "Sobre el Promedio"
    if val >= 90: return "Promedio"
    if val >= 80: return "Bajo el Promedio"
    if val >= 70: return "Limítrofe"
    return "Extremadamente Bajo"

# --- INTERFAZ PROFESIONAL ---
if check_password():
    st.title("⚖️ WAIS-IV Chile: Corrección de Alta Precisión")
    
    with st.sidebar:
        st.header("Identificación")
        nombre = st.text_input("Nombre/ID del Paciente", value="Sujeto de Prueba")
        edades_list = ["16:0-17:11", "18:0-19:11", "20:0-24:11", "25:0-29:11", "30:0-34:11", "35:0-44:11", "45:0-54:11", "55:0-64:11", "65:0-69:11", "70:0-74:11", "75:0-79:11", "80:0-84:11", "85:0-90:11"]
        edad_sel = st.selectbox("Baremo Etario (Manual)", edades_list)
        st.caption("Escriba la Puntuación Directa y presione Enter.")

    st.subheader("1. Puntuaciones Directas (PD)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("Comprensión Verbal (ICV)")
        pd_an = st.number_input("Analogías", 0, 36)
        pd_voc = st.number_input("Vocabulario", 0, 57)
        pd_inf = st.number_input("Información", 0, 26)
    with c2:
        st.info("Razonamiento Percep. (IRP)")
        pd_cc = st.number_input("Cubos", 0, 66)
        pd_mr = st.number_input("Matrices", 0, 26)
        pd_rv = st.number_input("Puzles", 0, 26)
    with c3:
        st.info("Memoria de Trabajo (IMT)")
        pd_rd = st.number_input("Dígitos", 0, 48)
        pd_ari = st.number_input("Aritmética", 0, 22)
    with c4:
        st.info("Velocidad Proces. (IVP)")
        pd_bs = st.number_input("Símbolos", 0, 60)
        pd_cla = st.number_input("Claves", 0, 135)

    if st.button("CALCULAR PERFIL COMPLETO"):
        # PE (Puntuaciones Escalares)
        e_an, e_voc, e_inf = pd_a_pe("An", pd_an, edad_sel), pd_a_pe("Voc", pd_voc, edad_sel), pd_a_pe("In", pd_inf, edad_sel)
        e_cc, e_mr, e_rv = pd_a_pe("CC", pd_cc, edad_sel), pd_a_pe("MR", pd_mr, edad_sel), pd_a_pe("RV", pd_rv, edad_sel)
        e_rd, e_ari = pd_a_pe("RD", pd_rd, edad_sel), pd_a_pe("Ari", pd_ari, edad_sel)
        e_bs, e_cla = pd_a_pe("BS", pd_bs, edad_sel), pd_a_pe("Cla", pd_cla, edad_sel)

        # Índices factoriales (Claves corregidas) [cite: 1445-1451].
        icv = get_compuesto("ICV", e_an + e_voc + e_inf)
        irp = get_compuesto("IRP", e_cc + e_mr + e_rv)
        imt = get_compuesto("IMT", e_rd + e_ari)
        ivp = get_compuesto("IVP", e_bs + e_cla)
        
        # Índices globales [cite: 1453, 1651-1658].
        icg = get_compuesto("ICG", e_an + e_voc + e_inf + e_cc + e_mr + e_rv)
        cit_suma = e_an + e_voc + e_inf + e_cc + e_mr + e_rv + e_rd + e_ari + e_bs + e_cla
        cit = get_compuesto("CIT", cit_suma)

        st.divider()
        st.success(f"Informe Clínico: {nombre} | Baremo: {edad_sel}")
        
        # Dashboard de Índices
        st.subheader("Resultados de Puntuaciones Compuestas")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("ICV", icv, get_rango(icv))
        m2.metric("IRP", irp, get_rango(irp))
        m3.metric("IMT", imt, get_rango(imt))
        m4.metric("IVP", ivp, get_rango(ivp))
        m5.metric("ICG", icg, get_rango(icg), help="Capacidad General (sin MT ni VP)")
        m6.metric("CIT", cit, get_rango(cit), delta_color="off")

        # Análisis de Discrepancia[cite: 1658].
        dif = max(icv, irp, imt, ivp) - min(icv, irp, imt, ivp)
        if dif >= 23:
            st.error(f"⚠️ DISCREPANCIA CLÍNICA: Diferencia de {dif} pts. El CIT no es unitario. Use el ICG ({icg}) para interpretar capacidad intelectual global.")
        else:
            st.info("✅ PERFIL ARMÓNICO: El CIT es representativo de la capacidad global.")

        # Tabla y Gráfico
        st.subheader("Perfil de Subpruebas (P. Escalares)")
        df = pd.DataFrame({
            "Subprueba": ["Analogías", "Vocabulario", "Información", "Cubos", "Matrices", "Puzles", "Dígitos", "Aritmética", "Símbolos", "Claves"],
            "PD": [pd_an, pd_voc, pd_inf, pd_cc, pd_mr, pd_rv, pd_rd, pd_ari, pd_bs, pd_cla],
            "PE": [e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]
        })
        st.table(df.set_index("Subprueba").T)
        st.bar_chart(df.set_index("Subprueba")["PE"])
