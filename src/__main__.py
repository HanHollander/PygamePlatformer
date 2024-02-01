import pygame as pg
import config as c
from model import Game
from pynkie.run import Pynkie
from pynkie.view import ScaledView, Viewport
from view import MyGUIView

pg.init()
init_scale = 3
camera_width = 320
camera_height = 180
world_view = ScaledView(Viewport(pg.Rect(0, 0, camera_width, camera_height),
                                 pg.Vector2(camera_width * init_scale, camera_height * init_scale)))
game = Game(world_view)
gui_view = MyGUIView()

event_listeners = {pg.MOUSEMOTION: [gui_view],
                   pg.KEYDOWN: [game, world_view],
                   pg.KEYUP: [game],
                   pg.VIDEORESIZE: [world_view]}

p = Pynkie(
           views=[world_view, gui_view],
           models=[game],
           event_listenters=event_listeners,
           screen_width=world_view.viewport.screen_size.x,
           screen_height=world_view.viewport.screen_size.y,
           debug_info=c.DEBUG_INFO,
           use_default_cursor=False)
p.run()










