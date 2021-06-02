from pygame.constants import AUDIO_ALLOW_FORMAT_CHANGE
from execute import *

# "compilador/tests/test_30.milf"
# levels/level1.milf
Executer("compilador/tests/test_28.milf").run(
    print_running=True,
    print_pre_quads=True,
    print_post_quads=False,
    print_instructions=False,
    run_game=False,
)
