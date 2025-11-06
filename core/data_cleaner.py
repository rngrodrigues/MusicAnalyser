import pandas as pd

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    # Remove linhas onde todas as colunas são nulas
    df = df.dropna(how="all")

    # Remove duplicatas
    df = df.drop_duplicates()

    # Substitui nulos restantes por vazio
    df = df.fillna("")

    return df

