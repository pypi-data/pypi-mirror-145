import json
import unittest
import moneymade_connect

from unittest.mock import Mock, patch

public_key = 'publicKey'
private_key = 'privateKey'

base64_payload = 'eyJ1c2VySWQiOiJhYmNkZWYtYWJjZGVmLWFiY2RlZi1hYmNkZWYtYWJjZGVmIiwiYWNjb3VudHMiOlt7ImlkIjoyLCJuYW1lIjoiUmVwYWlkIiwiYW1vdW50IjoxMDAwfV19'
signature = 'a604c5d3610dd5e3bf0548c26c75587b92fea1573a6d0921c7969b0913f7771b'
finish_oauth_request_signature = 'fa595194c0ba6526dcb2c4063d959cb3b7ed0d8848c7f40ddc491ff3a35805b1'

dict_payload = {
    "userId": "abcdef-abcdef-abcdef-abcdef-abcdef",
    "accounts": [
        {"id": 2, "name": "Repaid", "amount": 1000.0},
    ],
}

query_string = 'signature={}&payload={}'.format(signature, base64_payload)

params_dict = {
  "signature": signature,
  "payload": base64_payload 
}

class TestMoneyMadeConnect(unittest.TestCase):
  sdk = moneymade_connect.MoneyMadeConnect(public_key, private_key)

  def test_init(self):
    self.assertRaises(TypeError, moneymade_connect.MoneyMadeConnect)
    self.assertRaises(ValueError, moneymade_connect.MoneyMadeConnect, '', '')
    
    with self.assertRaises(ValueError):
      moneymade_connect.MoneyMadeConnect(None, None)

  def test_base64_to_dict(self):
    with self.assertRaises(ValueError):
      self.sdk.base64_to_dict('base64_payload')

    decoded_dict = self.sdk.base64_to_dict(base64_payload)
    self.assertDictEqual(decoded_dict, dict_payload)
    
  def test_dict_to_js_json(self):
    self.assertEqual(self.sdk.dict_to_js_json({ "test": 1.0 }), '{"test":1}')
    self.assertEqual(self.sdk.dict_to_js_json({ "test": 1.1 }), '{"test":1.1}')

  def test_dict_to_base64(self):
    with self.assertRaises(ValueError):
      self.sdk.dict_to_base64('string')
    
    self.assertEqual(self.sdk.dict_to_base64(dict_payload), base64_payload)
  
  def test_generate_signature(self):
    self.assertEqual(self.sdk.generate_signature(dict_payload), signature)
  
  def test_query_string_to_dict(self):
    self.assertDictEqual(self.sdk.query_string_to_dict(query_string), params_dict)

    with self.assertRaises(ValueError):
      self.sdk.query_string_to_dict('payload=123')
      self.sdk.query_string_to_dict('signature=123')
  
  def test_finish_oauth_request(self):
    with self.assertRaises(ValueError):
      self.sdk.finish_oauth_request('some-signature', {})
      
    try:
      with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        
        self.sdk.finish_oauth_request('', { "userId": '1', "accounts": {} })
    except ValueError:
      self.failed('Method finish_oauth_request raised error for right payload_dict parameter')
    
    with patch('requests.post') as mock_post:
      mock_post.return_value.status_code = 200
      
      oauth_sig = '123'
    
      payload = {
        "userId": dict_payload['userId'],
        "accounts": dict_payload
      }

      self.sdk.finish_oauth_request(oauth_sig, payload)
    
      oauth_call_kwargs = mock_post.call_args_list[0].kwargs
      balances_call_kwargs = mock_post.call_args_list[1].kwargs

      oauth_headers = {
        'api-key': public_key,
        "content-type": 'application/json',
        "request-signature": finish_oauth_request_signature,
        "oauth-signature": oauth_sig
      }
      
      balances_headers = {
        'api-key': public_key,
        "content-type": 'application/json',
        "request-signature": signature,        
      }
      
      oauth_request_data = {
        "userId": dict_payload["userId"]
      }
      
      self.assertDictEqual(oauth_call_kwargs['headers'], oauth_headers)
      self.assertEqual(oauth_call_kwargs['data'], json.dumps(oauth_request_data))
      
      self.assertDictEqual(balances_call_kwargs['headers'], balances_headers)
      self.assertEqual(balances_call_kwargs['data'], json.dumps(dict_payload))
      
  def test_get_finish_oauth_redirect_url(self):
    url = self.sdk.get_finish_oauth_redirect_url('123')
    self.assertEqual(url, 'https://stage-connect-oauth.moneymade.io/api/v1/oauth/finish/callback?oauth-signature=123')