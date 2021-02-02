import pandas as pd
from schoolstat.schools.build_table import add_city_or_rural
from schoolstat.stats import schools_per_year

voivodeships = ['Dolnośląskie', 'Kujawsko-pomorskie', 'Lubelskie', 'Lubuskie',
                'Łódzkie', 'Małopolskie', 'Mazowieckie', 'Opolskie',
                'Podkarpackie', 'Podlaskie', 'Pomorskie', 'Śląskie',
                'Świętokrzyskie', 'Warmińsko-mazurskie', 'Wielkopolskie',
                'Zachodniopomorskie']
voivodeships_lower = [v.lower() for v in voivodeships]


def district_population_table(data, schools_data, data_year):
    min_year = schools_data['Od'].min()
    max_year = schools_data['Do'].max()
    new_lines = []
    for voivodeship in data:
        lines = []
        d1 = data[voivodeship]
        district = ''
        if voivodeship == 'Śląske':
            voivodeship = 'Śląskie'
        if voivodeship.lower() not in voivodeships_lower:
            raise KeyError(f'Wrong sheet name: {voivodeship}, sheet names '
                           f'should be in {voivodeships}')
        voivodeship = 'WOJ. ' + voivodeship.upper()
        for index, row in d1.iterrows():
            if row['Wyszczególnienie'][0] != ' ':   # district name
                district = row['Wyszczególnienie']
            elif row['Wyszczególnienie'].strip().isdigit():   # specific age
                age = int(row['Wyszczególnienie'].strip())
                year = data_year - age
                if min_year <= year <= max_year:
                    lines.append([voivodeship, district, year, row['Ogółem']])
        lines.sort()
        prev_line = (0, 0, 0, 0)
        for line in lines:
            if line[:3] == prev_line[:3]:
                # summing multiple occurrences of the same district
                new_lines[-1][-1] += line[-1]
            else:
                new_lines.append(line)
            prev_line = line

    # adding number of schools accessible for students
    # from a given district and year
    prev_v, prev_d = 0, 0
    v_data = schools_data
    d_data = schools_data
    for line in new_lines:
        v, d, y = line[:3]
        if prev_v != v:
            v_data = schools_data[schools_data['Województwo'] == v]
            d_data = v_data[v_data['alt Gmina'] == d]
        elif prev_d != d:
            d_data = v_data[v_data['alt Gmina'] == d]
        line.append(schools_per_year(d_data, y))
        prev_v, prev_d = v, d

    return pd.DataFrame(new_lines, columns=['Województwo', 'Gmina',
                                            'Rok urodzenia', 'Liczba osób',
                                            'Liczba szkół'])


def add_students_per_school(data):
    if 0 in list(data['Liczba szkół']):
        raise ZeroDivisionError('0 found in "Liczba szkół" column, use '
                                'schoolstat.population.clean_table.drop_zeros() '
                                'first')
    elif 0 in list(data['Liczba osób']):
        with open('schoolstat.log', 'a') as f:
            f.write('Warning: population is 0\n'
                    + str(data[data['Liczba osób'] == 0]))
    data['Liczba uczniów na szkołę'] = data['Liczba osób'] / data['Liczba szkół']


def area_population_table(data, schools_data, data_year):
    min_year = schools_data['Od'].min()
    max_year = schools_data['Do'].max()
    data = data[data['Wiek'].apply(lambda x: isinstance(x, int))].copy()
    data['Rok urodzenia'] = data_year - data['Wiek']
    data = data[(min_year <= data['Rok urodzenia'])
                & (data['Rok urodzenia'] <= max_year)]

    cities = data[['Miasta', 'Rok urodzenia']].rename(
        columns={'Miasta': 'Liczba osób'})
    rural = data[['Wieś', 'Rok urodzenia']].rename(
        columns={'Wieś': 'Liczba osób'})
    cities['Miasto czy wieś'] = 'M'
    rural['Miasto czy wieś'] = 'W'
    data = pd.concat([cities, rural])
    data['Liczba szkół'] = 0
    if 'Miasto czy wieś' not in schools_data.columns:
        add_city_or_rural(schools_data)
    schools_cities = schools_data[schools_data['Miasto czy wieś'] == 'M']
    schools_rural = schools_data[schools_data['Miasto czy wieś'] == 'W']

    for index, row in data.iterrows():
        if row['Miasto czy wieś'] == 'M':
            n_schools = schools_per_year(schools_cities, row['Rok urodzenia'])
        else:
            n_schools = schools_per_year(schools_rural, row['Rok urodzenia'])
        data.at[index, 'Liczba szkół'] = n_schools
    return data
