class A:
    def __init__(self) -> None:
        self.a = 19
        self.b = 42

    def lol(self):
        print('jopa')

    def get_data(self):
        return self


class B(A):
    def __init__(self) -> None:
        super().__init__()
        self.c = 352

    def lol(self):
        self.c = 0
        print('popa')


b = B()
b.lol()
