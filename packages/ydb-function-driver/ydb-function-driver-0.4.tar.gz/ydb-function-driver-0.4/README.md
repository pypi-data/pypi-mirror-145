# Yandex Database Driver for cloud functions

Subj

```
from ydb_function_driver import execute_query

def get_user_ids():
    return [uid.id for uid in execute_query('select id from users')]
```

