
from Crypto.Util.number import getPrime, inverse
from Crypto.Random import get_random_bytes
#More secure than native 'number' or 'random' Python libs.
 
class RSA:
    #Generate an N-bit (roughly) public and private key pair.
    def __init__(self, bit_length):
        p = getPrime(bit_length//2)
        q = getPrime(bit_length//2)
        n = p*q #Modulus. n = p*q, size N.
        phi = (p-1)*(q-1)
        e = getPrime(bit_length, randfunc=get_random_bytes) # Public exponent e, relatively prime to (p-1)*(q-1).
        d = inverse(e, phi)

        self.modulus = n
        self.public_key = e #Public key = (Public exponent = e, modulus = n = p*q).
        self.private_key = d #Private key = private exponent = d = inverse(e, phi).

    #encrypt(self, m) = m^e mod PQ = m.
    def encrypt(self, message):
        return pow(message, self.e, self.n)

    #decrypt(e) = e^d mod PQ = e^private key mod modulus.
    def decrypt(self, encrypted_message):
        return pow(encrypted_message, self.private_key, self.n)