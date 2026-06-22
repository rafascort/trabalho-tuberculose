# Como rodar o projeto no VSCode (passo a passo)

Guia para executar tudo com a **base completa** (~560 mil casos). Feito para quem
esta comecando - siga na ordem.

## 1. Programas necessarios (uma vez so)

1. **Python 3.11** (ou 3.10): instale de https://www.python.org/downloads/
   - No instalador, marque a caixa **"Add Python to PATH"**.
2. **VSCode**: https://code.visualstudio.com/
3. No VSCode, instale as extensoes (icone de blocos na lateral esquerda):
   - **Python** (Microsoft)
   - **Jupyter** (Microsoft)

## 2. Abrir o projeto

- VSCode -> menu **File > Open Folder** -> selecione a pasta `projeto-tuberculose`.

## 3. Criar o ambiente e instalar as bibliotecas

Abra o terminal no VSCode (**Terminal > New Terminal**) e rode, uma linha por vez:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install torch
```

> Observacoes:
> - A linha `.venv\Scripts\activate` e para **Windows**. No Mac/Linux seria `source .venv/bin/activate`.
> - `pip install torch` baixa o backend da rede neural (pode demorar uns minutos).
> - Se aparecer "torch ja instalado", tudo bem, e so seguir.

## 4. Rodar os notebooks

1. Na lateral esquerda, abra a pasta `notebooks/`.
2. Abra o **01_preparacao_dados.ipynb**.
3. No canto **superior direito**, clique em **"Select Kernel"** e escolha o
   ambiente **.venv** (Python).
4. Clique em **"Run All"** (executar tudo) no topo do notebook.
5. Repita para os notebooks na ordem: **02, 03, 04, 05**.

### O que esperar em cada um
- **01**: carrega os dados e mostra o pre-processamento (rapido).
- **02**: graficos da analise exploratoria (rapido).
- **03**: regressao logistica na base completa. Mostra "Tamanho do treino usado: 562632".
  Leva ~1-3 min.
- **04**: rede neural (Keras/torch) na base completa. E o mais demorado
  (pode levar alguns minutos). Mostra o resumo do modelo e a curva de aprendizado.
- **05**: comparacao dos modelos, importancia das variaveis e SHAP.

> Os modelos treinados sao salvos automaticamente em `models/` e podem ser usados
> depois

## 5. Memoria

Os notebooks usam a **base completa** (~560 mil linhas) de proposito, para extrair
todo o desempenho. Por isso, o notebook 04 (rede neural) e o 06 (busca de
hiperparametros) sao pesados e podem demorar e consumir bastante memoria - rode num
computador com RAM suficiente e, de preferencia, um notebook de cada vez.

## Dica
Rode **um notebook de cada vez** e espere terminar antes de abrir o proximo, para
nao competir por memoria.

## Observação
A pasta data/raw não está no GitHub, caso queira reprocessar todos os dados para gerar treino/teste os dados estão disponíveis em https://drive.google.com/drive/folders/1qd1XTZ8_xqACKJiJCxMC4r4fIC1h3Qag?usp=drive_link
