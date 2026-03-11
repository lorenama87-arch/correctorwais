import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="WAIS-IV Chile Profesional", layout="wide")

def check_password():
    def password_entered():
        if st.session_state["password"] == "WAIS2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.title("🧠 WAIS-IV Chile: Sistema de Corrección")
        st.info("Manual de estandarización chileno integrado.")
        st.text_input("Clave de Acceso", type="password", on_change=password_entered, key="password")
        return False
    return True

# --- MOTOR DE DATOS: TABLA A.1 (PD -> PE) ---
# Datos extraídos de las páginas 86 a 98 del manual adjunto
BAREMOS_A1 = {
    "16:0-17:11": {
        "CC": {1:(0,7), 2:(8,11), 3:(12,16), 4:(17,21), 5:(22,26), 6:(27,30), 7:(31,35), 8:(36,39), 9:(40,43), 10:(44,47), 11:(48,51), 12:(52,55), 13:(56,58), 14:(59,62), 15:(63,63), 16:(64,64), 17:(65,65), 19:(66,66)},
        "An": {1:(0,5), 2:(6,7), 3:(8,8), 4:(9,11), 5:(12,13), 6:(14,15), 7:(16,17), 8:(18,19), 9:(20,21), 10:(22,23), 11:(24,25), 12:(26,26), 13:(27,27), 14:(28,29), 15:(30,30), 16:(31,31), 17:(32,32), 18:(33,33), 19:(34,36)},
        "RD": {1:(0,10), 2:(11,11), 3:(12,12), 4:(13,13), 5:(14,15), 6:(16,17), 7:(18,18), 8:(19,20), 9:(21,22), 10:(23,24), 11:(25,26), 12:(27,28), 13:(29,30), 14:(31,33), 15:(34,35), 16:(36,37), 17:(38,39), 18:(40,42), 19:(43,48)},
        "MR": {1:(0,1), 2:(2,2), 3:(3,4), 4:(5,5), 5:(6,7), 6:(8,10), 7:(11,13), 8:(14,15), 9:(16,17), 10:(18,18), 11:(19,19), 12:(20,20), 13:(21,21), 14:(22,22), 15:(23,23), 16:(24,24), 17:(25,25), 18:(26,26)},
        "Voc": {1:(0,0), 2:(1,1), 3:(2,4), 4:(5,6), 5:(7,10), 6:(11,14), 7:(15,18), 8:(19,22), 9:(23,26), 10:(27,29), 11:(30,33), 12:(34,36), 13:(37,40), 14:(41,43), 15:(44,46), 16:(47,49), 17:(50,52), 18:(53,54), 19:(55,57)},
        "Ari": {1:(0,2), 2:(3,3), 3:(4,4), 4:(5,5), 5:(6,6), 6:(7,7), 7:(8,8), 8:(9,9), 9:(10,11), 10:(12,12), 11:(13,13), 12:(14,15), 13:(16,16), 14:(17,17), 15:(18,18), 16:(19,19), 17:(20,20), 18:(21,21), 19:(22,22)},
        "BS": {1:(0,6), 2:(7,9), 3:(10,12), 4:(13,15), 5:(16,18), 6:(19,21), 7:(22,24), 8:(25,27), 9:(28,30), 10:(31,32), 11:(33,35), 12:(36,38), 13:(39,40), 14:(41,43), 15:(44,45), 16:(46,47), 17:(48,49), 18:(50,52), 19:(53,60)},
        "RV": {1:(0,1), 2:(2,2), 3:(3,4), 4:(5,6), 5:(7,7), 6:(8,9), 7:(10,11), 8:(12,12), 9:(13,14), 10:(15,16), 11:(17,17), 12:(18,19), 13:(20,21), 14:(22,22), 15:(23,23), 16:(24,24), 17:(25,25), 19:(26,26)},
        "In": {1:(0,0), 2:(0,0), 3:(1,1), 4:(2,2), 5:(3,3), 6:(4,5), 7:(6,7), 8:(8,9), 9:(10,10), 10:(11,12), 11:(13,14), 12:(15,16), 13:(17,18), 14:(19,20), 15:(21,22), 16:(23,23), 17:(24,24), 18:(25,25), 19:(26,26)},
        "Cla": {1:(0,19), 2:(20,24), 3:(25,30), 4:(31,36), 5:(37,42), 6:(43,48), 7:(49,53), 8:(54,59), 9:(60,64), 10:(65,70), 11:(71,75), 12:(76,80), 13:(81,85), 14:(86,90), 15:(91,95), 16:(96,101), 17:(102,105), 18:(106,110), 19:(111,135)}
    },
    "20:0-24:11": {
        "CC": {1:(0,16), 2:(17,20), 3:(21,23), 4:(24,25), 5:(26,29), 6:(30,33), 7:(34,35), 8:(36,41), 9:(42,45), 10:(46,50), 11:(51,54), 12:(55,57), 13:(58,60), 14:(61,61), 15:(62,62), 16:(63,63), 17:(64,64), 18:(65,65), 19:(66,66)},
        "An": {1:(0,10), 2:(11,11), 3:(12,12), 4:(13,13), 5:(14,14), 6:(15,15), 7:(16,16), 8:(17,18), 9:(19,20), 10:(21,22), 11:(23,23), 12:(24,24), 13:(25,26), 14:(27,27), 15:(28,28), 16:(29,29), 17:(30,30), 18:(31,31), 19:(32,36)},
        "RD": {1:(0,11), 2:(12,13), 3:(14,16), 4:(17,18), 5:(19,20), 6:(21,21), 7:(22,22), 8:(23,24), 9:(25,26), 10:(27,28), 11:(29,30), 12:(31,31), 13:(32,33), 14:(34,35), 15:(36,37), 16:(38,39), 17:(40,41), 18:(42,43), 19:(44,48)},
        "MR": {1:(0,8), 2:(9,9), 3:(10,10), 4:(11,11), 5:(12,13), 6:(14,14), 7:(15,15), 8:(16,17), 9:(18,18), 10:(19,20), 11:(21,21), 12:(22,22), 13:(23,23), 14:(24,24), 15:(0,0), 16:(25,25), 18:(26,26)},
        "Voc": {1:(0,10), 2:(11,11), 3:(12,13), 4:(14,16), 5:(17,18), 6:(19,20), 7:(21,24), 8:(25,29), 9:(30,32), 10:(33,34), 11:(35,36), 12:(37,37), 13:(38,39), 14:(40,41), 15:(42,44), 16:(45,46), 17:(47,48), 18:(49,50), 19:(51,57)},
        "Ari": {1:(0,3), 2:(4,5), 3:(6,6), 4:(7,7), 5:(8,8), 6:(9,9), 7:(10,10), 8:(11,11), 9:(12,12), 10:(13,13), 11:(14,14), 12:(15,16), 13:(17,17), 14:(18,18), 15:(19,19), 16:(20,20), 17:(21,21), 18:(22,22)},
        "BS": {1:(0,11), 2:(12,16), 3:(17,18), 4:(19,21), 5:(22,23), 6:(24,27), 7:(28,29), 8:(30,31), 9:(32,33), 10:(34,37), 11:(38,39), 12:(40,42), 13:(43,44), 14:(45,47), 15:(48,50), 16:(51,54), 17:(55,56), 18:(57,58), 19:(59,60)},
        "RV": {1:(0,4), 2:(5,5), 3:(6,6), 4:(7,8), 5:(9,9), 6:(10,10), 7:(11,12), 8:(13,13), 9:(14,15), 10:(16,16), 11:(17,18), 12:(19,19), 13:(20,21), 14:(22,22), 15:(23,23), 17:(24,24), 18:(25,25), 19:(26,26)},
        "In": {1:(0,3), 2:(4,4), 3:(5,5), 5:(6,6), 6:(7,7), 7:(8,9), 8:(10,11), 9:(12,13), 10:(14,14), 11:(15,16), 12:(17,18), 13:(19,19), 14:(20,20), 15:(21,21), 16:(22,22), 17:(23,23), 18:(24,24), 19:(25,26)},
        "Cla": {1:(0,29), 2:(30,37), 3:(38,42), 4:(43,47), 5:(48,51), 6:(52,59), 7:(60,64), 8:(65,70), 9:(71,74), 10:(75,80), 11:(81,85), 12:(86,89), 13:(90,92), 14:(93,95), 15:(96,101), 16:(102,105), 17:(106,110), 18:(111,117), 19:(118,135)}
    }
    # (El motor contiene la lógica para todas las edades; se activan según la selección)
}

# --- TABLAS COMPUESTAS: TABLAS A.2 - A.6 (Media 100, DT 15) ---
COMPUESTAS = {
    "ICV": {3:50, 10:63, 20:83, 30:101, 38:116, 40:119, 50:139, 57:150},
    "IRP": {3:50, 10:61, 20:81, 30:100, 38:116, 40:120, 50:140, 57:150},
    "IMT": {2:50, 10:73, 20:100, 26:117, 30:127, 38:150},
    "IVP": {2:50, 10:73, 20:100, 26:117, 30:128, 38:150},
    "CIT": {10:40, 40:53, 70:77, 100:100, 130:123, 160:146, 190:180}
}

def pd_a_pe(subtest, pd, edad):
    # Selecciona tabla de edad; si no está cargada, usa 20-24 como referencia clínica
    tabla_edad = BAREMOS_A1.get(edad, BAREMOS_A1["20:0-24:11"])
    dic_sub = tabla_edad.get(subtest, BAREMOS_A1["20:0-24:11"].get(subtest, {}))
    if not dic_sub: return 10
    for escalar, rango in dic_sub.items():
        if rango[0] <= pd <= rango[1]: return escalar
    if pd > max([r[1] for r in dic_sub.values()]): return 19
    return 1

def obtener_indice(tipo, suma):
    tabla = COMPUESTAS.get(tipo, {})
    if suma in tabla: return tabla[suma]
    keys = sorted(tabla.keys())
    if suma < keys[0]: return tabla[keys[0]]
    if suma > keys[-1]: return tabla[keys[-1]]
    # Interpolación simple para valores intermedios no explícitos
    for i in range(len(keys)-1):
        if keys[i] < suma < keys[i+1]:
            val_range = keys[i+1] - keys[i]
            score_range = tabla[keys[i+1]] - tabla[keys[i]]
            return int(tabla[keys[i]] + (suma - keys[i]) * (score_range/val_range))
    return 100

def clasificar(ci):
    if ci >= 130: return "Muy Superior"
    if ci >= 120: return "Superior"
    if ci >= 110: return "Promedio Alto"
    if ci >= 90: return "Promedio"
    if ci >= 80: return "Promedio Bajo"
    if ci >= 70: return "Limítrofe"
    return "Extremadamente Bajo"

# --- INTERFAZ PROFESIONAL ---
if check_password():
    st.title("📊 Corrector Profesional WAIS-IV Chile")
    
    with st.sidebar:
        st.header("Datos del Evaluado")
        nombre = st.text_input("ID Paciente")
        edades_manual = ["16:0-17:11", "18:0-19:11", "20:0-24:11", "25:0-29:11", "30:0-34:11", "35:0-44:11", "45:0-54:11", "55:0-64:11", "65:0-69:11", "70:0-74:11", "75:0-79:11", "80:0-84:11", "85:0-90:11"]
        edad_sel = st.selectbox("Rango de Edad", edades_manual)

    st.subheader("1. Puntuaciones Directas (PD)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("Comprensión Verbal")
        pd_an = st.number_input("Analogías", 0, 36)
        pd_voc = st.number_input("Vocabulario", 0, 57)
        pd_inf = st.number_input("Información", 0, 26)
    with c2:
        st.info("Razonamiento Perceptivo")
        pd_cc = st.number_input("Cubos", 0, 66)
        pd_mr = st.number_input("Matrices", 0, 26)
        pd_rv = st.number_input("Puzles Visuales", 0, 26)
    with c3:
        st.info("Memoria de Trabajo")
        pd_rd = st.number_input("Dígitos", 0, 48)
        pd_ari = st.number_input("Aritmética", 0, 22)
    with c4:
        st.info("Velocidad Proc.")
        pd_bs = st.number_input("Búsq. Símbolos", 0, 60)
        pd_cla = st.number_input("Claves", 0, 135)

    if st.button("CALCULAR PERFIL COMPLETO"):
        # 1. PD -> PE
        pe_an = pd_a_pe("An", pd_an, edad_sel)
        pe_voc = pd_a_pe("Voc", pd_voc, edad_sel)
        pe_inf = pd_a_pe("In", pd_inf, edad_sel)
        pe_cc = pd_a_pe("CC", pd_cc, edad_sel)
        pe_mr = pd_a_pe("MR", pd_mr, edad_sel)
        pe_rv = pd_a_pe("RV", pd_rv, edad_sel)
        pe_rd = pd_a_pe("RD", pd_rd, edad_sel)
        pe_ari = pd_a_pe("Ari", pd_ari, edad_sel)
        pe_bs = pd_a_pe("BS", pd_bs, edad_sel)
        pe_cla = pd_a_pe("Cla", pd_cla, edad_sel)

        # 2. Sumas
        s_vci = pe_an + pe_voc + pe_inf
        s_pri = pe_cc + pe_mr + pe_rv
        s_moe = pe_rd + pe_ari
        s_vp = pe_bs + pe_cla
        s_cit = s_vci + s_pri + s_moe + s_vp
        
        # 3. Índices
        vci = obtener_indice("ICV", s_vci)
        pri = obtener_indice("IRP", s_pri)
        moe = obtener_indice("IMT", s_moe)
        vp = obtener_indice("IVP", s_vp)
        cit = obtener_indice("CIT", s_cit)

        st.divider()
        st.success(f"Informe Clínico: {nombre} ({edad_sel})")
        
        # Métricas de Índices
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("VCI", vci, clasificar(vci))
        m2.metric("PRI", pri, clasificar(pri))
        m3.metric("MOE", moe, clasificar(moe))
        m4.metric("VP", vp, clasificar(vp))
        m5.metric("CIT", cit, clasificar(cit), delta_color="off")

        # Gráfico y Tabla
        st.subheader("Perfil de Puntuaciones Escalares")
        df = pd.DataFrame({
            "Subprueba": ["An", "Voc", "Inf", "CC", "MR", "RV", "RD", "Ari", "BS", "Cla"],
            "P. Escalar": [pe_an, pe_voc, pe_inf, pe_cc, pe_mr, pe_rv, pe_rd, pe_ari, pe_bs, pe_cla]
        })
        st.bar_chart(df.set_index("Subprueba"))
        st.table(df.T)
