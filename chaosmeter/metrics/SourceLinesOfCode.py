from littledarwin.JavaParse import JavaParse
from antlr4 import *
from chaosmeter.metrics import Metric


class SourceLinesOfCode(Metric):
    instantiable = True
    name = "Source Lines of Code"
    abbreviation = "SLOC"

    def __init__(self, javaParseInstance: JavaParse):
        super().__init__(javaParseInstance)

    def calculate(self, tree: RuleContext, sourceCode: str = ""):
        return self.javaParseInstance.getLinesOfCodePerMethod(tree)

