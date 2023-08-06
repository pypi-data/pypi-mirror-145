class AbstractAgent():
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, state, time):
        raise NotImplementedError("Define forward method with arguments state and time.")
