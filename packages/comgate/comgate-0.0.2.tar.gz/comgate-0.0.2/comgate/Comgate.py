import requests
from comgate.http.HttpClient import HttpClient
from comgate.model.Payment import Payment
from comgate.enum.CountryCodeEnum import CountryCodeEnum
from comgate.enum.CurrencyCodeEnum import CurrencyCodeEnum
from comgate.enum.LanguageCodeEnum import LanguageCodeEnum


class Comgate:
    def __init__(self, merchant: str, secret: str, is_test: bool = True, api_gateway: str = 'https://payments.comgate.cz/v1.0/'):
        self.merchant = merchant
        self.secret = secret
        self.is_test = is_test
        self.api_gateway = api_gateway

        self.session = requests.Session()

        base_data = {
            'merchant': self.merchant,
            'secret': self.secret,
            'test': 'true' if self.is_test else 'false'
        }
        self.http_client = HttpClient(self.session, base_data=base_data, base_url=self.api_gateway)

    def create(self, payment: Payment):
        return self.http_client.post('create', payment.to_dict())

    def get_status(self, trans_id: str):
        return self.http_client.get('status', {'transId': trans_id})

    def get_payment_methods(self,
                            lang: LanguageCodeEnum = LanguageCodeEnum.CS,
                            curr: CurrencyCodeEnum = CurrencyCodeEnum.CZK,
                            country: CountryCodeEnum = CountryCodeEnum.CZ
                            ):

        if country == CountryCodeEnum.ALL:
            raise Exception('Country must be specified, cannot use ALL')

        data = {
            'type': 'json',
            'lang': lang.value,
            'curr': curr.value,
            'country': country.value,
        }
        return self.http_client.get('methods', data)

    def refund(self, trans_id: str, amount: str, curr: CurrencyCodeEnum = CurrencyCodeEnum.CZK, ref_id: str = None):
        data = {
            'transId': trans_id,
            'amount': amount,
            'curr': curr
        }

        if ref_id:
            data['refId'] = ref_id

        return self.http_client.post('refund', data)
