import pandas as pd


def concat_teachers(data):
    data['Nauczyciele'] = data['Nauczyciele pełnozatrudnieni'] \
                          + data['Nauczyciele niepełnozatrudnieni (w etatach)']
    data.drop(columns=['Nauczyciele pełnozatrudnieni',
                       'Nauczyciele niepełnozatrudnieni (w etatach)'],
              inplace=True)


def add_students_per_teacher(data):
    if 0 in list(data['Nauczyciele']):
        raise ZeroDivisionError('0 found in "Nauczyciele" column, use '
                                'schoolstat.schools.clean_table.drop_zeros() '
                                'first')
    data['Liczba uczniów na nauczyciela'] = data['Uczniowie, wychow., słuchacze'] / data['Nauczyciele']


def add_city_or_rural(data):
    data['Miasto czy wieś'] = 'W'
    data.loc[data['Typ gminy'] == 'M', 'Miasto czy wieś'] = 'M'
    data.loc[(data['Typ gminy'] == 'M-Gm')
             & (data['Gmina'] == data['Miejscowość']), 'Miasto czy wieś'] = 'M'


def added_years(data, year_of_data):
    years = [(3, 6), (7, 14), (15, 18), (15, 19), (15, 17)]
    years = [(year_of_data - y[1], year_of_data - y[0]) for y in years]
    years0 = [y[0] for y in years]
    years1 = [y[1] for y in years]
    years_df = pd.DataFrame({'Nazwa typu': ['Przedszkole',
                                            'Szkoła podstawowa',
                                            'Liceum ogólnokształcące',
                                            'Technikum',
                                            'Branżowa szkoła I stopnia'],
                             'Od': years0, 'Do': years1})

    return data.join(years_df.set_index('Nazwa typu'), on='Nazwa typu')


def add_alt_name(data):
    data['alt Gmina'] = ''
    for index, row in data.iterrows():
        if '.' in row['Gmina']:
            data.at[index, 'alt Gmina'] = row['Gmina'].split('.')[-1].strip()
        else:
            data.at[index, 'alt Gmina'] = row['Gmina']
