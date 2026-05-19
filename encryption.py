import random
import sys
import time
import math
import os
sys.setrecursionlimit(30000)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def ME(base, exp, mod): #Modular Exponentiation
    return pow(base,exp,mod)
    if exp == 0:
        return 1
    if exp % 2 == 0:
        return ME((base*base) % mod, exp>>1, mod)
    else:
        return (base * ME(base, exp - 1, mod)) % mod

def millerTest(n, base):
    exp = n - 1
    
    seq = []
    while exp % 2 == 0:
        seq.append(ME(base, exp, n))
        exp >>= 1
    seq.append(ME(base, exp, n))

    c1 = True if seq[0] == 1 else False
    c2 = True
    for i in range(len(seq) - 1):
        if seq[i] == 1 and not(seq[i+1] == 1 or seq[i+1] == n - 1):
            c2 = False
            break
    
    return c1 and c2

def isDivisibleBySmallPrime(n):
    return any(n % p == 0 for p in smallPrimes)

def nBitRandom(n):
    return random.randrange(2**(n-1) + 1, 2**n - 1)

def nDigitRandom(n):
    return random.randrange(10**(n-1) + 1, 10**n - 1)

def primeTest(n):

    if n == 1 or n == 0:
        return False

    if isDivisibleBySmallPrime(n) and n > smallPrimes[-1]:
        return False

    bases = []
    i = 10 # i = 64 means probability of a false positive is <= 1/2^128
    for k in range(i):
        r = random.randint(1,n - 1 if n < 1001 else 1000)
        if r not in bases:
            bases.append(r)

    for b in bases:
        if not(millerTest(n, b)):
            return False
    
    return True

smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 
               191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 
               401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 
               631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 
               877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]


def genPrime(n):
    counter = 1
    expected = int(2.3 * n)
    timer = time.time()
    while True:
        counter += 1
        r = nBitRandom(n)
        if primeTest(r):
            return r

def euclid(phi,e):
    r1 = phi
    r2 = e
    t1 = 0
    t2 = 1
    while r2 != 0:
        q = math.floor(r1 / r2)

        r2 = r1 - q*(r1 := r2)

        t2 = t1 - q*(t1 := t2)
    
    if t1 < 0:
        t1 += phi
   
    return t1

def RSA():
    p = genPrime(1024)
    q = genPrime(1024)
    
    n = p * q
    phi = math.lcm(p - 1, q - 1)

    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    #e = 65537

    d = euclid(phi, e)

    with open(__location__ + "/rsakeys.txt", "w") as f:
        f.write(str(n) + "\n" + str(e) + "\n" + str(d))

    return [n,e,d]

def encrypt(m, n, e):
    return ME(m, e, n)

def decrypt(c, n, d):
    return ME(c, d, n)


def helperFunction1():
    args = sys.argv
    m = args[1]
    n = int(args[2])
    e = int(args[3])
    m = convertMessageToNumber(m)
    for M in m:
        print(encrypt(M, n, e))
        print("\n")

def helperFunction2():
    args = sys.argv
    d = int(args[4])
    n = int(args[2])
    c = args[1]
    c = c.split("\n")
    a = []
    for k in c:
        if k.isdigit():
            a.append(decrypt(int(k) + 0, n, d))
    
    result = convertNumbersToMessage(a)
    print(result)

def convertMessageToNumber(m):
    chars = [ord(c) for c in m]
    charsSplit = []

    while len(chars) > 0:
        if len(chars) >= 8:
            chunk = []
            for k in range(8):
                chunk.append(chars.pop(0))
            charsSplit.append(chunk)
        else:
            chunk = []
            for k in range(8):
                if len(chars) > 0:
                    chunk.append(chars.pop(0))
                else:
                    chunk.append(32)
            charsSplit.append(chunk)

    result = []
    for n in charsSplit:
        s = ""
        for k in n:
            k = str(k)
            while len(k) < 3:
                k = "0" + k
            s += k
        result.append(int(s))
    
    return result

def convertNumbersToMessage(l):
    result = ""
    for k in l:
        k = str(k)
        if len(k) < 24:
            k = "0" + k
        chars = []
        
        while len(k) > 0:
            chars.append(int(k[:3]))
            k = k[3:]
        
        for c in chars:
            result += chr(c)
    
    return result