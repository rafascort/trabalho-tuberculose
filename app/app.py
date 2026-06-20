"""
App de Producao - Triagem de Risco de Abandono do Tratamento de Tuberculose.

Interface simples para o profissional de saude: poucas informacoes de entrada e,
em troca, a probabilidade de abandono + classificacao de risco + acoes sugeridas.

Como rodar:  streamlit run app/app.py   (a partir da pasta do projeto)
"""
import os, json
import pandas as pd
import streamlit as st
import joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(BASE, "models")

# ---------- carga do modelo (cacheada) ----------
@st.cache_resource
def carregar():
    pipe = joblib.load(os.path.join(MOD, "modelo_producao.joblib"))
    lim = json.load(open(os.path.join(MOD, "limiares_producao.json")))
    return pipe, lim

pipe, lim = carregar()

st.set_page_config(page_title="Risco de Abandono - Tuberculose", page_icon="🫁", layout="centered")

# ---------- cabecalho ----------
st.markdown(
    "<h2 style='color:#063B3E;margin-bottom:0'>Triagem de Risco de Abandono</h2>"
    "<p style='color:#5A6B6B;margin-top:4px'>Tratamento de Tuberculose &middot; apoio a decisao do profissional de saude</p>",
    unsafe_allow_html=True,
)
st.caption("Preencha as informacoes abaixo (conhecidas no inicio do tratamento) e clique em Avaliar.")

SIM_NAO_IGN = {"Nao": "2", "Sim": "1", "Nao informado": "9"}
SIM_NAO = {"Nao": "2", "Sim": "1"}
HIV_OPC = {"Negativo": "2", "Positivo": "1", "Nao realizado": "4"}

# ---------- formulario ----------
with st.form("dados"):
    c1, c2 = st.columns(2)
    with c1:
        idade = st.number_input("Idade (anos)", min_value=18, max_value=110, value=40, step=1)
        alcool = st.selectbox("Uso de alcool", list(SIM_NAO_IGN), index=0)
        drogas = st.selectbox("Uso de drogas ilicitas", list(SIM_NAO_IGN), index=0)
        tabaco = st.selectbox("Tabagismo", list(SIM_NAO_IGN), index=0)
    with c2:
        hiv = st.selectbox("HIV", list(HIV_OPC), index=0)
        tdo = st.selectbox("Tratamento diretamente observado (TDO)", list(SIM_NAO_IGN), index=0)
        rua = st.selectbox("Situacao de rua", list(SIM_NAO), index=0)
        benef = st.selectbox("Recebe beneficio social", list(SIM_NAO_IGN), index=0)
    enviar = st.form_submit_button("Avaliar risco", use_container_width=True)

# ---------- predicao ----------
if enviar:
    entrada = pd.DataFrame([{
        "idade_anos": idade,
        "AGRAVALCOO": SIM_NAO_IGN[alcool],
        "AGRAVDROGA": SIM_NAO_IGN[drogas],
        "AGRAVTABAC": SIM_NAO_IGN[tabaco],
        "HIV": HIV_OPC[hiv],
        "TRAT_SUPER": SIM_NAO_IGN[tdo],
        "POP_RUA": SIM_NAO[rua],
        "BENEF_GOV": SIM_NAO_IGN[benef],
    }])
    prob = float(pipe.predict_proba(entrada)[:, 1][0])

    if prob >= lim["limiar_alto"]:
        nivel, cor, acoes = "ALTO", "#c0392b", [
            "Priorizar Tratamento Diretamente Observado (TDO).",
            "Agendar visita domiciliar / busca ativa preventiva.",
            "Acionar apoio social (assistencia, beneficios, reducao de danos).",
            "Contato frequente e lembretes nas primeiras semanas.",
        ]
    elif prob >= lim["limiar_medio"]:
        nivel, cor, acoes = "MEDIO", "#e08a3c", [
            "Reforcar orientacao sobre a importancia de concluir o tratamento.",
            "Considerar TDO e lembretes de consulta.",
            "Monitorar adesao nas primeiras semanas.",
        ]
    else:
        nivel, cor, acoes = "BAIXO", "#1e8449", [
            "Acompanhamento padrao.",
            "Reforcar orientacoes gerais sobre o tratamento.",
        ]

    st.markdown(
        f"<div style='background:{cor};color:white;padding:16px;border-radius:10px;text-align:center'>"
        f"<div style='font-size:14px;letter-spacing:1px'>PROBABILIDADE DE ABANDONO</div>"
        f"<div style='font-size:42px;font-weight:bold'>{prob:.0%}</div>"
        f"<div style='font-size:18px'>Risco {nivel}</div></div>",
        unsafe_allow_html=True,
    )
    st.progress(min(prob, 1.0))
    st.subheader("Acoes sugeridas")
    for a in acoes:
        st.markdown(f"- {a}")
    st.info(
        "Ferramenta de **apoio a decisao**, baseada em dados historicos do SINAN. "
        "Nao substitui a avaliacao clinica. O objetivo e direcionar MAIS apoio a quem "
        "tem maior risco, nunca negar cuidado.",
        icon="ℹ️",
    )
