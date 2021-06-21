from chardet.universaldetector import UniversalDetector
from decimal import getcontext, Decimal
import json
from loguru import logger
import re

import config


getcontext().prec = 8


def recognize_encoding(file: str) -> str:
    detector = UniversalDetector()
    with open(file, 'rb') as data:
        for line in data:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']  # type: ignore


def read_file(file: str, mode: str = 'r') -> str:
    """
    Read file
    """
    encoding = recognize_encoding(file)
    text = ''
    with open(file, mode=mode, encoding=encoding) as data:
        for line in data:
            text += line
    return text


def read_json_config(file: str, mode: str = 'r') -> dict:
    """
    Read json file
    """
    encoding = recognize_encoding(file)
    with open(file, mode=mode, encoding=encoding) as data:
        json_data = json.load(data)
    return json_data


def create_result_file(file_name: str, total, per_hour,
                       mode: str = 'w', encoding='utf-8') -> None:
    """
    Create text and write to file
    """
    logger.debug(f"total {type(total)}")
    logger.debug(f"per_hour {type(per_hour)}")
    text = f"All money = {total}\npayment per hour = {per_hour}"
    with open(file_name, mode=mode, encoding=encoding) as data:
        data.write(text)


def calculation_of_income(json_data, data, bot_level: str) -> int:
    """
    Calculate summ of all item
    """
    total_amount = 0

    for item in json_data:
        matches_name = re.findall(json_data[item]['search_line'], data)

        if matches_name:
            count = matches_name.pop()
            position_volume = Decimal(1 if not count else count)
            total_amount += position_volume * \
                json_data[item]['bot_level'][bot_level] * \
                json_data[item]['price_use_junk_shop']
            """Uncomment the line below to print the sum of each item in console"""
            text = position_volume * \
                json_data[item]['bot_level'][bot_level] * \
                json_data[item]['price_use_junk_shop']
            logger.info(f"{item} {text}")
    return total_amount


def sum_per_hour(text: str, total_amount: Decimal) -> Decimal:
    """
    Сalculates the average rate of return per hour
    """
    """Serch count days"""
    count_days = re.findall(r"\d+(?=д)", text)

    """Serch count hours"""
    count_hours = re.findall(r"\d+(?=ч)", text)
    if not count_days:
        formula = Decimal(count_hours.pop())
        per_hour = total_amount / formula
    else:
        day = Decimal(count_days.pop())
        if count_hours:
            hours = Decimal(count_hours.pop())
            formula = day * 24 + hours
        else:
            formula = 24 * day
        per_hour = total_amount / formula
    return per_hour


def main():
    data = read_file(config.INPUT_FILE)

    total = calculation_of_income(
        read_json_config(config.ITEM), data, config.BOT_LEVEL)
    logger.info(f"total {total}")

    per_hour = sum_per_hour(data, total)
    logger.info(f"per_hour {per_hour}")
    create_result_file(config.OUTPUT_FILE, total, per_hour)


if __name__ == '__main__':
    main()
