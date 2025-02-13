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

[VersionOne]
# import cx_Oracle
# import pandas as pd
# from datetime import datetime, timedelta
# import weasyprint
# import pytz
# import locale

# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# oracle_config = {
#     "user": "integra",
#     "password": "integra",
#     "dsn": "192.168.0.42:1521/POTIGUAR",
#     "encoding": "UTF-8"
# }

# mapeamento_colunas = {
#     "unidade_entrada": "UNIDADE_ENTRADA",
#     "DT_ENTRADA": "DT_ENTRADA",
#     "T073_CODIGO_EMITENTE_IU": "COD_FORNECEDOR", 
#     "NF": "NF",
#     "razao_social": "RAZAO_SOCIAL",
#     "T057_SEQUENCIAL_PARCELA": "PARCELA",
#     "Valor_Total": "VALOR_TOTAL",
#     "Vencimento": "VENCIMENTO",
#     "Dias": "DIAS",
#     "valor": "VALOR",
#     "Num_Pedido": "NUM_PEDIDO",
#     "comprador": "COMPRADOR"
# }

# def formatar_moeda(valor):
#     if isinstance(valor, (int, float)):
#         valor_formatado = locale.currency(valor, grouping=True)
#         return valor_formatado
#     else:
#         return "Valor inválido"

# total_valor_valor = 0
# def executar_consulta():
#     data_atual = datetime.now()
#     data_anterior = data_atual - timedelta(days=1)
#     data_inicio = data_anterior.strftime('%Y-%m-%d 00:00:00')
#     data_fim = data_anterior.strftime('%Y-%m-%d 23:59:59')

#     consulta_sql = f"""
#     SELECT
#         te.T073_UNIDADE_IE AS unidade_entrada,
#         te.T073_DATA_MOVIMENTO_CONTABIL AS DT_ENTRADA,
#         te.T073_NOTA_FISCAL_IU || '-' || te.T073_SERIE_IU AS NF,
#         te.T073_CODIGO_EMITENTE_IU AS COD_FORNECEDOR,
#         tf.T019_RAZAO_SOCIAL AS razao_social,
#         te.T073_VALOR_CONTABIL AS Valor_Total,
#         trunc(ttp.T057_DATA_LIMITE) AS Vencimento,
#         trunc(ttp.T057_DATA_LIMITE) - trunc(ttp.T057_DATA_EMISSAO) AS Dias,
#         ttp.T057_SEQUENCIAL_PARCELA AS Parcela,
#         ttp.T057_VALOR_BRUTO AS valor,
#         tpp.T108_NUMERO_PEDIDO_IU AS Num_Pedido,
#         tpp.T108_COMPRADOR AS comprador
#     FROM
#         DBAMDATA.T073_ENTRADA te
#     LEFT JOIN DBAMDATA.T019_FORNECEDOR tf 
#         ON tf.T019_FORNECEDOR_IU = te.T073_CODIGO_EMITENTE_IU
#     LEFT JOIN DBAMDATA.T108_PEDIDOS_PEND tpp 
#         ON tpp.T108_NUMERO_PEDIDO_IU = te.T073_NUMERO_PEDIDO_E
#         AND tpp.T108_UNIDADE_IE = te.T073_UNIDADE_IE
#     LEFT JOIN DBAMDATA.T057_TITULO_PAGAR ttp 
#         ON ttp.T057_UNIDADE_IE = te.T073_UNIDADE_IE
#         AND ttp.T057_NOTA_FISCAL = te.T073_NOTA_FISCAL_IU
#         AND ttp.T057_FORNECEDOR_E = te.T073_CODIGO_EMITENTE_IU
#         AND ttp.T057_NUMERO_PEDIDO_E = tpp.T108_NUMERO_PEDIDO_IU
#     WHERE
#         TE.T073_NATUREZA_OPERACAO_E IN (110201, 110250, 140301, 140350, 210201, 210250, 
#                                         240301, 240350, 265201, 265250, 211701, 211750, 
#                                         211601, 211650)
#         AND te.T073_DATA_MOVIMENTO_CONTABIL BETWEEN 
#             TO_DATE('{data_inicio}', 'YYYY-MM-DD HH24:MI:SS') AND 
#             TO_DATE('{data_fim}', 'YYYY-MM-DD HH24:MI:SS')
#     ORDER BY
#         tf.T019_RAZAO_SOCIAL,
#         T073_NOTA_FISCAL_IU,
#         ttp.T057_SEQUENCIAL_PARCELA
#     """

#     try:
#         with cx_Oracle.connect(**oracle_config) as conexao:
#             with conexao.cursor() as cursor:
#                 cursor.execute(consulta_sql)
#                 resultados = cursor.fetchall()
#                 colunas = [col[0] for col in cursor.description]
#                 df = pd.DataFrame(resultados, columns=colunas)
                
#                 if df.empty:
#                     print("Nenhum dado encontrado na consulta. O PDF não será gerado.")
#                     return  # Encerra a execução caso não haja dados
                
#                 print("Colunas originais do DataFrame:", df.columns)

#                 df = df.rename(columns=mapeamento_colunas)
#                 df = df.fillna(0)

#                 if 'VENCIMENTO' in df.columns:
#                     df['VENCIMENTO'] = df['VENCIMENTO'].fillna(0)
#                     df['VENCIMENTO'] = df['VENCIMENTO'].apply(
#                         lambda x: " " if x == 0 else pd.to_datetime(x).strftime('%d-%m-%Y')
#                     )
#                 else:
#                     print("Coluna 'VENCIMENTO' não encontrada no DataFrame.")

#                 if 'DT_ENTRADA' in df.columns:
#                     df['DT_ENTRADA'] = pd.to_datetime(df['DT_ENTRADA']).dt.strftime('%d-%m-%Y')
#                 else:
#                     print("Coluna 'DT_ENTRADA' não encontrada no DataFrame.")

#                 if 'PARCELA' in df.columns:
#                     df['PARCELA'] = df['PARCELA'].fillna(0)

#                     df['PARCELA'] = df['PARCELA'].apply(
#                         lambda x: "" if x == 0 else int(x)
#                     )
#                 else:
#                     print("Coluna 'Parcela' não encontrada no DataFrame.")
#                 if 'DIAS' in df.columns:
#                     df['DIAS'] = df['DIAS'].fillna(0)
#                     df['DIAS'] = df['DIAS'].apply(
#                         lambda x: " " if x == 0 else int(x)
#                     )
#                 else: 
#                     print("Coluna 'DIAS' não encontrada no DataFrame")   
#                 if "VALOR_TOTAL" in df.columns:
#                     df["VALOR_TOTAL"] = df["VALOR_TOTAL"].apply(formatar_moeda)
#                 else:
#                     print("Coluna 'VALOR_TOTAL' não encontrada no DataFrame.")
                
#                 if "VALOR" in df.columns:
#                     total_valor_valor = df["VALOR"].sum()
#                     total_valor_valor = formatar_moeda(total_valor_valor)
#                     df["VALOR"] = df["VALOR"].apply(formatar_moeda)
#                 else:
#                     print("Coluna 'VALOR' não encontrada no DataFrame.")
#                 # df = df.sort_values(by='RAZAO_SOCIAL', ascending=True)
#                 nome_arquivo_html = gerar_html_com_dados(df, total_valor_valor)
#                 gerar_pdf(nome_arquivo_html)

#     except cx_Oracle.DatabaseError as e:
#         print("Erro ao conectar ao banco de dados ou executar a consulta:", e)
#     finally:
#         print("Consulta finalizada.")

# def gerar_html_com_dados(df, valor):

#     nome_arquivo_html = "relatorio_notas_fiscais.html"

#     with open(nome_arquivo_html, 'w', encoding='utf-8') as f:

#         fuso_horario = pytz.timezone('America/Sao_Paulo')
#         data_geracao = datetime.now(fuso_horario).strftime('%d/%m/%Y %H:%M:%S')

#         f.write(f"""
#         <!DOCTYPE html>
#         <html lang="pt-br">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Relatorio de Notas Fiscais</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     font-size: 10px;  
#                     background-color: #fff;  
#                     color: #333;
#                 }}
#                 table {{
#                     width: 100%;
#                     border-collapse: collapse;
#                     margin-top: 20px;
#                     background-color: #ffffff;
#                 }}
#                 th, td {{
#                     padding: 5px 8px; 
#                     text-align: left;
#                     border: 1px solid #dcdcdc;
#                 }}
#                 th {{
#                     background-color: #fc0000;
#                     color: #f2f2ff;
#                     word-wrap: break-word;
#                     white-space: normal;
#                     text-align: center;
#                     font-weight: bold;
#                     text-transform: uppercase;
#                 }}
#                 tr:nth-child(even) {{
#                     background-color: #fff;  
#                     font-weight: bold;
#                 }}
#                 tr:nth-child(odd) {{
#                     background-color: #fff;
#                     font-weight: bold;
                
#                 }}
#                 .signature {{
#                     margin-top: 75px;
#                     text-align: center;
#                 }}
#                 .line {{
#                     width: 300px;
#                     border-top: 1px solid #000;
#                     margin: 0 auto;
#                 }}
#                 .header {{
#                     background-color: #FC0000;
#                     color: white;
#                     text-align: center;
#                     padding: 12px;
#                 }}
#                 .header p {{
#                     font-size: 16px;
#                 }}
#                 .logo {{
#                     width: 150px;  /* Aumentar o tamanho da imagem */
#                     height: auto;
#                     margin-bottom: -20px;  /* Espaçamento entre a imagem e o título */
#                 }}
#                 .total-table {{
#                     width: 100%;
#                     margin-top: 5px;
#                     border-collapse: collapse;
#                     background-color: #f2f2f2;
                
#                 }}
#                 .total-table td {{
#                     text-align: right;
#                     padding: 8px;
#                     background-color: #f2f2f2;
#                     border-top: 1px solid #ddd;
#                     color:#000;
#                 }}
#                 .total-table #totalidade {{
#                     background-color: #555;  
#                     color: #f2f2ff;
#                     font-weight: bold;
#                     text-align: center;
                
#                 }}
#                 .total-table #total {{
#                     background-color: #555;  
#                     color: #f2f2ff;
#                     font-weight: bold;
#                     text-align: center;
#                 }}
#                 .total-table #valor {{
#                     background-color: #555;
#                     color: #f2f2ff;
#                     font-weight: bold;
#                     text-align: center; 
#                 }}
#                 .total-table th {{
#                     text-align: left;
#                     padding: 8px;
#                     border-top: 1px solid #ddd;
#                     background-color: #f2f2f2;
#                 }}
#                 .generated-by {{
#                     margin-top: 30px;
#                     text-align: center;
#                     color: #222;
#                     font-size: 16px;
#                     font-weight: bold;
#                  }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <img src="assets/logo_potiguar.png" class="logo" alt="Logo Potiguar">
#                 <h1>Relatorio de Notas Fiscais</h1>
#                 <p>Data da Geracao: {data_geracao}</p>
#             </div>
#             <table>
#                 <tr>""")
        
#         for column in df.columns:
  
#             titulo_coluna = column.replace('_', ' ').title()  
#             f.write(f"<th>{titulo_coluna.replace(' ', '<br>')}</th>")
        
#         f.write("</tr>")

#         for _, row in df.iterrows():
#             f.write("<tr>")
#             for value in row:
#                 f.write(f"<td>{value}</td>")
#             f.write("</tr>")
#         f.write(f"""
#             <table class="total-table">
#                 <!-- Primeira linha -->
#                 <tr>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td id="valor">Valor</td>  <!-- Texto "Valor" na posição 1x9 -->
#                 </tr>
#                 <!-- Segunda linha -->
#                 <tr>
#                     <td id="totalidade">Totalidade</td>  <!-- Texto "Totalidade" na posição 2x1 -->
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td></td>
#                     <td>{valor}</td>  <!-- Variável na posição 2x9 -->
#                 </tr>
#             </table>
#             """)
#         f.write("""
#             </table>
           
#             <div class="signature">
#                 <div class="line"></div>
#                 <p>Assinatura do Responsável</p>
#             </div>
#             <div class="generated-by">
#                 <p>Documento gerado automaticamente pelo sistema</p>
#             </div>
#         </body>
#         </html>
#         """)

#     return nome_arquivo_html

# def gerar_pdf(nome_arquivo_html):
#     nome_arquivo_pdf = nome_arquivo_html.replace(".html", ".pdf")

#     weasyprint.HTML(nome_arquivo_html).write_pdf(nome_arquivo_pdf, stylesheets=[weasyprint.CSS(string="""
#         @page {
#             size: landscape;
#             margin: 10mm;
#             @bottom-right {
#                 content: "Página " counter(page) " | " counter(pages);
#                 font-size: 8pt;
#                 color: #555;
#             }
#         }
#         body {
#             font-family: 'DejaVu Sans', sans-serif;
#         }
#     """)])
    
#     print(f"PDF gerado com sucesso em {nome_arquivo_pdf}")

# if __name__ == "__main__":
#     executar_consulta()
