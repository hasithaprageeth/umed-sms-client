import unittest
from umedsmsclient.fire_text_api_client import InvalidCredentialsException, FireTextException, SmsFailedException


class TestExceptions(unittest.TestCase):
    def test_invalid_credentials_exception(self):
        message = "Invalid API key."
        exception = InvalidCredentialsException(message)
        self.assertEqual(str(exception), message)

    def test_sms_failed_exception(self):
        reason = "Insufficient credit"
        sender = "uMedTeam"
        receiver = "07123456789"
        sms_body = "Test text message"
        scheduled_time = "2023-05-01 00:00"
        exception = SmsFailedException(reason, sender, receiver, sms_body, scheduled_time)
        self.assertEqual(str(exception), "Failed to send the sms.")

    def test_fire_text_exception(self):
        message = "Unsuccessful response received from Fire Text API"
        status_code = 500
        exception = FireTextException(message, status_code)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.status_code, status_code)
        self.assertIsNone(exception.exception)

        original_exception = ConnectionRefusedError("Connection refused.")
        exception = FireTextException(message, status_code, original_exception)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.status_code, status_code)
        self.assertEqual(exception.exception, original_exception)
        self.assertEqual(str(exception), message)
