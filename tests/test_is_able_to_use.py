import unittest
from ..main import is_able_to_use


class TestIsAbleToUse(unittest.TestCase):
    def setUp(self):
        self.filtration_keys = {'[not_interesting_parts]': ['3lflsdfj', 'xgl334'],
                                '[not_interesting_tails]': [],
                                }


    def test_not_empty_list(self):
        self.assertTrue(is_able_to_use(self.filtration_keys, '[not_interesting_parts]'))


    def test_empty_list(self):
        self.assertFalse(is_able_to_use(self.filtration_keys, '[not_interesting_tails]'))


if __name__ == '__main__':
    unittest.main()
