import bcrypt

def complexity_check(password, min_length):
    """
    Check if the given password meets the complexity requirements:
    - Minimum length of characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    # Set of allowed special characters
    special_characters = set("!@#$%^&*()-_+=[]{}|;:,.<>?/")

    # Check the minimum length requirement
    if len(password) < min_length:
        return False

    # Flags for conditions
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

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

    # Ensure all conditions are met
    return has_upper and has_lower and has_digit and has_special

def hash_salt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')