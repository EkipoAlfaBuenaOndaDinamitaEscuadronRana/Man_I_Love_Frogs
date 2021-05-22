import sys
import os

route = os.getcwd().replace("/compilador/tests", "").replace("/compilador", "")
sys.path.insert(1, route)
