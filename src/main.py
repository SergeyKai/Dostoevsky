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


dataset_1 = '105ч1.csv'
dataset_2 = '159ч2.csv'

data1 = read_csv(dataset_1)
data2 = read_csv(dataset_2)

# Обзор данных
print("Данные из первого датасета:")
print(data1)
print("\nДанные из второго датасета:")
print(data2)


def min_by_metric(metric, data):
    the_min = 100000
    current_year = 0
    for year in data['Год']:
        if data['Год'][year][metric] < the_min:
            the_min = data['Год'][year][metric]
            current_year = year
    return current_year, the_min


def max_by_metric(metric, data):
    the_most = 0
    current_year = 0
    for year in data['Год']:
        if data['Год'][year][metric] > the_most:
            the_most = data['Год'][year][metric]
            current_year = year
    return current_year, the_most


def one_metric_for_all_years(metric: str):
    all_convicted1 = sum(data1['Год'][year]['Всего осуждено'] for year in data1['Год'])
    all_convicted2 = sum(data2['Год'][year]['Всего осуждено'] for year in data1['Год'])

    total_convictions1 = sum(data1['Год'][year][metric] for year in data1['Год'])
    total_convictions2 = sum(data2['Год'][year][metric] for year in data2['Год'])
    average1 = total_convictions1 / len(data1['Год'])
    average2 = total_convictions2 / len(data2['Год'])

    firs_year = list(data1["Год"].items())[0][0]
    last_year = list(data1["Год"].items())[-1][0]

    percentage1 = (total_convictions1 / all_convicted1) * 100
    percentage2 = (total_convictions2 / all_convicted2) * 100

    print('=' * 40)
    print(f'Сравнение за период {firs_year} - {last_year} по полю: "{metric}", ')
    print('-' * 20)
    print(f"Статья \"{data1['Статья']['Название']}\" {data1['Статья']['Номер']}")
    print(f"{metric}: {total_convictions1}")
    print(f'Больше всего осуждено в {max_by_metric(metric, data1)[0]} году. {max_by_metric(metric, data1)[1]}')
    print(f'Меньше всего осуждено в {min_by_metric(metric, data1)[0]} году. {min_by_metric(metric, data1)[1]}')
    print(f'Среднее значение: {average1:.2f}')
    print(f'% от общего числа осужденных составляет {percentage1:.2f}%') if metric != 'Всего осуждено' else None
    print('-' * 20)
    print(f"Статья \"{data2['Статья']['Название']}\" {data2['Статья']['Номер']}")
    print(f"{metric}: {total_convictions2}")
    print(f'Больше всего осуждено в {max_by_metric(metric, data2)[0]} году. {max_by_metric(metric, data2)[1]}')
    print(f'Меньше всего осуждено в {min_by_metric(metric, data2)[0]} году. {min_by_metric(metric, data2)[1]}')
    print(f'Среднее значение: {average2:.2f}')
    print(f'% от общего числа осужденных составляет {percentage2:.2f}%') if metric != 'Всего осуждено' else None
    print('-' * 20)
    print(
        f"{data1['Статья']['Название'] if average1 > average2 else data2['Статья']['Название']} в среднем более осуждаемая статья")
    print('=' * 40)


# one_metric_for_all_years('Лишение свободы')


def average_for_each_metric(year):
    all_convicted1 = data1['Год'][year]['Всего осуждено']
    all_convicted2 = data2['Год'][year]['Всего осуждено']

    current_metric = ''
    current_convicted = 0

    print('=' * 40)
    print(f'Сравнение за {year} год ')
    for metric in data1['Год'][year] | data2['Год'][year]:
        value1 = data1['Год'][year][metric]
        value2 = data2['Год'][year][metric]
        percentage1 = (value1 / all_convicted1) * 100
        percentage2 = (value2 / all_convicted2) * 100

        print('-' * 20)
        print(f"Статья \"{data1['Статья']['Название']}\" {data1['Статья']['Номер']}")
        print(f"{metric}: {value1}")
        print(
            f'% от общего числа осужденных составляет {percentage1:.2f} %') if metric != 'Всего осуждено' else None
        print('-' * 20)
        print(f"Статья \"{data2['Статья']['Название']}\" {data2['Статья']['Номер']}")
        print(f"{metric}: {value2}")
        print(
            f'% от общего числа осужденных составляет {percentage2:.2f}%') if metric != 'Всего осуждено' else None
    print('=' * 40)


average_for_each_metric(2020)


def ration_metrics_for_year(first_metric, second_metric, year):
    all_convicted1 = data1['Год'][year]['Всего осуждено']
    all_convicted2 = data2['Год'][year]['Всего осуждено']

    first_metric_value1 = data1['Год'][year][first_metric]
    first_metric_value2 = data2['Год'][year][first_metric]

    second_metric_value1 = data1['Год'][year][second_metric]
    second_metric_value2 = data2['Год'][year][second_metric]

    first_metric_percentage1 = (first_metric_value1 / all_convicted1) * 100
    first_metric_percentage2 = (first_metric_value2 / all_convicted2) * 100

    second_metric_percentage1 = (second_metric_value1 / all_convicted1) * 100
    second_metric_percentage2 = (second_metric_value2 / all_convicted2) * 100

    print('=' * 40)
    print(f"Статистика за {year} год")
    print(f"Статья \"{data1['Статья']['Название']}\" {data1['Статья']['Номер']}")
    print(f"{first_metric}: {first_metric_value1} | {first_metric_percentage1:.2f}% от общего количества осужденных")
    print(f"{second_metric}: {second_metric_value1} | {second_metric_percentage1:.2f}% от общего количества осужденных")
    print('-' * 20)
    print(f"Статья \"{data2['Статья']['Название']}\" {data2['Статья']['Номер']}")
    print(f"{first_metric}: {first_metric_value2} | {first_metric_percentage2:.2f}% от общего количества осужденных")
    print(f"{second_metric}: {second_metric_value2} | {second_metric_percentage2:.2f}% от общего количества осужденных")
    print('=' * 40)


ration_metrics_for_year(
    'Лишение свободы: количество осужденных по срокам свыше 10 до 15 лет включительно',
    'Условное осуждение к лишению свободы',
    2017
)
