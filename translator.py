import random
import math

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        
        if is_prime(num):
            print("Prime number found!" + str(num))
            return num

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    return ((n, e), (n, d))

if __name__ == "__main__":
    bit_size = int(input("Enter the desired bit size (e.g., 512, 1024, 2048): "))
    public_key, private_key = generate_keypair(bit_size)

    with open("public_key.txt", "w") as public_file:
        public_file.write(f"Public Key (n, e):\n{n}\n{e}")

    with open("private_key.txt", "w") as private_file:
        private_file.write(f"Private Key (n, d):\n{n}\n{d}")

    print(f"RSA key pair with {bit_size}-bit size generated.")
    print("Public key saved as public_key.txt")
    print("Private key saved as private_key.txt")
