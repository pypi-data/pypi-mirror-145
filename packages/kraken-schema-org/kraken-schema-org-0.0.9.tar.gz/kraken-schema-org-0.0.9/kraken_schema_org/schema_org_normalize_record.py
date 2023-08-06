import os
import copy
import datetime
import uuid

from kraken_schema_org import kraken_schema_org as norm
import kraken_datatype as dt 



def get(original_record, strict = False):
    """
    Normalize keys and vlues of a record
    """
    
    # Deal with list
    if isinstance(original_record, list):
        records = []
        for i in original_record:
            records.append(get(i))
        return records

    # Deal with non-dict
    if not isinstance(original_record, dict):
        if strict:
            return None
        else:
            return original_record

        
    # Make copy of original
    record = copy.deepcopy(original_record)
    output_record = {}

    # Normalize record type
    record_type = norm.normalize_type(record.get('@type', None))
    output_record['@type'] = record_type

    # Normalize record_id
    record_id = record.get('@id', None)
    output_record['@id'] = record_id
    
    # Normalize values
    for k in record:
        if k in ['@type', '@id']:
            continue

        # Normalize key
        key = norm.normalize_key(k)

        if not key:
            if strict:
                continue
            else:
                key = k

        
        # Get datatypes
        datatypes = norm.get_datatype(record_type, key)

        # Intialize output_record value
        output_record[key] = []

        # Cycle through possible datatypes
        for i in datatypes or []:
            result = normalize_value(i, key, record[k], strict)
            if result and result not in output_record[key]:
                output_record[key].append(result)


        # Assign original value if not strict and empty
        if len(output_record[key]) == 0 and not strict:
            output_record[key] = record[k]
                
        # Convert back from list if one or None
        if len(output_record[key]) == 1:
            output_record[key] = output_record[key][0]

            
    # Normalize id
    output_record['@id'] = norm.get_record_id(output_record)

    
    return output_record



def normalize_value(datatype, key, value, strict = False):
    
    if isinstance(value, list):
        values = []
        for i in value:
            values.append(normalize_value(i))
        return values

    # Normalize value if also a record
    if isinstance(value, dict):
        # Normalize record if schema
        if '@type' in value.keys():
            value = value = get(value)

        # Return normalized record if same datatype
        if value.get('@type', None) == datatype:
            return value
        else:
            return None

    
    if not isinstance(value, (int, str, float)):
        return value

    # Try to normalize, if not working keep value
    try:
        result = dt.normalize(datatype, value)
    except:
        if strict:
            result = None
        else:
            return value

    
    return result

