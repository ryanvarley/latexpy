class LatexObject(object):

    def __init__(self):
        self.texLines = []  # the main list

    def _startObject(self):
        return ['']

    def _endObject(self):
        return ['']

    def _proccessTex(self):
        return self.texLines

    def output(self):
        """ outputs tex as a string
        """
        texFile = '\n'.join(self._startObject() + self.texLines + self._endObject())

        return texFile


class LatexMultiFigure(LatexObject):
    """ Handles a multiple plots in a figure instance
    """

    def __init__(self):
        LatexObject.__init__(self)

        self.pos = 'htbp'  # position argument
        self.centering = True
        self.figsPerRow = 2
        self.maxWidthUnit = '\\textwidth'

        self._caption = False
        self._figColNum = 1

    def _getWidth(self):
        return '{}{}'.format(0.5, self.maxWidthUnit)  # TODO replace with calculation

    def addFigure(self, path):
        figColNum = self._figColNum
        if figColNum < self.figsPerRow:
            endChar = '&'  # TODO endchar should be appended to the previous value after the next value is processed
            self._figColNum += 1
        elif figColNum == self.figsPerRow:
            endChar = '\\\\'
            self._figColNum = 1
        else:
            raise ValueError('somethings wrong with the figure count')

        figureTex = '\includegraphics[width={}]{}'.format(self._getWidth(), '{' + path + '}')
        self.texLines.append(figureTex + endChar)

    def addCaption(self, caption):
        self._caption = '\caption{' + caption + '}'

    def _startObject(self):
        startObject= ['\\begin{figure}[' + self.pos + ']']
        if self._caption:
            startObject.append(self._caption)
        if self.centering:
            startObject.append('\\centering')
        startObject.append('\\begin{tabular}{cc}')
        return startObject

    def _endObject(self):
        endObject = ['\\end{tabular}\n'
                     '\\end{figure}']
        return endObject


class LatexTable(LatexObject):
    """ Handles a table instance
    """

    def __init__(self, colums):
        LatexObject.__init__(self)

        self.colums = colums
        self.colSep = '|' # symbol seperating colums


    def endTable(self):

        # appends the end of table
        pass

    def getTEX(self):

        # turn results into a TEX string
        pass