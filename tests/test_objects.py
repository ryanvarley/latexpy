import unittest
import numpy as np
import sys

from os.path import join
sys.path.append(join('..'))

import objects as tex


class Test_MultiFigure(unittest.TestCase):

    def setUp(self):
        self.answerStart = ['\\begin{figure}[htbp]', '\\centering', '\\begin{tabular}{cc}']
        self.answerContent = ['\\includegraphics[width=0.5\\textwidth]{path1.png}&',
                      '\\includegraphics[width=0.5\\textwidth]{path2.png}\\\\',
                      '\\includegraphics[width=0.5\\textwidth]{path3.png}&',
                      '\\includegraphics[width=0.5\\textwidth]{path4.png}\\\\']
        self.answerEnd = ['\\end{tabular}', '\\end{figure}']

        self.basicFig = tex.MultiFigure()
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


class Test_Table(unittest.TestCase):

    def setUp(self):
        self.answerStart = ['\\begin{table}[htbp]', '\\centering', '\\begin{tabular}{llll}']
        self.answerContent = ['1 & 2 & 3 & 4 \\\\',
                              '1.6 & 3.2 & 5.2 & 7.4 \\\\',
                              'a & ~ & b & c \\\\',
                              ]
        self.answerEnd = ['\\end{tabular}', '\\end{table}']

        self.basicTab = tex.Table(columns=4)
        self.basicTab.addRow([1, 2, 3, 4])
        self.basicTab.addRow([1.6, 3.2, 5.2, 7.4])
        self.basicTab.addRow(['a', np.nan, 'b', 'c'])

    def test_MultiFigureParse4cols(self):
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())

    def test_MultiFigureParse4cols_with_header(self):
        self.basicTab.addHeader(['a', 'b', 'c', 'd'])

        self.answerStart.append('a & b & c & d \\\\\n\\hline')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())


class Test_LongTable(Test_Table):
    """ support for a long table object. Note that at present this isn't super customisable
    """

    def setUp(self):
        self.answerStart = ['\\begin{longtable}[htbp]{llll}',]
        self.answerContent = ['1 & 2 & 3 & 4 \\\\',
                              '1.6 & 3.2 & 5.2 & 7.4 \\\\',
                              'a & ~ & b & c \\\\',
                              ]
        self.answerEnd = ['\\end{longtable}']

        self.basicTab = tex.LongTable(columns=4)
        self.basicTab.addRow([1, 2, 3, 4])
        self.basicTab.addRow([1.6, 3.2, 5.2, 7.4])
        self.basicTab.addRow(['a', np.nan, 'b', 'c'])

    # def test_MultiFigureParse4cols(self):
    #     answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
    #     self.assertEqual(answer, self.basicTab.output())

    def test_MultiFigureParse4cols_with_header(self):
        self.basicTab.addHeader(['a', 'b', 'c', 'd'])
        self.answerStart.append('\\hline\na & b & c & d \\\\\n\\hline\n\\endhead')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())

    def test_MultiFigureParse4cols_with_header_label(self):
        self.basicTab.addPageHeaderLabel('Continued from previous page')
        self.answerStart.append('\\multicolumn{4}{l}{Continued from previous page}\\\\\n\\hline\n\\endhead')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())

    def test_MultiFigureParse4cols_with_firstpage_header(self):
        self.basicTab.addCaption('first page header / caption')
        self.answerStart.append('\\caption{first page header / caption}\\\\\n\\hline\n\\endfirsthead')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())

    def test_MultiFigureParse4cols_with_footer(self):
        self.basicTab.addFooter('cont on next page')
        self.answerStart.append('\\multicolumn{4}{l}{cont on next page}\\\\\n\\endfoot')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())

    def test_MultiFigureParse4cols_with_lastfooter(self):
        self.basicTab.addLastPageFooter('thats the end of the table')
        self.answerStart.append('\\hline\nthats the end of the table\\\\\n\\endlastfoot')
        answer = '\n'.join(self.answerStart + self.answerContent + self.answerEnd)
        self.assertEqual(answer, self.basicTab.output())

if __name__ == '__main__':
    unittest.main()