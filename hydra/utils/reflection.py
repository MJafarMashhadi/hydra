import inspect

def _get_all_subclasses_generator(base, include_self):
    q = [base]
    while q:
        cls = q.pop()
        q.extend(cls.__subclasses__())
        if include_self or cls is not base:
            yield cls

def get_all_subclasses(base, include_self=False):

    return list(_get_all_subclasses_generator(base, include_self))
