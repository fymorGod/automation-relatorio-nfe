# 📌 Automação Python - Relatório de Notas Fiscais com Envio de Documentos para WhatsApp

## 📖 Sobre o Projeto
Este projeto tem como objetivo a **automação do processo de geração de relatórios de notas fiscais**, utilizando **Python** para gerar os documentos em **PDF** e enviá-los automaticamente para **assinatura via WhatsApp** através da **ClickSign**. Após a assinatura, o documento é recuperado e enviado por **e-mail** para outro usuário.

A automação reduz o tempo e esforço manual necessário para processar, assinar e distribuir notas fiscais, garantindo maior eficiência e segurança no fluxo de trabalho.

---
## 📌 Índice
- [🎯 Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias Utilizadas](#%EF%B8%8F-tecnologias-utilizadas)
- [📌 Como Funciona?](#-como-funciona)
- [🚀 Como Executar](#-como-executar)
- [📩 Contato](#-contato)

---
## 🎯 Funcionalidades
✅ Geração automática de PDFs com base em consultas SQL.
✅ Envio do documento para assinatura via **ClickSign**.
✅ Notificação ao signatário para assinatura via **WhatsApp**.
✅ Recuperação do documento assinado.
✅ Envio do documento assinado via **e-mail**.
✅ Processo 100% automatizado para reduzir esforço manual.

---
## 🛠️ Tecnologias Utilizadas
- **Python** 🐍
- **ClickSign API** 📜 (para assinaturas digitais)
- **WhatsApp API** 📲 (para notificações)
- **SMTP (Email)** 📧 (para envio do documento assinado)
- **SQL** 🗄️ (para consulta de dados)

---
## 📌 Como Funciona?
A automação segue o seguinte fluxo:

1️⃣ **Gerar o PDF** a partir de uma consulta SQL.
2️⃣ **Enviar o documento para ClickSign** para assinatura.
3️⃣ **Vincular o documento** ao signatário já cadastrado.
4️⃣ **Notificar o signatário no WhatsApp** para assinar o documento.
5️⃣ **Recuperar o documento assinado** via API da ClickSign.
6️⃣ **Enviar o documento assinado por e-mail** para outro usuário.

Todo esse processo ocorre de forma automática, garantindo agilidade e confiabilidade na assinatura e envio das notas fiscais.

---
## 🚀 Como Executar
### 📌 Pré-requisitos
Antes de começar, você precisa ter instalado em sua máquina:
- **Python 3.x**
- Bibliotecas necessárias (instaláveis com `pip install -r requirements.txt`)
- Configuração de credenciais para ClickSign e WhatsApp API
- Servidor de e-mail configurado para envio de documentos

### 🏁 Passo a Passo
1️⃣ Clone este repositório:
```bash
  git clone local_disponibilizado.
```

2️⃣ Acesse a pasta do projeto:
```bash
  cd projeto-automacao
```

3️⃣ Instale as dependências:
```bash
  pip install -r requirements.txt
```

4️⃣ Configure as variáveis de ambiente:
```bash
  export CLICKSIGN_API_KEY="sua-chave-aqui"
  export EMAIL_USER="seu-email"
  export EMAIL_PASS="sua-senha"
```

5️⃣ Execute o script:
```bash
  python main.py
```

Pronto! O sistema começará a processar e enviar os documentos automaticamente. 🚀

---
## 📩 Contato
📌 **Developed by:** Luiz Fylip Viana Moreira Costa  
🏢 **Enterprise:** Potiguar Home Center  
✉ **Email:** luizfylip@outlook.com  
🙏 **Thanks for reviews!**

