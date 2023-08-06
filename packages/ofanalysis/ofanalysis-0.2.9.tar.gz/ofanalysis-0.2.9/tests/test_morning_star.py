from unittest import TestCase

from ofanalysis.morningstar.morning_star import MorningStar


class TestMorningStar(TestCase):
    def setUp(self) -> None:
        self.morning_star = MorningStar(
            web_driver_path='./drivers/chromedriver',
            assets_path='./assets',
            cookie_str='user=username=laye0619@gmail.com&nickname=laye0619&status=Free&memberId=458975&password=trWMrjKv97VkUvhSrVRdJw==; MS_LocalEmailAddr=laye0619@gmail.com=; ASP.NET_SessionId=qrx24lbjffrtp145wuiqkerf; Hm_lvt_eca85e284f8b74d1200a42c9faa85464=1648263052,1648272775; MSCC=71fCj3A7jjI=; authWeb=A1A092B6A25E170610F5809DA546E3CA7330E16977D0A69E57D08F0A112A7D908AEEAFACC306F069987FA320F192C785DAD2ACE34EB9E9902DF714E7C3C62DF46736817E7123964377C793BA1E3708FBAC1CD5EE676F0C0777C60A7E59F5E897156EC43322A4DDB02C6C29AAA38750A030A4ABE3; Hm_lpvt_eca85e284f8b74d1200a42c9faa85464=1648274187; AWSALB=5s5Li0yx7jB0+Ycd/MhLfQLikR8HvYO0RvPuI6X/o8suHu5LKHyxk45piZJlppGk7otNW1tZLNUy6hUAwO4pRAbgvPEcPD4fIa0IY0cH4jIpfMPPrMHGZGYgy5ko; AWSALBCORS=5s5Li0yx7jB0+Ycd/MhLfQLikR8HvYO0RvPuI6X/o8suHu5LKHyxk45piZJlppGk7otNW1tZLNUy6hUAwO4pRAbgvPEcPD4fIa0IY0cH4jIpfMPPrMHGZGYgy5ko'
        )

    def test_get_fund_list(self):
        self.morning_star.get_fund_list()

    def test_write_to_db(self):
        # self.morning_star.write_to_db()
        pass
