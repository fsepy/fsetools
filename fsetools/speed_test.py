def test():
    from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer import _speed_test as test1
    from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import _speed_test as test2
    from timeit import timeit

    print(timeit(test1, number=2))
    print(timeit(test2, number=2))
