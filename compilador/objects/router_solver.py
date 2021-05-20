import sys
import os

route = os.getcwd().replace("/compilador/objects", "").replace("/compilador", "")
sys.path.insert(1, route)
