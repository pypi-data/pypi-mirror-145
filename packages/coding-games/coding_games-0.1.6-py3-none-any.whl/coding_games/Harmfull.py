from pgzero.actor import Actor




class Harmful(Actor):
    def __init__(self, image, *args, **kwargs):
        super().__init__(image, **kwargs)

    def harm(self, actors):
        pass
