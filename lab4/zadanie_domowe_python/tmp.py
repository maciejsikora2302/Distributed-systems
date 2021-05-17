# import pykka


# class Playback(object):
#     def play(self):
#         return True

# class AnActor(pykka.ThreadingActor):
#     def __init__(self):
#         super().__init__()
#         self.playback = pykka.traversable(Playback())

# proxy = AnActor.start().proxy()
# play_success = proxy.playback.play().get()
# print(play_success)
# proxy.stop()

import os
try:
    os.remove("./baza.json")
except Exception as e:
    pass
open("./baza.json", "w+").close()