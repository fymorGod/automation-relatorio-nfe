import requests
import base64
from datetime import datetime, timedelta
import json
import hmac
import hashlib

DOCUMENT_URL = "https://app.clicksign.com/api/v1/documents"
LIST_URL = "https://app.clicksign.com/api/v1/lists"
SEND_DOCS = "https://app.clicksign.com/api/v1/notify_by_whatsapp"
ACCESS_TOKEN = "b02810a6-97f7-4695-846e-2603f75f8888"
PDF_PATH = "./relatorio_notas_fiscais.pdf"
shared_secret = "6fbce93f44eb8fe759a6ded3d28bae2e"

def pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        encoded_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
    return f"data:application/pdf;base64,{encoded_pdf}"

def get_tomorrow_datetime():
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%dT%H:%M:%S-03:00")

def send_document_request():
    document_data = {
        "document": {
            "path": "/COMPRAS/Contrato_de_Prestacao_de_Servicos-123.pdf",
            "content_base64": pdf_to_base64(PDF_PATH),
            "deadline_at": get_tomorrow_datetime(),
            "auto_close": True,
            "locale": "pt-BR",
            "sequence_enabled": False,
            "block_after_refusal": True
        }
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{DOCUMENT_URL}?access_token={ACCESS_TOKEN}", json=document_data, headers=headers)
    response_data = response.json()

    if "document" in response_data and "key" in response_data["document"]:
        return response_data["document"]["key"]
    else:
        return None

def send_list_request(document_key, signer_key):
    if not document_key:
        return None

    list_data = {
        "list": {
            "document_key": document_key,
            "signer_key": signer_key,
            "sign_as": "sign",
            "refusable": True,
            "message": "Prezado Fylip,\nPor favor assine o documento.\n\nQualquer dúvida estou à disposição.\n\nAtenciosamente,\nGuilherme Alvez"
        }
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{LIST_URL}?access_token={ACCESS_TOKEN}", json=list_data, headers=headers)
    response_data = response.json()
    if "list" in response_data and "request_signature_key" in response_data["list"]:
        return response_data["list"]["request_signature_key"]
    else:
        return None

def post_request(signature_key):
    payload = {
        "request_signature_key": signature_key
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{SEND_DOCS}?access_token={ACCESS_TOKEN}", json=payload, headers=headers)
    
    print("Resposta Bruta:", response.text)
    
    if response.status_code == 202:
        print("Request bem-sucedido!")
    else:
        print(f"Erro {response.status_code}: {response.text}")

if __name__ == "__main__":
    document_key = send_document_request()
   
    if document_key:
        signer_key = "ddf0b037-1783-4978-806c-e076a21b660e"
        response_2 = send_list_request(document_key, signer_key)
        if response_2:
            post_request(response_2)
