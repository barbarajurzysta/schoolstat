import schoolstat.io.read_data
from schoolstat.schools.build_table import concat_teachers, \
    add_students_per_teacher, add_city_or_rural, added_years, add_alt_name
from schoolstat.schools.clean_table import add_teachers_by_regon, fix_records,\
    find_diffs, simplified
from schoolstat.population.build_table import district_population_table, \
    area_population_table, add_students_per_school
import schoolstat.schools.clean_table
import schoolstat.population.clean_table


def tables(file1, file2, file3, year1, year2, year3, differences_file=None):
    schools = schoolstat.io.read_data.schools(file1)
    dis_popul = schoolstat.io.read_data.district_population(file2)
    popul = schoolstat.io.read_data.population(file3)

    concat_teachers(schools)
    add_teachers_by_regon(schools)
    schoolstat.schools.clean_table.drop_zeros(schools)
    if differences_file:
        differences = schoolstat.io.read_data.differences(differences_file)
        fix_records(schools, differences)
    add_students_per_teacher(schools)
    add_city_or_rural(schools)
    schools_simple = added_years(simplified(schools), year1)
    add_alt_name(schools_simple)

    dis_popul = district_population_table(dis_popul, schools_simple, year2)
    schoolstat.population.clean_table.drop_zeros(dis_popul)
    add_students_per_school(dis_popul)

    difs = find_diffs(schools_simple, dis_popul)
    if difs:
        with open('schoolstat.log', 'a') as f:
            f.write('Warning: detected some inconsistencies, the following '
                    'districts are not in the districts population data\n'
                    + str(difs))

    popul = area_population_table(popul, schools_simple, year3)
    add_students_per_school(popul)
    dis_popul.reset_index(drop=True, inplace=True)
    popul.reset_index(drop=True, inplace=True)

    return schools, dis_popul, popul
