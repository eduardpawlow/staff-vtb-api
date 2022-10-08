from cmath import log
from django.conf import settings
import requests

class BlockchainService:
  url = settings.BLOCKCHAIN_URL

  def send_coins(self, source_private_key, target_public_key, amount):
    print(source_private_key, target_public_key, amount)

    try:
      r = requests.post(self.url + '/v1/transfers/ruble', {
        "fromPrivateKey": source_private_key,
        "toPublicKey": target_public_key,
        "amount": amount
      })

      if r.status_code == 200:
        return True
      
      return False
    except Exception as err:
      return False
