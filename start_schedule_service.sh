#!/bin/bash

# Navega até o diretório do projeto
cd /home/fylip/Desktop/relatorio_notas_fiscais || exit

# Ativa o ambiente virtual do Python
source env/bin/activate

# Executa o script schedule_task.py
python3 schedule_task.py
