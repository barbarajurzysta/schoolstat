import pandas as pd


# How many schools can students from a given year attend to
def schools_per_year(data, year):
    return len(data[(data['Od'] <= year) & (data['Do'] >= year)])


# Returns a multi-index dataframe with statistics:
# min, max, mean number of students per teacher
# and number of schools of a given type in a given area
# indexed by (area, type of school) or (district, type of school, voivodeship)
def group_students_per_teacher(data, col):
    if col not in ['Gmina', 'Miasto czy wieś']:
        raise ValueError('Wrong column name. Possible names: '
                         '["Gmina", "Miasto czy wieś"]')
    if col == 'Gmina':
        d = data.groupby([col, 'Nazwa typu', 'Województwo'])
    else:
        d = data.groupby([col, 'Nazwa typu'])
    d = d['Liczba uczniów na nauczyciela']
    res = pd.DataFrame(d.mean())
    res = res.rename(columns={'Liczba uczniów na nauczyciela': 'avg'})
    res['min'] = d.min()
    res['max'] = d.max()
    res['number'] = d.size()
    return res


# Returns a multi-index dataframe with number of students
# from a given year per school
# indexed by (area, year) or (district, year, voivodeship)
def students_per_school(data):
    res = data.drop(['Liczba osób', 'Liczba szkół'], axis=1)
    if 'Miasto czy wieś' in res.columns:
        res.set_index(['Miasto czy wieś', 'Rok urodzenia'], inplace=True)
    elif 'Gmina' in res.columns:
        res.set_index(['Gmina', 'Rok urodzenia', 'Województwo'], inplace=True)
    return res


def group_students_per_school(data, by):
    if by not in data.columns and by not in data.index.names:
        raise KeyError(f'Cannot group data by {by}, there is no such column')
    d = data.groupby(by)['Liczba uczniów na szkołę']
    res = pd.DataFrame(d.mean())
    res = res.rename(columns={'Liczba uczniów na szkołę': 'avg'})
    res['min'] = d.min()
    res['max'] = d.max()
    return res


# Filter a multi-index dataframe
# i1 - first index (usually 'M' or 'W' or district)
# i2 - second index (school type or year of birth)
def filter_stats(stats, i1=None, i2=None, stat=None):
    ids = [item for sublist in stats.index for item in sublist]
    if i1 and i1 not in ids:
        raise KeyError(f'{i1=} is a wrong index')
    if i2 and i2 not in ids:
        raise KeyError(f'{i2=} is a wrong index')
    if i1:
        if i2:
            stats = stats.loc[(i1, i2)]
        else:
            stats = stats.loc[i1]
    else:
        if i2:
            stats = stats.loc[pd.IndexSlice[:, i2], :]
    if stat:
        if stat not in stats.columns:
            raise KeyError(f'{stat} is not covered by the statistics')
        stats = stats[stat]
    return stats
