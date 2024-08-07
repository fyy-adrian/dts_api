import base64
from dateutil.parser import parse
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

def encrypt(data):
    key = "tken_743d_dts1af"
    iv_key = "dts_743d_tken1af"
    iv = iv_key.encode("utf-8")
    data = pad(data.encode(), AES.block_size)
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)
    # Encode ke base64
    base64_encrypted = base64.b64encode(encrypted).decode("utf-8")
    # Ubah ke Base64URL
    base64url_encrypted = base64_encrypted.replace('+', '-').replace('/', '_').replace('=', '')
    return base64url_encrypted


def decrypt(enc):
    key = 'tken_743d_dts1af'
    iv_key = 'dts_743d_tken1af'
    iv = iv_key.encode("utf-8")
    # Ubah dari Base64URL ke Base64
    base64_encrypted = enc.replace('-', '+').replace('_', '/') + '=='
    encrypted = base64.b64decode(base64_encrypted)
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
    
    try:
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode("utf-8")
    except Exception as e:
        # Tangani kesalahan yang mungkin terjadi
        print("Error during decryption:", e)
        return None