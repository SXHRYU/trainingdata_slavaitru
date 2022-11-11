def read_token(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_xlsx(path: str) -> None:
    with open(path, 'rb') as f:
        return f.read()
