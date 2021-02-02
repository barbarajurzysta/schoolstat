import pandas as pd


def add_teachers_by_regon(data):
    in_complex = data[data['Regon'] != data['Regon jednostki sprawozdawczej']]
    for gr in in_complex.groupby('Regon jednostki sprawozdawczej'):
        df = data[data['Regon'] == gr[0]]
        if len(df) > 0:
            if df['Uczniowie, wychow., słuchacze'].sum() == 0:
                teachers = df['Nauczyciele'].sum()
                students = gr[1]['Uczniowie, wychow., słuchacze'].sum()
                if students:
                    mult = teachers / students
                    new_teachers = gr[1]['Uczniowie, wychow., słuchacze'] * mult
                    for i in gr[1].index:
                        data.at[i, 'Nauczyciele'] += new_teachers[i]
            else:
                df = pd.concat([df, gr[1]])
                teachers = df['Nauczyciele'].sum()
                students = df['Uczniowie, wychow., słuchacze'].sum()
                if students:
                    mult = teachers / students
                    new_teachers = df['Uczniowie, wychow., słuchacze'] * mult
                    for i in df.index:
                        data.at[i, 'Nauczyciele'] = new_teachers[i]


def drop_zeros(data):
    data.drop(data[(data['Uczniowie, wychow., słuchacze'] == 0)
                   | (data['Nauczyciele'] == 0)].index, inplace=True)


def simplified(data):
    data = data[data['Nazwa typu'].isin(['Przedszkole', 'Punkt przedszkolny',
                                         'Zespół wychowania przedszkolnego',
                                         'Szkoła podstawowa',
                                         'Liceum ogólnokształcące',
                                         'Technikum',
                                         'Branżowa szkoła I stopnia'])].copy()
    data.loc[data['Nazwa typu'] == 'Punkt przedszkolny', 'Nazwa typu'] = 'Przedszkole'
    data.loc[data['Nazwa typu'] == 'Zespół wychowania przedszkolnego', 'Nazwa typu'] = 'Przedszkole'
    return data


def find_diffs(schools_data, dist_popul_data):
    s1 = set(schools_data[['Województwo', 'alt Gmina']].itertuples(index=False))
    s2 = set(dist_popul_data[['Województwo', 'Gmina']].itertuples(index=False))
    return s1.difference(s2)


def fix_records(data, differences):
    for index, row in differences.iterrows():
        data.at[(data['Gmina'] == row['Gmina'])
                & (data['Miejscowość'] == row['Miejscowość']),
                'Gmina'] = row['Nowa Gmina']
