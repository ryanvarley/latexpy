import unittest

import latexpy.objects as tex


class Test_MultiFigure(unittest.TestCase):

    def test_MultiFigureParse2cols(self):

        fig = tex.LatexMultiFigure()
        fig.addFigure('path1.png')
        fig.addFigure('path2.png')
        fig.addFigure('path3.png')
        fig.addFigure('path4.png')

        answer = '\\begin{figure}[htbp]\n' \
                      '\\centering\n' \
                      '\\begin{tabular}{cc}\n' \
                      '\\includegraphics[width=0.5\\textwidth]{path1.png}&\n' \
                      '\\includegraphics[width=0.5\\textwidth]{path2.png}\\\\\n' \
                      '\\includegraphics[width=0.5\\textwidth]{path3.png}&\n' \
                      '\\includegraphics[width=0.5\\textwidth]{path4.png}\\\\\n' \
                      '\\end{tabular}\n' \
                      '\\end{figure}'

        self.assertEqual(answer, fig.output())

if __name__ == '__main__':
    unittest.main()