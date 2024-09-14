import unittest
from ..main import is_not_valid


class TestIsNotValid(unittest.TestCase):
    def setUp(self):
        self.headers = ('[not_interesting_parts]',
                        '[not_interesting_tails]',
                        '[interesting_parts]',
                        '[interesting_tails]',
                        )

        self.messages = {'no_headers_msg': 'Указанный Вами файл не содержит хотя бы одно из необходимых названий списков ключей фильтрации. Либо их названия отличаются от перечисленных выше.',
                         'empty_lists_msg': 'В указанном Вами файле имеются необходимые названия списков, но все они не содержат ключи фильтрации (пустые)',
                         }

    def test_empty_dict(self):
        self.assertTrue(is_not_valid({}, self.headers, self.messages))

    def test_no_correct_headers(self):
        self.assertTrue(is_not_valid({'[!!!not_interesting_parts]': [],
                                      '[not_interesting123456_tails]':['sff', 'siueel'],
                                      },
                                     self.headers,
                                     self.messages
                                     )
                        )

    def test_empty_lists(self):
        self.assertTrue(is_not_valid({'[not_interesting_parts]': [],
                                      '[not_interesting_tails]': [],
                                      },
                                     self.headers,
                                     self.messages
                                     )
                        )

    def test_correct_headers_and_not_empty_lists(self):
        self.assertFalse(is_not_valid({'[not_interesting_parts]': ['3lflsdfj', 'xgl334'],
                                      '[not_interesting_tails]': [],
                                      },
                                     self.headers,
                                     self.messages
                                     )
                        )


if __name__ == '__main__':
    unittest.main()
