import math
import simpy

m = 10

p = [29, 23, 17, 19]
q = [3, 5, 11, 13]

e = 7

# d is the inverse of e modulo n.
def egcd(a, b):
	# Compute the Extended Euclidean Algorithm (EEA) and return (g, x, y) a*x + b*y = gcd(x, y)
	if a == 0:
		return (b, 0, 1)
	else:
		g, x, y = egcd(b % a, a)
		return (g, y - (b // a) * x, x)


def mulinv(b, n):
	#Return the multiplicative inverse of b modulo n
	g, x, _ = egcd(b, n)
	if g == 1:
		return x % n


def encrypt(msg, n):
	c = math.pow(msg, e) % n
	return c

n_list = []
c_list = []

for x in range(0, len(p)):
	n_list.append(int(p[x] * q[x]))
	phi = (p[x] - 1) * (q[x] - 1)
	d = mulinv(e, phi)
	print("public key: n=", n_list[x], " e=", e)
	print("private key: n=", n_list[x], " d=", d)
	c_list.append(int(encrypt(m, n_list[x])))

print("n: ", n_list)
print("c: ", c_list)

# ATTACK
N = 1
for x in range(0, len(p)):
	N = N * n_list[x]

N_list = []
d_list = []
cuberoot = 0
for x in range(0, len(n_list)):
	N_list.append(int(N / n_list[x]))

	# calculate mod inverse
	d_list.append(int(mulinv(N_list[x], n_list[x])))

	cuberoot =int((c_list[x]*N_list[x]*d_list[x]) + cuberoot)

print(cuberoot)
# FINAL STAGE OF ATTACK: finding cube root
x = int(cuberoot % N)
print(x)
decrypt = math.pow(x, 1/3)
print(decrypt)
