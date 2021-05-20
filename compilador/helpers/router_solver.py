import sys
import os

route = os.getcwd().replace("/compilador/helpers", "").replace("/compilador", "")
sys.path.insert(1, route)
