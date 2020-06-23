import pytest
from unittest.mock import patch, MagicMock


# @patch(
#     'mc_db.data_handler.prod_power_reading.measurement_aggregation_data_handler.'
#     'get_final_power',
#     MagicMock(
#         return_value=pd.DataFrame(
#             data=np.array(
#                 [
#                     [200., 203.],
#                     [300., 303.],
#                 ]
#             ),
#             index=pd.date_range(
#                 datetime(2019, 1, 1, 13),
#                 datetime(2019, 1, 1, 14),
#                 freq=pd.DateOffset(hours=1)
#             ),
#             columns=[1, 3]
#         )
#     )
# )
# def test_download():
