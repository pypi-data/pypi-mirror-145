from unittest import TestCase
from ofanalysis.aks.akshare_data_update import AKShareDataUpdate


class TestAKShareDataUpdate(TestCase):
    def setUp(self) -> None:
        self.akshare_data_update_object = AKShareDataUpdate()

    def test_retrieve_index_value_hist(self):
        self.akshare_data_update_object.retrieve_index_value_hist()
        pass

    def test_retrieve_fund_rating_summary(self):
        self.akshare_data_update_object.retrieve_fund_rating_summary()
        pass
