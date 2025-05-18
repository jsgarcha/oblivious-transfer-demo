
from Crypto.Util import number
from Crypto.Util.number import getPrime, inverse
from Crypto.Random import get_random_bytes
import random

class RSA:
    #Generate an N-bit (roughly) public and private key pair.
    def __init__(self, bit_length):
        self.p = getPrime(bit_length//2)
        self.q = getPrime(bit_length//2)
        self.n = self.p*self.q #Modulus. n = p*q, size N.
        self.phi = (self.p-1)*(self.q-1)
        self.e = number.getPrime(bit_length, randfunc=get_random_bytes) # Public exponent e, relatively prime to (p-1)*(q-1).
        self.d = inverse(self.e, self.phi)

        self.modulus = self.n
        self.public_key = self.e #Public key = (Public exponent = e, modulus = n = p*q).
        self.private_key = self.d #Private key = private exponent = d = inverse(e, phi).

    #encrypt(self, m) = m^e mod PQ = m
    def encrypt(self, message):
        return pow(message, self.e, self.n)

    #decrypt(e) = e^d mod PQ = e^private key mod modulus.
    def decrypt(self, encrypted_message):
        return pow(encrypted_message, self.private_key, self.n)