import typing
from checkpy import *

only("weather1.py")
download("DeBiltTempMaxOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMaxOLD.txt")
download("DeBiltTempMinOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLD.txt")


def _read_data(file_name):
    dates = []
    temps = []
    input_file = open(file_name, 'r')
    for line in list(input_file)[19:]:
        fields = line.split(',')
        dates.append(int(fields[2]))
        temps.append(float(fields[3])/10)
    input_file.close()
    return dates, temps

max_dates, max_temps = _read_data('DeBiltTempMaxOLD.txt')
min_dates, min_temps = _read_data('DeBiltTempMinOLD.txt')

read_data_fun = (declarative
    .function("read_data")
    .params("filename")
)

def all_int(lst):
    return [int(str(e)) for e in lst]

@test()
def test_read_data1():
    """Testing read_data("DeBiltTempMaxOLD.txt")"""
    returned = read_data_fun.call('DeBiltTempMaxOLD.txt')().returned
    assert (
        isinstance(returned, tuple)
        and len(returned) == 2
        and all(isinstance(el, list) for el in returned)
    ), "Expected the function to return two lists"
    _max_dates, _max_temps = returned
    assert all_int(_max_dates) == max_dates, "You're not returning the right dates"
    assert _max_temps == max_temps, "You're not returning the right temperatures"

@test()
def test_read_data2():
    """Testing read_data("DeBiltTempMinOLD.txt")"""
    returned = read_data_fun.call('DeBiltTempMinOLD.txt')().returned
    assert (
        isinstance(returned, tuple)
        and len(returned) == 2
        and all(isinstance(el, list) for el in returned)
    ), "Expected the function to return two lists"
    _min_dates, _min_temps = returned
    assert all_int(_min_dates) == min_dates, "You're not returning the right dates"
    assert _min_temps == min_temps, "You're not returning the right temperatures"