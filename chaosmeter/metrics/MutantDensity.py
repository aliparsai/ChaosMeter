from littledarwin.JavaParse import JavaParse
from littledarwin.JavaMutate import JavaMutate
from antlr4 import *
from chaosmeter.metrics import Metric


class MutantDensity(Metric.Metric):
    instantiable = True
    name = "Mutant Density"
    abbreviation = "MD"

    def __init__(self, javaParseInstance: JavaParse):
        super().__init__(javaParseInstance)

    def calculate(self, tree: RuleContext, sourceCode: str = ""):
        javaMutate = JavaMutate(tree, sourceCode, self.javaParseInstance, False)
        javaMutate.gatherMutants(["Traditional"])
        result = javaMutate.mutantsPerMethod.copy()

        del javaMutate

        return result



