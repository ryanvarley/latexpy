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

        # internal variables for code only
        self._caption = False
        self._figColNum = 1


    def _getWidth(self):
        return '{}{}'.format(0.5, self.maxWidthUnit)  # TODO replace with calculation

    def addFigure(self, path):
        figColNum = self._figColNum

        if len(self.texLines):  # if we have a previous figure
            if figColNum > 1:  # not the first in the row
                self.texLines[-1] += '&'  # add endchar to previous figure now we are adding another fig

        if figColNum < self.figsPerRow:
            self._figColNum += 1
            endChar = ''
        elif figColNum == self.figsPerRow:
            endChar = '\\\\'  # add end row char is last in row
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