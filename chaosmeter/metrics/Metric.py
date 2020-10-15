from typing import Set, List, Dict, Tuple

from littledarwin.JavaParse import JavaParse
from antlr4 import *


class Metric(object):
    instantiable = False
    name = "Metric"
    abbreviation = "M"

    def __init__(self, javaParseInstance: JavaParse):
        self.javaParseInstance = javaParseInstance

    def calculate(self, tree: RuleContext, sourceCode: str = ""):
        pass


def getAllInstantiableSubclasses(parentClass):
    """

    :param parentClass: the class that all its subclasses must be returned
    :type parentClass: Type[MutationOperator]
    :return: set of MutationOperator instantiable subclasses
    :rtype: set
    """
    allInstantiableSubclasses = set()

    for subClass in parentClass.__subclasses__():
        if subClass.instantiable:
            allInstantiableSubclasses.add(subClass)
        allInstantiableSubclasses.update(getAllInstantiableSubclasses(subClass))

    return allInstantiableSubclasses


def getAllMetrics() -> Set[Metric]:
    return getAllInstantiableSubclasses(Metric)


def aggregateMetrics(**kargs: Dict[str, int]) -> Tuple[Dict[str, List[int]], List[str]]:
    aggregate = dict()
    labels = ["Method Name"]
    labels.extend([str(metricName) for metricName in kargs.keys()])

    methodList = set()

    for mL in kargs.values():
        methodList.update(mL.keys())

    for method in methodList:
        aggregate[method] = [metricValue.get(method, 0) for metricValue in kargs.values()]

    return aggregate, labels
