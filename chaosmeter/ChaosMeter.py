################################################################################################################
##                                                                                                            ##
##                                                                                                            ##
##        ▄█▄     ▄  █ ██   ████▄    ▄▄▄▄▄   █▀▄▀█ ▄███▄      ▄▄▄▄▀ ▄███▄   █▄▄▄▄                             ##
##        █▀ ▀▄  █   █ █ █  █   █   █     ▀▄ █ █ █ █▀   ▀  ▀▀▀ █    █▀   ▀  █  ▄▀                             ##
##        █   ▀  ██▀▀█ █▄▄█ █   █ ▄  ▀▀▀▀▄   █ ▄ █ ██▄▄        █    ██▄▄    █▀▀▌                              ##
##        █▄  ▄▀ █   █ █  █ ▀████  ▀▄▄▄▄▀    █   █ █▄   ▄▀    █     █▄   ▄▀ █  █                              ##
##         ▀███▀     █     █                     █  ▀███▀     ▀      ▀███▀     █                              ##
##                  ▀     █                     ▀                             ▀                               ##
##                       ▀                                                                                    ##
##                                                                                                            ##
##       Copyright (c) 2020 Ali Parsai                                                                        ##
##                                                                                                            ##
##       This program is free software: you can redistribute it and/or modify it under the terms of           ##
##       the GNU General Public License as published by the Free Software Foundation, either version 3        ##
##       of the License, or (at your option) any later version.                                               ##
##                                                                                                            ##
##       This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;            ##
##       without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.            ##
##       See the GNU General Public License for more details.                                                 ##
##                                                                                                            ##
##       You should have received a copy of the GNU General Public License along with this program.           ##
##       If not, see <https://www.gnu.org/licenses/>.                                                         ##
##                                                                                                            ##
##       Find me at:                                                                                          ##
##       https://www.parsai.net                                                                               ##
##                                                                                                            ##
################################################################################################################

import os
import sys
from optparse import OptionParser, Values

from littledarwin import JavaParse
from littledarwin import JavaIO

from .metrics import *
from chaosmeter import License

chaosMeterVersion = '0.1.0'


def main(mockArgs: list = None):
    """
    Main ChaosMeter Function
    """
    print("""

▄█▄     ▄  █ ██   ████▄    ▄▄▄▄▄   █▀▄▀█ ▄███▄      ▄▄▄▄▀ ▄███▄   █▄▄▄▄
█▀ ▀▄  █   █ █ █  █   █   █     ▀▄ █ █ █ █▀   ▀  ▀▀▀ █    █▀   ▀  █  ▄▀
█   ▀  ██▀▀█ █▄▄█ █   █ ▄  ▀▀▀▀▄   █ ▄ █ ██▄▄        █    ██▄▄    █▀▀▌
█▄  ▄▀ █   █ █  █ ▀████  ▀▄▄▄▄▀    █   █ █▄   ▄▀    █     █▄   ▄▀ █  █
▀███▀     █     █                     █  ▀███▀     ▀      ▀███▀     █
         ▀     █                     ▀                             ▀
              ▀

    ChaosMeter version %s Copyright (C) 2020 Ali Parsai

    ChaosMeter comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; run ChaosMeter --license for details.


    """ % chaosMeterVersion)

    optionParser = OptionParser(prog="chaosmeter")
    options = parseCmdArgs(optionParser, mockArgs)

    if options.sourcePath is None:
        optionParser.print_help()
        print("\nYou need to specify at least the path to the source files.\n")
        print("\nExample:\n\t ChaosMeter -p ./src/main -t ./target \n\n")
        sys.exit(1)

    if not os.path.isdir(options.sourcePath):
        print("Source path must be a directory.")
        sys.exit(2)

    javaParseInstance = JavaParse.JavaParse()
    javaIOInstance = JavaIO.JavaIO()

    metricList = Metric.getAllMetrics()
    metricInstanceList = list()

    if len(metricList) == 0:
        print("No metrics found!")
        sys.exit(3)

    # Find all metrics

    for MetricClass in metricList:
        metricInstance = MetricClass(javaParseInstance)
        metricInstanceList.append(metricInstance)
        print("Found metric: \"" + MetricClass.name + "\"")

    # Get file list





    return 0



def mutationPhase(options, filterType, filterList, higherOrder):
    """

    :param options:
    :type options:
    :param filterType:
    :type filterType:
    :param filterList:
    :type filterList:
    :param higherOrder:
    :type higherOrder:
    """
    # creating our module objects.
    javaIO = JavaIO(options.isVerboseActive)
    javaParse = JavaParse(options.isVerboseActive)
    totalMutantCount = 0

    try:
        assert os.path.isdir(options.sourcePath)
    except AssertionError as exception:
        print("Source path must be a directory.")
        sys.exit(1)
    # getting the list of files.
    javaIO.listFiles(targetPath=os.path.abspath(options.sourcePath), buildPath=os.path.abspath(options.buildPath),
                     filterType=filterType, filterList=filterList)
    fileCounter = 0
    fileCount = len(javaIO.fileList)
    # creating a database for generated mutants. the format of this database is different on different platforms,
    # so it cannot be simply copied from a platform to another.
    databasePath = os.path.join(javaIO.targetDirectory, "mutationdatabase")
    densityResultsPath = os.path.join(javaIO.targetDirectory, "ProjectDensityReport.csv")
    print("Source Path: ", javaIO.sourceDirectory)
    print("Target Path: ", javaIO.targetDirectory)
    print("Creating Mutation Database: ", databasePath)
    mutationDatabase = shelve.open(databasePath, "c")
    mutantTypeDatabase = dict()
    averageDensityDict = dict()

    # go through each file, parse it, calculate all mutations, and generate files accordingly.
    for srcFile in javaIO.fileList:
        print("\n(" + str(fileCounter + 1) + "/" + str(fileCount) + ") Source file: ", srcFile)
        targetList = list()

        try:
            # parsing the source file into a tree.
            sourceCode = javaIO.getFileContent(srcFile)
            tree = javaParse.parse(sourceCode)

        except Exception as e:
            print("Error in parsing Java code, skipping the file.")
            sys.stderr.write(str(e))
            continue

        fileCounter += 1

        enabledMutators = ["Traditional"]

        if options.isNullCheck:
            enabledMutators = ["Null"]

        if options.isAll:
            enabledMutators = ["All"]

        if options.isMethodLevel:
            enabledMutators = ["Method"]

        # apply mutations on the tree and receive the resulting mutants as a list of strings, and a detailed
        # list of which operators created how many mutants.

        javaMutate = JavaMutate(tree, sourceCode, javaParse, options.isVerboseActive)

        if higherOrder == 1:
            mutated, mutantTypes = javaMutate.gatherMutants(enabledMutators)
        else:
            mutated, mutantTypes = javaMutate.gatherHigherOrderMutants(higherOrder, enabledMutators)

        print("--> Mutations found: ", len(mutated))

        # go through all mutant types, and add them in total. also output the info to the user.
        for mutantType in mutantTypes.keys():
            if mutantTypes[mutantType] > 0:
                print("---->", mutantType, ":", mutantTypes[mutantType])
            mutantTypeDatabase[mutantType] = mutantTypes[mutantType] + mutantTypeDatabase.get(mutantType, 0)
        totalMutantCount += len(mutated)

        # for each mutant, generate the file, and add it to the list.
        fileRelativePath = os.path.relpath(srcFile, javaIO.sourceDirectory)
        densityReport = javaMutate.aggregateReport(littleDarwinVersion)
        averageDensityDict[fileRelativePath] = javaMutate.averageDensity
        aggregateComplexity = javaIO.getAggregateComplexityReport(javaMutate.mutantsPerMethod,
                                                                  javaParse.getCyclomaticComplexityAllMethods(tree),
                                                                  javaParse.getLinesOfCodePerMethod(tree))

        for mutatedFile in mutated:
            targetList.append(javaIO.generateNewFile(srcFile, mutatedFile, javaMutate.mutantsPerLine,
                                                     densityReport, aggregateComplexity))

        # if the list is not empty (some mutants were found), put the data in the database.
        if len(targetList) != 0:
            mutationDatabase[fileRelativePath] = targetList

        del javaMutate

    mutationDatabase.close()
    print("\nTotal mutations found: ", totalMutantCount)

    with open(densityResultsPath, 'w') as densityReportHandle:
        for key in averageDensityDict.keys():
            densityReportHandle.write(key + ',' + str(averageDensityDict[key]) + '\n')

    for mutantType in list(mutantTypeDatabase.keys()):
        if mutantTypeDatabase[mutantType] > 0:
            print("-->", mutantType + ":", mutantTypeDatabase[mutantType])



def parseCmdArgs(optionParser: OptionParser, mockArgs: list = None) -> Values:
    """

    :param mockArgs:
    :type mockArgs:
    :param optionParser:
    :type optionParser:
    :return:
    :rtype:
    """
    # parsing input options
    optionParser.add_option("-p", "--path", action="store", dest="sourcePath",
                            default=None, help="Path to Java source files.")
    optionParser.add_option("-t", "--target", action="store", dest="targetPath",
                            default=os.path.dirname(os.path.realpath(__file__)),
                            help="Path to store results.")
    optionParser.add_option("--license", action="store_true", dest="isLicenseActive", default=False,
                            help="Output the license and exit.")

    if mockArgs is None:
        (options, args) = optionParser.parse_args()
    else:
        (options, args) = optionParser.parse_args(args=mockArgs)

    if options.isLicenseActive:
        License.outputLicense()
        sys.exit(0)

    return options
