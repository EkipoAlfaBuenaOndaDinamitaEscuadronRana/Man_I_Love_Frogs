from pygame.constants import AUDIO_ALLOW_FORMAT_CHANGE
from execute import *

Executer("compilador/tests/test_30.milf").run(
    print_running=True,
    print_pre_quads=True,
    print_post_quads=False,
    print_instructions=True,
    run_game=False,
)

# levels = ["*", "levels/level1.milf","levels/level2.milf"]

# if len(sys.argv) > 1:

#     num = int(sys.argv[1])
#     file =levels[num]
#     Executer(file).run(
#     print_running=False, print_quads=True, print_instructions=False, run_game=num)

# else:
#     Executer("levels/level2.milf").run(
#     print_running=False, print_quads=True, print_instructions=False, run_game=2)
