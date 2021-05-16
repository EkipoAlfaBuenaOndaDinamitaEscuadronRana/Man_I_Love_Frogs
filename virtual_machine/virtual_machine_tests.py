from virtual_machine_map import *
import unittest

class TestVirtualMachineMap(unittest.TestCase):
  def test_insert_symbol(self):
    vmm = VirtualMachineMap(4, 4, 4, 4)
    a_int = Symbol("a", "INT")
    b_int = Symbol("b", "INT")
    self.assertEqual(vmm.insert_symbol_in_segment("Data Segment", a_int), True)
    self.assertEqual(vmm.insert_symbol_in_segment("Data Segment", b_int), False)
