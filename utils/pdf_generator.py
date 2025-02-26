from datetime import datetime
import weasyprint
import pytz
from config.settings import FUSO_HORARIO


def gerar_html_com_dados(df, valor):

    nome_arquivo_html = "relatorio_notas_fiscais.html"

    with open(nome_arquivo_html, 'w', encoding='utf-8') as f:

        data_geracao = datetime.now(FUSO_HORARIO).strftime('%d/%m/%Y %H:%M:%S')

        f.write(f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatorio de Notas Fiscais</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 10px;  
                    background-color: #fff;  
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                    background-color: #ffffff;
                }}
                th, td {{
                    padding: 5px 8px; 
                    text-align: left;
                    border: 1px solid #dcdcdc;
                }}
                th {{
                    background-color: #fc0000;
                    color: #f2f2ff;
                    word-wrap: break-word;
                    white-space: normal;
                    text-align: center;
                    font-weight: bold;
                    text-transform: uppercase;
                }}
                tr:nth-child(even) {{
                    background-color: #fff;  
                    font-weight: bold;
                }}
                tr:nth-child(odd) {{
                    background-color: #fff;
                    font-weight: bold;
                
                }}
                .signature {{
                    margin-top: 75px;
                    text-align: center;
                }}
                .line {{
                    width: 300px;
                    border-top: 1px solid #000;
                    margin: 0 auto;
                }}
                .header {{
                    background-color: #FC0000;
                    color: white;
                    text-align: center;
                    padding: 12px;
                }}
                .header p {{
                    font-size: 16px;
                }}
                .logo {{
                    width: 150px;  /* Aumentar o tamanho da imagem */
                    height: auto;
                    margin-bottom: -20px;  /* Espaçamento entre a imagem e o título */
                }}
                .total-table {{
                    width: 100%;
                    margin-top: 5px;
                    border-collapse: collapse;
                    background-color: #f2f2f2;
                
                }}
                .total-table td {{
                    text-align: right;
                    padding: 8px;
                    background-color: #f2f2f2;
                    border-top: 1px solid #ddd;
                    color:#000;
                }}
                .total-table #totalidade {{
                    background-color: #555;  
                    color: #f2f2ff;
                    font-weight: bold;
                    text-align: center;
                
                }}
                .total-table #total {{
                    background-color: #555;  
                    color: #f2f2ff;
                    font-weight: bold;
                    text-align: center;
                }}
                .total-table #valor {{
                    background-color: #555;
                    color: #f2f2ff;
                    font-weight: bold;
                    text-align: center; 
                }}
                .total-table th {{
                    text-align: left;
                    padding: 8px;
                    border-top: 1px solid #ddd;
                    background-color: #f2f2f2;
                }}
                .generated-by {{
                    margin-top: 30px;
                    text-align: center;
                    color: #222;
                    font-size: 16px;
                    font-weight: bold;
                 }}
            </style>
        </head>
        <body>
            <div class="header">
                <img src="assets/logo_potiguar.png" class="logo" alt="Logo Potiguar">
                <h1>Relatorio de Notas Fiscais</h1>
                <p>Data da Geracao: {data_geracao}</p>
            </div>
            <table>
                <tr>""")
        
        for column in df.columns:
  
            titulo_coluna = column.replace('_', ' ').title()  
            f.write(f"<th>{titulo_coluna.replace(' ', '<br>')}</th>")
        
        f.write("</tr>")

        for _, row in df.iterrows():
            f.write("<tr>")
            for value in row:
                f.write(f"<td>{value}</td>")
            f.write("</tr>")
        f.write(f"""
            <table class="total-table">
                <!-- Primeira linha -->
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td id="valor">Valor</td>  <!-- Texto "Valor" na posição 1x9 -->
                </tr>
                <!-- Segunda linha -->
                <tr>
                    <td id="totalidade">Totalidade</td>  <!-- Texto "Totalidade" na posição 2x1 -->
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td>{valor}</td>  <!-- Variável na posição 2x9 -->
                </tr>
            </table>
            """)
        f.write("""
            </table>
           
            <div class="signature">
                <div class="line"></div>
                <p>Assinatura do Responsável</p>
            </div>
            <div class="generated-by">
                <p>Documento gerado automaticamente pelo sistema</p>
            </div>
        </body>
        </html>
        """)

    return nome_arquivo_html

def gerar_pdf(nome_arquivo_html):
    nome_arquivo_pdf = nome_arquivo_html.replace(".html", ".pdf")

    weasyprint.HTML(nome_arquivo_html).write_pdf(nome_arquivo_pdf, stylesheets=[weasyprint.CSS(string="""
        @page {
            size: landscape;
            margin: 10mm;
            @bottom-right {
                content: "Página " counter(page) " | " counter(pages);
                font-size: 8pt;
                color: #555;
            }
        }
        body {
            font-family: 'DejaVu Sans', sans-serif;
        }
    """)])

    print(f"PDF gerado com sucesso em {nome_arquivo_pdf}")
