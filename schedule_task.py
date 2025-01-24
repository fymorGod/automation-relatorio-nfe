import schedule
import time
import subprocess

# Função para executar o main.py
def executar_main():
    subprocess.run(["python", "/home/fylip/Desktop/relatorio_notas_fiscais/main.py"])

# Função para executar o send_mail.py
def executar_send_mail():
    subprocess.run(["python", "/home/fylip/Desktop/relatorio_notas_fiscais/send_mail.py"])

# Agendar a execução do main.py às 7h da manhã
schedule.every().day.at("07:01").do(executar_main)

# Agendar a execução do send_mail.py às 7h05 (5 minutos após o main.py)
schedule.every().day.at("07:02").do(executar_send_mail)

# Loop para verificar as tarefas agendadas
while True:
    schedule.run_pending()
    time.sleep(1)
