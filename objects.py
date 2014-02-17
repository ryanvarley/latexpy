import numpy as np

class LatexObject(object):

    def __init__(self):
        self.texLines = []  # the main list
        self._caption = False
        self._label = False

    def _startObject(self):
        return ['']

    def _endObject(self):
        return ['']

    def _proccessTex(self):
        return self.texLines

    def addCaption(self, caption):
        self._caption = '\\caption{' + caption + '}'

    def addLabel(self, label):
        self._label = '\\label{' + label + '}'

    def output(self):
        """ outputs tex as a string
        """
        texFile = '\n'.join(self._startObject() + self.texLines + self._endObject())

        return texFile


class LatexMultiFigure(LatexObject):
    """ Handles a multiple plots in a figure instance
    """

    def __init__(self, pos='htbp'):
        LatexObject.__init__(self)

        self.pos = pos  # position argument
        self.centering = True
        self.figsPerRow = 2
        self.maxWidthUnit = '\\textwidth'

        # internal variables for code only
        self._figColNum = 1


    def _getWidth(self):
        return '{}{}'.format(0.5, self.maxWidthUnit)  # TODO replace with calculation

    def addFigure(self, path):
        figColNum = self._figColNum
        # TODO complicated code can be replaced by ' & '.join (possibly)
        if len(self.texLines):  # if we have a previous figure
            if figColNum > 1:  # not the first in the row
                self.texLines[-1] += '&'  # add endchar to previous figure now we are adding another fig

        if figColNum < self.figsPerRow:
            self._figColNum += 1
            endChar = ''
        elif figColNum == self.figsPerRow:
            endChar = '\\\\'  # add end row char if last in row
            self._figColNum = 1
        else:
            raise ValueError('somethings wrong with the figure count')

        figureTex = '\includegraphics[width={}]{}'.format(self._getWidth(), '{' + path + '}')
        self.texLines.append(figureTex + endChar)

    def _startObject(self):
        startObject= ['\\begin{figure}[' + self.pos + ']']
        if self._caption:
            startObject.append(self._caption)
        if self.centering:
            startObject.append('\\centering')
        startObject.append('\\begin{tabular}{cc}')
        return startObject

    def _endObject(self):
        endObject = ['\\end{tabular}']
        if self._label:
            endObject.append(self._label)
        endObject.append('\\end{figure}')
        return endObject


class LatexTable(LatexObject):
    """ Handles a table instance
    """

    def __init__(self, columns):
        LatexObject.__init__(self)

        self.columns = columns
        self.pos = 'htbp'
        self.centering = True

        self._header = False

    def _startObject(self):
        startObject= ['\\begin{table}[' + self.pos + ']']
        if self._caption:
            startObject.append(self._caption)
        if self.centering:
            startObject.append('\\centering')

        layout = 'l' * self.columns
        startObject.append('\\begin{tabular}{' + layout + '}')

        if self._header:
            startObject.append(self._header)
            startObject.append('\hline')
        return startObject

    def addRow(self, rowList):

        if len(rowList) != self.columns:
            raise ValueError('You must give the exact number of columns each time. use np.nan for blanks')

        parsedRowList = ['~' if val is np.nan else str(val) for val in rowList]
        self.texLines.append(' & '.join(parsedRowList) + ' \\\\')  # seperate values by & next cell char and lines by new line\\

    def _endObject(self):
        endObject = ['\\end{tabular}']
        if self._label:
            endObject.append(self._label)
        endObject.append('\\end{table}')
        return endObject

    def addHeader(self, headerList):
        """ Currently you can only have one header, it will be seperated from the rest by a line and will replace any
        existing header
        """

        # for ease and to avoid extra function calls just add row then pop it into the header

        self.addRow(headerList)
        self._header = self.texLines.pop()