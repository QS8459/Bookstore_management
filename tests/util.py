import time
def time_utility(func):
    a = time.time()
    def wrapper(*args,**kwargs):
        return func(*args,**kwargs);
    b = time.time()
    print(b-a)
    return wrapper