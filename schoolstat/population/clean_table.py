def drop_zeros(data):
    data.drop(data[data['Liczba szkół'] == 0].index, inplace=True)
