from unittest import TestCase
from sudoku_engine import SudokuEngine

# Tests for several difficulty levels :
#  EASY   : all grid can be found by checking missing numbers in lines
#  MEDIUM : same with less initial digits
#  HARD   : above logic insufficient, need also to check for cells being the only one
#           in their line/column/square able to contain a specific digit
# EXPERT  : above logic insufficient, also need to take some guesses and revert them if
#           they lead to an invalid grid

SAMPLES = {
    'easy': {
        'input':
            '29 873 1 \n' +
            '4    592 \n' +
            ' 1  24   \n' +
            '    896  \n' +
            '  4   83 \n' +
            ' 8231 5  \n' +
            '  9238  7\n' +
            '8   47   \n' +
            '3 5 9 284',
        'expected':
            '296873415\n' +
            '437165928\n' +
            '518924763\n' +
            '153489672\n' +
            '964752831\n' +
            '782316549\n' +
            '649238157\n' +
            '821547396\n' +
            '375691284'
    },
    'medium': {
        'input':
            '6  5 3  4\n' +
            ' 31  42 7\n' +
            '5 9     3\n' +
            '   4698  \n' +
            '    8   5\n' +
            '      19 \n' +
            '9 8   5  \n' +
            '   1   2 \n' +
            '  5926 7 ',
        'expected':
            '672513984\n' +
            '831694257\n' +
            '549872613\n' +
            '157469832\n' +
            '396281745\n' +
            '284735196\n' +
            '928347561\n' +
            '763158429\n' +
            '415926378'
    },
    'hard': {
        'input':
            '  5  8   \n' +
            '    7  8 \n' +
            '   3  475\n' +
            '     7   \n' +
            '    941  \n' +
            ' 9 8     \n' +
            '92     38\n' +
            '1    6  9\n' +
            '34   26  ',
        'expected':
            '735248916\n' +
            '469175382\n' +
            '281369475\n' +
            '513627894\n' +
            '872594163\n' +
            '694813527\n' +
            '926451738\n' +
            '158736249\n' +
            '347982651'
    },
    'expert': {
        'input':
            '    3    \n' +
            '  1 7694 \n' +
            ' 8 9     \n' +
            ' 4   1   \n' +
            ' 28 9    \n' +
            '      16 \n' +
            '7  8     \n' +
            '      4 2\n' +
            ' 9  1 3  ',
        'expected':
            '469138275\n' +
            '351276948\n' +
            '287945631\n' +
            '946751823\n' +
            '128693754\n' +
            '573482169\n' +
            '734829516\n' +
            '815367492\n' +
            '692514387'
    }
}


class TestSudokuEngine(TestCase):

    def test_all_levels(self):
        for level in SAMPLES:
            print('Level', level)
            sample = SAMPLES[level]
            engine = SudokuEngine(sample['input'])
            engine.solve()
            assert engine.state.is_complete()
            result = engine.state.display().replace(' ', '').strip()
            assert result == sample['expected']
