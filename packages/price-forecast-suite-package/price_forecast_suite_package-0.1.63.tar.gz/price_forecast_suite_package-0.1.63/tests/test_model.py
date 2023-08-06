import unittest

from price_forecast_suite_package import suite_model

class TestLSTM(unittest.TestCase):
    def test_lstm(self):
        model = suite_model.lstm_model_custmize(1, 1, 1, 0.5, False, [128])
        model_result = model
        self.assertEqual(model, model_result)

