"""
Get record_id for a given record


Rules:
- use url if possible as id



"""


import uuid



def get(record):


    by_url = ['website', 'webpage', 'datafeed', 'webapi']
    by_content_url = ['imageobject', 'videoobject']
    by_email = ['contactpoint']
    by_phone = ['contactpoint']

    
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    url = record.get('schema:url', None)
    content_url = record.get('schema:contentUrl', None)
    email = record.get('schema:email', None)
    phone = record.get('schema:telephone', None)


    

    simple_type = record_type.replace('schema:', '').lower()


    if simple_type in by_url and url:
        return get_id_by_url(record)
    
    elif simple_type in by_content_url and content_url:
        return get_id_by_content_url(record)

    elif simple_type in by_email:
        return get_id_by_email(record)
    
    elif simple_type in by_phone and phone:
        return get_id_by_phone(record)
    
    else:
        try:
            valid = uuid.UUID(record_id)
        except:
            valid = False
            
        if record_id and valid:
            return record_id
        else:
            return str(uuid.uuid4())
    



def get_id_by_url(record):
    """
    Returns uuid of url
    """
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    url = record.get('schema:url', None)
    
    hash_url = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
    return hash_url


def get_id_by_content_url(record):
    """
    returns uuid of content url
    """
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    content_url = record.get('schema:contentUrl', None)
    
    hash_url = str(uuid.uuid3(uuid.NAMESPACE_URL, content_url))
    return hash_url


def get_id_by_email(record):
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    email = record.get('schema:email', None)

    return email


def get_id_by_phone(record):
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    phone = record.get('schema:telephone', None)


    return phone