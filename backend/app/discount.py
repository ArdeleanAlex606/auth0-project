class Discount:
    def __init__(self, code: str, discount: float, store: str):
        self.code: str = code
        self.discount: float = discount
        self.store: str = store

    def __str__(self):
        return f"Discount: {self.code} ({self.discount}% off at {self.store})"

    __repr__ = __str__

    def __iter__(self):
        yield from {
            "code": self.code,
            "discount": self.discount,
            "store": self.store
        }.items()