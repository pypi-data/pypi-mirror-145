from typing import List
from comgate.enum.PaymentMethodCodeEnum import PaymentMethodCodeEnum
from comgate.enum.CountryCodeEnum import CountryCodeEnum
from comgate.enum.CurrencyCodeEnum import CurrencyCodeEnum
from comgate.enum.LanguageCodeEnum import LanguageCodeEnum


class Payment:
    def __init__(self,
                 price: int,
                 curr: CurrencyCodeEnum,
                 label: str,
                 ref_id: str,
                 email: str,
                 prepare_only: bool,
                 payer_id: str = None,
                 account: str = None,
                 phone: str = None,
                 name: str = None,
                 lang: LanguageCodeEnum = LanguageCodeEnum.CS,
                 pre_auth: bool = None,
                 init_recurring: bool = None,
                 verification: bool = None,
                 embedded: bool = None,
                 eet_report: bool = None,
                 eet_data: dict = None,
                 included_methods: List[PaymentMethodCodeEnum] = None,
                 excluded_methods: List[PaymentMethodCodeEnum] = None,
                 country: CountryCodeEnum=CountryCodeEnum.ALL):
        self.price = price
        self.curr = curr
        self.label = label
        self.ref_id = ref_id
        self.email = email
        self.payer_id = payer_id
        self.account = account
        self.phone = phone
        self.name = name
        self.lang = lang
        self.prepare_only = prepare_only
        self.pre_auth = pre_auth
        self.init_recurring = init_recurring
        self.verification = verification
        self.embedded = embedded
        self.eet_report = eet_report
        self.eet_data = eet_data
        self.included_methods = included_methods
        self.excluded_methods = excluded_methods
        self.country = country

        self.method = '+'.join([i.value for i in included_methods])
        if excluded_methods:
            self.method += '-' + '-'.join([e.value for e in excluded_methods])

    def to_dict(self):
        return {
            'price': self.price,
            'curr': self.curr.value,
            'label': self.label,
            'refId': str(self.ref_id),
            'method': self.method,
            'country': self.country.value,
            'lang': self.lang.value,
            'email': self.email,
            'prepareOnly': 'true' if self.prepare_only else 'false',
        }
