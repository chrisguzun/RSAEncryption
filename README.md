# RSAEncryption

A from-scratch implementation of RSA public-key encryption in Python — no cryptography libraries used. Generates 1024-bit RSA key pairs using a custom Miller-Rabin primality tester, then encrypts and decrypts messages via modular exponentiation.

## Features

- Custom Miller-Rabin probabilistic primality test
- 1024-bit prime generation
- Key generation with extended Euclidean algorithm for private key `d`
- Message-to-integer chunking and back
- Keys saved to `rsakeys.txt`

> **Note:** This is an educational implementation. Do not use it for real security-sensitive applications.

## Requirements

- Python 3.8+ (standard library only — no pip installs needed)

## Usage

### Generate a key pair

```bash
python encryption.py
```

This generates a fresh RSA key pair and saves `n`, `e`, and `d` to `rsakeys.txt`.

### Encrypt a message

```bash
python encryption.py "your message" <n> <e>
```

### Decrypt a message

```bash
python encryption.py "<ciphertext>" <n> <e> <d>
```

Where `n`, `e`, and `d` come from `rsakeys.txt`.

## How It Works

1. Two large random 1024-bit primes `p` and `q` are generated.
2. `n = p * q` (the modulus), `phi = lcm(p-1, q-1)`
3. A random public exponent `e` coprime to `phi` is chosen.
4. The private key `d` is the modular inverse of `e mod phi`, found via the extended Euclidean algorithm.
5. Encrypt: `c = m^e mod n` — Decrypt: `m = c^d mod n`
