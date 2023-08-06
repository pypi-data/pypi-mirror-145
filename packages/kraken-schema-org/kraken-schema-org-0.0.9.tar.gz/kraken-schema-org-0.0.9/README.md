Library to schema_org


How to use:

from kraken_schema_org import kraken_schema_org as k

normalize_type:
```
record_type = 'person'
normalized_type = k.normalize_type(record_type)
```

normalize_key:
```
key = 'givenname'
normalized_key = k.normalize_key(key)
```

get_keys:
```
record_type = 'person'
keys = k.get_keys(record_type)
```

get_datatype():
```
record_type = 'schema:Person'
key = 'schema:givenName'
datatypes = k.get_datatype(record_type, key)
```

