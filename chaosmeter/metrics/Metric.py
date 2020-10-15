from typing import Set, List, Dict, Tuple

from antlr4 import *
from littledarwin.JavaParse import JavaParse


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


class Metric(object):
    instantiable = False
    name = "Metric"
    abbreviation = "M"

    def __init__(self, javaParseInstance: JavaParse):
        self.javaParseInstance = javaParseInstance
        self.defaultValue = 0

    def calculate(self, tree: RuleContext, sourceCode: str = ""):
        pass


def getAllMetrics() -> Set[Metric]:
    return getAllInstantiableSubclasses(Metric)


def aggregateMetrics(**kargs: Dict[str, int]) -> Tuple[Dict[str, List[int]], List[str]]:
    aggregate = dict()
    labels = ["Method Name"]
    metricList = sorted(kargs.keys())
    labels.extend([str(metricName) for metricName in metricList])

    methodList = set()

    for mL in metricList:
        methodList.update(kargs[mL].keys())

    for method in methodList:
        aggregate[method] = list()
        for mL in metricList:
            aggregate[method].append(kargs[mL].get(method, 0))
    return aggregate, labels
