from pyspark.sql import DataFrame

def limpar_dados(df: DataFrame) -> DataFrame:

  # Remove linhas onde todas as colunas são nulas
    df = df.na.drop(how="all")
    # Remove duplicatas
    df = df.dropDuplicates()
    # Substitui nulos restantes por vazio
    df = df.na.fill("")

    return df
