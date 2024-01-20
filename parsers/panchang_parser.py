import requests
import pytz
from bs4 import BeautifulSoup
from datetime import datetime




def current_date():
    desired_timezone = pytz.timezone("Europe/Kiev")
    current_date = datetime.now()
    current_local_time = current_date.replace(tzinfo=pytz.utc).astimezone(desired_timezone)
    formatted_date = current_local_time.strftime("%d/%m/%Y")
    return formatted_date

class panchang_parser:
    def parser_from_city_id(city_id):
        formatted_date = current_date()

        url = f"https://www.drikpanchang.com/panchang/month-panchang.html?geoname-id={city_id}&date={formatted_date}&time-format=24plushour"
        response = requests.get(url)
        res = f"Дата выгрузки: {formatted_date}: \n\n"

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Создаем объект BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # Находим все элементы <div> с классом 'dpPanchang'
            divs = soup.find_all('div', class_='dpPanchang')

            # Проходим по найденным div'ам
            for div in divs:
                # Находим все элементы <p> с классом 'dpElement'
                paragraphs = div.find_all('p', class_='dpElement')

                # Проходим по найденным параграфам
                for paragraph in paragraphs:
                    # Находим элементы <span> с классами 'dpElementKey' и 'dpElementValue'
                    key_span = paragraph.find('span', class_='dpElementKey')
                    value_span = paragraph.find('span', class_='dpElementValue')

                    # Выводим значения
                    if key_span and value_span:
                        res += f"{key_span.text}: {value_span.text} \n"
        else:
            res = f"Ошибка запроса: {response.status_code}"

        return res
