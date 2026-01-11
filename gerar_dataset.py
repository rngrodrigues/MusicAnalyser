import os
import random
import string
import pandas as pd
from tqdm import tqdm

# ================= CONFIGURAÇÕES =================
ARQUIVO_SAIDA = "music_data_gigante.parquet"
LINHAS_TOTAIS = 25_000_000  # aproximadamente ~11GB de RAM, seguro para 16GB
LINHAS_POR_BLOCO = 1_000_000
SEED = 42
# =================================================

random.seed(SEED)

GENEROS = [
    "Pop", "Rock", "Hip Hop", "Jazz", "Classical",
    "Electronic", "Reggae", "Metal", "Blues", "Country"
]

def gerar_nome_musica():
    return ''.join(random.choices(string.ascii_letters + " ", k=random.randint(8, 25))).strip()

def gerar_popularidade():
    return random.randint(0, 100)

def main():
    blocos = []
    blocos_gerados = 0
    total_blocos = (LINHAS_TOTAIS // LINHAS_POR_BLOCO) + 1

    with tqdm(total=LINHAS_TOTAIS, unit="linhas", dynamic_ncols=True, desc="Gerando Parquet") as pbar:
        while blocos_gerados < total_blocos:
            # Calcula quantas linhas gerar neste bloco
            linhas_no_bloco = min(LINHAS_POR_BLOCO, LINHAS_TOTAIS - blocos_gerados * LINHAS_POR_BLOCO)

            df = pd.DataFrame({
                "genre": [random.choice(GENEROS) for _ in range(linhas_no_bloco)],
                "track_name": [gerar_nome_musica() for _ in range(linhas_no_bloco)],
                "popularity": [gerar_popularidade() for _ in range(linhas_no_bloco)]
            })

            blocos.append(df)
            blocos_gerados += 1
            pbar.update(linhas_no_bloco)

    print("\n🔹 Concatenando blocos e gravando arquivo Parquet único...")
    df_final = pd.concat(blocos, ignore_index=True)
    df_final.to_parquet(ARQUIVO_SAIDA, engine="pyarrow", index=False, compression="snappy")

    tamanho_final = os.path.getsize(ARQUIVO_SAIDA) / (1024**3)
    print(f"\n✅ Geração finalizada! Arquivo: {ARQUIVO_SAIDA}")
    print(f"Tamanho final no disco: {tamanho_final:.2f} GB")

if __name__ == "__main__":
    main()
