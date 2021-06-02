from pygame.constants import AUDIO_ALLOW_FORMAT_CHANGE
from execute import *

Executer("levels/level2.milf").run(
    print_running=False,
    print_pre_quads=False,
    print_post_quads=False,
    print_instructions=False,
    run_game=True,
)
