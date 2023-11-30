import math
import random
import threading
import time
import cryptoMath  # Assumed to have findModInverse function
import translator  # Assumed to have encrypt function

def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

def pollards_rho(n, thread_id, result):
    """Pollard's Rho algorithm for integer factorization."""
    if n % 2 == 0:
        result.append(2)
        return
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    iteration = 0
    while d == 1:
        iteration += 1
        if iteration % 1000 == 0:
            print(f"Thread {thread_id} iteration: {iteration}")
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        d = gcd(abs(x - y), n)
        if d != 1 and d != n:
            print(f"Factor found by thread {thread_id}: {d}")
            result.append(d)
            return
    return None

def find_factor(n):
    """Find factors of n using multiple threads and keep trying until a factor is found."""
    start_time = time.time()
    thread_count = 4
    result = []

    while not result:
        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=pollards_rho, args=(n, i, result))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if result:
            break

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return result

def int_to_string(integer):
    """Converts an integer back to a string assuming UTF-8 encoding."""
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big').decode('utf-8')

def read_private_key(file_path):
    """Reads the private key from a file."""
    with open(file_path, "r") as f:
        _, n, d = [int(x) for x in f.read().split(',')]
    return n, d

def compare_keys(generated_n, generated_d, file_path):
    """Compares the generated private key with the actual private key."""
    try:
        actual_n, actual_d = read_private_key(file_path)
        return generated_n == actual_n and generated_d == actual_d
    except Exception as e:
        print(f"Error reading the actual private key file: {e}")
        return False
    
def make_key(n, p, q, e):
    """Generate RSA private key and decrypt a message."""
    phi_n = (p - 1) * (q - 1)
    d = cryptoMath.findModInverse(e, phi_n)
    is_same_key = compare_keys(n, d, "actual_private_key.txt")  # Replace with the actual file name
    print(f"The generated private key is {'the same as' if is_same_key else 'different from'} the actual private key.")
        
    # Encrypt a message
    encrypted_message = translator.encrypt("ianis is best", "_privkey.txt")  # Ensure this returns an integer
    
    # If encrypted_message is bytes, convert to int
    if isinstance(encrypted_message, bytes):
        encrypted_message = int.from_bytes(encrypted_message, 'big')

    decrypted_message = pow(encrypted_message, d, n)
    print("Decrypted message:", int_to_string(decrypted_message))
# Main execution
try:
    with open("_pubkey.txt", "r") as f:
        lines = f.read().split(",")
        n = int(lines[1])  # Assuming n is the second number in the file
        e = int(lines[2])  # Assuming e is the third number in the file

    key_matched = False
    while not key_matched:
        factors = find_factor(n)
        if factors:
            p = factors[0]
            q = n // p
            print(f"Prime factors found: p = {p}, q = {q}")

            make_key(n, p, q, e)
            _, d = read_private_key("actual_private_key.txt")  # Replace with the actual file name
            phi_n = (p - 1) * (q - 1)
            generated_d = cryptoMath.findModInverse(e, phi_n)

            if generated_d == d:
                print("Guessed private key matches the actual private key.")
                key_matched = True
            else:
                print("Guessed private key does not match. Retrying...")
        else:
            print("No factor found. Retrying...")

except FileNotFoundError:
    print("Error: Public key file not found.")
except IndexError:
    print("Error: Public key file format is incorrect.")
except Exception as e:
    print(f"An error occurred: {e}")

