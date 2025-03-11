from cryptography.fernet import Fernet

def criptografar(mensagem: str, chave: bytes) -> bytes:
    """Criptografa a mensagem usando a chave fornecida."""
    f = Fernet(chave)
    mensagem_bytes = mensagem.encode('utf-8')
    return f.encrypt(mensagem_bytes)

def descriptografar(mensagem_criptografada: bytes, chave: bytes) -> str:
    """Descriptografa a mensagem usando a chave fornecida."""
    f = Fernet(chave)
    mensagem_bytes = f.decrypt(mensagem_criptografada)
    return mensagem_bytes.decode('utf-8')

def bytes_para_gb(bytes_value):
    gb = bytes_value / (1024 ** 3)
    return round(gb, 2)