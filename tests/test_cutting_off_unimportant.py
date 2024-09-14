import unittest
from ..main import cutting_off_unimportant


class TestCuttingOffUnimportant(unittest.TestCase):
    def setUp(self):
        self.row = {"@timestamp": "Mar 30, 2023 @ 15:50:22.000",
                    "src_ip": "10.1.1.1",
                    "realm": "SomeRealm",
                    "auth_user": "aspushkin",
                    "response_code": "200",
                    "http_method": "CONNECT",
                    "bytes_from_client": "2,690",
                    "bytes_to_client": "6,500",
                    "media_type": "",
                    "url": "www.moscowmap.ru:443",
                    }

        self.new_row = {'date': '2023 03 30',
                        'time': '15:50:22',
                        'url': 'www.moscowmap.ru:443',
                        }

    def test_cutting_off(self):
        self.assertEqual(cutting_off_unimportant(self.row), self.new_row)


if __name__ == '__main__':
    unittest.main()
