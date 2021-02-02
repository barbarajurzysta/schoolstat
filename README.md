# Schoolstat

## General info
Package for analysis of Polish schools and population
	
## Requirements
* Python: >= 3.6
* Libraries: pandas, openpyxl, xlrd

## Setup
Clone this repository and run `pip install ./path/to_package`

## Data
The package works with three datasets: 
1. Schools
2. District population
3. Total population

You can download the data from: 
[Schools](https://dane.gov.pl/pl/dataset/839,wykaz-szko-i-placowek-oswiatowych/resource/16251,wykaz-szkol-i-placowek-wg-stanu-na-30ix-2018-r/table) and
[Population](https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/ludnosc-stan-i-struktura-ludnosci-oraz-ruch-naturalny-w-przekroju-terytorialnym-stan-w-dniu-30-06-2020,6,28.html)
   (district population is in tabela12.xls, total population is in tabela01.xls)

You also need to provide the information about year of creating each dataset (in this example the Schools dataset is from 2018 and both of the Population datasets are from 2020).  
If you know about any inconsistencies between the datasets, you can also specify the differences_file, it should look like:
```
Gmina,Miejscowość,Nowa Gmina
Ostrowice,Ostrowice,Drawsko Pomorskie
Ostrowice,Nowe Worowo,Złocieniec
```
where 'Gmina' is the name of a district in Schools dataset, 'Miejscowość' is the name of the town and 'Nowa Gmina' is the name of the district in Population dataset.

## Code Example
```
from schoolstat.prepare_tables import tables
from schoolstat.stats import group_students_per_teacher, students_per_school, filter_stats
schools, dist_popul, popul = tables(file1, file2, file3, 2018, 2020, 2020, differences_file)
d1 = group_students_per_teacher(schools, 'Gmina')
d2 = group_students_per_teacher(schools, 'Miasto czy wieś')
d3 = students_per_school(dist_popul)
d4 = students_per_school(popul)
print(filter_stats(d2, i2='Przedszkole'))
print(filter_stats(d3, 'Warszawa'))
```