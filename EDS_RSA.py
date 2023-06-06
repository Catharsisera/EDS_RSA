import random
from sympy import *
from hashlib import sha256

def extendEvklid(a, b):
    if a == 0:
        return b, 0, 1
    mod, x1, y1 = extendEvklid(b % a, a)
    x = y1 - (b//a) * x1
    y = x1
    return mod, x, y

def invE(e, Fn):
    gcd, x, y = extendEvklid(e, Fn)
    if gcd == 1:
        return (x % Fn + Fn) % Fn
    else:
        return -1

def nod(a, b):
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b

def prime_pq():
    p = random.randint(10*99, 10**99*7)
    q = random.randint(10*99, 10**99*7)
    if p == q:
        q = random.randint(10*99, 10**99*7)
    while not isprime(p):
        p += 1
    while not isprime(q):
        q += 1
    return(p, q)

def gen_key():
    p, q = prime_pq()
    N = p * q
    Fn = (p - 1) * (q - 1)
    e = random.randint(2, Fn - 1)
    if e % 2 == 0:
        e += 1
    while not isprime(e):
        if nod(e, Fn) != 1:
            e += 2
        else:
            break

    res = invE(e, Fn)
    if res != -1:
        d = res

    file = open('Открытый ключ.txt', 'w', encoding='UTF-8')
    file.write(str(e) + '\n' + str(N))
    file.close()
    file = open('Закрытый ключ.txt', 'w', encoding='UTF-8')
    file.write(str(d) + '\n' + str(N))
    file.close()

def Hash():
    file = open('Л2-Митюшкина .docx', 'rb')
    f = file.read()
    file.close()
    hash_object = int(sha256(f).hexdigest(), 16)
    print('Хеш:', format(hash_object, 'x'))
    return hash_object

"""Подпись документа"""
def Sign():
    hash_object = Hash()
    file = open('Закрытый ключ.txt', 'r', encoding='UTF-8')
    d = int(file.readline())
    N = int(file.readline())
    file.close()

    c = format(pow(hash_object, d, N), 'x')
    print('Подпись:', c, '\n')
    # print(type(c))
    file = open('Подпись.txt', 'w')
    file.write(c)
    file.close()

"""Проверка документа"""
def Verification():
    hash_object = Hash()
    file = open('Открытый ключ.txt', 'r', encoding='UTF-8')
    e = int(file.readline())
    N = int(file.readline())
    file.close()

    file = open('Подпись.txt', 'r')
    signature = int(file.read(), 16)
    file.close()

    M = pow(signature, e, N)
    print('Хеш проверенного доумента:', format(M, 'x'))
    file = open('Хеш подписанного документа.txt', 'w')
    file.write(format(M, 'x'))
    file.close()

    if hash_object == M:
        print('Подпись действительна!')
    else:
        print('Подпись недействительна!')

actions = int(input('Генерация новых ключей:'))
if actions == 1:
    gen_key()
    Sign()
    Verification()
else:
    Verification()