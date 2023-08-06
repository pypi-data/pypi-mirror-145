from unittest import TestCase
from ofanalysis.lixingren.lixingren_index_data import LixingrenIndexData


class TestLixingrenIndexData(TestCase):
    def setUp(self) -> None:
        self.index_data_object = LixingrenIndexData(
            lxr_token='1364169b-e34f-41ab-95eb-094a10638652',
            code='000300'
        )

    def test_build_index_df(self):
        self.index_data_object.build_index_df(
            type='pe_ttm',
            granularity='fs',
            metrics_type='median'
        )
        print()
