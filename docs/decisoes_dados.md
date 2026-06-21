# Documentacao das Decisoes de Manipulacao dos Dados

Este documento registra e justifica todas as decisoes tomadas no tratamento dos
dados, conforme exigido pelo projeto.

## 1. Recorte da populacao (filtros)

Partimos de **2.188.471** registros brutos do SINAN (todos os anos). Aplicamos os
filtros abaixo, chegando a **563.894** casos validos.

| Filtro | Justificativa |
|--------|---------------|
| Idade >= 18 anos | O abandono em adultos tem fatores distintos dos pediatricos; foco no publico adulto. |
| `FORMA` = pulmonar | TB pulmonar e a forma transmissivel e mais prevalente; padroniza o desfecho. |
| Exclui multirresistente (`TRATAMENTO`=6, `TEST_MOLEC`/`TEST_SENSI`) | Casos resistentes tem esquema e duracao diferentes (ate 18-24 meses), o que mudaria o significado de "abandono". |
| Exclui gestantes (`CS_GESTANT`) | Manejo e adesao especificos; evita confundimento. |
| `SITUA_ENCE` em {1,2} | Mantem apenas desfechos comparaveis: cura (0) e abandono (1). Removidos obitos, transferencias e mudanca de diagnostico. |

## 2. Criacao da variavel-alvo

`ltfu` = 1 se `SITUA_ENCE` = 2 (abandono), 0 se `SITUA_ENCE` = 1 (cura). Linhas sem
esse desfecho foram removidas.

## 3. Divisao treino/teste (temporal)

A divisao **nao** e aleatoria: e **temporal**, para simular o uso real (treinar no
passado, prever o futuro).
- **treino**: notificacoes anteriores a 2025.
- **teste1**: primeira metade de 2025 (ordenada por data).
- **teste2**: segunda metade de 2025.

Protocolo: treina-se no treino e avalia-se no teste1; depois incorpora-se o teste1 ao
treino e avalia-se no teste2. Os conjuntos de teste sao usados o minimo possivel.

### Alerta metodologico: censura a direita
A taxa de abandono salta de **19,4%** (treino) para **43,9%** (teste1) e **69,4%**
(teste2). Isso **nao** e erro: como a cura so e registrada apos ~6 meses de
tratamento, os casos de 2025 ja encerrados sao desproporcionalmente abandonos
(que encerram mais cedo). E uma mudanca real de distribuicao entre treino e teste,
discutida no relatorio - e um motivo para priorizar metricas como ROC-AUC, menos
sensiveis a prevalencia.

## 4. Variaveis criadas (feature engineering)

| Variavel | Como foi criada |
|----------|-----------------|
| `idade_anos` | Decodificada de `NU_IDADE_N` (unidade + valor) para anos. |
| `dias_diag_trat` | `DT_INIC_TR` - `DT_DIAG`; atrasos negativos ou > 365 dias viram ausentes. |

## 5. Variaveis removidas

- **Vazamento (data leakage):** `SITUA_ENCE` (origem do alvo) e variaveis so conhecidas
  no fim do tratamento (ex.: baciloscopia do 6o mes).
- **Identificadores e datas administrativas** sem valor preditivo.
- **Constantes pos-filtro:** `FORMA`, `TEST_SENSI` (passam a ter um unico valor).

## 6. Valores ausentes (missing)

- **Numericas:** imputadas pela **mediana** (`SimpleImputer`).
- **Categoricas:** o ausente vira a categoria **`ignorado`** (no SINAN, "nao informado"
  e em si uma informacao relevante).

## 7. Outliers

- `NU_CONTATO` > 50 e tratado como ausente (provavel erro de digitacao).
- `dias_diag_trat` fora de [0, 365] dias tratado como ausente.

## 8. Normalizacao e codificacao

- **Numericas:** `StandardScaler` (media 0, desvio 1).
- **Categoricas:** `OneHotEncoder(drop='first')`, com `handle_unknown='ignore'` para
  lidar com categorias novas nos conjuntos de teste.
- Tudo encapsulado em um `ColumnTransformer` , garantindo que
  os parametros sejam aprendidos **apenas no treino** e aplicados ao teste.

## 9. Desbalanceamento de classes

Optamos por `class_weight='balanced'` na regressao logistica e por **pesos de classe**
no `fit` da rede neural. Justificativa: o **SMOTE**  e inviavel em
~560 mil linhas pelo custo computacional do calculo de vizinhos.

## 10. Reprodutibilidade

`random_state=42` em todas as etapas estocasticas; pipeline de pre-processamento
reaproveitavel em `src/preprocessing.py`.
