from pygame.constants import AUDIO_ALLOW_FORMAT_CHANGE
from execute import *

level = "levels/level1.milf"
miPrograma = "miPrograma.milf"
test = "compilador/tests/test_28.milf"

Executer(test).run(
    print_running=True,
    print_pre_quads=True,
    print_post_quads=False,
    print_instructions=False,
    return_quads=False,
    run_game=False,
    play_level=1,
)
