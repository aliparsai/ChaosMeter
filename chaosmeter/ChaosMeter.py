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

from .metrics import *
from .writers import *
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
        for fileName in fnmatch.filter(filenames, "*.java"):
            fileList.append(os.path.join(root, fileName))

    fileCounter = 0
    fileCount = len(fileList)

    print("Source Path: ", sourcePath)
    print("Target Path: ", targetPath)

    # Main loop

    for srcFile in fileList:
        fileCounter += 1
        print("\n(" + str(fileCounter) + "/" + str(fileCount) + ") Source file: ", srcFile)

        try:
            # parsing the source file into a tree.
            sourceCode = javaIOInstance.getFileContent(srcFile)
            tree = javaParseInstance.parse(sourceCode)

        except Exception as e:
            print("Error in parsing Java code, skipping the file.")
            sys.stderr.write(str(e))
            continue

        # Calculate metrics

        metricResults = dict()
        for metricInstance in metricInstanceList:
            metricResults[metricInstance.name] = metricInstance.calculate(tree, sourceCode)

        metricResultsAggregate, metricLabels = Metric.aggregateMetrics(**metricResults)

        # Prepare the result file

        fileRelativePath = os.path.relpath(srcFile, sourcePath)
        srcFileRoot, srcFileName = os.path.split(srcFile)
        targetDir = os.path.join(targetPath, os.path.relpath(srcFileRoot, sourcePath))
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)

        targetFilePath = os.path.splitext(os.path.join(targetDir, srcFileName))[0]

        for writerInstance in writerInstanceList:
            fileContent = writerInstance.createTargetFormat(metricResultsAggregate, metricLabels)
            writerInstance.write(targetFilePath, fileContent)

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

