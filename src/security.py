import bcrypt

def hash_password(password):
    """
    Cria um hash bcrypt de uma senha.
    
    Args:
        password: String contendo a senha em texto plano
        
    Returns:
        String contendo o hash bcrypt da senha
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')

def verify_password(stored_hash, password):
    """
    Verifica se uma senha corresponde a um hash armazenado.
    
    Args:
        stored_hash: Hash bcrypt armazenado
        password: Senha em texto plano para verificar
        
    Returns:
        True se a senha corresponder ao hash, False caso contrário
    """
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.checkpw(password, stored_hash)
