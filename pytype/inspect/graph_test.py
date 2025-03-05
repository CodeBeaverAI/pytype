"""Tests for inspect.graph."""

from pytype.inspect import graph
class Program:
    def __init__(self):
        self.cfg_nodes = []
        self.variables = []
        self.entrypoint = object()
        self.node_counter = 0
        self.var_counter = 0
    def NewCFGNode(self):
        node = CFGNode(self)
        self.cfg_nodes.append(node)
        return node
    def NewVariable(self):
        variable = Variable(self)
        self.variables.append(variable)
        return variable

class CFGNode:
    def __init__(self, program):
        self.program = program
        self.id = program.node_counter
        program.node_counter += 1
        self.name = "CFGNode"
        self.outgoing = []
    def ConnectNew(self):
        new_node = self.program.NewCFGNode()
        self.outgoing.append(new_node)
        return new_node

class Variable:
    def __init__(self, program):
        self.program = program
        self.id = program.var_counter
        program.var_counter += 1
        self.bindings = []
    def AddBinding(self, data, origins, where):
        binding = Binding(data, origins, where)
        self.bindings.append(binding)
        return binding

class Binding:
    def __init__(self, data, origins, where):
        self.data = data
        self.origins = origins
        self.where = where
        self.source_sets = []
    def __repr__(self):
        return f"Binding({self.data!r})"

import unittest


class GraphTest(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.prog = Program()
    self.current_location = self.prog.NewCFGNode()

  def test_program_to_dot(self):
    v1 = self.prog.NewVariable()
    b = v1.AddBinding("x", [], self.current_location)
    n = self.current_location.ConnectNew()
    v2 = self.prog.NewVariable()
    v2.AddBinding("y", {b}, n)
    # smoke test
    tg = graph.TypeGraph(self.prog, set(), False)
    assert isinstance(tg.to_dot(), str)


if __name__ == "__main__":
  unittest.main()
