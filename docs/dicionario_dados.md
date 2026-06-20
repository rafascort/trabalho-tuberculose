# Dicionario de Dados

Variaveis dos microdados do SINAN (Sistema de Informacao de Agravos de Notificacao)
usadas no projeto. Os codigos seguem a ficha de notificacao/investigacao de
Tuberculose do Ministerio da Saude.

## Variavel-alvo

| Variavel | Origem | Descricao | Codificacao |
|----------|--------|-----------|-------------|
| `ltfu` | derivada de `SITUA_ENCE` | Desfecho do tratamento (alvo da predicao) | **1 = abandono** (SITUA_ENCE=2); **0 = cura** (SITUA_ENCE=1) |

`SITUA_ENCE` (situacao de encerramento) original: 1=Cura, 2=Abandono, 3=Obito por TB,
4=Obito por outra causa, 5=Transferencia, 6=Mudanca de diagnostico, 7=TB-DR, 8=Mudanca
de esquema, 9=Falencia. **Mantivemos apenas 1 e 2** (desfechos comparaveis cura/abandono).

## Variaveis preditoras

### Numericas
| Variavel | Descricao |
|----------|-----------|
| `idade_anos` | Idade do paciente em anos (decodificada de `NU_IDADE_N`) |
| `NU_CONTATO` | Numero de contatos identificados/examinados |
| `dias_diag_trat` | Dias entre a data de diagnostico (`DT_DIAG`) e o inicio do tratamento (`DT_INIC_TR`) (variavel criada) |

### Categoricas (codigos do SINAN)
| Variavel | Descricao | Principais codigos |
|----------|-----------|--------------------|
| `CS_SEXO` | Sexo | M=Masculino, F=Feminino, I=Ignorado |
| `CS_RACA` | Raca/cor | 1=Branca, 2=Preta, 3=Amarela, 4=Parda, 5=Indigena, 9=Ignorado |
| `CS_ESCOL_N` | Escolaridade | 0=Analfabeto ... 10=Superior completo, 9=Ignorado |
| `SG_UF_NOT` | UF de notificacao | Codigo IBGE da Unidade Federativa |
| `RAIOX_TORA` | Resultado do raio-X de torax | 1=Suspeito, 2=Normal, 3=Outra patologia, 4=Nao realizado |
| `TESTE_TUBE` | Teste tuberculinico (PPD) | 1=Nao reator, 2=Reator fraco, 3=Reator forte, 4=Nao realizado |
| `BACILOSC_E` | Baciloscopia de escarro (diagnostico) | 1=Positivo, 2=Negativo, 3=Nao realizado, 4=Nao se aplica |
| `HIV` | Resultado da sorologia HIV | 1=Positivo, 2=Negativo, 3=Em andamento, 4=Nao realizado |
| `AGRAVAIDS` | Agravo associado: AIDS | 1=Sim, 2=Nao, 9=Ignorado |
| `AGRAVALCOO` | Agravo associado: alcoolismo | 1=Sim, 2=Nao, 9=Ignorado |
| `AGRAVDIABE` | Agravo associado: diabetes | 1=Sim, 2=Nao, 9=Ignorado |
| `AGRAVDOENC` | Agravo associado: doenca mental | 1=Sim, 2=Nao, 9=Ignorado |
| `AGRAVDROGA` | Agravo associado: uso de drogas ilicitas | 1=Sim, 2=Nao, 9=Ignorado |
| `AGRAVTABAC` | Agravo associado: tabagismo | 1=Sim, 2=Nao, 9=Ignorado |
| `TRAT_SUPER` | Tratamento Diretamente Observado (TDO/DOT) | 1=Sim, 2=Nao, 9=Ignorado |
| `ANT_RETRO` | Uso de antirretroviral (TARV) durante o tratamento | 1=Sim, 2=Nao, 9=Ignorado |
| `BENEF_GOV` | Beneficiario de programa de transferencia de renda | 1=Sim, 2=Nao, 9=Ignorado |
| `POP_RUA` | Populacao em situacao de rua | 1=Sim, 2=Nao |
| `POP_LIBER` | Populacao privada de liberdade | 1=Sim, 2=Nao |
| `POP_IMIG` | Populacao imigrante | 1=Sim, 2=Nao |
| `POP_SAUDE` | Profissional de saude | 1=Sim, 2=Nao |

> A categoria `ignorado` e criada no pre-processamento para representar valores ausentes.

## Variaveis usadas apenas como filtro (nao entram no modelo)
| Variavel | Uso |
|----------|-----|
| `NU_IDADE_N` | Codigo composto (unidade+valor) de idade; usado para derivar `idade_anos` |
| `FORMA` | Forma clinica; mantida apenas TB **pulmonar** (=1) |
| `TRATAMENTO` | Tipo de entrada; excluido caso multirresistente (=6) |
| `CS_GESTANT` | Gestacao; usada para excluir gestantes |
| `TEST_MOLEC`, `TEST_SENSI` | Testes moleculares/sensibilidade; usados para manter casos sensiveis |
| `DT_NOTIFIC` | Data de notificacao; base para a divisao temporal treino/teste |

## Conjuntos de dados
| Arquivo | Periodo | Linhas | Taxa de abandono |
|---------|---------|--------|------------------|
| `treino.csv` | notificacoes < 2025 | 562.632 | 19,4% |
| `teste1.csv` | 1a metade de 2025 | 631 | 43,9% |
| `teste2.csv` | 2a metade de 2025 | 631 | 69,4% |
