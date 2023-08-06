from unittest import TestCase
from ofanalysis.ts.ts_data_update import TSDataUpdate


class TestTSDataUpdate(TestCase):
    def setUp(self) -> None:
        self.ts_data_update_object = TSDataUpdate('602e5ad960d66ab8b1f3c13b4fd746f5323ff808b0820768b02c6da3')

    def test_retrieve_all(self):
        self.ts_data_update_object.retrieve_all()
        print()
