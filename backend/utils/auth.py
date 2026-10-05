import hashlib

def login_key(login: str) -> str:
    norm = login.strip().lower()
    digest = hashlib.sha256(norm.encode()).hexdigest()
    return f"rl:login:user:{digest}"