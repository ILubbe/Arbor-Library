def is_role_valid(role, valid_roles):
    if role not in valid_roles:
        print(role)
        print(valid_roles)
        return False
    return True