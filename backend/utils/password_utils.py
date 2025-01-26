from flask_bcrypt import Bcrypt

def complexity_check(password, min_length):
    special_characters = set("!@#$%^&*()-_+=[]{}|;:,.<>?/")

    message = []
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    if len(password) < min_length:
        message.append(f"Password must be at least {min_length} characters long.")
    
    # Iterate through the password and check each character
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    # Collect messages based on unmet password requirements
    if not has_upper:
        message.append("Password must include at least one uppercase letter.")
    if not has_lower:
        message.append("Password must include at least one lowercase letter.")
    if not has_digit:
        message.append("Password must include at least one digit.")
    if not has_special:
        message.append("Password must include at least one special character.")
    
    # If there are any errors, return False and the message
    if message:
        return False, message

    return True, ""

def hash_salt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')