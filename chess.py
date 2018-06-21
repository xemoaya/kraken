from global_cfg import *
import pyglet  

class Chess(pyglet.sprite.Sprite) :
    def __init__(self, *args, **kwargs):
        super(Chess, self).__init__(img=kwargs["img"], x=kwargs["x"], y=kwargs["y"])
        self.type = kwargs["type"]
        self.isalive = True


        