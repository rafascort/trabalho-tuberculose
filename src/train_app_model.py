# Treina o modelo de producao (poucas variaveis) que o app usa.
import os,sys,json,warnings; warnings.filterwarnings("ignore"); sys.path.insert(0,os.path.dirname(__file__))
import pandas as pd, numpy as np, joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
BASE=os.path.dirname(os.path.dirname(__file__)); MOD=BASE+"/models"; ALVO="ltfu"
# poucas variaveis, conhecidas no inicio do tratamento e relevantes (xAI)
NUM=["idade_anos"]
CAT=["AGRAVALCOO","AGRAVDROGA","AGRAVTABAC","HIV","TRAT_SUPER","POP_RUA","BENEF_GOV"]
def prep(df):
    df=df.copy(); df["idade_anos"]=pd.to_numeric(df["idade_anos"],errors="coerce")
    for c in CAT:
        df[c]=df[c].map(lambda v:"ignorado" if pd.isna(v) else (str(int(v)) if isinstance(v,float) and float(v).is_integer() else str(v)))
    return df[NUM+CAT]
tr=pd.read_csv(BASE+"/data/processed/treino.csv"); t1=pd.read_csv(BASE+"/data/processed/teste1.csv"); t2=pd.read_csv(BASE+"/data/processed/teste2.csv")
ct=ColumnTransformer([("num",Pipeline([("sc",StandardScaler())]),NUM),
                      ("cat",OneHotEncoder(handle_unknown="ignore"),CAT)])
pipe=Pipeline([("prep",ct),("clf",LogisticRegression(max_iter=300,class_weight="balanced"))])
pipe.fit(prep(tr),tr[ALVO])
for nome,d in [("teste1",t1),("teste2",t2)]:
    auc=roc_auc_score(d[ALVO],pipe.predict_proba(prep(d))[:,1]); print(f"AUC producao {nome}: {auc:.3f}",flush=True)
joblib.dump(pipe,MOD+"/modelo_producao.joblib")
json.dump({"NUM":NUM,"CAT":CAT},open(MOD+"/features_producao.json","w"))
# limiares de risco (tercis das probabilidades no treino) p/ classificar Baixo/Medio/Alto
p=pipe.predict_proba(prep(tr))[:,1]; q=np.quantile(p,[0.5,0.8])
json.dump({"limiar_medio":float(q[0]),"limiar_alto":float(q[1])},open(MOD+"/limiares_producao.json","w"))
print("limiares (medio/alto):",round(q[0],3),round(q[1],3))
print("modelo de producao salvo.")
