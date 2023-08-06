import base64
import hashlib
import hmac
import json
import binascii
import requests

from urllib import parse

class MoneyMadeConnect:
  __urls = {
    "PRODUCTION_FINISH_OAUTH_URL_V1": 'https://connect.moneymade.io/connect/oauth',
    "PRODUCTION_PUSH_ACCOUNTS_API_V1": 'https://connect.moneymade.io/connect/balance',

    "DEVELOPMENT_FINISH_OAUTH_URL_V1": 'https://development.connect.moneymade.io/connect/oauth',
    "DEVELOPMENT_PUSH_ACCOUNTS_API_V1": 'https://development.connect.moneymade.io/connect/balance',

    "DEVELOPMENT_PUSH_ACCOUNTS_API_V2": 'https://stage-connect-oauth.moneymade.io/api/v1/data/accounts',
    "DEVELOPMENT_FINISH_OAUTH_URL_V2": 'https://stage-connect-oauth.moneymade.io/api/v1/oauth/finish',

    "PRODUCTION_FINISH_OAUTH_URL_V2": 'https://stage-connect-oauth.moneymade.io/api/v1/oauth/finish',
    "PRODUCTION_PUSH_ACCOUNTS_API_V2": 'https://stage-connect-oauth.moneymade.io/api/v1/data/accounts',
  
    "PRODUCTION_FINISH_REDIRECT_URL_V2": "https://stage-connect-oauth.moneymade.io/api/v1/oauth/finish/callback",
    "DEVELOPMENT_FINISH_REDIRECT_URL_V2": "https://stage-connect-oauth.moneymade.io/api/v1/oauth/finish/callback",
  }
  
  __versions = ['v1', 'v2']
  
  def __init__(self,
              public_key, 
              private_key,
              env = 'development',
              version = 'v1',
              data_strategy = 'pushing'
              ):
    """
      MoneyMadeConnect SDK constuctor.
      It implements features for: https://docs.moneymade.io/docs/interaction/connect-flow
      Arguments:
          public_key(str): moneymade aouth api public key
          private_key(str): moneymade aouth api private_key
          env(str): environment, possible values are 'development' or 'production', default = development
          version(str): moneymade oauth api version, currently exists v1 and v2, default = v1
          data_strategy(str): string equals to pushing or pulling.
            Represents data interchage strategy (https://docs.moneymade.io/docs/get-started/get-started#data-interchange-strategies)
      Returns:
         MoneyMadeConnect class instance
    """
    if public_key == '' or public_key is None:
      raise ValueError('Argument public_key is required!')

    if private_key == '' or private_key is None:
      raise ValueError('Argument private_key is required!')

    if not (env == 'development' or env == 'production'):
      raise ValueError('Argument env should equal to "production" or "development"')

    if version not in self.__versions:
      values = ' ,'.join(self.__versions)
      raise ValueError('Argument version should be one value in "{}"'.format(values))

    self.__env = env
    self.__version = version
    self.__public_key = public_key
    self.__private_key = private_key
    self.__data_strategy = data_strategy
    
    _version = version.upper()
    _env = env.upper()

    accounts_url_key = '{}_PUSH_ACCOUNTS_API_{}'.format(_env, _version)
    finish_oauth_url_key = '{}_FINISH_OAUTH_URL_{}'.format(_env, _version)
    oauth_redirect_url_key = '{}_FINISH_OAUTH_URL_{}'.format(_env, _version)

    self.__PUSH_ACCOUNTS_API_URL = self.__urls[accounts_url_key]
    self.__FINISH_OAUTH_URL = self.__urls[finish_oauth_url_key]
    self.__FINISH_REDIRECT_URL_V2 = self.__urls[_env + '_FINISH_REDIRECT_URL_V2']
    
  def push_accounts(self, accounts_payload_dict):
    """
      Push user accounts to moneymade-oauth API.
      See full docs here: 
      Arguments:
          accounts_payload_dict(dict): dict implements interface was set up in moneymade dashboard
    """
    
    headers = {
      "api-key": self.__public_key,
      "request-signature": self.generate_signature(accounts_payload_dict),
      "content-type": 'application/json'
    }
    
    response = requests.post(self.__PUSH_ACCOUNTS_API_URL,
                  headers=headers,
                  data=json.dumps(accounts_payload_dict)
                  )
            
    if response.status_code != 200:
      json_res = response.json()
      message = json_res['message']
      
      raise requests.exceptions.HTTPError(message)
     
  def finish_oauth_request(self, oauth_signature, oauth_payload_dict):
    """
      Finish oauth request handshake.
      See full docs here: https://docs.moneymade.io/docs/interaction/connect-flow#finish-oauth-request
      Arguments:
          oauth_signature(str): oauth_signature you got on fronted oauth url (https://docs.moneymade.io/docs/interaction/connect-flow#oauth-page)
          oauth_payload_dict(dict): Payload contains connected userId. 
            Optionally it might contain accessToken if selected pulling data interchange strategy (https://docs.moneymade.io/docs/interaction/connect-flow#oauth-page)
            For pushing data interchage strategy is should contain accounts field with accounts payload you set up in the dahboard.
    """
    payload_dict = oauth_payload_dict.copy()

    if type(oauth_signature) is not str:
      raise ValueError("Parameter oauth_signature should be a string!")

    try:
      payload_dict['userId']
      
      if self.__data_strategy == 'pushing':
        payload_dict['accounts']
    except KeyError as e:
      raise ValueError("Payload dict should have {} key with value".format(str(e)))

    accounts = None
    
    if self.__version == 'v1' and self.__data_strategy == 'pushing':
      accounts = payload_dict['accounts']
      del payload_dict['accounts']
    
    if self.__version == 'v2' and self.__data_strategy == 'pushing':
      payload_dict = {
        "accounts": payload_dict,
      }
      
    headers = {
      "api-key": self.__public_key,
      "oauth-signature": oauth_signature,
      "request-signature": self.generate_signature(payload_dict),
      "content-type": 'application/json'
    }
    
    response = requests.post(self.__FINISH_OAUTH_URL,
                             data=json.dumps(payload_dict),
                             headers=headers
                            )
    
    if response.status_code != 200:
      json_res = response.json()
      message = json_res['message']
      
      raise requests.exceptions.HTTPError(message)
    
    if self.__version == 'v1' and accounts is not None:
      self.push_accounts(accounts)
            
  def base64_to_dict(self, base64_payload):
    """
      Transform base64 string to dict.
      Arguments:
          base64_payload(str): base64 encoded payload
      Returns:
        dict with parsed keys
    """
    
    try:
      decoded = base64.b64decode(base64_payload)
      decoded = decoded.decode("UTF-8")
      
      return json.loads(decoded)
    except Exception as e:
      raise ValueError("Can't decode base64 to dict: " + str(e))
  
  def js_encode_float(self, float_str):
    float_value = float(float_str)
    
    if float_value % 1 == 0:
      return int(float_value)
    
    return float(float_value)
  
  def get_finish_oauth_redirect_url(self, oauth_signature):
    return '{}?oauth-signature={}'.format(self.__FINISH_REDIRECT_URL_V2,
                                          oauth_signature
                                        )

  
  def dict_to_js_json(self, dict_var):
    """
      Dump dict to json.
      Arguments:
          dict_var(dict): Dict variable to be transformed
      Returns:
        json string 
    """
    dumped = json.dumps(dict_var)
    loaded = json.loads(dumped, parse_float=self.js_encode_float)
    
    return json.dumps(loaded, separators=(',', ':'))

  def dict_to_base64(self, dict_payload):
    """
    Transform dict to base64 string.
    Arguments:
        dict_payload(dict): dict contains some keys  
    Returns:
        base64 encoded string
    """

    if type(dict_payload) is not dict:
      raise ValueError('dict_payload must be dict!')

    json_string_payload = self.dict_to_js_json(dict_payload)
    
    payload_bytes = json_string_payload.encode("ascii")
    base64_bytes = base64.b64encode(payload_bytes)
    base64_payload = base64_bytes.decode("ascii")
    
    return base64_payload

  def generate_signature(self, dict_payload):
    """
    Generate request signature for provided dict payload.
    Arguments:
        dict_payload(dict): dict contains parameters for request  
    Returns:
        signature string
    """
   
    base64_payload = self.dict_to_base64(dict_payload)
    signature_body = bytes(
            "{}{}{}".format(
                self.__public_key,
                base64_payload,
                self.__public_key,
            ),
            "UTF-8",
        )
    
    generated_signature = hmac.new(
        bytes(self.__private_key, "UTF-8"),
        signature_body,
        hashlib.sha256,
    ).hexdigest()
    
    return generated_signature
  
  def query_string_to_dict(self, query_string):
    """
    Parse http query string and converts it to dict.
    Method throws ValueError if query_string argument doesn't contain payalod or signature
    Arguments:
        query_string(str): Http query string like payload=asad&signature=12s 
    Returns:
        dict with keys (payload and signature are required)
    """
    
    params = parse.parse_qs(query_string)
  
    try:
      params['signature']
      params['payload']
    except KeyError as e:
      raise ValueError('Query string should contain {} key'.format(str(e)))
    
    params['signature'] = params['signature'][0] 
    params['payload'] = params['payload'][0]
    
    return params
