import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="WAIS-IV Chile: Sistema de Alta Precisión", layout="wide")

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 WAIS-IV Pich: Acceso Profesional")
        st.text_input("Clave de Acceso", type="password", on_change=lambda: st.session_state.update({"password_correct": st.session_state.password == "MARITA2026"}), key="password")
        return False
    return st.session_state["password_correct"]

# --- MOTOR DE RANGOS: TABLA A.1 ---
BAREMOS_RANGOS = {
    "16:0-17:11": {
        "CC": {1:(0,7), 10:(44,47), 19:(66,66)},
        "An": {1:(0,5), 10:(22,23), 19:(34,36)},
        "RD": {1:(0,10), 10:(23,24), 19:(43,48)},
        "MR": {1:(0,1), 10:(18,18), 18:(26,26)},
        "Voc": {1:(0,0), 10:(27,29), 19:(55,57)},
        "Ari": {1:(0,2), 10:(12,12), 19:(22,22)},
        "BS": {1:(0,6), 10:(31,32), 19:(53,60)},
        "RV": {1:(0,1), 10:(15,16), 19:(26,26)},
        "In": {1:(0,0), 10:(11,12), 19:(26,26)},
        "Cla": {1:(0,19), 10:(65,70), 19:(111,135)}
    },
    "20:0-24:11": {
        "CC": {1:(0,16), 10:(46,50), 19:(66,66)},
        "An": {1:(0,10), 10:(21,22), 19:(32,36)},
        "RD": {1:(0,11), 10:(25,26), 19:(44,48)},
        "MR": {1:(0,8), 10:(19,20), 18:(26,26)},
        "Voc": {1:(0,10), 10:(32,35), 19:(51,57)},
        "Ari": {1:(0,3), 10:(12,12), 19:(22,22)},
        "BS": {1:(0,11), 10:(34,37), 19:(59,60)},
        "RV": {1:(0,4), 10:(16,16), 19:(26,26)},
        "In": {1:(0,3), 10:(14,14), 19:(25,26)},
        "Cla": {1:(0,29), 10:(75,80), 19:(118,135)}
    }
}

# --- TABLAS COMPUESTAS (Páginas 99-105) ---
INDICES_CL = {
    "VCI": {9:61, 20:83, 30:101, 38:116, 45:129, 57:150},
    "PRI": {9:59, 20:81, 30:100, 38:116, 45:130, 57:150},
    "MOE": {8:67, 10:73, 20:100, 26:117, 38:150},
    "VP": {8:67, 10:73, 20:100, 26:117, 38:150},
    "CIT": {40:53, 70:77, 100:100, 130:123, 190:180},
    "ICG": {18:67, 30:84, 45:103, 60:125, 75:146, 85:160}
}

def convertir_pe(sub, pd, edad):
    # Selección robusta de baremo [cite: 1655, 1656]
    tabla_edad = BAREMOS_RANGOS.get(edad, BAREMOS_RANGOS["20:0-24:11"])
    tabla_sub = tabla_edad.get(sub, BAREMOS_RANGOS["20:0-24:11"][sub])
    escalares = sorted(tabla_sub.keys())
    for e in escalares:
        if pd <= tabla_sub[e][1]: return e
    return 19

def obtener_compuesta(tipo, suma):
    tabla = INDICES_CL[tipo]
    if suma in tabla: return tabla[suma]
    puntos = sorted(tabla.keys())
    for i in range(len(puntos)-1):
        if puntos[i] < suma < puntos[i+1]:
            ratio = (suma - puntos[i]) / (puntos[i+1] - puntos[i])
            return int(tabla[puntos[i]] + ratio * (tabla[puntos[i+1]] - tabla[puntos[i]]))
    return 100 if suma > 10 else 40

def desc_clinico(ci):
    if ci >= 130: return "Muy Superior"
    if ci >= 120: return "Superior"
    if ci >= 110: return "Promedio Alto"
    if ci >= 90: return "Promedio"
    if ci >= 80: return "Promedio Bajo"
    if ci >= 70: return "Limítrofe"
    return "Extremadamente Bajo"

# --- INTERFAZ ---
if check_password():
    st.title("⚖️ WAIS-IV Chile: Sistema Clínico de Alta Precisión")
    
    with st.sidebar:
        st.header("Datos")
        nombre = st.text_input("Identificador")
        edades = ["16:0-17:11", "18:0-19:11", "20:0-24:11", "25:0-29:11", "30:0-34:11", "35:0-44:11", "45:0-54:11", "55:0-64:11", "65:0-69:11", "70:0-74:11", "75:0-79:11", "80:0-84:11", "85:0-90:11"]
        edad_sel = st.selectbox("Baremo Etario", edades)
        st.caption("Escriba la PD y presione Enter.")

    st.subheader("1. Puntuaciones Directas (PD)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("Comprensión Verbal")
        p_an = st.number_input("Analogías", 0, 36)
        p_voc = st.number_input("Vocabulario", 0, 57)
        p_inf = st.number_input("Información", 0, 26)
    with c2:
        st.info("Razonamiento Perceptivo")
        p_cc = st.number_input("Cubos", 0, 66)
        p_mr = st.number_input("Matrices", 0, 26)
        p_rv = st.number_input("Puzles", 0, 26)
    with c3:
        st.info("Memoria de Trabajo")
        p_rd = st.number_input("Dígitos", 0, 48)
        p_ari = st.number_input("Aritmética", 0, 22)
    with c4:
        st.info("Velocidad Procesamiento")
        p_bs = st.number_input("Símbolos", 0, 60)
        p_cla = st.number_input("Claves", 0, 135)

    if st.button("CALCULAR PERFIL CLÍNICO"):
        # Conversiones
        e_an, e_voc, e_inf = convertir_pe("An", p_an, edad_sel), convertir_pe("Voc", p_voc, edad_sel), convertir_pe("In", p_inf, edad_sel)
        e_cc, e_mr, e_rv = convertir_pe("CC", p_cc, edad_sel), convertir_pe("MR", p_mr, edad_sel), convertir_pe("RV", p_rv, edad_sel)
        e_rd, e_ari = convertir_pe("RD", p_rd, edad_sel), convertir_pe("Ari", p_ari, edad_sel)
        e_bs, e_cla = convertir_pe("BS", p_bs, edad_sel), convertir_pe("Cla", p_cla, edad_sel)

        # Índices
        vci = obtener_compuesta("VCI", e_an + e_voc + e_inf)
        pri = obtener_compuesta("PRI", e_cc + e_mr + e_rv)
        moe = obtener_compuesta("MOE", e_rd + e_ari)
        vp = obtener_compuesta("VP", e_bs + e_cla)
        icg = obtener_compuesta("ICG", e_an + e_voc + e_inf + e_cc + e_mr + e_rv)
        cit = obtener_compuesta("CIT", sum([e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]))

        # --- ANÁLISIS DE DISCREPANCIAS --- [cite: 1538, 1658]
        max_ind = max(vci, pri, moe, vp)
        min_ind = min(vci, pri, moe, vp)
        discrepancia = max_ind - min_ind
        
        st.divider()
        st.success(f"Informe: {nombre} | Baremo: {edad_sel}")
        
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("VCI", vci, desc_clinico(vci))
        m2.metric("PRI", pri, desc_clinico(pri))
        m3.metric("MOE", moe, desc_clinico(moe))
        m4.metric("VP", vp, desc_clinico(vp))
        m5.metric("ICG", icg, desc_clinico(icg))
        m6.metric("CIT", cit, desc_clinico(cit), delta_color="off")

        # Mensaje de interpretabilidad
        if discrepancia >= 23:
            st.error(f"⚠️ **ADVERTENCIA CLÍNICA**: Existe una discrepancia de {discrepancia} puntos entre los índices. El CIT no es una medida unitaria representativa. Se recomienda basar la interpretación en el ICG y el análisis de los índices por separado.")
        else:
            st.info("✅ **PERFIL ARMÓNICO**: No existen discrepancias clínicas significativas entre los índices. El CIT es interpretable.")

        st.subheader("Perfil de Subpruebas")
        df = pd.DataFrame({"Subprueba": ["An", "Voc", "Inf", "CC", "MR", "RV", "RD", "Ari", "BS", "Cla"], "PE": [e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]})
        st.bar_chart(df.set_index("Subprueba"))
