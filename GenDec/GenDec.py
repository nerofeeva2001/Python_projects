import functools
import warnings

def sliding_window(func, xs, n):
    for i in range(len(xs) - n + 1):
        window = xs[i:i+n]
        yield func(window)

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated", category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper

def deprecated_first_use(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:  # Проверяем, была ли функция вызвана
            warnings.warn(f"{func.__name__} is deprecated", category=DeprecationWarning, stacklevel=2)
            wrapper.has_run = True  
        return func(*args, **kwargs)
    wrapper.has_run = False 
    return wrapper

def cached(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = args + tuple(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    wrapper.cache = cache 
    return wrapper


