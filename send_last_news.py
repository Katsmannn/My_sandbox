import os
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import telegram as tl


load_dotenv()
# Токен телеграм-бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# Чат, в который отправляется сообщение
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# URL, с которого получаем данные
URL = 'https://vc.ru/new'
# Параметры TELEGRAM_TOKEN, TELEGRAM_CHAT_ID указываются в файле .env


def send_message(bot, message):
    '''
    Отправляет сообщение message от телеграм-бота bot в чат
    TELEGRAM_CHAT_ID.
    '''
    return bot.send_message(TELEGRAM_CHAT_ID, message)


def get_text_from_tag(last_news_tag, tag, attrs=None):
    '''
    Ищет тэг tag с атрибутами attrs внутри тэга last_news_tag
    и возвращает его содержимое. Если тэг не найден, возвращает
    пустую строку.
    '''
    text_tags = last_news_tag.find(
        'div',
        attrs={'class': 'content-container'}
    ).find_all(tag, attrs=attrs)
    result = ''
    if text_tags != []:
        for tag in text_tags:
            result += tag.get_text().strip() + '\n'
    return result


def get_content_link(last_news_tag, tag, attrs=None):
    '''
    Ищет тэг tag с атрибутами attrs внутри тэга last_news_tag
    и возвращает URL из его атрибутов. Если тэг не найден, возвращает
    пустую строку.
    '''
    link_tag = last_news_tag.find(tag, attrs=attrs)
    if link_tag:
        return link_tag.get('href')
    return ''


if __name__ == '__main__':

    def main():
        '''
        Получает последнюю новость с сайта vc.ru и отправляет
        её в телеграм-чат.
        '''
        try:
            bot = tl.Bot(token=TELEGRAM_TOKEN)
            response = requests.get(URL)
            soup = BeautifulSoup(response.content, features='html.parser')
            last_news_tag = soup.find(
                'div',
                attrs={'data-gtm': 'Feed — Item 1 — Click'}
            )
            title = get_text_from_tag(
                last_news_tag=last_news_tag,
                tag='div',
                attrs={
                    'class': 'content-title content-title--short l-island-a'
                }
            )
            description = get_text_from_tag(
                last_news_tag=last_news_tag,
                tag='div',
                attrs={'class': 'block-quote__text'}
            )
            content = get_text_from_tag(
                last_news_tag=last_news_tag,
                tag='div',
                attrs={'class': 'l-island-a'}
            )
            content_link = get_content_link(
                last_news_tag=last_news_tag,
                tag='a',
                attrs={'class': 'content-link'}
            )
            message = (
                'Последняя новость на сайте vc.ru' + '\n'
                + title + '\n'
                + description + '\n'
                + content + '\n\n'
                + 'Подробности по ссылке:' + '\n'
                + content_link
            )
            send_message(bot, message)
        except Exception as e:
            send_message(bot, f'Не удалось получить данные. Ошибка {e}.')

    main()
