from pygame.constants import AUDIO_ALLOW_FORMAT_CHANGE
from execute import *

file_name = input("Escribe el nombre de tu programa: ")

Executer(file_name).run(
    print_running=True,
    print_pre_quads=False,
    print_post_quads=False,
    print_instructions=False,
    play_level=None,
    run_game=True,
)
