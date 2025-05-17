import random
from Crypto.Util.number import getPrime, inverse

class RSA:
    def __init__(self, bit_length):
        self.p = getPrime(bit_length // 2)
        self.q = getPrime(bit_length // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 65537
        self.d = inverse(self.e, self.phi)

    def encrypt(self, m):
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)