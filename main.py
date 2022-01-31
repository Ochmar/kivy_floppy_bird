from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint

from src.pipe.pipe import Pipe
from src.hero.hero import Hero


class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        def create_textures():
            self.cloud_texture = Image(source="./assets/cloud.png").texture
            self.cloud_texture.wrap = "repeat"
            self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

            self.floor_texture = Image(source="./assets/floor.png").texture
            self.floor_texture.wrap = "repeat"
            self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

        super().__init__(**kwargs)

        # Create textures
        create_textures()

    def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        self.cloud_texture.uvpos = (
            (self.cloud_texture.uvpos[0] + time_passed / 2.0) % Window.width,
            self.cloud_texture.uvpos[1]
        )
        self.floor_texture.uvpos = (
            (self.cloud_texture.uvpos[0] + time_passed * 1.5) % Window.width,
            self.cloud_texture.uvpos[1]
        )
        # Redraw the texture
        self.property('cloud_texture').dispatch(self)
        self.property('floor_texture').dispatch(self)


class MainApp(App):
    pipes = []
    GRAVITY = 300
    num_pipes = 5
    distance_between_pipes = Window.width / (num_pipes - 2)
    was_colliding = False

    def move_hero(self, time_passed):
        hero = self.root.ids.hero
        hero.y += hero.velocity * time_passed
        hero.velocity -= self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        hero = self.root.ids.hero
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(hero):
                is_colliding = True
                if hero.y < (pipe.pipe_center - pipe.GAP_SIZE / 2.0) \
                        or hero.top > (pipe.pipe_center + pipe.GAP_SIZE / 2.0):
                    self.game_over()
        if hero.y < 96 or hero.top > Window.height:
            self.game_over()
        print(self.was_colliding and not is_colliding)
        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.root.ids.hero.pos = (20, (self.root.height - 96) / 2.0)
        self.clear_pipes()
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

    def next_frame(self, time_passed):
        self.move_hero(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_textures(time_passed)

    def clear_pipes(self):
        for pipe in self.pipes:
            self.root.remove_widget(pipe)

    def start_game(self):
        self.was_colliding = False
        self.root.ids.score.text = "0"
        self.pipes = []
        self.frames = Clock.schedule_interval(self.next_frame, 1 / 60.)
        # Create the pipes
        for i in range(self.num_pipes):
            pipe = Pipe.pipe_factory(
                pipe_center=randint(96 + 100, self.root.height - 100),
                size_hint=(None, None),
                pos=(Window.width + i * self.distance_between_pipes, 96),
                size=(64, self.root.height - 96)
            )
            self.pipes.append(pipe)
            self.root.add_widget(pipe)

    def move_pipes(self, time_passed):
        # Move pipes
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # Reposition the pipe at the right side
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - self.distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width


MainApp().run()
