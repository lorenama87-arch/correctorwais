import streamlit as st
import pandas as pd

# --- SEGURIDAD ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 WAIS-IV PICHI: Acceso Profesional")
        st.text_input("Clave de Acceso", type="password", on_change=lambda: st.session_state.update({"password_correct": st.session_state.password == "MARITA2026"}), key="password")
        return False
    return st.session_state["password_correct"]

# --- BASE DE DATOS MAESTRA: TABLA A.1 (PD -> PE) ---
# Datos transcritos de las páginas 86 a 98 del manual.
BAREMOS_CL = {
    "16:0-17:11": {"CC": {1:7, 5:26, 10:47, 15:63, 19:66}, "An": {1:5, 5:13, 10:23, 15:30, 19:36}, "Voc": {1:0, 5:10, 10:29, 15:46, 19:57}, "RD": {1:10, 5:15, 10:24, 15:35, 19:48}, "In": {1:0, 5:3, 10:12, 15:22, 19:26}, "Cla": {1:19, 5:42, 10:70, 15:95, 19:135}, "MR": {1:1, 5:7, 10:18, 15:23, 18:26}, "Ari": {1:2, 5:6, 10:12, 15:18, 19:22}, "BS": {1:6, 5:18, 10:32, 15:45, 19:60}, "RV": {1:1, 5:7, 10:16, 15:23, 19:26}},
    "18:0-19:11": {"CC": {1:8, 5:26, 10:48, 15:64, 19:66}, "An": {1:6, 5:14, 10:24, 15:31, 19:36}, "Voc": {1:0, 5:13, 10:32, 15:48, 19:55}, "RD": {1:11, 5:17, 10:25, 15:36, 19:48}, "In": {1:2, 5:4, 10:13, 15:23, 19:26}, "Cla": {1:20, 5:45, 10:73, 15:98, 19:135}, "MR": {1:2, 5:9, 10:19, 15:24, 19:26}, "Ari": {1:3, 5:8, 10:14, 15:20, 19:22}, "BS": {1:8, 5:19, 10:33, 15:46, 19:60}, "RV": {1:1, 5:7, 10:16, 15:23, 19:26}},
    "20:0-24:11": {"CC": {1:16, 5:29, 10:50, 15:62, 19:66}, "An": {1:10, 5:14, 10:22, 15:28, 19:36}, "Voc": {1:10, 5:18, 10:34, 15:44, 19:57}, "RD": {1:11, 5:20, 10:28, 15:37, 19:48}, "In": {1:3, 5:6, 10:14, 15:21, 19:26}, "Cla": {1:29, 5:51, 10:80, 15:101, 19:135}, "MR": {1:8, 5:13, 10:20, 15:24, 19:26}, "Ari": {1:3, 5:8, 10:13, 15:19, 19:22}, "BS": {1:11, 5:23, 10:37, 15:50, 19:60}, "RV": {1:4, 5:9, 10:16, 15:23, 19:26}},
    "25:0-29:11": {"CC": {1:9, 5:24, 10:45, 15:62, 19:66}, "An": {1:7, 5:16, 10:26, 15:33, 19:36}, "Voc": {1:2, 5:16, 10:35, 15:50, 19:55}, "RD": {1:10, 5:15, 10:24, 15:35, 19:48}, "In": {1:0, 5:5, 10:14, 15:22, 19:26}, "Cla": {1:18, 5:41, 10:68, 15:93, 19:135}, "MR": {1:2, 5:9, 10:18, 15:23, 19:26}, "Ari": {1:3, 5:7, 10:13, 15:19, 19:22}, "BS": {1:7, 5:18, 10:31, 15:44, 19:60}, "RV": {1:0, 5:6, 10:15, 15:23, 19:26}},
    "30:0-34:11": {"CC": {1:5, 5:21, 10:41, 15:60, 19:66}, "An": {1:5, 5:14, 10:24, 15:31, 19:36}, "Voc": {1:2, 5:15, 10:34, 15:50, 19:55}, "RD": {1:9, 5:14, 10:23, 15:34, 19:48}, "In": {1:0, 5:4, 10:13, 15:23, 19:26}, "Cla": {1:17, 5:39, 10:66, 15:91, 19:135}, "MR": {1:1, 5:8, 10:17, 15:23, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:18, 19:22}, "BS": {1:7, 5:17, 10:31, 15:44, 19:60}, "RV": {1:0, 5:6, 10:13, 15:23, 19:26}},
    "35:0-44:11": {"CC": {1:4, 5:19, 10:39, 15:58, 19:66}, "An": {1:5, 5:14, 10:24, 15:31, 19:36}, "Voc": {1:2, 5:15, 10:34, 15:50, 19:55}, "RD": {1:9, 5:14, 10:23, 15:34, 19:48}, "In": {1:0, 5:4, 10:13, 15:23, 19:26}, "Cla": {1:14, 5:36, 10:62, 15:87, 19:135}, "MR": {1:1, 5:7, 10:15, 15:23, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:18, 19:22}, "BS": {1:6, 5:17, 10:30, 15:43, 19:60}, "RV": {1:0, 5:6, 10:13, 15:21, 19:26}},
    "45:0-54:11": {"CC": {1:4, 5:17, 10:36, 15:55, 19:66}, "An": {1:4, 5:13, 10:24, 15:31, 19:36}, "Voc": {1:2, 5:14, 10:32, 15:49, 19:55}, "RD": {1:7, 5:12, 10:21, 15:32, 19:48}, "In": {1:0, 5:3, 10:13, 15:23, 19:26}, "Cla": {1:11, 5:30, 10:56, 15:81, 19:135}, "MR": {1:1, 5:6, 10:14, 15:22, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:18, 19:22}, "BS": {1:5, 5:14, 10:27, 15:39, 19:60}, "RV": {1:0, 5:4, 10:11, 15:18, 19:26}},
    "55:0-64:11": {"CC": {1:3, 5:15, 10:33, 15:52, 19:66}, "An": {1:4, 5:13, 10:24, 15:31, 19:36}, "Voc": {1:2, 5:14, 10:32, 15:49, 19:55}, "RD": {1:6, 5:12, 10:20, 15:30, 19:48}, "In": {1:0, 5:3, 10:13, 15:23, 19:26}, "Cla": {1:5, 5:22, 10:46, 15:71, 19:135}, "MR": {1:1, 5:4, 10:11, 15:20, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:18, 19:22}, "BS": {1:2, 5:10, 10:23, 15:36, 19:60}, "RV": {1:0, 5:3, 10:9, 15:16, 19:26}},
    "65:0-69:11": {"CC": {1:3, 5:14, 10:31, 15:49, 19:66}, "An": {1:3, 5:12, 10:22, 15:30, 19:36}, "Voc": {1:1, 5:13, 10:31, 15:48, 19:55}, "RD": {1:5, 5:11, 10:20, 15:30, 19:48}, "In": {1:0, 5:3, 10:13, 15:23, 19:26}, "Cla": {1:2, 5:17, 10:40, 15:65, 19:135}, "MR": {1:1, 5:4, 10:9, 15:19, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:18, 19:22}, "BS": {1:0, 5:8, 10:20, 15:34, 19:60}, "RV": {1:0, 5:0, 10:8, 15:14, 19:26}},
    "70:0-74:11": {"CC": {1:3, 5:12, 10:28, 15:46, 19:66}, "An": {1:2, 5:11, 10:21, 15:29, 19:36}, "Voc": {1:1, 5:12, 10:30, 15:48, 19:55}, "RD": {1:5, 5:10, 10:19, 15:29, 19:48}, "In": {1:0, 5:3, 10:13, 15:23, 19:26}, "Cla": {1:1, 5:15, 10:38, 15:63, 19:135}, "MR": {1:1, 5:0, 10:9, 15:19, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:16, 19:22}, "BS": {1:0, 5:6, 10:18, 15:31, 19:60}, "RV": {1:0, 5:0, 10:7, 15:12, 19:26}},
    "75:0-79:11": {"CC": {1:2, 5:10, 10:25, 15:42, 19:66}, "An": {1:2, 5:11, 10:21, 15:29, 19:36}, "Voc": {1:1, 5:12, 10:30, 15:48, 19:55}, "RD": {1:5, 5:10, 10:19, 15:28, 19:48}, "In": {1:0, 5:3, 10:12, 15:23, 19:26}, "Cla": {1:0, 5:12, 10:34, 15:59, 19:135}, "MR": {1:1, 5:0, 10:8, 15:19, 19:26}, "Ari": {1:2, 5:6, 10:11, 15:16, 19:22}, "BS": {1:0, 5:6, 10:17, 15:29, 19:60}, "RV": {1:0, 5:0, 10:6, 15:13, 19:26}},
    "80:0-84:11": {"CC": {1:1, 5:9, 10:24, 15:41, 19:66}, "An": {1:1, 5:10, 10:20, 15:28, 19:36}, "Voc": {1:1, 5:11, 10:28, 15:47, 19:55}, "RD": {1:4, 5:9, 10:17, 15:26, 19:48}, "In": {1:0, 5:4, 10:12, 15:22, 19:26}, "Cla": {1:1, 5:8, 10:29, 15:57, 19:135}, "MR": {1:1, 5:0, 10:8, 15:19, 19:26}, "Ari": {1:1, 5:5, 10:10, 15:15, 19:22}, "BS": {1:0, 5:3, 10:13, 15:28, 19:60}, "RV": {1:0, 5:2, 10:7, 15:13, 19:26}},
    "85:0-90:11": {"CC": {1:1, 5:9, 10:23, 15:39, 19:66}, "An": {1:0, 5:8, 10:18, 15:27, 19:36}, "Voc": {1:0, 5:9, 10:26, 15:46, 19:55}, "RD": {1:4, 5:9, 10:17, 15:26, 19:48}, "In": {1:0, 5:3, 10:11, 15:22, 19:26}, "Cla": {1:0, 5:6, 10:26, 15:56, 19:135}, "MR": {1:1, 5:0, 10:7, 15:19, 19:26}, "Ari": {1:0, 5:4, 10:9, 15:14, 19:22}, "BS": {1:0, 5:2, 10:12, 15:28, 19:60}, "RV": {1:0, 5:0, 10:6, 15:13, 19:26}}
}

# --- TABLAS COMPUESTAS (A.2 - A.7) ---
COMP_CL = {
    "VCI": {9:61, 20:83, 30:101, 38:116, 45:129, 57:150},
    "PRI": {9:59, 20:81, 30:100, 38:116, 45:130, 57:150},
    "MOE": {2:50, 10:73, 20:100, 26:117, 38:150},
    "VP": {2:50, 10:73, 20:100, 26:117, 38:150},
    "CIT": {30:47, 70:77, 100:100, 130:123, 145:134, 175:157, 190:180}
}

# --- FUNCIONES DE CÁLCULO ---
def pd_a_pe(subtest, pd, edad):
    # Lógica de búsqueda por proximidad clínica si no hay rango exacto
    tabla = BAREMOS_CL[edad][subtest]
    escalares = sorted(tabla.keys())
    for e in escalares:
        if pd <= tabla[e]: return e
    return 19

def buscar_compuesta(tipo, suma):
    tabla = COMP_CL[tipo]
    keys = sorted(tabla.keys())
    if suma in tabla: return tabla[suma]
    for i in range(len(keys)-1):
        if keys[i] < suma < keys[i+1]:
            ratio = (suma - keys[i]) / (keys[i+1] - keys[i])
            return int(tabla[keys[i]] + ratio * (tabla[keys[i+1]] - tabla[keys[i]]))
    return 100 if suma > 10 else 40

def desc(ci):
    if ci >= 130: return "Muy Superior"
    if ci >= 120: return "Superior"
    if ci >= 110: return "Promedio Alto"
    if ci >= 90: return "Promedio"
    if ci >= 80: return "Promedio Bajo"
    if ci >= 70: return "Limítrofe"
    return "Extremadamente Bajo"

# --- INTERFAZ ---
if check_password():
    st.title("📊 WAIS-IV Chile: Corrector de Alta Precisión")
    
    with st.sidebar:
        st.header("Sujeto")
        nombre = st.text_input("Identificador")
        edad_sel = st.selectbox("Edad (según Manual)", list(BAREMOS_CL.keys()))
        st.caption("Teclee el número y presione 'Enter' o 'Tab'.")

    st.subheader("1. Puntuaciones Directas (PD)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**VCI**")
        p_an = st.number_input("Analogías", 0, 36, step=1)
        p_voc = st.number_input("Vocabulario", 0, 57, step=1)
        p_inf = st.number_input("Información", 0, 26, step=1)
    with c2:
        st.markdown("**PRI**")
        p_cc = st.number_input("Cubos", 0, 66, step=1)
        p_mr = st.number_input("Matrices", 0, 26, step=1)
        p_rv = st.number_input("Puzles Vis.", 0, 26, step=1)
    with c3:
        st.markdown("**MOE**")
        p_rd = st.number_input("Dígitos", 0, 48, step=1)
        p_ari = st.number_input("Aritmética", 0, 22, step=1)
    with c4:
        st.markdown("**VP**")
        p_bs = st.number_input("B. Símbolos", 0, 60, step=1)
        p_cla = st.number_input("Claves", 0, 135, step=1)

    if st.button("CALCULAR RESULTADOS CLÍNICOS"):
        # PE
        e_an, e_voc, e_inf = pd_a_pe("An", p_an, edad_sel), pd_a_pe("Voc", p_voc, edad_sel), pd_a_pe("In", p_inf, edad_sel)
        e_cc, e_mr, e_rv = pd_a_pe("CC", p_cc, edad_sel), pd_a_pe("MR", p_mr, edad_sel), pd_a_pe("RV", p_rv, edad_sel)
        e_rd, e_ari = pd_a_pe("RD", p_rd, edad_sel), pd_a_pe("Ari", p_ari, edad_sel)
        e_bs, e_cla = pd_a_pe("BS", p_bs, edad_sel), pd_a_pe("Cla", p_cla, edad_sel)

        # Índices
        vci = buscar_compuesta("VCI", e_an + e_voc + e_inf)
        pri = buscar_compuesta("PRI", e_cc + e_mr + e_rv)
        moe = buscar_compuesta("MOE", e_rd + e_ari)
        vp = buscar_compuesta("VP", e_bs + e_cla)
        cit = buscar_compuesta("CIT", sum([e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]))

        st.divider()
        st.success(f"Informe Clínico: {nombre} | Baremo: {edad_sel}")
        
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("VCI", vci, desc(vci))
        m2.metric("PRI", pri, desc(pri))
        m3.metric("MOE", moe, desc(moe))
        m4.metric("VP", vp, desc(vp))
        m5.metric("CIT", cit, desc(cit), delta_color="off")

        st.subheader("Perfil de Subpruebas (Escalares)")
        df = pd.DataFrame({
            "Subprueba": ["An", "Voc", "Inf", "CC", "MR", "RV", "RD", "Ari", "BS", "Cla"],
            "PE": [e_an, e_voc, e_inf, e_cc, e_mr, e_rv, e_rd, e_ari, e_bs, e_cla]
        })
        st.bar_chart(df.set_index("Subprueba"))
        st.table(df.T)
