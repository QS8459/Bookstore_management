class A():
    __tablename__ = "A"

class B():
    def __init__(self, model):
        self.model = model

    def cls_n(self, **kwargs):
        print(kwargs)

if __name__ == "__main__":
    b = B(A())
    kwargs = {
        "year_published": "2001",
        'title' : '300 spartans',
        'author': 'Unknown'
    }
    field_string: str = "{"

    for k,v in kwargs.items():
        field_string += f'\"{k}\":\"{v}\",'
    field_string += "}"
    field_arr = [i for i in field_string]
    field_arr.pop(-2)
    result_string = ''.join(field_arr)
