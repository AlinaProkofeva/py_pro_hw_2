import csv
import re

'''создаем записную книжку и список дубликатов'''
phonebook = []
duplicates_ids = []

def formatted_phonebook(phonebook_raw):
    '''приводим записи к единому шаблону'''
    with open(phonebook_raw, 'rt', encoding='utf-8') as f:
        lines = csv.reader(f)
        contacts_list = list(lines)

    # задаем паттерны для форматирования
    pattern_1_to_5 = r'([A-Яа-я]+)[, ]([A-Яа-я]+)[, ]([A-Яа-я]+|)[, ]+([А-Яа-я]+|)[, ]+([a-zа-яА-я \–]+|)'
    pattern_phone = r'[7|8]{1}[ ]?\(?(\d{3})[ \)-]?[ ]?(\d{3})[-]?(\d{2})[-]?(\d{2})'
    pattern_phone_2 = r'[доб. ]+(\d{4})'
    pattern_email = r'[A-Za-z.0-9]+[@][a-z.]+'

    for id, line in enumerate(contacts_list): # отрабатываем каждую строку
        if id == 0:
            phonebook.append(line)
            continue
        else:
            text = (',').join(line)
            phonebook_line = [] # создаем список для каждой записи
            phonebook_line.append(re.search(pattern_1_to_5, text).group(1))
            phonebook_line.append(re.search(pattern_1_to_5, text).group(2))
            phonebook_line.append(re.search(pattern_1_to_5, text).group(3))
            phonebook_line.append(re.search(pattern_1_to_5, text).group(4))
            phonebook_line.append(re.search(pattern_1_to_5, text).group(5))

            raw_phone = re.search(pattern_phone, text) # проверяем наличие номера и записываем тедефон
            raw_phone_2 = re.search(pattern_phone_2, text)
            if raw_phone is not None and raw_phone_2 is None:
                final_phone = f'+7({raw_phone.group(1)}){raw_phone.group(2)}-{raw_phone.group(3)}-{raw_phone.group(4)}'
            elif raw_phone is not None and raw_phone_2 is not None:
                final_phone = (f'+7({raw_phone.group(1)}){raw_phone.group(2)}-{raw_phone.group(3)}-'
                               f'{raw_phone.group(4)} доб.{raw_phone_2.group(1)}')
            else:
                final_phone = ''
            phonebook_line.append(final_phone)

            mail = re.search(pattern_email, text) # проверяем наличие почты и записываем почту
            if mail is not None:
                phonebook_line.append(re.search(pattern_email, text).group(0))
            else:
                phonebook_line.append('')

            # проверяем по ФИО на дубликат, обновляем основную запись и записываем id ненужного дубля
            for el in phonebook:
                if phonebook_line[0] and phonebook_line[1] in el:
                    duplicates_ids.append(int(id))
                    for i in range(3,7):
                        el[i] = el[i]+phonebook_line[i]

        phonebook.append(phonebook_line)
    for i in reversed(duplicates_ids): # удаляем дубликаты
        del (phonebook[i])


def write_phonebook(formatted_phonebook):
    '''записываем отформатированную записную книжку'''
    with open(formatted_phonebook, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=';')
        datawriter.writerows(phonebook)


if __name__ == '__main__':
    formatted_phonebook('phonebook_raw.csv')
    write_phonebook("phonebook.csv")














