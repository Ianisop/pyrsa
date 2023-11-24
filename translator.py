import random, sys, os, rabinMiller, cryptoMath

def main():
   makeKeyFiles('RSA_demo', 2048)

def generateKey(keySize):
   # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
   print('Generating p prime...')
   p = rabinMiller.generateLargePrime(keySize)
   print('Generating q prime...')
   q = rabinMiller.generateLargePrime(keySize)
   n = p * q
	
   # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
   print('Generating e that is relatively prime to (p-1)*(q-1)...')
   while True:
      e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
      if cryptoMath.gcd(e, (p - 1) * (q - 1)) == 1:
         break
   
   # Step 3: Calculate d, the mod inverse of e.
   print('Calculating d that is mod inverse of e...')
   d = cryptoMath.findModInverse(e, (p - 1) * (q - 1))
   publicKey = (n, e)
   privateKey = (n, d)
   print('Public key:', publicKey)
   print('Private key:', privateKey)
   return (publicKey, privateKey)

def makeKeyFiles(name, keySize):
   if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
     return "keys are already made"
   publicKey, privateKey = generateKey(keySize)
   print()
   print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1])))) 
   print('Writing public key to file %s_pubkey.txt...' % (name))
   
   fo = open('%s_pubkey.txt' % (name), 'w')
   fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
   fo.close()
   print()
   print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
   print('Writing private key to file %s_privkey.txt...' % (name))
   
   fo = open('%s_privkey.txt' % (name), 'w')
   fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
   fo.close()

def encrypt(message, key_file_path):
    try:
        # Read the public key from file
        with open(key_file_path, "r") as f:
            key_size, n, e = f.readline().strip().split(',')
        n = int(n)
        e = int(e)

        # Convert the message to an integer
        message_as_int = int.from_bytes(message.encode('utf-8'), 'big')

        # Encrypt the message
        encrypted_int = pow(message_as_int, e, n)

        # Convert the encrypted integer back to bytes
        # The size of the byte array needs to be calculated correctly
        encrypted_message = encrypted_int.to_bytes((encrypted_int.bit_length() + 7) // 8, 'big')
        
        return encrypted_message

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def decrypt(encrypted_message, key_file_path):
    try:
        # Read the private key from file
        with open(key_file_path, "r") as f:
            key_size, n, d = f.readline().strip().split(',')
        n = int(n)
        d = int(d)

        # Convert the encrypted message to an integer
        encrypted_int = int.from_bytes(encrypted_message, 'big')

        # Decrypt the message
        decrypted_int = pow(encrypted_int, d, n)

        # Convert the decrypted integer back to bytes
        decrypted_message_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')

        # Decode the bytes back to a string
        return decrypted_message_bytes.decode('utf-8')

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



if __name__ == '__main__':
   main()