from io import BytesIO
from typing import Dict, List
from chaosmeter.writers.Writer import Writer

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P
from odf.table import Table, TableRow, TableCell


class ODSWriter(Writer):
    instantiable = True
    name = "ODS Writer"

    def __init__(self, outputPath):
        super().__init__(outputPath)
        self.extension = ".ods"

    def createTargetFormat(self, metricValues: Dict[str, List[int]], metricLabels: List[str]) -> bytes:
        textdoc = OpenDocumentSpreadsheet()
        tablecontents = Style(name="Table Contents", family="paragraph")
        tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
        tablecontents.addElement(TextProperties(fontweight="bold"))
        textdoc.styles.addElement(tablecontents)

        table = Table(name="Java Metrics")

        tr = self.newRow(table)
        for metricLabel in metricLabels:
            self.addElementToRow(metricLabel, "string", tr, tablecontents)

        for methodName in metricValues.keys():
            tr = self.newRow(table)
            self.addElementToRow(methodName, "string", tr, tablecontents)

            for metricValue in metricValues[methodName]:
                self.addElementToRow(str(metricValue), "float", tr, tablecontents)

        textdoc.spreadsheet.addElement(table)

        stringOutput = BytesIO()
        textdoc.write(stringOutput)
        return stringOutput.getvalue()

    def createFinalReportTargetFormat(self, finalReport: List[list]) -> bytes:
        textdoc = OpenDocumentSpreadsheet()
        tablecontents = Style(name="Table Contents", family="paragraph")
        tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
        tablecontents.addElement(TextProperties(fontweight="bold"))
        textdoc.styles.addElement(tablecontents)

        table = Table(name="Java Metrics")

        tr = self.newRow(table)
        for columnLabels in finalReport[0]:
            self.addElementToRow(columnLabels, "string", tr, tablecontents)

        for row in finalReport[1:]:
            tr = self.newRow(table)
            self.addElementToRow(row[0], "string", tr, tablecontents)
            self.addElementToRow(row[1], "string", tr, tablecontents)

            for element in row[2:]:
                self.addElementToRow(str(element), "float", tr, tablecontents)

        textdoc.spreadsheet.addElement(table)

        stringOutput = BytesIO()
        textdoc.write(stringOutput)
        return stringOutput.getvalue()

    def newRow(self, table):
        tr = TableRow()
        table.addElement(tr)
        return tr

    def addElementToRow(self, element, elementType, tableRow, tablecontents):
        if elementType == "float":
            tc = TableCell(valuetype=elementType, value=element.strip())
        else:
            tc = TableCell(valuetype=elementType)

        tableRow.addElement(tc)
        p = P(stylename=tablecontents, text=element)
        tc.addElement(p)
