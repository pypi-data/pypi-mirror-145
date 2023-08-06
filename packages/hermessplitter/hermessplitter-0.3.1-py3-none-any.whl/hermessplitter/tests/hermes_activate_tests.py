from hermessplitter.main import HermesSplitter
import unittest


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MainTest, self).__init__(*args, **kwargs)
        self.hs = HermesSplitter('0.0.0.0', 2295,  'wdb', 'watchman', 'hect0r1337',
                            '192.168.100.118', debug=True)

    def test_a(self):
        self.hs.activate(carnum='В060ХА702', client=1, record_id=12)
        all_data = ['0', '-50', '10', '40', '100','350', '500', '1000', '6660',
                    '15000', '20000']
        magic_data = []
        for data in all_data:
            response = self.hs.make_magic(data)
            magic_data.append(response)
        print("MAGIC DATA", dict(zip(all_data, magic_data)))


if __name__ == '__main__':
    unittest.main()