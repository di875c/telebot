import requests, datetime
from decimal import Decimal
from tgbot.models import Currency
from bs4 import BeautifulSoup


class Converter:

    def cb_request(self, date):
        if Currency.objects.filter(date_request=date): return BeautifulSoup(Currency.objects.get(date_request=date).xml, "html.parser")
        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': date})
        soup = BeautifulSoup(response.content, "html.parser")
        xml = Currency.objects.create(date_request=date, xml = str(soup))
        return soup

    def currency_extract(self, curr, date):
        soup = self.cb_request(date)
        for data in soup.find_all('charcode'):
            if data.text == curr:
                data_cur = data.parent
                val_cur = Decimal(data_cur.find('value').text.replace(',', '.'))
                num_cur = Decimal(data_cur.find('nominal').text.replace(',', '.'))
        return val_cur/num_cur

    def calculate(self, amount, cur_from, cur_to, date):
        if cur_from == 'RUR': val_from = Decimal(1)
        else: val_from = self.currency_extract(cur_from, date)
        if cur_to == 'RUR': val_to = Decimal(1)
        else: val_to = self.currency_extract(cur_to, date)
        return Decimal(Decimal(amount) * val_from / val_to).quantize(
            Decimal("1.0000"))


def rate_currency(currency, date=None):
    if date==None: date = datetime.datetime.today().strftime("%d/%m/%Y")
    conv=Converter()
    return conv.currency_extract(currency, date)


def convert(text_input):
    try:
        list_input = ['amount', 'cur_from', 'cur_to', 'date']
        dict_input = {}
        for idx, val in enumerate(text_input.split()):
            dict_input[list_input[idx]] = val.upper()
        for val in ['cur_from', 'cur_to']:
            if val not in dict_input.keys(): dict_input[val] = 'RUR'
        if 'date' not in dict_input.keys():
            dict_input['date'] = datetime.datetime.today().strftime("%d/%m/%Y")
        result = Converter()
        return result.calculate(*list(dict_input.values()))
    except:
        return None
