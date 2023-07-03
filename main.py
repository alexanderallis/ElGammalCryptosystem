# Alexander Allis
# Breaking the ElGammal Cryptosystem
import math


# 3. Compute the decryption exponent, 'a,' as the inverse of b modulo φ(N), from Cryptography Theory and Practice, 4ed
# Returns the inverse of b modulo "modulus"
def compute_inverse(modulus, num):
    a_0 = modulus
    b_0 = num
    t_0 = 0
    t = 1
    q = math.floor(a_0 / b_0)
    r = a_0 - (q * b_0)
    while r > 0:
        temp = (t_0 - (q * t)) % modulus
        t_0 = t
        t = temp
        a_0 = b_0
        b_0 = r
        q = math.floor(a_0 / b_0)
        r = a_0 - (q * b_0)
    if b_0 != 1:
        return -1
    if t < 0:
        print("nooo")
    return t


# 3. Returns x^c modulo n, from Cryptography Theory and Practice, 4ed
def square_and_multiply(x, c, n):
    binary_exponent = []
    while c > 0:
        binary_exponent.append(c % 2)
        c = c // 2
    binary_exponent.reverse()

    z = 1
    for i in range(len(binary_exponent)):
        z = (z * z) % n
        if binary_exponent[i] == 1:
            z = (z * x) % n
    return z


def decode(decryption_integers):
    letters_by_index = []
    for number in decryption_integers:
        plaintext1 = number % 26
        number = number - plaintext1

        plaintext2_ = number % math.pow(26, 2)
        plaintext2 = plaintext2_ // math.pow(26, 1)
        number = number - plaintext2_

        plaintext3_ = number // math.pow(26, 3)
        plaintext3 = number // math.pow(26, 2)
        number = number - plaintext3_

        # plaintext6_ = number // math.pow(26, 6)
        # plaintext6 = number // math.pow(26, 5)
        # number = number - plaintext6_

        # letters_by_index.append(plaintext6)
        # letters_by_index.append(plaintext5)
        # letters_by_index.append(plaintext4)
        letters_by_index.append(plaintext3)
        letters_by_index.append(plaintext2)
        letters_by_index.append(plaintext1)

    return letters_by_index


def index_to_character(i):
    return chr(int(i) + 65)


def multiply_mod_n(a, b, modulus):
    return (a * b) % modulus


def decrypt(y_1, y_2, a, modulus):
    y_1 = square_and_multiply(y_1, a, modulus)
    y_1_inverse = compute_inverse(modulus, y_1)
    x = multiply_mod_n(y_2, y_1_inverse, modulus)
    return x


def decode_message():

    f = open('alex-cipher', "r")
    cipherTextInt = []
    for line in f:
        cipherTextInt.append(line.strip('\n'))
    cipherTextInt = list(map(int, line.split()))

    p = 28607
    alpha = 10
    a = 11111
    beta = square_and_multiply(alpha, a, p)

    decryptedIntegers = []
    plaintext = []

    # Loop through ciphertext
    for i in range(0, len(cipherTextInt), 2):
        # Parse out y_1 and y_2
        y_1 = cipherTextInt[i]
        y_2 = cipherTextInt[i + 1]
        # decrypt(y_1, y_2)
        decryption = decrypt(y_1, y_2, a, p)
        decryptedIntegers.append(decryption)

    # decode
    characterIndices = decode(decryptedIntegers)
    # convert index to character & add character to plaintext
    for index in characterIndices:
        plaintext.append(index_to_character(index))

    # print plaintext
    for c in plaintext:
        print(c, end="")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    decode_message()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
