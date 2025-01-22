import re
from flask import request
from models import db

def check_required_fields(required_fields):
    # Check if any required field is missing, convert from camelCase to spaces
    missing_fields = [
        re.sub('(?<!^)(?=[A-Z])', ' ', field).lower() 
        for field in required_fields 
        if not request.json.get(field)
    ]
    
    if missing_fields:
        return False, missing_fields
    
    return True, None

def field_length_ok(model, row_to_add):
    model_keys = model.__table__.columns.keys()
    for key in model_keys:
        key_type = model.__table__.columns[key].type
        if isinstance(key_type, db.String):
            key_len = key_type.length
            if len(getattr(row_to_add, key)) > key_len:
                return False, key
    return True, None