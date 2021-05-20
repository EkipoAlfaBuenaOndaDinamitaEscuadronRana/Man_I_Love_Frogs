import sys
import os

route = os.getcwd().replace("/compilador/helpers", "")
route = route.replace("/compilador", "")
sys.path.insert(1, route)
