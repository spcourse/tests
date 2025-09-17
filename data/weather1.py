
def read_data(filename):
    dates = []
    temps = []
    input_file = open(filename, 'r')
    for line in list(input_file)[19:]:
        fields = line.split(',')
        dates.append(fields[2])
        temps.append(float(fields[3])/10)
    input_file.close()
    return dates, temps

max_dates, max_temps = read_data('DeBiltTempMaxOLD.txt')
min_dates, min_temps = read_data('DeBiltTempMinOLD.txt')