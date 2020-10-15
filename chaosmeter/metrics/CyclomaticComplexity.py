from littledarwin.JavaParse import JavaParse
from antlr4 import *
from chaosmeter.metrics import Metric


class CyclomaticComplexity(Metric.Metric):
    instantiable = True
    name = "Cyclomatic Complexity"
    abbreviation = "CC"

    def __init__(self, javaParseInstance: JavaParse):
        super().__init__(javaParseInstance)
        self.defaultValue = 1

    def calculate(self, tree: RuleContext, sourceCode: str = ""):
        return self.javaParseInstance.getCyclomaticComplexityAllMethods(tree)
