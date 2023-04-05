import unittest
from unittest.mock import Mock, patch

import requests

from umedsmsclient.fire_text_api_client import FireTextApiClient, InvalidCredentialsException, FireTextException, \
    SmsFailedException


class TestFireTextApiClient(unittest.TestCase):

    def setUp(self):
        self.api_key = "dgNnIiH0K9XvSfO7BbMctE4jwLQ2z6U"
        self.username = "USERNAME"
        self.password = "PASSWORD"
        self.sender = "uMedTeam"
        self.receiver = "07123456789"
        self.message = "Test text message"
        self.scheduled_time = "2023-05-01 00:00"

    def test_init_with_valid_api_key(self):
        client = FireTextApiClient(api_key=self.api_key)
        self.assertEqual(client.api_key, self.api_key)
        self.assertEqual(client.base_url, "https://www.firetext.co.uk/api")

    def test_init_with_valid_username_and_password(self):
        client = FireTextApiClient(username=self.username, password=self.password)
        self.assertEqual(client.username, self.username)
        self.assertEqual(client.password, self.password)
        self.assertEqual(client.base_url, "https://www.firetext.co.uk/api")

    def test_init_with_none_or_empty_api_key(self):
        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient(api_key=None)

        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient(api_key="")

    def test_init_with_none_or_empty_username_and_password(self):
        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient(username=None, password=self.password)

        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient(username=self.username, password=None)

        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient(username="", password=self.password)

        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient(username=self.username, password="")

    def test_init_with_no_credentials(self):
        with self.assertRaises(InvalidCredentialsException):
            FireTextApiClient()

    def test_send_sms_with_valid_input(self):
        client = FireTextApiClient(api_key=self.api_key)
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"code": 0, "description": "SMS successfully queued"}
            mock_post.return_value = mock_response

            client.send_sms(self.sender, self.receiver, self.message, self.scheduled_time)

    def test_send_sms_with_invalid_sender(self):
        client = FireTextApiClient(api_key=self.api_key)
        with self.assertRaises(ValueError):
            client.send_sms("", self.receiver, self.message, self.scheduled_time)

        with self.assertRaises(ValueError):
            client.send_sms("@random{}", self.receiver, self.message, self.scheduled_time)

        with self.assertRaises(ValueError):
            client.send_sms("ra", self.receiver, self.message, self.scheduled_time)

        with self.assertRaises(ValueError):
            client.send_sms("randomlongtext", self.receiver, self.message, self.scheduled_time)

    def test_send_sms_with_invalid_receiver(self):
        client = FireTextApiClient(api_key=self.api_key)
        with self.assertRaises(ValueError):
            client.send_sms(self.sender, "", self.message, self.scheduled_time)

        with self.assertRaises(ValueError):
            client.send_sms(self.sender, "+447123456789", self.message, self.scheduled_time)

        with self.assertRaises(ValueError):
            client.send_sms(self.sender, "44712345678", self.message, self.scheduled_time)

        with self.assertRaises(ValueError):
            client.send_sms(self.sender, "4471234567890", self.message, self.scheduled_time)

    def test_send_sms_with_invalid_message(self):
        client = FireTextApiClient(api_key=self.api_key)
        with self.assertRaises(ValueError):
            client.send_sms(self.sender, self.receiver, "", self.scheduled_time)

    def test_send_sms_with_invalid_scheduled_time(self):
        client = FireTextApiClient(api_key=self.api_key)
        with self.assertRaises(ValueError):
            client.send_sms(self.sender, self.receiver, self.message, "2023/05/01 12:00")

    def test_send_sms_with_invalid_credentials(self):
        client = FireTextApiClient(username="INVALID_USERNAME", password="INVALID_PASSWORD")
        with self.assertRaises(SmsFailedException):
            client.send_sms(self.sender, self.receiver, self.message, self.scheduled_time)

        client_ = FireTextApiClient(api_key="INVALID_API_KEY")
        with self.assertRaises(SmsFailedException):
            client_.send_sms(self.sender, self.receiver, self.message, self.scheduled_time)

    def test_send_sms_with_http_error(self):
        client = FireTextApiClient(api_key=self.api_key)
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=Mock(status_code=403))
            mock_post.return_value = mock_response

            with self.assertRaises(FireTextException):
                client.send_sms(self.sender, self.receiver, self.message, self.scheduled_time)

    def test_send_sms_with_timeout(self):
        client = FireTextApiClient(api_key=self.api_key)
        with patch('requests.post') as mock_post:
            mock_post.side_effect = requests.exceptions.Timeout()

            with self.assertRaises(FireTextException) as e:
                client.send_sms(self.sender, self.receiver, self.message, self.scheduled_time)
            self.assertEqual(str(e.exception), 'Time out exception from Fire Text API')

    def test_send_sms_with_unknown_error(self):
        client = FireTextApiClient(api_key=self.api_key)
        with patch('requests.post') as mock_post:
            mock_post.side_effect = Exception('An unknown error occurred')

            with self.assertRaises(Exception) as e:
                client.send_sms(self.sender, self.receiver, self.message, self.scheduled_time)
            self.assertEqual(str(e.exception), 'An unknown error occurred. exception : An unknown error occurred')