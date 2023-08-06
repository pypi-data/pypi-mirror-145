from unittest import TestCase
from ofanalysis.lixingren.lixingren_sw_data import LixingrenSWData


class TestLixingrenSWData(TestCase):
    def setUp(self) -> None:
        self.index_data_object = LixingrenSWData(
            lxr_token='1364169b-e34f-41ab-95eb-094a10638652',
            code='370000'
        )
    def test_build_sw_ind_df(self):
        self.index_data_object.build_sw_ind_df(
            type='pe_ttm',
            granularity='fs',
            metrics_type='median'
        )
        print()
