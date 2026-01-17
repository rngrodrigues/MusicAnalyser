<h1 align="center">Music Analyser</h1>
<p align="center"> ↓ Acesse o projeto </p>
<p align="center">
  <a href="https://musicanalyser.vercel.app/">
    <img src="https://img.shields.io/badge/deploy-online-green?style=for-the-badge&logo=vercel" alt="Demonstração Music Analyser" />
  </a>
</p>

## Visão Geral

O **Music Analyser** é uma aplicação desktop desenvolvida em Python para **análise eficiente de grandes volumes de dados musicais**.  
O projeto permite importar datasets em diversos formatos, processar os dados de forma otimizada e visualizar o **Top 10 de músicas mais populares por gênero** por meio de uma interface gráfica intuitiva.

O foco do projeto está em **Big Data, performance, visualização de dados e experiência do usuário**.

---

## Objetivo do Projeto
- Processar grandes datasets musicais de forma performática;
- Identificar as músicas mais populares por gênero;  
- Apresentar visualizações claras e interativas;
- Facilitar o uso mesmo para usuários não técnicos; 

---

## Funcionalidades

### Importação de Dados
- Suporte aos formatos:
  - CSV / TSV
  - Excel (`.xlsx`, `.xls`)
  - JSON
  - Parquet
- Upload via:
  - Seletor de arquivos
  - Drag and Drop
- Validação automática de formatos e colunas obrigatórias

### Processamento de Dados
- Mapeamento inteligente de colunas (nomes diferentes são reconhecidos)
- Limpeza automática:
  - Remoção de linhas nulas e duplicadas
  - Conversão segura de tipos
- Processamento em **streaming** com DuckDB
- Uso controlado de memória (processamento em disco)

### Análise e Visualização
- Cálculo do **Top 10 de músicas mais populares por gênero**;
- Gráficos horizontais interativos;
- Suporte a múltiplos idiomas e caracteres especiais;
- Seleção dinâmica de gêneros;

### Exportação de Resultados
- Exportação em:
  - PNG
  - PDF
  - CSV
  - Excel
- Opção de salvar:
  - Apenas o gênero selecionado
  - Todos os gêneros (compactados automaticamente em ZIP)

### Interface Gráfica
- Interface desenvolvida com Tkinter;
- Barra de progresso durante o processamento;
- Modais de ajuda e informações do projeto;
- Interface moderna, simples e intuitiva;

---

## Possíveis Melhorias Futuras

- Filtros avançados (ano, artista, país);
- Dashboard interativo;
- Integração com APIs de streaming;
- Versão web;
- Persistência em banco de dados;

---

## Tecnologias Utilizadas

### Linguagem e Bibliotecas
- **Python**;
- **Pandas**;
- **DuckDB**;
- **Matplotlib**;
- **Tkinter**;
- **TkinterDnD2**;

### Conceitos Aplicados

- Big Data;
- Processamento em streaming;
- Window Functions (ROW_NUMBER, PARTITION BY);
- Multithreading;
- Arquitetura modular;
- Separação de responsabilidades;
  
---

## Estrutura de Pastas

```
MusicAnalyser/
│
├── core/
│ ├── data_loader.py # Carregamento e validação de arquivos
│ ├── data_cleaner.py # Limpeza de dados
│ ├── data_processing.py # Processamento e análise com DuckDB
│ └── result_download.py # Exportação de resultados
│
├── interface/
│ ├── main_window.py # Janela principal
│ ├── result_window.py # Visualização dos resultados
│ ├── modal_help.py # Modal de ajuda
│ ├── modal_saiba_mais.py # Modal sobre o projeto
│ └── close_window.py # Encerramento da aplicação
│
├── fonts/ # Fontes para suporte multilíngue
│
├── main.py # Ponto de entrada da aplicação
└── README.md
```
---

## Prévia

![Tela inicial](https://github.com/rngrodrigues/MusicAnalyser/blob/main/img/inicio.png?raw=true)

![Tela de resultado](https://github.com/rngrodrigues/MusicAnalyser/blob/main/img/grafico.png?raw=true)

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.9 ou superior
- Pip

 ### Clonando o repositório
 
```bash
git clone https://github.com/rngrodrigues/MusicAnalyser.git
cd MusicAnalyser
```

### Instalação das dependências

```bash
pip install pandas duckdb matplotlib tkinterdnd2 openpyxl
```

### Executando a aplicação

```bash
python main.py
```


