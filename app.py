import streamlit as st
import pandas as pd
import joblib
import shap
import os

st.title('Predição - Óbito Neonatal')

#st.sidebar.image(os.getcwd() + os.sep + "logo2.png", width=100)
st.sidebar.markdown('## BabyCare')
st.sidebar.markdown('Improving the neonatal and maternal assistance')
st.sidebar.markdown('---')
st.sidebar.markdown('**Atenção:** este modelo não deve ser utilizado em produção sem a devida validação externa.    ')

st.write('Preencha os dados abaixo')

st.markdown('---')
st.subheader('Dados do Recém-nascido')

options_sexo = ['Selecione', 'Masculino', 'Feminino', 'Ignorado']
SEXO_DN = st.selectbox('Sexo', options_sexo)

PESO = st.slider('Peso ao nascer (em gramas)', 0, 7000, 0)

APGAR_1 = st.slider('Índice de Apgar 1o. minuto', 0, 10)

APGAR_5 = st.slider('Índice de Apgar 5o. minuto', 0, 10)

options_anomal = ['Selecione', 'Sim', 'Não', 'Ignorado']
IDANOMAL = st.selectbox('Detectada alguma anomalia ou defeito congênito?',
                        options_anomal)

st.markdown('---')
st.subheader('Local da Ocorrência')

ESFERAPUBLICO = st.selectbox('Nascimento na esfera pública?',
                             ['Selecione', 'Sim', 'Não'])

options_locnasc = [
    'Selecione', 'Hospital', 'Outros estabelecimentos de Saúde', 'Domicílio',
    'Outros'
]
LOCNASC = st.selectbox('Local de Nascimento', options_locnasc)

st.markdown('---')
st.subheader('Mãe')

IDADEMAE = st.slider('Informe a idade da mãe', 0, 130, 0)

SEMAGESTAC = st.slider('Semanas de Gestação', 15, 45, 15)

options_escomae = [
    'Selecione', 'Sem Escolaridade', 'Fundamental I', 'Fundamental II',
    'Médio', 'Superior incompleto', 'Superior completo', 'Ignorado'
]
ESCMAE2010 = st.selectbox('Escolaridade da Mãe', options_escomae)

options_racamae = [
    'Selecione', 'Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'
]

RACACORMAE = st.selectbox('Raça / Cor da Mãe', options_racamae)

st.markdown('---')
st.subheader('Gestação e Parto')

st.write('Histórico Gestacional')

QTDGESTANT = st.number_input('No. de gestações anteriores', 0, 10, 0)
QTDPARTNOR = st.number_input('No. de partos vaginais', 0, 10, 0)
QTDPARTCES = st.number_input('No. de partos cesáreas', 0, 10, 0)
QTDFILVIVO = st.number_input('No. de nascidos vivos', 0, 10, 0)
QTDFILMORT = st.number_input('No. de perdas fetais / abortos', 0, 10, 0)

st.write('Gestação atual')

CONSPRENAT = st.number_input('No. de consultas de pré-natal', 0, 10, 0)

MESPRENAT = st.number_input('Mês de gestação que inicou o pré-natal', 0, 10, 0)

options_gravidez = [
    'Selecione', 'Única', 'Dupla', 'Tripla ou mais', 'Ignorado'
]
GRAVIDEZ = st.selectbox('Tipo de Gravidez', options_gravidez)

st.write('Parto')

options_apresentacao = [
    'Selecione', 'Cefálica', 'Pélvica ou Podática', 'Transversa', 'Ignorado'
]
TPAPRESENT = st.selectbox('Apresentação', options_apresentacao)

STTRABPART = st.selectbox('O trabalho de parto foi induzido?',
                          ['Selecione',     'Sim', 'Não', 'Ignorado'])

options_parto = ['Selecione', 'Vaginal', 'Cesáreo', 'Ignorado']
PARTO = st.selectbox('Tipo de Parto', options_parto)

options_assist = [
    'Selecione', 'Médico', 'Enfermeira - Obstetriz', 'Parteira', 'Outros',
    'Ignorado'
]
TPNASCASSI = st.selectbox('Nascimento assistido por', options_assist)

### MAPEAMENTO DE CAMPOS PARA O DATAFRAME

IDADEMAE = IDADEMAE
PESO = PESO
SEMAGESTAC = SEMAGESTAC
CONSPRENAT = CONSPRENAT
QTDFILVIVO = QTDFILVIVO
QTDFILMORT = QTDFILMORT
QTDGESTANT = QTDGESTANT
QTDPARTNOR = QTDPARTNOR
QTDPARTCES = QTDPARTCES

if ESFERAPUBLICO == 'Sim':
    ESFERA_PUBLICO = 1
else:
    ESFERA_PUBLICO = 0

if LOCNASC == 'Outros estabelecimentos de Saúde':
    LOCNASC_2 = 1
    LOCNASC_3 = 0
elif LOCNASC == 'DDomícilio':
    LOCNASC_3 = 1
    LOCNASC_2 = 0
else:
    LOCNASC_2 = 0
    LOCNASC_3 = 0

if SEXO_DN == 'Masculino':
    SEXO_DN_M = 1
    SEXO_DN_I = 0
elif SEXO_DN == 'Ignorado':
    SEXO_DN_M = 0
    SEXO_DN_I = 1
else:
    SEXO_DN_M = 0
    SEXO_DN_I = 0

APGAR1_1 = 0
APGAR1_2 = 0
APGAR1_3 = 0
APGAR1_4 = 0
APGAR1_5 = 0
APGAR1_6 = 0
APGAR1_7 = 0
APGAR1_8 = 0
APGAR1_9 = 0
APGAR1_10 = 0
APGAR1_99 = 0

if APGAR_1 == 1:
    APGAR1_1 += 1
if APGAR_1 == 2:
    APGAR1_2 += 1
if APGAR_1 == 3:
    APGAR1_3 += 1
if APGAR_1 == 4:
    APGAR1_4 += 1
if APGAR_1 == 5:
    APGAR1_5 += 1
if APGAR_1 == 6:
    APGAR1_6 += 1
if APGAR_1 == 7:
    APGAR1_7 += 1
if APGAR_1 == 8:
    APGAR1_8 += 1
if APGAR_1 == 9:
    APGAR1_9 += 1
if APGAR_1 == 10:
    APGAR1_10 += 1

APGAR5_1 = 0
APGAR5_2 = 0
APGAR5_3 = 0
APGAR5_4 = 0
APGAR5_5 = 0
APGAR5_6 = 0
APGAR5_7 = 0
APGAR5_8 = 0
APGAR5_9 = 0
APGAR5_10 = 0
APGAR5_99 = 0

if APGAR_5 == 1:
    APGAR5_1 += 1
if APGAR_5 == 2:
    APGAR5_2 += 1
if APGAR_5 == 3:
    APGAR5_3 += 1
if APGAR_5 == 4:
    APGAR5_4 += 1
if APGAR_5 == 5:
    APGAR5_5 += 1
if APGAR_5 == 6:
    APGAR5_6 += 1
if APGAR_5 == 7:
    APGAR5_7 += 1
if APGAR_5 == 8:
    APGAR5_8 += 1
if APGAR_5 == 9:
    APGAR5_9 += 1
if APGAR_5 == 10:
    APGAR5_10 += 1

if IDANOMAL == 'Não':
    IDANOMAL_2 = 1
    IDANOMAL_9 = 0
elif IDANOMAL == 'Ignorado':
    IDANOMAL_2 = 0
    IDANOMAL_9 = 1
else:
    IDANOMAL_2 = 0
    IDANOMAL_9 = 0

if GRAVIDEZ == 'Dupla':
    GRAVIDEZ_2 = 1
    GRAVIDEZ_3 = 0
elif GRAVIDEZ == 'Tripla ou mais':
    GRAVIDEZ_2 = 0
    GRAVIDEZ_3 = 1
else:
    GRAVIDEZ_2 = 0
    GRAVIDEZ_3 = 0

if PARTO == 'Cesáreo':
    PARTO_2 = 1
else:
    PARTO_2 = 0

ESCMAE2010_1 = 0
ESCMAE2010_2 = 0
ESCMAE2010_3 = 0
ESCMAE2010_4 = 0
ESCMAE2010_5 = 0
ESCMAE2010_9 = 0

if ESCMAE2010 == 'Fundamental I':
    ESCMAE2010_1 = 1
if ESCMAE2010 == 'Fundamental II':
    ESCMAE2010_2 = 1
if ESCMAE2010 == 'Médio':
    ESCMAE2010_3 = 1
if ESCMAE2010 == 'Superior incompleto':
    ESCMAE2010_4 = 1
if ESCMAE2010 == 'Superior completo':
    ESCMAE2010_5 = 1
if ESCMAE2010 == 'Ignorado':
    ESCMAE2010_9 = 1

RACACORMAE_2 = 0
RACACORMAE_3 = 0
RACACORMAE_4 = 0
RACACORMAE_5 = 0
RACACORMAE_9 = 0

if RACACORMAE == 'Preta':
    RACACORMAE_2 = 1

if RACACORMAE == 'Amarela':
    RACACORMAE_3 = 1

if RACACORMAE == 'Parda':
    RACACORMAE_4 = 1

if RACACORMAE == 'Indígena':
    RACACORMAE_5 = 1

if RACACORMAE == 'Ignorado':
    RACACORMAE_9 = 1

MESPRENAT_2 = 0
MESPRENAT_3 = 0
MESPRENAT_4 = 0
MESPRENAT_5 = 0
MESPRENAT_6 = 0
MESPRENAT_7 = 0
MESPRENAT_8 = 0
MESPRENAT_9 = 0
MESPRENAT_10 = 0
MESPRENAT_99 = 0

if MESPRENAT == 2:
    MESPRENAT_2 = 1

if MESPRENAT == 3:
    MESPRENAT_3 = 1

if MESPRENAT == 4:
    MESPRENAT_4 = 1

if MESPRENAT == 5:
    MESPRENAT_5 = 1

if MESPRENAT == 6:
    MESPRENAT_6 = 1

if MESPRENAT == 7:
    MESPRENAT_7 = 1

if MESPRENAT == 8:
    MESPRENAT_8 = 1

if MESPRENAT == 9:
    MESPRENAT_9 = 1

if MESPRENAT == 10:
    MESPRENAT_10 = 1

TPAPRESENT_2 = 0
TPAPRESENT_3 = 0
TPAPRESENT_9 = 0

if TPAPRESENT == 'Pélvica ou Podática':
    TPAPRESENT_2 = 1
if TPAPRESENT == 'Transversa':
    TPAPRESENT_3 = 1
if TPAPRESENT == 'Ignorado':
    TPAPRESENT_9 = 1

STTRABPART_2 = 0
STTRABPART_9 = 0

if STTRABPART == 'Não':
    STTRABPART_2 = 1

if STTRABPART == 'Ignorado':
    STTRABPART_9 = 1

TPNASCASSI_2 = 0
TPNASCASSI_3 = 0
TPNASCASSI_4 = 0
TPNASCASSI_9 = 0
if TPNASCASSI == 'Enfermeira - Obstetriz':
    TPNASCASSI_2 = 1
if TPNASCASSI == 'Parteira':
    TPNASCASSI_3 = 1

if TPNASCASSI == 'Outros':
    TPNASCASSI_4 = 1

if TPNASCASSI == 'Ignorado':
    TPNASCASSI_9 = 1

dados = {
    'IDADEMAE': [IDADEMAE],
    'PESO': [PESO],
    'SEMAGESTAC': [SEMAGESTAC],
    'CONSPRENAT': [CONSPRENAT],
    'QTDFILVIVO': [QTDFILVIVO],
    'QTDFILMORT': [QTDFILMORT],
    'QTDGESTANT': [QTDGESTANT],
    'QTDPARTNOR': [QTDPARTNOR],
    'QTDPARTCES': [QTDPARTCES],
    'ESFERA_PUBLICO': [ESFERA_PUBLICO],
    'LOCNASC_2': [LOCNASC_2],
    'LOCNASC_3': [LOCNASC_3],
    'SEXO_DN_I': [SEXO_DN_I],
    'SEXO_DN_M': [SEXO_DN_M],
    'APGAR1_1.0': [APGAR1_1],
    'APGAR1_2.0': [APGAR1_2],
    'APGAR1_3.0': [APGAR1_3],
    'APGAR1_4.0': [APGAR1_4],
    'APGAR1_5.0': [APGAR1_5],
    'APGAR1_6.0': [APGAR1_6],
    'APGAR1_7.0': [APGAR1_7],
    'APGAR1_8.0': [APGAR1_8],
    'APGAR1_9.0': [APGAR1_9],
    'APGAR1_10.0': [APGAR1_10],
    'APGAR1_99.0': [APGAR1_99],
    'APGAR5_1.0': [APGAR5_1],
    'APGAR5_2.0': [APGAR5_2],
    'APGAR5_3.0': [APGAR5_3],
    'APGAR5_4.0': [APGAR5_4],
    'APGAR5_5.0': [APGAR5_5],
    'APGAR5_6.0': [APGAR5_6],
    'APGAR5_7.0': [APGAR5_7],
    'APGAR5_8.0': [APGAR5_8],
    'APGAR5_9.0': [APGAR5_9],
    'APGAR5_10.0': [APGAR5_10],
    'APGAR5_99.0': [APGAR5_99],
    'IDANOMAL_2.0': [IDANOMAL_2],
    'IDANOMAL_9.0': [IDANOMAL_9],
    'GRAVIDEZ_2.0': [GRAVIDEZ_2],
    'GRAVIDEZ_3.0': [GRAVIDEZ_3],
    'PARTO_2.0': [PARTO_2],
    'ESCMAE2010_1.0': [ESCMAE2010_1],
    'ESCMAE2010_2.0': [ESCMAE2010_2],
    'ESCMAE2010_3.0': [ESCMAE2010_3],
    'ESCMAE2010_4.0': [ESCMAE2010_4],
    'ESCMAE2010_5.0': [ESCMAE2010_5],
    'ESCMAE2010_9.0': [ESCMAE2010_9],
    'RACACORMAE_2.0': [RACACORMAE_2],
    'RACACORMAE_3.0': [RACACORMAE_3],
    'RACACORMAE_4.0': [RACACORMAE_4],
    'RACACORMAE_5.0': [RACACORMAE_5],
    'RACACORMAE_9.0': [RACACORMAE_9],
    'MESPRENAT_2.0': [MESPRENAT_2],
    'MESPRENAT_3.0': [MESPRENAT_3],
    'MESPRENAT_4.0': [MESPRENAT_4],
    'MESPRENAT_5.0': [MESPRENAT_5],
    'MESPRENAT_6.0': [MESPRENAT_6],
    'MESPRENAT_7.0': [MESPRENAT_7],
    'MESPRENAT_8.0': [MESPRENAT_8],
    'MESPRENAT_9.0': [MESPRENAT_9],
    'MESPRENAT_10.0': [MESPRENAT_10],
    'MESPRENAT_99.0': [MESPRENAT_99],
    'TPAPRESENT_2.0': [TPAPRESENT_2],
    'TPAPRESENT_3.0': [TPAPRESENT_3],
    'TPAPRESENT_9.0': [TPAPRESENT_9],
    'STTRABPART_2.0': [STTRABPART_2],
    'STTRABPART_9.0': [STTRABPART_9],
    'TPNASCASSI_2.0': [TPNASCASSI_2],
    'TPNASCASSI_3.0': [TPNASCASSI_3],
    'TPNASCASSI_4.0': [TPNASCASSI_4],
    'TPNASCASSI_9.0': [TPNASCASSI_9]
}
df = pd.DataFrame.from_dict(dados)
st.dataframe(df)

model = joblib.load('model_st.pkl')
explainer = shap.TreeExplainer(model)

if st.button('Executar predição'):
    pred= model.predict(df)
    shap_values = explainer.shap_values(df)
    if pred == 0:
        st.success('Óbito Neonatal: Baixa')
        st.write('Probabilidade de óbito neonatal: ', model.predict_proba(df)[:,1][0])
    if pred == 1:
        st.warning('Óbito Neonatal: Razoavel')
        st.write('Probabilidade de óbito neonatal: ', model.predict_proba(df)[:,1][0])
    shap.force_plot(explainer.expected_value, shap_values[0,:], df.iloc[0,:], 
link='logit', matplotlib=True, figsize=(25,3))
    st.pyplot(bbox_inches='tight',dpi=300,pad_inches=0)
    #plt.clf()
