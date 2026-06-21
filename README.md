# Predicao do Abandono do Tratamento de Tuberculose (LTFU)

Projeto de Machine Learning para estimar a **probabilidade de um paciente abandonar
o tratamento de tuberculose** (LTFU - *Loss to Follow-Up*), a partir dos microdados
do SINAN/DataSUS. O codigo segue o mesmo padrao usado nas aulas.

## Estrutura das pastas

```
projeto-tuberculose/
├── data/
│   ├── raw/          -> base bruta (tuberculose_unificado.feather)  
│   └── processed/    -> treino.csv, teste1.csv, teste2.csv 
├── src/              -> codigo reutilizavel
│   ├── data_prep.py        (feather bruto -> treino/teste1/teste2)
│   └── preprocessing.py    (listas de variaveis + ColumnTransformer)
├── notebooks/        -> 01 a 05, na ordem da analise (rodam no VSCode)
├── models/           -> modelos e transformadores salvos (.joblib / .keras)
├── docs/             -> dicionario de dados e decisoes
├── requirements.txt
└── README.md
```

## Para que serve cada pasta

- **data/raw**: a base original do SINAN (um arquivo .feather gigante). serve só para regerar os CSVs.
- **data/processed**: os tres conjuntos ja limpos e divididos. Sao a entrada dos modelos.
- **src**: scripts que os notebooks importam, para nao repetir codigo.
- **notebooks**: onde a analise acontece, passo a passo, com comentarios curtos.
- **models**: o "cerebro" treinado, salvo para reuso (ex.: num app).
- **docs**: documentacao (dicionario de dados, decisoes de tratamento).

## Como rodar

```bash
pip install -r requirements.txt
```
Depois, abra a pasta `notebooks/` no VSCode e rode na ordem **01 -> 05**.
(Os CSVs ja vem prontos em `data/processed/`; o passo do feather e opcional.)

## Notebooks

| Nº | Arquivo | Conteudo |
|----|---------|----------|
| 01 | 01_preparacao_dados.ipynb | Da base bruta aos splits; ColumnTransformer |
| 02 | 02_eda.ipynb | Analise exploratoria (alvo, missings, variaveis) |
| 03 | 03_regressao_logistica.ipynb | Modelo baseline + interpretacao |
| 04 | 04_rede_neural.ipynb | Rede neural (Keras, backend torch) |
| 05 | 05_avaliacao_xai.ipynb | Comparacao, threshold, Permutation Importance, SHAP |
| 06 | 06_tuning_hiperparametros.ipynb | Busca de hiperparametros (evidencia de que o baseline ja e otimo) |

## Protocolo de avaliacao

1. Treina em `treino.csv` -> avalia em `teste1.csv`.
2. Junta `teste1.csv` ao treino -> avalia em `teste2.csv`.

## Resultados (resumo)

| Modelo | Conjunto | ROC-AUC | F1 | Recall |
|--------|----------|---------|----|--------|
| Reg. Logistica | teste1 | 0,781 | 0,684 | 0,758 |
| Reg. Logistica | teste2 | 0,752 | 0,786 | 0,769 |
| Rede Neural | teste1 | 0,785 | 0,682 | 0,783 |
| Rede Neural | teste2 | 0,757 | 0,777 | 0,756 |


## Notas de estilo

- Pre-processamento com `ColumnTransformer`, sem classes customizadas.
- Desbalanceamento tratado com `class_weight='balanced'`.
- Rede neural com **Keras 3**.

## App de producao (Streamlit)

Prototipo de apoio a decisao para o profissional de saude: poucos campos de entrada,
retorna a probabilidade de abandono + classificacao de risco + acoes sugeridas.
Usa um modelo reduzido a 8 variaveis (em `models/modelo_producao.joblib`).

```bash
streamlit run app/app.py
```
