import pandas as pd


def schools(file_name):
    cols = ['Lp.', 'Województwo', 'Gmina', 'Typ gminy', 'Miejscowość',
            'Nazwa typu', 'Regon', 'Uczniowie, wychow., słuchacze',
            'Nauczyciele pełnozatrudnieni',
            'Nauczyciele niepełnozatrudnieni (w etatach)',
            'Regon jednostki sprawozdawczej']
    df = pd.read_excel(file_name, engine='openpyxl', index_col=0,
                       usecols=cols, skiprows=[1], header=0,
                       dtype={'Regon': str,
                              'Regon jednostki sprawozdawczej': str})
    if set(df.columns) != set(set(cols).difference({'Lp.'})):
        raise ValueError(f'Incomplete data in file {file_name}')
    return df


def district_population(file_name):
    df = pd.read_excel(file_name, sheet_name=None,
                       usecols=[0, 2], skiprows=[0, 1, 2, 3, 4, 6, 7],
                       names=['Wyszczególnienie', 'Ogółem'])
    for sheet in df:
        if len(df[sheet].columns) != 2:
            raise ValueError(f'Incomplete data in sheet {sheet}, '
                             f'file {file_name}')
    return df


def population(file_name):
    df = pd.read_excel(file_name, usecols=[0, 1, 4, 7], skiprows=range(9),
                       nrows=102, names=['Wiek', 'Razem', 'Miasta', 'Wieś'])
    if len(df.columns) != 4:
        raise ValueError(f'Incomplete data in file {file_name}')
    return df


def differences(file_name):
    data = pd.read_csv(file_name)
    assert set(data.columns) == {'Miejscowość', 'Gmina', 'Nowa Gmina'}
    return data
