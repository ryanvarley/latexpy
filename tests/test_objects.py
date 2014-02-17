import unittest
import numpy as np

import latexpy.objects as tex


class Test_MultiFigure(unittest.TestCase):

    def setUp(self):
        self.answerStart = ['\\begin{figure}[htbp]', '\\centering', '\\begin{tabular}{cc}']
        self.answerContent = ['\\includegraphics[width=0.5\\textwidth]{path1.png}&',
                      '\\includegraphics[width=0.5\\textwidth]{path2.png}\\\\',
                      '\\includegraphics[width=0.5\\textwidth]{path3.png}&',
                      '\\includegraphics[width=0.5\\textwidth]{path4.png}\\\\']
        self.answerEnd = ['\\end{tabular}', '\\end{figure}']

        self.basicFig = tex.LatexMultiFigure()
        self.basicFig.addFigure('path1.png')
        self.basicFig.addFigure('path2.png')
        self.basicFig.addFigure('path3.png')
        self.basicFig.addFigure('path4.png')

    def test_MultiFigureParse2cols(self):
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicFig.output())

    def test_MultiFigureParse2colsNoCenter(self):
        self.answerStart.pop(1)  # remove center line
        self.basicFig.centering = False
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicFig.output())

    def test_MultiFigureParse2colsWithCaption(self):
        self.answerStart.insert(1, '\\caption{test caption}')  # remove center line
        self.basicFig.addCaption('test caption')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicFig.output())

    def test_MultiFigureParse2colsWithLabel(self):
        self.answerEnd.insert(-1, '\\label{test label}')  # remove center line
        self.basicFig.addLabel('test label')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicFig.output())

    def test_MultiFigureParse2colsWithOddRow(self):
        self.answerContent.append('\\includegraphics[width=0.5\\textwidth]{path5.png}')
        self.basicFig.addFigure('path5.png')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicFig.output())


class Test_LatexTable(unittest.TestCase):

    def setUp(self):
        self.answerStart = ['\\begin{table}[htbp]', '\\centering', '\\begin{tabular}{llll}']
        self.answerContent = ['1 & 2 & 3 & 4 \\\\',
                              '1.6 & 3.2 & 5.2 & 7.4 \\\\',
                              'a & ~ & b & c \\\\',
                              ]
        self.answerEnd = ['\\end{tabular}', '\\end{table}']

        self.basicTab = tex.LatexTable(columns=4)
        self.basicTab.addRow([1, 2, 3, 4])
        self.basicTab.addRow([1.6, 3.2, 5.2, 7.4])
        self.basicTab.addRow(['a', np.nan, 'b', 'c'])

    def test_MultiFigureParse4cols(self):
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())



if __name__ == '__main__':
    unittest.main()