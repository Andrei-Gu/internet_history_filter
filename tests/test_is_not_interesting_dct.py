import unittest
from ..main import is_not_interesting_dct


class TestIsNotInterestingDct(unittest.TestCase):
    def setUp(self):
        self.rows = ({"@timestamp": "Mar 30, 2023 @ 15:50:22.000",
                      "src_ip": "10.1.1.1",
                      "realm": "SomeRealm",
                      "auth_user": "aspushkin",
                      "response_code": "200",
                      "http_method": "CONNECT",
                      "bytes_from_client": "2,690",
                      "bytes_to_client": "6,500",
                      "media_type": "",
                      "url": "https://metrika.kontur.ru/track?e_c=signingNotification&e_a=getResponseSigning&e_n=nu18",
                      },
                     {"@timestamp": "Mar 30, 2023 @ 15:55:22.000",
                      "src_ip": "10.1.1.1",
                      "realm": "SomeRealm",
                      "auth_user": "aspushkin",
                      "response_code": "200",
                      "http_method": "CONNECT",
                      "bytes_from_client": "1500",
                      "bytes_to_client": "2000",
                      "media_type": "",
                      "url": "https://www.bing.com/threshold/xls.aspx",
                      },
                     {"@timestamp": "Mar 30, 2023 @ 15:55:22.000",
                      "src_ip": "10.1.1.1",
                      "realm": "SomeRealm",
                      "auth_user": "aspushkin",
                      "response_code": "200",
                      "http_method": "CONNECT",
                      "bytes_from_client": "1500",
                      "bytes_to_client": "2000",
                      "media_type": "",
                      "url": "https://yandex.ru/search?clid=2186620&text=%D0%9C%D0%B0%D0%B4%D0%BD%D0%B8+%D0%B7%D0%B0%D",
                      },
                     )

        self.filtration_keys = {'[not_interesting_parts]': ['arbitr.ru', '.gov.ru', 'alta.ru', 'metrika.kontur'],
                                '[not_interesting_tails]': ['.xml', '.aspx', '/websocket', '.svg'],
                                '[interesting_parts]': ['yandex.ru/search'],
                                }

        self.headers = ('[not_interesting_parts]',
                        '[not_interesting_tails]',
                        '[interesting_parts]',
                        '[interesting_tails]',
                        )

    def test_url_contains_part(self):
        self.assertTrue(is_not_interesting_dct(self.rows[0], self.filtration_keys, self.headers))

    def test_url_ends_with_tail(self):
        self.assertTrue(is_not_interesting_dct(self.rows[1], self.filtration_keys, self.headers))

    def test_url_doesnt_contain_part(self):
        self.assertFalse(is_not_interesting_dct(self.rows[2], self.filtration_keys, self.headers))

    def test_url_doesnt_end_with_tail(self):
        self.assertFalse(is_not_interesting_dct(self.rows[2], self.filtration_keys, self.headers))


if __name__ == '__main__':
    unittest.main()
