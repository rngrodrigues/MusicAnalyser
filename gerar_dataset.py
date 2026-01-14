import csv
import json
import os
import random
import string
import sys
import time

from openpyxl import Workbook
import pyarrow as pa
import pyarrow.parquet as pq

# ===============================
# CONFIGURAÇÕES
# ===============================
PASTA_SAIDA = "dados_musicais"

TOTAL_LINHAS = 10_000_000
MAX_JSON = 1_000_000
MAX_EXCEL = 500_000

BATCH_PRINT = 100_000
PARQUET_BATCH = 500_000

GENEROS = [
    "Rock", "Pop", "Hip-Hop", "Jazz", "Blues",
    "Electronic", "Classical", "Reggae",
    "Country", "Metal"
]

TOP_POPULARIDADES = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

# ===============================
# UTILIDADES
# ===============================
def gerar_nome_musica(i):
    return f"Track_{i}_{''.join(random.choices(string.ascii_letters, k=5))}"

def barra_progresso(atual, total, inicio):
    progresso = atual / total
    largura = 40
    preenchido = int(largura * progresso)
    barra = "█" * preenchido + "-" * (largura - preenchido)

    tempo = time.time() - inicio
    vel = atual / tempo if tempo > 0 else 0
    eta = (total - atual) / vel if vel > 0 else 0

    sys.stdout.write(
        f"\r[{barra}] {progresso*100:6.2f}% | "
        f"{atual:,}/{total:,} | ETA: {int(eta)}s"
    )
    sys.stdout.flush()

# ===============================
# MAIN
# ===============================
def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    inicio = time.time()

    # CSV / TSV
    csv_file = open(os.path.join(PASTA_SAIDA, "dados.csv"), "w", newline="", encoding="utf-8")
    tsv_file = open(os.path.join(PASTA_SAIDA, "dados.tsv"), "w", newline="", encoding="utf-8")

    csv_writer = csv.writer(csv_file)
    tsv_writer = csv.writer(tsv_file, delimiter="\t")

    header = ["genre", "track_name", "popularity"]
    csv_writer.writerow(header)
    tsv_writer.writerow(header)

    # JSON streaming (array)
    json_file = open(os.path.join(PASTA_SAIDA, "dados_10M.json"), "w", encoding="utf-8")
    json_file.write("[")
    first_json = True

    # Excel streaming
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("dados")
    ws.append(header)

    # Parquet
    parquet_path = os.path.join(PASTA_SAIDA, "dados.parquet")
    parquet_writer = None
    parquet_buffer = []

    linhas = 0
    id_musica = 1

    # Top hits
    for genero in GENEROS:
        for pop in TOP_POPULARIDADES:
            row = [genero, gerar_nome_musica(id_musica), pop]

            csv_writer.writerow(row)
            tsv_writer.writerow(row)

            if linhas < MAX_JSON:
                if not first_json:
                    json_file.write(",")
                json.dump(
                    {"genre": row[0], "track_name": row[1], "popularity": row[2]},
                    json_file,
                    ensure_ascii=False
                )
                first_json = False

            if linhas < MAX_EXCEL:
                ws.append(row)

            parquet_buffer.append(
                {"genre": row[0], "track_name": row[1], "popularity": row[2]}
            )

            linhas += 1
            id_musica += 1

    # Restante
    while linhas < TOTAL_LINHAS:
        row = [
            random.choice(GENEROS),
            gerar_nome_musica(id_musica),
            round(random.uniform(1, 89), 2)
        ]

        csv_writer.writerow(row)
        tsv_writer.writerow(row)

        if linhas < MAX_JSON:
            if not first_json:
                json_file.write(",")
            json.dump(
                {"genre": row[0], "track_name": row[1], "popularity": row[2]},
                json_file,
                ensure_ascii=False
            )
            first_json = False

        if linhas < MAX_EXCEL:
            ws.append(row)

        parquet_buffer.append(
            {"genre": row[0], "track_name": row[1], "popularity": row[2]}
        )

        if len(parquet_buffer) >= PARQUET_BATCH:
            table = pa.Table.from_pylist(parquet_buffer)
            if parquet_writer is None:
                parquet_writer = pq.ParquetWriter(parquet_path, table.schema)
            parquet_writer.write_table(table)
            parquet_buffer.clear()

        linhas += 1
        id_musica += 1

        if linhas % BATCH_PRINT == 0:
            barra_progresso(linhas, TOTAL_LINHAS, inicio)

    # Finalizações
    if parquet_buffer:
        table = pa.Table.from_pylist(parquet_buffer)
        if parquet_writer is None:
            parquet_writer = pq.ParquetWriter(parquet_path, table.schema)
        parquet_writer.write_table(table)

    if parquet_writer:
        parquet_writer.close()

    json_file.write("]")
    json_file.close()

    wb.save(os.path.join(PASTA_SAIDA, "dados_1M.xlsx"))

    csv_file.close()
    tsv_file.close()

    barra_progresso(TOTAL_LINHAS, TOTAL_LINHAS, inicio)
    print("\n✅ FINALIZADO COM SUCESSO")

# ===============================
if __name__ == "__main__":
    main()
