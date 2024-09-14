import csv
from datetime import datetime


def reading_lines_from_file(file_name, messages):
    with open(file_name, 'r', encoding='utf-8') as file:
        print(messages['got_file_msg'])
        for line in file:
            yield line


def reading_keys_from_file(file_name, headers, messages):
    parts_and_tails = {}
    new_header_flag = True
    incorrect_header_flag = True
    header = ''
    temp_list = []

    for line in reading_lines_from_file(file_name, messages):
        # skipping empty strings and comments
        if any((line in ('', '\n'),
                line[0] == '#',
                )):
            continue

        elif line[0] == '[':
            # getting the first header
            if new_header_flag:
                header = line.rstrip('\n')
                # header verification
                if header in headers:
                    new_header_flag = False
                    incorrect_header_flag = False

            else:
                # dumping the current list and getting next header
                parts_and_tails[header] = temp_list
                temp_list = []
                header = line.rstrip('\n')
                # header verification
                if header not in headers:
                    incorrect_header_flag = True

        # adding new key to the current list
        else:
            if incorrect_header_flag:
                continue
            else:
                temp_list.append(line.rstrip('\n'))

    # dumping the current list when the file ends
    if not incorrect_header_flag:
        parts_and_tails[header] = temp_list

    return parts_and_tails


def is_not_valid(sample, headers, messages):
    correct_header_flag = False

    # if there's at least one list with the correct name and it is not empty
    for header in headers:
        if header in sample:
            correct_header_flag = True
            if sample[header]:
                return False

    # if there are a few lists with the correct names, but each of them is empty
    if correct_header_flag:
        print(messages['empty_lists_msg'])
    # if there's no any lists with the correct name
    else:
        print(messages['no_headers_msg'])

    return True


def printing_received_headers(sample, messages):
    print(messages['rcvd_headers_msg'])
    for item in sample:
        if not sample[item]:
            print(item, messages['no_keys_msg'])
        else:
            print(item)


def checking_bad_keys(sample, messages):
    bad_keys = ('.', '/', 'com', 'ru', 'net', 'gov', 'api', 'http', 'www')
    temp_dct = {}
    temp_lst = []

    for item in sample:
        if not sample[item]:
            continue
        else:
            temp_lst = [key for key in bad_keys if key in sample[item]]
            if temp_lst:
                temp_dct[item] = temp_lst
                temp_lst = []

    if temp_dct:
        print(messages['bad_keys_msg'])
        for element in temp_dct:
            print(element, '\n'.join(temp_dct[element]), sep='\n')


def is_able_to_use(filtration_keys, title):
    try:
        if filtration_keys[title]:
            return True
    except KeyError:
        return False


def is_not_interesting_dct(row, filtration_keys, headers):
    url = row['url']

    # checking if filtration_keys contains [not_interesting_parts] list and it isn't empty
    if is_able_to_use(filtration_keys, headers[0]):
        parts = filtration_keys[headers[0]]
        for part in parts:
            if part in url:
                return True

    # checking if filtration_keys contains [not_interesting_tails] list and it isn't empty
    if is_able_to_use(filtration_keys, headers[1]):
        tails = filtration_keys[headers[1]]
        for tail in tails:
            if url.endswith(tail):
                return True

    return False


def is_interesting_dct(row, filtration_keys, headers):
    url = row['url']

    # checking if filtration_keys contains [interesting_parts] list and it isn't empty
    if is_able_to_use(filtration_keys, headers[2]):
        parts = filtration_keys[headers[2]]
        for part in parts:
            if part in url:
                return True

    # checking if filtration_keys contains [interesting_tails] list and it isn't empty
    if is_able_to_use(filtration_keys, headers[3]):
        tails = filtration_keys[headers[3]]
        for tail in tails:
            if url.endswith(tail):
                return True

    return False


def cutting_off_unimportant(row):
    temp_dt = datetime.strptime(row['@timestamp'], '%b %d, %Y @ %H:%M:%S.000')
    new_row = {'date': temp_dt.strftime('%Y %m %d'),
               'time': temp_dt.strftime('%H:%M:%S'),
               'url': row['url'],
               }
    return new_row


def reading_urls_from_dump(file_name, messages):
    with open(file_name, 'r', encoding='utf-8') as file:
        print(messages['got_file_msg'])
        rows = csv.DictReader(file, quotechar='"')

        # checking if file contains all required fields
        for field in ('@timestamp', 'url'):
            if field not in rows.fieldnames:
                raise KeyError

        yield from rows


def filtering_urls_dump(file_name, filtration_keys, headers, messages):
    interesting_lst = []
    suspicious_lst = []

    for row in reading_urls_from_dump(file_name, messages):
        if is_not_interesting_dct(row, filtration_keys, headers):
            continue
        else:
            if is_interesting_dct(row, filtration_keys, headers):
                interesting_lst.append(row)
            else:
                suspicious_lst.append(row)

    # there's no need to carry all information from the dump. Just date, time and URL are important
    interesting_lst = list(map(cutting_off_unimportant, interesting_lst))
    suspicious_lst = list(map(cutting_off_unimportant, suspicious_lst))

    return interesting_lst, suspicious_lst


def writing_to_file(sample_lst, file_name, messages):
    columns = ['date', 'time', 'url']
    try:
        with open(file_name, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(sample_lst)
        print(file_name, messages['file_saved_msg'])

    except OSError:
        print(messages['os_error_msg'])

    except Exception as err:
        print(messages['error_msg'])
        print(err)


def main():
    headers = ('[not_interesting_parts]',
               '[not_interesting_tails]',
               '[interesting_parts]',
               '[interesting_tails]',
               )

    messages = {'input_keys_msg': 'Пожалуйста, введите имя файлa с ключами фильтрации: ',
                'input_dump_msg': 'Пожалуйста, введите имя файлa с выгрузкой посещенных сайтов: ',
                'not_found_msg': 'Файл с таким именем не найден. Попробуйте снова',
                'os_error_msg': 'Не удается открыть или записать файл. Попробуйте снова',
                'utf_8_error_msg': 'Не удается прочесть файл. В файле должна использоваться именно кодировка utf-8. Либо Вы могли указать неверный файл',
                'error_msg': 'Ошибка. Убедитесь, что Вы пытаетесь открыть файл, соответствующий требованиям в описании. Либо не удается сохранить результаты фильтрации в файл. Подробнее об ошибке:',
                'got_file_msg': 'Файл открыт',
                'no_headers_msg': 'Указанный Вами файл не содержит хотя бы одно из необходимых названий списков ключей фильтрации. Либо их названия отличаются от перечисленных выше.',
                'empty_lists_msg': 'В указанном Вами файле имеются необходимые названия списков, но все они не содержат ключи фильтрации (пустые)',
                'rcvd_headers_msg': 'Прочитаны следующие списки ключей фильтрации:',
                'no_keys_msg': 'Данный список не содержит ключей фильтрации (пустой)',
                'bad_keys_msg': 'Указанные ниже списки содержат ключи вида ".", "com", "ru", которые могут существенно снизить качество фильтрации. Рекомендуется внести соответствующие корректировки',
                'no_fields_msg': 'Проверьте файл выгрузки посещенных сайтов. Либо Вы открыли не тот файл, либо в нём отсутствуют все необходимые заголовки: @timestamp и url',
                'no_interesting_urls_msg': 'Интересующие Вас ссылки не выявлены. Файл с названием вида aspushkin_02_interesting.csv не был сохранен',
                'no_suspicious_urls_msg': '"Подозрительные" ссылки не выявлены. Файл с названием вида aspushkin_02_suspicious.csv не был сохранен',
                'file_saved_msg': 'Файл сохранен',
                'final_msg': 'Работа с указанными Вами файлами завершена',
                }

    filtration_keys = {}
    interesting_links = []
    suspicious_links = []
    url_dump_name = ''
    filtering_finished_flag = False

    while not filtration_keys:
        file_name = input(messages['input_keys_msg'])
        try:
            filtration_keys = reading_keys_from_file(file_name, headers, messages)
        except FileNotFoundError:
            print(messages['not_found_msg'])
            continue

        except OSError:
            print(messages['os_error_msg'])
            continue

        except UnicodeDecodeError:
            print(messages['utf_8_error_msg'])
            continue

        except Exception as err:
            print(messages['error_msg'])
            print(err)
            continue

        if is_not_valid(filtration_keys, headers, messages):
            filtration_keys = {}

    printing_received_headers(filtration_keys, messages)

    checking_bad_keys(filtration_keys, messages)

    while not filtering_finished_flag:
        url_dump_name = input(messages['input_dump_msg'])
        try:
            interesting_links, suspicious_links = filtering_urls_dump(url_dump_name, filtration_keys, headers, messages)
            filtering_finished_flag = True
        except FileNotFoundError:
            print(messages['not_found_msg'])

        except OSError:
            print(messages['os_error_msg'])

        except UnicodeDecodeError:
            print(messages['utf_8_error_msg'])

        except KeyError:
            print(messages['no_fields_msg'])

        except Exception as err:
            print(messages['error_msg'])
            print(err)

    if interesting_links:
        i_url_fn = url_dump_name.replace('.csv', '_interesting.csv')
        writing_to_file(interesting_links, i_url_fn, messages)
    else:
        print(messages['no_interesting_urls_msg'])

    if suspicious_links:
        s_url_fn = url_dump_name.replace('.csv', '_suspicious.csv')
        writing_to_file(suspicious_links, s_url_fn, messages)
    else:
        print(messages['no_suspicious_urls_msg'])

    print(messages['final_msg'])


info = '''
Скрипт фильтрует выгрузку посещенных работниками сайтов в сети Интернет.
Коллеги предоставляют выгрузку в файлах формата .csv с кодировкой utf-8, данные в которых имеют заголовки.
Фильтрация проводится по спискам ключей, которые необходимо указать в файле формата .txt с кодировкой utf-8.
Это позволяет:
- исключить те ссылки, которые Вас точно НЕ интересуют;
- собрать в отдельный файл ссылки, которые Вас интересуют;
- собрать в отдельный файл ссылки, которые не соответствуют первым двум пунктам и являются "подозрительными".

ВАЖНО! Названия списков ключей должны строго соответствовать перечисленным ниже, включая квадратные скобки:
[not_interesting_parts]
[not_interesting_tails]
[interesting_parts]
[interesting_tails]

Все файлы должны находиться в одной папке. Названия файла выгрузки и файла с ключами фильтрации необходимо указывать полностью, а длина названий не должна превышать 25 символов. Например:
keys.txt
aspushkin_02.csv

Результаты работы скрипта (дата, время, ссылка) сохраняются в файлы формата .csv с кодировкой utf-8 и названиями вида:
aspushkin_02_interesting.csv - для ссылок, которые Вас интересуют; 
aspushkin_02_suspicious.csv - для "подозрительных" ссылок.
ВАЖНО! Если файл с таким названием уже существует, то он будет полностью перезаписан без каких-либо предупреждений!
'''

if __name__ == '__main__':
    print(info)

    while True:
        main()
