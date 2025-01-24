sudo systemctl daemon-reload
sudo systemctl enable schedule_task.service
sudo systemctl start schedule_task.service

# status
sudo systemctl status schedule_task.service
# logs
journalctl -u schedule_task.service -f
# Restart
sudo systemctl restart schedule_task.service

# Bash criado
[Unit]
Description=Serviço para executar o script schedule_task.py
After=network.target

[Service]
Type=simple
User=fylip
WorkingDirectory=/home/fylip/Desktop/relatorio_notas_fiscais
ExecStart=/home/fylip/Desktop/relatorio_notas_fiscais/start_schedule_service.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
