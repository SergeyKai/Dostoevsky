def read_csv(file_name):
    data = {}
    with open(file_name, encoding='utf-16') as file:
        lines = file.readlines()

        headers = lines[0].strip().split('\t')
        data.update({
            'Статья': {
                'Номер': lines[1].strip().split('\t')[1],
                'Название': lines[1].strip().split('\t')[2],
            },
            'Год': {}}
        )

        for line in lines[1:]:
            values = line.strip().split('\t')
            year = int(values[headers.index('Год')])
            data['Год'].update({year: {header: int(values[headers.index(header)]) for header in headers[3:]}})
        return data


def percent_by_metrics(data, first_metric, second_metric, new_metric_name):
    """
    :param data: Датасет
    :param first_metric: Метрика относительно которой будет произведен расчет. Тобишь 100%
    :param second_metric: Метрика для которой производится расчет
    :param new_metric_name: Наиминование поля для результатов рассчета
    :return: dict результат за каждый год в процентном соотношении second_metric от first_metric
    """
    result_data = {}
    for year, metric in data['Год'].items():
        result_data.update(
            {
                year: {new_metric_name: (metric[second_metric] / metric[first_metric]) * 100}
                # year: {new_metric_name: round((metric[second_metric] / metric[first_metric]) * 100, 2)}
            }
        )
    return result_data


dataset1 = read_csv('105ч1.csv')
dataset2 = read_csv('105ч2.csv')

print("Данные из первого датасета:")
print(dataset1)
print("\nДанные из второго датасета:")
print(dataset2)


def max_by_metric(metric, data):
    the_most = 0
    current_year = 0
    for year in data['Год']:
        if data['Год'][year][metric] > the_most:
            the_most = data['Год'][year][metric]
            current_year = year
    return current_year, the_most


def min_by_metric(metric, data):
    the_min = 100000
    current_year = 0
    for year in data['Год']:
        if data['Год'][year][metric] < the_min:
            the_min = data['Год'][year][metric]
            current_year = year
    return current_year, the_min


def one_metric_for_all_years(metric: str):
    all_convicted1 = sum(dataset1['Год'][year]['Всего осуждено'] for year in dataset1['Год'])
    all_convicted2 = sum(dataset2['Год'][year]['Всего осуждено'] for year in dataset2['Год'])

    total_convictions1 = sum(dataset1['Год'][year][metric] for year in dataset1['Год'])
    total_convictions2 = sum(dataset2['Год'][year][metric] for year in dataset2['Год'])
    average1 = total_convictions1 / len(dataset1['Год'])
    average2 = total_convictions2 / len(dataset2['Год'])

    first_year = list(dataset1["Год"].items())[0][0]
    last_year = list(dataset1["Год"].items())[-1][0]

    percentage1 = (total_convictions1 / all_convicted1) * 100
    percentage2 = (total_convictions2 / all_convicted2) * 100

    print('=' * 40)
    print(f'Сравнение за период {first_year} - {last_year} по полю: "{metric}", ')
    print('-' * 20)
    print(f"Статья \"{dataset1['Статья']['Название']}\" {dataset1['Статья']['Номер']}")
    print(f"{metric}: {total_convictions1}")
    print(f'Больше всего осуждено в {max_by_metric(metric, dataset1)[0]} году. {max_by_metric(metric, dataset1)[1]}')
    print(f'Меньше всего осуждено в {min_by_metric(metric, dataset1)[0]} году. {min_by_metric(metric, dataset1)[1]}')
    print(f'Среднее значение: {average1:.2f}')
    print(f'% от общего числа осужденных составляет {percentage1:.2f}%') if metric != 'Всего осуждено' else None
    print('-' * 20)
    print(f"Статья \"{dataset2['Статья']['Название']}\" {dataset2['Статья']['Номер']}")
    print(f"{metric}: {total_convictions2}")
    print(f'Больше всего осуждено в {max_by_metric(metric, dataset2)[0]} году. {max_by_metric(metric, dataset2)[1]}')
    print(f'Меньше всего осуждено в {min_by_metric(metric, dataset2)[0]} году. {min_by_metric(metric, dataset2)[1]}')
    print(f'Среднее значение: {average2:.2f}')
    print(f'% от общего числа осужденных составляет {percentage2:.2f}%') if metric != 'Всего осуждено' else None
    print('-' * 20)
    print(
        f"{dataset1['Статья']['Название'] if average1 > average2 else dataset2['Статья']['Название']} в среднем более осуждаемая статья")
    print('=' * 40)


one_metric_for_all_years('Всего осуждено')
one_metric_for_all_years('Условное осуждение к лишению свободы')

result_dataset1 = {
    'Статья': dataset1['Статья']['Название'],
    'Номер': dataset1['Статья']['Номер'],
    'Год': {key: {} for key in dataset1['Год']},
}

percent_convicted = percent_by_metrics(dataset1, 'Всего осуждено', 'Оправдано',
                                       '% Оправданных от общего колличество осужденных')

percent_convicted_to_duress = percent_by_metrics(dataset1, 'Всего осуждено', 'Лишение свободы',
                                                 '% Осужденных на лишение свободы от общего количества осужденных')

percent_convicted_to_duress_3_5 = percent_by_metrics(dataset1, 'Всего осуждено',
                                                     'Лишение свободы: количество осужденных по срокам свыше 3 до 5 лет включительно',
                                                     '% Осужденных на срок от 3-5 от общего количества осужденных')
percent_convicted_to_duress_5_8 = percent_by_metrics(dataset1, 'Всего осуждено',
                                                     'Лишение свободы: количество осужденных по срокам свыше 5 до 8 лет включительно',
                                                     '% Осужденных на срок от 5-8 от общего количества осужденных')
percent_convicted_to_duress_10_15 = percent_by_metrics(dataset1, 'Всего осуждено',
                                                       'Лишение свободы: количество осужденных по срокам свыше 10 до 15 лет включительно',
                                                       '% Осужденных на срок от 10-15 от общего количества осужденных')


def update_result_dataset(dataset, data_):
    """
    :param dataset: Датасет в который будут добавлены данные
    :param data_: Данные которые необходимо добавить в датасет
    :return: dict обновленные датасет
    """
    for year, value in data_.items():
        dataset['Год'][year].update(value)

    return dataset


result_dataset1 = update_result_dataset(result_dataset1, percent_convicted)
result_dataset1 = update_result_dataset(result_dataset1, percent_convicted_to_duress)
result_dataset1 = update_result_dataset(result_dataset1, percent_convicted_to_duress_3_5)
result_dataset1 = update_result_dataset(result_dataset1, percent_convicted_to_duress_5_8)
result_dataset1 = update_result_dataset(result_dataset1, percent_convicted_to_duress_10_15)

result_dataset2 = {
    'Статья': dataset2['Статья']['Название'],
    'Номер': dataset2['Статья']['Номер'],
    'Год': {key: {} for key in dataset2['Год']},
}

percent_convicted_2 = percent_by_metrics(dataset2, 'Всего осуждено', 'Оправдано',
                                         '% Оправданных от общего колличество осужденных')

percent_convicted_to_duress_2 = percent_by_metrics(dataset2, 'Всего осуждено', 'Лишение свободы',
                                                   '% Осужденных на лишение свободы от общего количества осужденных')

percent_convicted_to_duress_3_5_2 = percent_by_metrics(dataset2, 'Всего осуждено',
                                                       'Лишение свободы: количество осужденных по срокам свыше 3 до 5 лет включительно',
                                                       '% Осужденных на срок от 3-5 от общего количества осужденных')
percent_convicted_to_duress_5_8_2 = percent_by_metrics(dataset2, 'Всего осуждено',
                                                       'Лишение свободы: количество осужденных по срокам свыше 5 до 8 лет включительно',
                                                       '% Осужденных на срок от 5-8 от общего количества осужденных')
percent_convicted_to_duress_10_15_2 = percent_by_metrics(dataset2, 'Всего осуждено',
                                                         'Лишение свободы: количество осужденных по срокам свыше 10 до 15 лет включительно',
                                                         '% Осужденных на срок от 10-15 от общего количества осужденных')

result_dataset2 = update_result_dataset(result_dataset2, percent_convicted_2)
result_dataset2 = update_result_dataset(result_dataset2, percent_convicted_to_duress_2)
result_dataset2 = update_result_dataset(result_dataset2, percent_convicted_to_duress_3_5_2)
result_dataset2 = update_result_dataset(result_dataset2, percent_convicted_to_duress_5_8_2)
result_dataset2 = update_result_dataset(result_dataset2, percent_convicted_to_duress_10_15_2)


def compose_in_list(data):
    headers = [header for header in data]
    data_lists = []
    for year, value in data['Год'].items():
        data_row = [data['Статья'], data['Номер'], year]
        for k, v in value.items():
            headers.append(k) if k not in headers else None
            data_row.append(v)
        data_lists.append(data_row)
    data_lists.insert(0, headers)
    return data_lists


def write_to_file(data):
    with open('result.csv', 'w', encoding='utf-16') as file:
        for row in data:
            row = [f'{value:.4f}%' if isinstance(value, float) else value for value in row]
            file.write('\t'.join(map(str, row)) + '\n')


result_data = compose_in_list(result_dataset1) + (compose_in_list(result_dataset2)[1:])

sorted_data = sorted(result_data[1:], key=lambda x: x[7], reverse=True)
sorted_data.insert(0, result_data[0])
write_to_file(sorted_data)
