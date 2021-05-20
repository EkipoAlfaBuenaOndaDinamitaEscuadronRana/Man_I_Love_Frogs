import sys
import os

route = os.getcwd().replace("/compilador/vm", "")
route = route.replace("/compilador", "")
sys.path.insert(1, route)
