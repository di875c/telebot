import requests, datetime
from decimal import Decimal
from tgbot.models import Currency
from bs4 import BeautifulSoup


class Converter:
    # def __init__(self, date):
    #     self.soup = soup

    def cb_request(self, date):
        if date in Currency.objects.find_all()('date'): return Currency.objects.get(date=date).soup
        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': date})
        soup = BeautifulSoup(response.content, "xml")
        xml = Currency()
        xml.date = date
        xml.soup = soup
        xml.save()
        return soup

    @classmethod
    def currency_extract(cls, curr, date):
        soup = cls.cb_request(date)
        for data in soup.find_all('CharCode'):
            if data.text == curr:
                data_cur = data.parent
                val_cur= Decimal(data_cur.find('Value').text.replace(',', '.'))
                num_cur = Decimal(data_cur.find('Nominal').text.replace(',', '.'))
        return val_cur/num_cur

    def calculate(self, amount, cur_from, cur_to, date):
        if cur_from == 'RUR': val_from = Decimal(1)
        else: val_from = self.currency_extract(cur_from)
        if cur_to == 'RUR': val_to = Decimal(1)
        else: val_to = self.currency_extract(self.soup, cur_to)
        return Decimal(Decimal(amount) * val_from / val_to).quantize(
            Decimal("1.0000"))


def rate_currency(currency, date=datetime.datetime.today().strftime("%d/%m/%Y")):
    return Converter.currency_extract(currency, date)


def convert(text_input):
    try:
        list_input = ['amount', 'cur_from', 'cur_to', 'date']
        dict_input = {}
        for idx, val in enumerate(text_input.split()[1::]):
            dict_input[list_input[idx]] = val.upper()
        for val in ['cur_from', 'cur_to']:
            if val not in dict_input.keys(): dict_input[val] = 'RUR'
        if 'date' not in dict_input.keys():
            dict_input['date'] = datetime.datetime.today().strftime("%d/%m/%Y")
        result = Converter(dict_input['date'])
        return result.calculate(*list(dict_input.values()))
    except:
        return None
