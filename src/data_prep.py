# Gera treino/teste1/teste2 a partir do feather bruto do SINAN.
# (detalhes em docs/decisoes_dados.md)

import os
import polars as pl

# Caminhos relativos à raiz do projeto
RAW = os.path.join("data", "raw", "tuberculose_unificado.feather")
OUT = os.path.join("data", "processed")
os.makedirs(OUT, exist_ok=True)


def preparar(df: pl.DataFrame) -> pl.DataFrame:
    # limpeza, filtros e criacao do alvo

    # 1) Limpeza de strings (remove espaços das colunas de texto do SINAN)
    df = df.with_columns(pl.col(pl.Utf8).str.strip_chars())

    # 2) Trata idade vazia e decompõe NU_IDADE_N (unidade + valor) em anos
    df = df.with_columns(
        pl.when(pl.col("NU_IDADE_N") == "").then(None)
        .otherwise(pl.col("NU_IDADE_N")).alias("NU_IDADE_N")
    )
    df = df.with_columns(
        pl.col("NU_IDADE_N").str.slice(0, 1).cast(pl.Int8, strict=False).alias("idade_unid"),
        pl.col("NU_IDADE_N").str.slice(1, 3).cast(pl.Int16, strict=False).alias("idade_val"),
    )
    df = df.with_columns(
        pl.when(pl.col("idade_unid") == 4).then(pl.col("idade_val"))            # anos
        .when(pl.col("idade_unid") == 3).then((pl.col("idade_val") / 12).floor())   # meses
        .when(pl.col("idade_unid") == 2).then((pl.col("idade_val") / 365).floor())  # dias
        .otherwise(None).cast(pl.Int16).alias("idade_anos")
    )

    # 3) Recorte populacional (filtros justificáveis - ver documentação)
    df = (
        df
        .filter(pl.col("idade_anos") >= 18)                # adultos
        .filter(pl.col("FORMA") == "1")                    # TB pulmonar
        .filter(pl.col("TRATAMENTO") != "6")               # exclui multirresistente
        .filter(pl.col("POP_RUA").is_in(["1", "2"]) | pl.col("POP_RUA").is_null())
        .filter(pl.col("POP_LIBER").is_in(["1", "2"]) | pl.col("POP_LIBER").is_null())
        .filter(pl.col("POP_IMIG").is_in(["1", "2"]) | pl.col("POP_IMIG").is_null())
        .filter(pl.col("POP_SAUDE").is_in(["2", "9"]) | pl.col("POP_SAUDE").is_null())
        .filter(pl.col("CS_GESTANT").is_in(["5", "6", "9"]) | pl.col("CS_GESTANT").is_null())
        .filter(~pl.col("TEST_MOLEC").is_in(["2"]))        # sem resistência detectada
        .filter(~pl.col("TEST_SENSI").is_in(["1", "2", "3", "4"]))
        .filter(pl.col("SITUA_ENCE") != "7")               # remove transferências
        .filter(pl.col("SITUA_ENCE").is_in(["1", "2"]))    # apenas cura/abandono
    )

    # 4) Variável-alvo: 1 = abandono (SITUA_ENCE=2), 0 = cura (SITUA_ENCE=1)
    df = df.with_columns(
        pl.when(pl.col("SITUA_ENCE") == "2").then(1)
        .when(pl.col("SITUA_ENCE") == "1").then(0)
        .otherwise(None).cast(pl.Int8).alias("ltfu")
    )
    df = df.drop_nulls(subset=["ltfu"])
    return df


def main():
    print("Lendo feather bruto...")
    df = pl.read_ipc(RAW)
    df = preparar(df)

    # Split temporal: treino (<2025) e teste (2025), este dividido ao meio por data
    df_train = df.filter(pl.col("DT_NOTIFIC").dt.year() < 2025)
    df_2025 = df.filter(pl.col("DT_NOTIFIC").dt.year() == 2025).sort("DT_NOTIFIC")

    corte = df_2025.height // 2
    test1 = df_2025.head(corte)
    test2 = df_2025.tail(df_2025.height - corte)

    df_train.write_csv(os.path.join(OUT, "treino.csv"))
    test1.write_csv(os.path.join(OUT, "teste1.csv"))
    test2.write_csv(os.path.join(OUT, "teste2.csv"))

    # Relatório rápido de saída
    for nome, d in [("treino", df_train), ("teste1", test1), ("teste2", test2)]:
        taxa = d["ltfu"].mean()
        print(f"{nome}: {d.height:>8} linhas | taxa de abandono = {taxa:.4f}")


if __name__ == "__main__":
    main()
