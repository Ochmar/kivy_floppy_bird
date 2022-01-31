from kivy.properties import NumericProperty
from kivy.uix.image import Image


class Hero(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "assets/hero_jump.png"
        self.velocity = 150
        super(Hero, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "assets/hero_fall.png"
        super(Hero, self).on_touch_up(touch)
