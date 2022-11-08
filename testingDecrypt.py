import sys
import os
import time
import timeit
import sys
import math
from datetime import datetime
import cProfile
import matplotlib.pyplot as plt
import numpy as np

sys.setrecursionlimit(1000000)


# Assume p and q are randomly generated prime numbers
p = 1103
q = 1543

print("[*] p = %d" % (p))
print("[*] q = %d" % (q))

# Compute N = p * q
n = p*q
print("[*] n = p * q = %d" % (n))

# Compute the Euler totient function
# \phi(n) = (p-1)*(q-1):
phi = (p-1)*(q-1)
print("[*] phi = %d" % (phi))

# Choose public exponent e that is relatively prime to \phi(n) = (p-1)*(q-1).
# Choosing 17 works because it is itself a prime. So the numbers will be coprime.
e = 17
print("[*] e = %d" % (e))

# Compute d to be the inverse of e modulo n.
# Do this with the extended Euclidean algorithm
def egcd(a, b):
	"""
	Compute the Extended Euclidean Algorithm (EEA) and return (g, x, y) a*x + b*y = gcd(x, y)
	"""
	if a == 0:
		return (b, 0, 1)
	else:
		g, x, y = egcd(b % a, a)
		return (g, y - (b // a) * x, x)


def mulinv(b, n):
	"""
	Return the multiplicative inverse of b modulo n
	"""
	g, x, _ = egcd(b, n)
	if g == 1:
		return x % n

d = mulinv(e, phi)
print("[*] d = %d" % (d))

# m = int(input("Input message: "))
#print("[*] m = %d" % (m))

# (d, n) is the private key

pub_k = (e, n)
priv_k = (d, n)

m = int(input("insert message: "))

# NORMAL DECRYPTION
# Encrypt
c = (m ** e) % n

# Decrypt
start = time.time()
m_txtbook = (c**d) % n
end = time.time()
print("decrypted message: ", m_txtbook, "\n decrypt execution time with textbook RSA: ", end-start)


# GAUSS DECRYPTION
start = time.time()

dP = d % (p-1)
dQ = d % (q-1)
a1 = ((c%p)**dP) % p
a2 = ((c%q)**dQ) % q

N1 = n/p # isnt this just q
d1 = mulinv(N1,p) # p is the modulus
N2 = n/q # isnt this just p
# yes - because usually gauss method is for CRT where there are more than 2 congruences in the system
# e.g modulus divided by 1 factor is the product of several others
d2 = mulinv(N2,q) # q is the modulus
print("d1 is: ", d1)
print("d2 is: ", d2)
m_gauss = ((a1*N1*d1) + (a2*N2*d2)) % n
end = time.time()

print("decrypted message with gauss:", m_gauss, "; time: ", end-start)


# GARNER'S FORMULA DECRYPTION
start = time.time()

dP = d % (p-1)
dQ = d % (q-1)
a1 = ((c%p)**dP) % p
a2 = ((c%q)**dQ) % q
qInv = mulinv(q, p)
print("[*] qInv = %d" % (qInv))
print("value is: ", a1-a2)
m_garner = ( ( ( (a1-a2)*qInv ) % p) * q ) + a2

end = time.time()

print("decrypted message with garner: ", m_garner, "; time: ", end-start)