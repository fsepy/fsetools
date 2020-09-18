import binascii
import hashlib


def hash_simple(key: bytes, string: bytes, algorithm: str = 'sha512', length: int = 20):
    cipher = int(binascii.hexlify(hashlib.pbkdf2_hmac(algorithm, string, key, 100000)), 16) % (10 ** length)
    return cipher


def interp1d(x, y):
    def func(x_):
        y_ = None
        for i in range(len(x) - 1):
            if (x[i] <= x_ <= x[i + 1]) or (x[i] >= x_ >= x[i + 1]):
                a = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
                y_ = a * (x_ - x[i]) + y[i]
        return y_

    return func


def test_interp1d():
    interp_func = interp1d([0, 10], [0, 10])
    assert all([interp_func(i) == i for i in [0., 1.2, 1.5, 5.5, 8.5, 9.5, 10.]])

    interp_func = interp1d([10, 0], [0, 10])
    assert all([interp_func(i) == (10 - i) for i in [0., 1.2, 1.5, 5.5, 8.5, 9.5, 10.]])


if __name__ == "__main__":
    test_interp1d()
