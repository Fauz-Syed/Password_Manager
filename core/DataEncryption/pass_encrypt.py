from argon2 import PasswordHasher

ph = PasswordHasher()

def hasher(password: str) -> str:
	return ph.hash(password)


def verify_pass(hash_pass: str, password: str):
	return ph.verify(hash_pass, password)
