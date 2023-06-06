import numpy as np

from fsetools.lib.fse_din_en_1991_1_2_parametric_fire import temperature


def test_0():
    """
    Benchmark against numerical results detailed in:

    Zehfuss, J., Hosser, D. (2006) - A parametric natural fire model for the structural fire design of multi-storey
    buildings.

    Note the Python function was coded based on DIN EN 1991-1-2 rather than the above paper. Thus, there maybe trivial
    deviations between the two sources in terms variable names. For example, Q_2_x and Q_3_x are present in the paper
    but do not present in DIN EN 1991-1-2.

    First drafted on 16/07/2022, Yan Fu.
    Last updated on 16/07/2022, Yan Fu.
    """
    inputs = dict(
        t=np.arange(0., 180. * 60. + 1. / 2., 1.),
        A_w=8.,
        h_w=2.5,
        A_t=80.,
        A_f=16.,
        t_alpha=300.,
        b=1500.,
        q_x_d=511. * 1e6,
        gamma_fi_Q=1.0,
        q_ref=1300. * 1e6,
        rho_Q_dot=0.25 * 1e6,
    )

    res = {k: -1 for k in (
        't_1', 't_2', 't_3',
        't_1_x', 't_2_x', 't_3_x',
        'Q_1', 'Q_2', 'Q_3',
        'Q_1_x', 'Q_2_x', 'Q_3_x',
        'T_1_f', 'T_2_f', 'T_3_f',
        'T_2_x', 'T_3_x',
    )}

    temperature(**inputs, outputs=res)

    assert abs(res['t_1'] - 600.) <= 1.
    assert abs(res['t_2'] - 4040.) <= 1.
    assert abs(res['t_3'] - 7160.) <= 1.
    assert abs(res['Q_1'] - 800.) <= 1.
    assert abs(res['Q_2'] - 13760.) <= 1.
    assert abs(res['Q_3'] - 6240.) <= 1.
    # assert abs(outputs['Q_2_x'] - 4923.) <= 1.  # does not exist in BS EN 1991-1-2 but present in the paper
    # assert abs(outputs['Q_3_x'] - 2453.) <= 1.  # does not exist in BS EN 1991-1-2 but present in the paper
    assert abs(res['t_2_x'] - 1831.) <= 1.
    assert abs(res['t_3_x'] - 3057.) <= 1.
    assert abs(res['T_1_f'] - 565.) <= 1.
    assert abs(res['T_2_f'] - 769.) <= 1.
    assert abs(res['T_3_f'] - 383.) <= 1.
    assert abs(res['T_2_x'] - 689.) <= 2.
    assert abs(res['T_3_x'] - 316.) <= 1.


def test_temperature_and_key_locations():
    res = {k: -1 for k in (
        't_1', 't_2', 't_3',
        't_1_x', 't_2_x', 't_3_x',
        'Q_1', 'Q_2', 'Q_3',
        'Q_1_x', 'Q_2_x', 'Q_3_x',
        'T_1', 'T_2_x', 'T_3_x'
    )}
    t = np.arange(0., 180. * 60. + 1. / 2., 1.)
    T = temperature(
        t=t,
        A_w=6.,
        h_w=1.,
        A_t=220.,
        A_f=100.,
        t_alpha=300.,
        b=1500.,
        q_x_d=400. * 1e6,
        gamma_fi_Q=1.0,
        q_ref=1300. * 1e6,
        rho_Q_dot=0.25 * 1e6,
        outputs=res
    )

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        ax.plot(t / 60., T - 273.15, '-k')
        ax.set_xlabel('Time [min]')
        ax.set_ylabel('Temperature [$^oC$]')

        def func_(t_1, t_2_x, t_3_x, Q_1, Q_2, Q_3, T_1, T_2_x, T_3_x, **__):
            ax.plot([t_1 / 60, t_2_x / 60, t_3_x / 60], [T_1, T_2_x, T_3_x])
            ax2.plot(
                [0, t_1 / 60., t_2_x / 60., t_3_x / 60.],
                [0, Q_2 / 1e3, Q_2 / 1e3, 0],
                '--r'
            )
            ax2.set_ylabel('HRR [MW]')
            ax2.set_ylim(0, Q_2 / 1e3 + Q_2 / 1e3 * 0.3)

        func_(**res)
        plt.show()
    except Exception as e:
        raise e

    assert abs(res['Q_2'] - 89043.83749141336) < 1e-6
    assert abs(t[np.argmin(np.abs(t - res['t_2_x']))] - t[np.argmax(T)]) < 2


if __name__ == '__main__':
    # test_0()
    test_temperature_and_key_locations()
