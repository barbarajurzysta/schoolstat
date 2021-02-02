import pytest
import pandas as pd
import os
import schoolstat.io.read_data
import schoolstat.schools.build_table
import schoolstat.population.build_table
import schoolstat.schools.clean_table
from schoolstat.stats import group_students_per_school


def test_empty_schools(tmpdir):
    file_name = os.path.join(str(tmpdir), 'test.xlsx')
    x = pd.DataFrame()
    x.to_excel(file_name, engine='openpyxl')
    with pytest.raises(ValueError):
        schoolstat.io.read_data.schools(file_name)


def test_empty_distr(tmpdir):
    file_name = os.path.join(str(tmpdir), 'test.xls')
    x = pd.DataFrame()
    x.to_excel(file_name)
    with pytest.raises(ValueError):
        schoolstat.io.read_data.district_population(file_name)


def test_empty_popul(tmpdir):
    file_name = os.path.join(str(tmpdir), 'test.xls')
    x = pd.DataFrame()
    x.to_excel(file_name)
    with pytest.raises(ValueError):
        schoolstat.io.read_data.population(file_name)


def test_empty_differences(tmpdir):
    file_name = os.path.join(str(tmpdir), 'test.csv')
    x = pd.DataFrame()
    x.to_csv(file_name)
    with pytest.raises(AssertionError):
        schoolstat.io.read_data.differences(file_name)


def test_add_spt():
    cols = ['Uczniowie, wychow., słuchacze', 'Nauczyciele']
    data = pd.DataFrame([[4, 1], [5, 1]], columns=cols)
    schoolstat.schools.build_table.add_students_per_teacher(data)
    assert list(data['Liczba uczniów na nauczyciela']) == [4, 5]


def test_add_sps_zero():
    cols = ['Liczba osób', 'Liczba szkół']
    data = pd.DataFrame([[4, 1], [5, 0]], columns=cols)
    with pytest.raises(ZeroDivisionError):
        schoolstat.population.build_table.add_students_per_school(data)


def test_drop_zeros():
    cols = ['Uczniowie, wychow., słuchacze', 'Nauczyciele']
    data = pd.DataFrame([[4, 1], [5, 0], [0, 1]], columns=cols)
    schoolstat.schools.clean_table.drop_zeros(data)
    assert len(data) == 1


def test_stats():
    cols = ['Miasto czy wieś', 'Rok urodzenia', 'Liczba uczniów na szkołę']
    rows = [['M', 2000, 120], ['W', 2000, 100], ['W', 2000, 50]]
    data = pd.DataFrame(rows, columns=cols)
    grouped = group_students_per_school(data, 'Rok urodzenia')
    assert len(grouped) == 1
    assert float(grouped['min']) == 50
    assert float(grouped['max']) == 120
    assert float(grouped['avg']) == (120 + 100 + 50) / 3
