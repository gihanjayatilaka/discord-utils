# Run like python extract.py path-to-discord-log.html > log.txt

from bs4 import BeautifulSoup
import lxml
import logging
import sys

logger = logging.getLogger(__name__)

def extract_message(html_file_path):
    with open(html_file_path, 'r') as html_file:
        logger.info('Parsing HTML...')
        html = html_file.read()
        soup = BeautifulSoup(html, 'lxml')
        logger.info('Done!')
        groups = soup.find_all(class_='chatlog__message-group')
        for group in groups:
            author_node = group.find(class_='chatlog__author')
            if author_node is None:
                logger.info('Skipping message group without author...')
                continue
            author = group.find(class_='chatlog__author').text
            date = group.find(class_='chatlog__timestamp').text
            texts = [m.text for m in group.find_all(
                class_='chatlog__markdown-preserve')]
            print(f'{date} [{author}] {" ".join(texts)}')


if __name__ == '__main__':
    # Just log level, YYMMDD:HHMMSS, and message.
    logging.basicConfig(
        format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)
    extract_message(sys.argv[1])
