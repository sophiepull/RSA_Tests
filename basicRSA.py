from datetime import datetime
import math

p = 11
q = 3
n = p*q
phi = (p-1)*(q-1)

d = 7
e = 3

print("public key: n=", n, " e=", e)
print("private key: n=", n, " d=", d)

def encrypt(msg):
    c = math.pow(msg, e) % n
    return c

def decrypt_CRT(c):
    dP = (d) % (p - 1)
    dQ = (d) % (q - 1)
    qInv = (1 / q) % p
    m1 = math.pow(c, dP) % p
    m2 = math.pow(c, dQ) % q
    h = qInv*(m1 - m2) % p
    m = m2 + h*q
    return m

def decrypt(c):
    m = math.pow(c, d) % n
    return m

m = int(input("input numerical message"))
cipher = encrypt(m)
print(cipher)

start = datetime.now()
message = decrypt(cipher)
end = datetime.now()
print("time taken with normal decryption:", start-end)
print(message)

start = datetime.now()
message = decrypt_CRT(cipher)
end = datetime.now()
print("time taken with crt decryption:", start-end)
print(message)
