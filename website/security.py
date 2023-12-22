from werkzeug.security import generate_password_hash, check_password_hash

def hash(password):
    hashed_password = generate_password_hash(password,
                                             method='pbkdf2:sha256',
                                             salt_length=8)
    return hashed_password

def check_hashed_password(db_password,form_password):
    checked_password = check_password_hash(db_password,form_password)
    return checked_password
