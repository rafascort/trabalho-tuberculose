# App de Producao - Triagem de Risco de Abandono

Interface simples (Streamlit) para o profissional de saude: poucas informacoes de
entrada e, em troca, a probabilidade de abandono do tratamento + classificacao de
risco (Baixo/Medio/Alto) + acoes sugeridas.

## Modelo
Usa um modelo de **producao** treinado com um subconjunto pequeno e relevante de
variaveis (idade, alcool, drogas, tabagismo, HIV, tratamento diretamente observado,
situacao de rua e beneficio social) - por isso o profissional digita pouco.
Arquivo: `models/modelo_producao.joblib`.

## Como rodar
A partir da pasta do projeto:
```bash
pip install -r requirements.txt
streamlit run app/app.py
```
O app abre no navegador (geralmente http://localhost:8501).

## Observacao
E uma ferramenta de **apoio a decisao**, baseada em dados historicos do SINAN. Nao
substitui a avaliacao clinica. O objetivo e direcionar MAIS apoio a quem tem maior
risco, nunca negar cuidado.
