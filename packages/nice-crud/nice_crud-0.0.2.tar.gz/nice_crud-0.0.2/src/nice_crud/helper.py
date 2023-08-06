from .exceptions import WrongTypeException


def type_helper(query: str) -> str:
    query = query.lower()

    if 'insert' in query:
        return 'WRITE'
    elif 'create' in query:
        return 'WRITE'
    elif 'select' in query:
        return 'READ'
    elif 'update' in query:
        return 'WRITE'
    elif 'delete' in query:
        return 'WRITE'
    elif 'drop' in query:
        return 'WRITE'
    else:
        raise WrongTypeException('type_helper', sql=query)
