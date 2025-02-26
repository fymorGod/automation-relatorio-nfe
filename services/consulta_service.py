
import pandas as pd
from datetime import datetime, timedelta
from config.database import get_connection
from utils.formatters import formatar_moeda
from utils.pdf_generator import gerar_html_com_dados, gerar_pdf

mapeamento_colunas = {
    "unidade_entrada": "UNIDADE_ENTRADA",
    "DT_ENTRADA": "DT_ENTRADA",
    "T073_CODIGO_EMITENTE_IU": "COD_FORNECEDOR", 
    "NF": "NF",
    "razao_social": "RAZAO_SOCIAL",
    "T057_SEQUENCIAL_PARCELA": "PARCELA",
    "Valor_Total": "VALOR_TOTAL",
    "Vencimento": "VENCIMENTO",
    "Dias": "DIAS",
    "valor": "VALOR",
    "Num_Pedido": "NUM_PEDIDO",
    "comprador": "COMPRADOR"
}

total_valor_valor = 0
def executar_consulta():
    data_atual = datetime.now()
    data_anterior = data_atual - timedelta(days=1)
    data_inicio = data_anterior.strftime('%Y-%m-%d 00:00:00')
    data_fim = data_anterior.strftime('%Y-%m-%d 23:59:59')

    consulta_sql = f"""
    SELECT
        te.T073_UNIDADE_IE AS unidade_entrada,
        te.T073_DATA_MOVIMENTO_CONTABIL AS DT_ENTRADA,
        te.T073_NOTA_FISCAL_IU || '-' || te.T073_SERIE_IU AS NF,
        te.T073_CODIGO_EMITENTE_IU AS COD_FORNECEDOR,
        tf.T019_RAZAO_SOCIAL AS razao_social,
        te.T073_VALOR_CONTABIL AS Valor_Total,
        trunc(ttp.T057_DATA_LIMITE) AS Vencimento,
        trunc(ttp.T057_DATA_LIMITE) - trunc(ttp.T057_DATA_EMISSAO) AS Dias,
        ttp.T057_SEQUENCIAL_PARCELA AS Parcela,
        ttp.T057_VALOR_BRUTO AS valor,
        tpp.T108_NUMERO_PEDIDO_IU AS Num_Pedido,
        tpp.T108_COMPRADOR AS comprador
    FROM
        DBAMDATA.T073_ENTRADA te
    LEFT JOIN DBAMDATA.T019_FORNECEDOR tf 
        ON tf.T019_FORNECEDOR_IU = te.T073_CODIGO_EMITENTE_IU
    LEFT JOIN DBAMDATA.T108_PEDIDOS_PEND tpp 
        ON tpp.T108_NUMERO_PEDIDO_IU = te.T073_NUMERO_PEDIDO_E
        AND tpp.T108_UNIDADE_IE = te.T073_UNIDADE_IE
    LEFT JOIN DBAMDATA.T057_TITULO_PAGAR ttp 
        ON ttp.T057_UNIDADE_IE = te.T073_UNIDADE_IE
        AND ttp.T057_NOTA_FISCAL = te.T073_NOTA_FISCAL_IU
        AND ttp.T057_FORNECEDOR_E = te.T073_CODIGO_EMITENTE_IU
        AND ttp.T057_NUMERO_PEDIDO_E = tpp.T108_NUMERO_PEDIDO_IU
    WHERE
        TE.T073_NATUREZA_OPERACAO_E IN (110201, 110250, 140301, 140350, 210201, 210250, 
                                        240301, 240350, 265201, 265250, 211701, 211750, 
                                        211601, 211650)
        AND te.T073_DATA_MOVIMENTO_CONTABIL BETWEEN 
            TO_DATE('{data_inicio}', 'YYYY-MM-DD HH24:MI:SS') AND 
            TO_DATE('{data_fim}', 'YYYY-MM-DD HH24:MI:SS')
    ORDER BY
        tf.T019_RAZAO_SOCIAL,
        T073_NOTA_FISCAL_IU,
        ttp.T057_SEQUENCIAL_PARCELA
    """

    try:
        with get_connection() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(consulta_sql)
                resultados = cursor.fetchall()
                colunas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultados, columns=colunas)
                
                if df.empty:
                    print("Nenhum dado encontrado na consulta. O PDF não será gerado.")
                    return  # Encerra a execução caso não haja dados
                
                print("Colunas originais do DataFrame:", df.columns)

                df = df.rename(columns=mapeamento_colunas)
                df = df.fillna(0)

                if 'VENCIMENTO' in df.columns:
                    df['VENCIMENTO'] = df['VENCIMENTO'].fillna(0)
                    df['VENCIMENTO'] = df['VENCIMENTO'].apply(
                        lambda x: " " if x == 0 else pd.to_datetime(x).strftime('%d-%m-%Y')
                    )
                else:
                    print("Coluna 'VENCIMENTO' não encontrada no DataFrame.")

                if 'DT_ENTRADA' in df.columns:
                    df['DT_ENTRADA'] = pd.to_datetime(df['DT_ENTRADA']).dt.strftime('%d-%m-%Y')
                else:
                    print("Coluna 'DT_ENTRADA' não encontrada no DataFrame.")

                if 'PARCELA' in df.columns:
                    df['PARCELA'] = df['PARCELA'].fillna(0)

                    df['PARCELA'] = df['PARCELA'].apply(
                        lambda x: "" if x == 0 else int(x)
                    )
                else:
                    print("Coluna 'Parcela' não encontrada no DataFrame.")
                if 'DIAS' in df.columns:
                    df['DIAS'] = df['DIAS'].fillna(0)
                    df['DIAS'] = df['DIAS'].apply(
                        lambda x: " " if x == 0 else int(x)
                    )
                else: 
                    print("Coluna 'DIAS' não encontrada no DataFrame")   
                if "VALOR_TOTAL" in df.columns:
                    df["VALOR_TOTAL"] = df["VALOR_TOTAL"].apply(formatar_moeda)
                else:
                    print("Coluna 'VALOR_TOTAL' não encontrada no DataFrame.")
                
                if "VALOR" in df.columns:
                    total_valor_valor = df["VALOR"].sum()
                    total_valor_valor = formatar_moeda(total_valor_valor)
                    df["VALOR"] = df["VALOR"].apply(formatar_moeda)
                else:
                    print("Coluna 'VALOR' não encontrada no DataFrame.")
                # df = df.sort_values(by='RAZAO_SOCIAL', ascending=True)
                nome_arquivo_html = gerar_html_com_dados(df, total_valor_valor)
                gerar_pdf(nome_arquivo_html)

    except Exception as e:
        print("Erro ao conectar ao banco de dados ou executar a consulta:", e)
