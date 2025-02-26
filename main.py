from services.consulta_service import executar_consulta
from send_mail import send_email_with_attachment

if __name__ == "__main__":
    
    executar_consulta()
    send_email_with_attachment(
        subject="Relatório PDF",
        body="Segue em anexo o relatório solicitado.",
        to_emails=["marcos.fernando@apotiguar.com.br", "lima@apotiguar.com.br", "luiz.costa@apotiguar.com.br"], 
        pdf_path = "relatorio_notas_fiscais.pdf" 
    )
