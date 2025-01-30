from config import app

def add_to_index(index, model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    app.es.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
    if not app.es:
        return
    app.es.delete(index=index, id=model.id)

def query_index(index, query, page, per_page, field=None):
    if not app.es:
        return [], 0
    
    if field:
        search = app.es.search(
            index = index,
            query = {'match': {field: query}},
            from_ = (page - 1) * per_page,
            size = per_page
        )
    else: 
        search = app.es.search(
            index = index,
            query = {'multi_match': {'query': query, 'fields': ['*']}},
            from_ = (page - 1) * per_page,
            size = per_page
        )

    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']