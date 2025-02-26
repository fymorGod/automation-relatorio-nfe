import hmac
import hashlib

# Chave secreta compartilhada (Shared Secret)
shared_secret = "6fbce93f44eb8fe759a6ded3d28bae2e"

# Mensagem a ser assinada
message = "6381e9f5-6d54-4d09-9f48-591e0a15d627"

# Criando o HMAC-SHA256
hmac_hash = hmac.new(
    key=bytes(shared_secret, 'UTF-8'),  # Convertendo a chave para bytes
    msg=message.encode(),               # Convertendo a mensagem para bytes
    digestmod=hashlib.sha256            # Algoritmo SHA-256
).hexdigest()

print(hmac_hash)  # Exibe a assinatura HMAC em hexadecimal
