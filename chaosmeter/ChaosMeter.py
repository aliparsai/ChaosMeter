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
import fnmatch
import os
import sys
from optparse import OptionParser, Values

from littledarwin import JavaParse
from littledarwin import JavaIO
from tqdm import tqdm

from .metrics import *
from .writers import *
from chaosmeter import License

chaosMeterVersion = '0.1.2'


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

    sourcePath = os.path.abspath(options.sourcePath)
    targetPath = os.path.abspath(options.targetPath)

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

    print(os.linesep)

    # Find all writers
    writerList = Writer.getAllWriters()
    writerInstanceList = list()

    if len(writerList) == 0:
        print("No writers found!")
        sys.exit(4)

    for WriterClass in writerList:
        writerInstance = WriterClass(targetPath)
        writerInstanceList.append(writerInstance)
        print("Found writer: \"" + WriterClass.name + "\"")

    # Get the file list

    if not os.path.isdir(sourcePath):
        print("Source path must be a directory.")
        sys.exit(5)

    fileList = list()

    for root, dirnames, filenames in os.walk(sourcePath):
        for filePath in fnmatch.filter(filenames, "*.java"):
            fileList.append(os.path.join(root, filePath))

    fileCounter = 0
    fileCount = len(fileList)

    print(os.linesep)
    print("Source Path: ", sourcePath)
    print("Target Path: ", targetPath)
    print(os.linesep)

    # Main loop
    completeResults = dict()
    completeResultsPath = os.path.join(targetPath, "FinalReport")
    for srcFile in tqdm(fileList, dynamic_ncols=True, unit='files'):
        fileCounter += 1
        fileRelativePath = os.path.relpath(srcFile, sourcePath)
        try:
            tqdm.write("({:,}/{:,}) {}".format(fileCounter, fileCount, fileRelativePath), end="\n\n")
        except UnicodeError as e:
            tqdm.write(str(e) + os.linesep)
            tqdm.write("Non-unicode filename detected. Not showing in terminal.")

        try:
            # parsing the source file into a tree.
            sourceCode = javaIOInstance.getFileContent(srcFile)
            tree = javaParseInstance.parse(sourceCode)
        except Exception as e:
            tqdm.write(str(e) + os.linesep, file=sys.stderr)
            tqdm.write("Error in parsing Java code, skipping the file.")
            continue

        # Calculate metrics

        metricResults = dict()
        for metricInstance in metricInstanceList:
            metricResults[metricInstance.name] = metricInstance.calculate(tree, sourceCode)

        metricResultsAggregate, metricLabels = Metric.aggregateMetrics(**metricResults)

        # Prepare the result file
        completeResults[fileRelativePath] = metricResultsAggregate

        srcFileRoot, srcFileName = os.path.split(srcFile)
        targetDir = os.path.join(targetPath, os.path.relpath(srcFileRoot, sourcePath))
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)

        targetFilePath = os.path.splitext(os.path.join(targetDir, srcFileName))[0]

        for writerInstance in writerInstanceList:
            fileContent = writerInstance.createTargetFormat(metricResultsAggregate, metricLabels)
            writerInstance.write(targetFilePath, fileContent)

    completeResultsLabels = ["File"]
    completeResultsLabels.extend(metricLabels)
    completeResultsAggregate = [completeResultsLabels]

    for filePath in sorted(completeResults.keys()):
        for methodName in sorted(completeResults[filePath].keys()):
            cellList = [filePath, methodName]
            cellList.extend(completeResults[filePath][methodName])
            completeResultsAggregate.append(cellList)

    for writerInstance in writerInstanceList:
        completeFileContent = writerInstance.createFinalReportTargetFormat(completeResultsAggregate)
        writerInstance.write(completeResultsPath, completeFileContent)

    print(os.linesep)

    return 0


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
