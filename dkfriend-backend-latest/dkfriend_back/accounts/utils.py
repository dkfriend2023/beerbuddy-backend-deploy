import hashlib
import hmac
import base64

def make_signature(timestamp):
    access_key = 'tXFTpMViHVCr8WWM4tVL' #(예시 = 'nCH86JcJ6FCl40eYc4qp')
    secret_key = 'ph3Ips89Skgp2Bk0sOHaa98YO6oKzezFqv9sFZ9D' #(예시 = 'jkaPmt102mwMy9YvI7i6IGWTt4QiAn731SF1cNUA')
    secret_key = bytes(secret_key, 'UTF-8')

    uri = "/sms/v2/services/ncp:sms:kr:313351985365:beerbuddy/messages"
    # uri 중간에 Console - Project - 해당 Project 서비스 ID 입력 (예시 = ncp:sms:kr:263092132141:sms)

    
    message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey