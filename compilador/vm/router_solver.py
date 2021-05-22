import sys
import os

route = os.getcwd().replace("/compilador/vm", "").replace("/compilador", "")
sys.path.insert(1, route)
