import importlib
import multiprocessing as mp
import os
import subprocess
import time
from os import path
from typing import List, Dict, Callable
from typing import Union

import numpy as np
from numpy import ndarray

from fsetools import logger
from fsetools.libstd.bs_en_1993_1_2_2005_k_y_theta import clause_3_2_1_1_k_y_theta_mod, \
    clause_3_2_1_1_k_y_theta_mod_reversed


class Thermal2DPPXML:
    """
    SAFIR Thermal2D Post Processor XML
    """

    def __init__(self):
        self.__data: dict = None  # dict parsed from xml
        self.__ns: np.ndarray = None  # node indexes where temperatures are measured `ns=[n1, n2, ...]`
        self.__xs: np.ndarray = None  # x coordinates [x1, x2, ...]
        self.__ys: np.ndarray = None  # y coordinates [y1, y2, ...]
        self.__ts: np.ndarray = None  # time steps [30, 60, ...]
        self.__Ts: np.ndarray = None  # temperatures [T1, T2, ...], T1 = [T11, T12, ...]
        self.__xml = None  # xml raw
        self.__xml_changed = True  # whether `self.__xml` has changed
        self.__ns_xys_changed = True  # whether `self.__ns` or `self.__xys` haved changed

    def get_nodes_temp(self, nodes: ndarray) -> ndarray:
        self.process_xml()
        temps = self.nodes2temp(Ts=self.__Ts, nodes=np.array(nodes))
        return temps

    def get_line_temp(self, n1: Union[tuple, list], n2: Union[tuple, list], dx: float = None, ds: int = None):
        if dx is not None:
            pass
        elif ds is not None:
            pass
        else:
            raise ValueError('Either dx or dn need to be defined')

        self.process_xml()

        for i, t in enumerate(self.__ts):
            pass

    def get_nodes_temp_ave(
            self,
            ns: ndarray = None, ws: ndarray = None, mode: str = 'ws', T_ns: ndarray = None,
            fp_save_plot: str = None, figsize: Union[list, tuple] = (3.5, 3.5), ylim: Union[list, tuple] = (0, 1200),
            xlim: Union[list, tuple] = None, show_legnend: bool = False,
            fp_save_num: str = None,
    ):
        """
        Get average temperature based on the defined nodes :code:`ns` or temperatures :code:`T_ns`.

        :param ns:              A list/tuple of integers describing node index. This is not required if :code:`T_ns` is
                                provided.
                                :code:`ns = [n1, n2, ...]`
        :param ws:              A list/tuple of floats describing weighting of the defined nodes when averaging
                                temperatures.
                                :code:`ws = [w1, w2, ...]`
        :param mode:            `ws` for weighted average, k_y_theta for
        :param T_ns:            An array of temperatures. This will be derived from the xml if not provided.
                                :code:`T_ns = [T_n1, T_n2, ...]`
                                :code:`T_n1 = [float, float, ...]`
        :param fp_save_plot:    A full file path with .png suffix which a plot will be saved. The plot includes `T_ns`
                                and the calculated average temperature.
        :return:                [C] Averaged temperatures

        The below condition should be satisfied.

        :code:`len(ns) == len(ws) == T_ns.shape[0]`
        """
        plt = getattr(importlib.import_module('matplotlib'), 'pyplot')
        plt.style.use('seaborn-paper')

        self.process_xml()

        if T_ns is None:
            if ns is None:
                raise ValueError('Either `nodes` or `temperature_nodes` must be defined')
            T_ns = self.get_nodes_temp(ns)

        if mode == 'ws':
            T_ave = self.__T_ave(Ts=T_ns, weights=ws)
        elif mode == 'k_y_theta':
            T_ave = self.__T_ave_k_y_theta(Ts=T_ns, weights=ws)
        else:
            raise ValueError(f'`mode` can be either `ws` or `k_y_theta`, `{mode}` is provided')

        if fp_save_plot is not None:
            try:
                T_ave_ = np.copy(T_ave)
                T_ave_[T_ave_ < 400.] = np.nan
                fig, ax = plt.subplots(1, 1, figsize=figsize)
                for i, T_n in enumerate(T_ns):
                    ax.plot(self.__ts / 60., T_n, label=f'{ns[i]}')
                ax.plot(self.__ts / 60., T_ave_, ls='--', c='k', label='Mean')
                ax.set_ylim(ylim)
                if xlim is not None:
                    ax.set_xlim(xlim)
                ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
                ax.set_xlabel('Time [min]')
                ax.set_ylabel('Temperature [°C]')
                ax.tick_params(axis='both', which='both', labelsize='xx-small')
                if show_legnend:
                    ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=3, fontsize='xx-small',
                              loc='lower right').set_visible(True)
                else:
                    ax.legend().set_visible(False)
                fig.savefig(fp_save_plot, dpi=300, bbox_inches='tight', transparent=True)
                plt.close('all')
            except Exception as e:
                logger.error(f'Failed to save plot to {fp_save_plot}, {e}')

        if fp_save_num is not None:
            try:
                np.savetxt(
                    fname=fp_save_num,
                    X=np.vstack((self.__ts, T_ns, T_ave)).transpose(),
                    fmt='%.3f',
                    header=f'TIME,' + ','.join([f'node {n}' for n in ns]) + ',MEAN',
                    delimiter=',',
                    comments='',
                )
            except Exception as e:
                logger.error(f'Failed to numerical data to {fp_save_num}, {e}')

        return T_ave

    def get_nodes_from_xy(self, xys: Union[tuple, list]) -> ndarray:
        self.process_xml()
        return self.xys2nodes(self.__xs, self.__ys, xys)

    def get_xys_temp(self, xys: Union[tuple, list]):
        return self.get_nodes_temp(nodes=self.get_nodes_from_xy(xys))

    def get_xys_temp_ave(self, xys: Union[tuple, list], *args, **kwargs):
        ns = self.get_nodes_from_xy(xys=xys)
        return self.get_nodes_temp_ave(ns=ns, *args, **kwargs)

    def process_xml(self):
        if self.__xml_changed:
            # only process if the xml is changed
            self.xml = self.xml  # assign xml
            self.__data = self.xml2dict(self.xml)  # convert xml to dict
            self.__xs, self.__ys = self.dict2xys(self.__data)  # obtain all node x and y coordinates
            self.__ts, self.__Ts = self.dict2tsTs(
                self.__data)  # obtain all time steps and temperatures at each time step
            self.__xml_changed = False

    @property
    def t(self):
        self.process_xml()
        return self.__ts

    @property
    def T(self):
        self.process_xml()
        return self.__Ts

    @property
    def x(self):
        self.process_xml()
        return self.__xs

    @property
    def y(self):
        self.process_xml()
        return self.__ys

    @property
    def xml(self):
        return self.__xml

    @xml.setter
    def xml(self, xml: str):
        self.__xml = xml
        self.__xml_changed = True

    @staticmethod
    def xml2dict(xml: str) -> dict:
        data_dict = getattr(importlib.import_module('xmltodict'), 'parse')(xml)
        return data_dict

    @staticmethod
    def dict2xys(data: dict) -> tuple:
        xys = data['SAFIR_RESULTS']['NODES']['N']
        xs, ys = list(), list()
        for xy in xys:
            xs.append(float(xy['P2']))
            ys.append(float(xy['P1']))
        return np.array(xs), np.array(ys)

    @staticmethod
    def dict2tsTs(data: dict) -> tuple:
        ts, Ts = list(), list()
        steps = data['SAFIR_RESULTS']['STEP']
        for step in steps:
            ts.append(float(step['TIME']['#text']))
            Ts.append([float(i) for i in step['TEMPERATURES']['T']])
        return np.array(ts), np.array(Ts)

    @staticmethod
    def xys2nodes(xs, ys, xys) -> ndarray:
        nodes = list()
        xys1 = np.stack((xs, ys), axis=0)
        for xy in xys:
            i = np.argmin(((xys1[0, :] - xy[0]) ** 2) + ((xys1[1, :] - xy[1]) ** 2))
            i += 1
            nodes.append(i)

        return np.array(nodes)

    @staticmethod
    def nodes2temp(Ts: ndarray, nodes: ndarray) -> ndarray:
        nodes_safir2py = [i - 1 for i in nodes]
        Ts_nodes = list()
        for node in nodes_safir2py:
            Ts_nodes.append([T[node] for T in Ts])
        return np.array(Ts_nodes)

    @staticmethod
    def __T_ave(Ts: ndarray, weights: ndarray) -> ndarray:
        # populate `weights` to match the shape of `Ts_nodes`
        Ts_weights = np.repeat(weights, Ts.shape[1])
        Ts_weights = np.reshape(Ts_weights, (Ts.shape[1], len(weights)), order='F')
        Ts_weights = Ts_weights.transpose()

        # calculate the summed weights for all time steps
        Ts_weights_sum = np.sum(Ts_weights, axis=0)

        # calculate normalised weights
        Ts_weights_normalised = np.zeros_like(Ts)
        for i in range(Ts_weights_normalised.shape[0]):
            Ts_weights_normalised[i, :] = np.divide(Ts_weights[i, :], Ts_weights_sum[:])

        return np.sum(Ts_weights_normalised * Ts, axis=0)

    @staticmethod
    def __T_ave_k_y_theta(Ts: ndarray, weights: ndarray) -> ndarray:
        T_ave = np.zeros_like(Ts[0, :])
        for i in range(len(T_ave)):
            k_y_theta_i = clause_3_2_1_1_k_y_theta_mod(Ts[:, i] + 273.15)
            k_y_theta_mean = np.sum(np.multiply(k_y_theta_i, weights)) / np.sum(weights)
            T_ave_ = clause_3_2_1_1_k_y_theta_mod_reversed(k_y_theta_mean) - 273.15
            T_ave[i] = T_ave_

        return T_ave


class Thermal2DRun:
    def __init__(self):
        self.__fp = None
        self.__fp_safir_exe = r'C:\work\fem\safir\safir.exe'

    def run(self):
        if self.__fp is None:
            raise ValueError('`fp_input_file` is missing')

        self.safir_single_run(
            fp_safir_exe=self.fp_safir_exe,
            fp_in=self.fp_input_file,
            fp_stdout=path.splitext(self.__fp)[0] + '.stdout'
        )

    def run_solve_k(
            self,
            xys: Union[list, tuple],
            T_target: float,
            ws: Union[list, tuple],
            k_1=0.010,
            k_2=200.000,
            T_target_tol=1,
            bc_old2new=None,
            teq_solve: bool = False,
            teq_bc_old2new: tuple = None
    ):
        """
        Solve k for a given maximum temperature :code:`T_target ± T_target_tol`. Text `{k:.5f}` should exists in the SAFIR input file.

        :param xys:             x and y coordinates where temperatures will be sampled from (used to calculate average temperature)
        :param T_target:        [°C] Target temperature which k is solved for
        :param ws:              [-] Weighting factor used to calculate average temperature
        :param ky_theta_to_ws:  [-] True apply k_y_theta to `ws`
        :param k_1:             [W/m/K] Conductivity lower bound
        :param k_2:             [W/m/K] Conductivity upper bound
        :param T_target_tol:    [°C] Target temperature tolerance
        :param bc_old2new:      Replace BC in SAFIR input file :code:`bc_old2new=((old1, new1), (old2, new2), ...)`, old and new are strings representing BC in the SAFIR input file
        :param teq_solve:       True to solve time equivalence
        :param teq_bc_old2new:  Similar to `bc_old2new` but performed only for solving time equivalence
        :return:                dict containing `k` and `T`. Also includes `teq` if `teq_solve` is True
        """

        logger.info(f'{self.fp_input_file}')

        case = Thermal2DRun()
        case_p = Thermal2DPPXML()

        def replace_input_file(fp_, old2new_):
            if old2new_ is not None:
                with open(fp_, 'r+') as f:
                    t_ = f.read()
                    f.seek(0)
                    for bc in old2new_:
                        t_ = t_.replace(*bc)
                    f.write(t_)
                    f.truncate()

        def run_and_get_max_temp(k_, bc_old2new_=bc_old2new):
            case.fp_input_file = self.update_params(fp_in=self.fp_input_file, k=k_)
            replace_input_file(case.fp_input_file, bc_old2new_)
            case.run()
            case_p.xml = case.xml
            T_ave = case_p.get_xys_temp_ave(
                xys=xys, ws=ws, mode='k_y_theta',
                fp_save_plot=path.splitext(case.fp_input_file)[0] + '.png',
                fp_save_num=path.splitext(case.fp_input_file)[0] + '.temp.csv',
            )
            return np.nanmax(T_ave)

        def run_and_get_teq(k_solved, T_solved, teq_bc_old2new_=teq_bc_old2new):
            case.fp_input_file = self.update_params(fp_in=self.fp_input_file, suffix='_iso', k=k_solved)
            replace_input_file(case.fp_input_file, teq_bc_old2new_)
            case.run()
            case_p.xml = case.xml
            T_ave = case_p.get_xys_temp_ave(
                xys=xys, ws=ws, mode='k_y_theta',
                fp_save_plot=path.splitext(case.fp_input_file)[0] + '.png',
                fp_save_num=path.splitext(case.fp_input_file)[0] + '.temp.csv',
            )
            return np.amin(case_p.t[T_ave >= T_solved])

        T_2 = run_and_get_max_temp(k_=k_2)
        self.logger('Iteration {}: {:<20}{:<20}'.format(f'-2', f'{k_2:.5f} W/m/K', f'{T_2:.1f} °C'))
        if T_2 < T_target:
            logger.warning(f'The maximum possible temperature {T_2:.1f} is less than the target {T_target:.1f}')
            return dict(k=np.inf, T=T_2)

        T_1 = run_and_get_max_temp(k_=k_1)
        self.logger('Iteration {}: {:<20}{:<20}'.format(f'-1', f'{k_1:.5f} W/m/K', f'{T_1:.1f} °C'))
        if T_1 > (T_target + T_target_tol):
            logger.warning(f'The minimum possible temperature {T_1:.1f} is higher than the target {T_target:.1f}')
            return dict(k=-np.inf, T=T_1)

        '''
        T_1, k_1
        T_2, k_2
        y = a x + b
        k_1 = a T_1 + b
        k_2 = a T_2 + b
        k_1 - k_2 = a T_1 + b - a T_2 - b
        k_1 - k_2 = a (T_1 - T_2) + b - b
        a = (k_1 - k_2) / (T_1 - T_2)
        b = k_1 - a ((k_1 - k_2) / (T_1 - T_2))
        '''

        k_3 = 100
        T_3 = run_and_get_max_temp(k_=k_3)
        self.logger('Iteration {}: {:<20}{:<20}'.format(f'0', f'{k_3:.5f} W/m/K', f'{T_3:.1f} °C'))

        iter_count = 1
        while True:
            if iter_count > 20:
                logger.warning('Maximum solver iteration reached')
                if teq_solve:
                    return dict(k=np.nan, T=np.nan, teq=np.nan)
                else:
                    return dict(k=np.nan, T=np.nan)

            if T_3 < T_target - T_target_tol:
                # the section is cooler than the target
                k_1 = k_3  # increase the conductivity by increasing the lower bound
            elif T_3 > T_target + T_target_tol:
                # the section is hotter than the target
                k_2 = k_3  # decrease the conductivity by decreasing the upper bound
            else:
                if teq_solve:
                    case.fp_input_file = self.update_params(fp_in=self.fp_input_file, k=k_3)
                    teq = run_and_get_teq(k_solved=k_3, T_solved=T_3)
                    self.logger(f'Solved time equivalence: {teq / 60.:.2f} min')
                    return dict(k=k_3, T=T_3, teq=teq)
                else:
                    return dict(k=k_3, T=T_3)

            k_3 = (k_1 + k_2) / 2.
            T_3 = run_and_get_max_temp(k_=k_3)
            self.logger('Iteration {}: {:<20}{:<20}'.format(f'{iter_count:d}', f'{k_3:.5f} W/m/K', f'{T_3:.1f} °C'))
            iter_count += 1

    def logger(self, msg: str):
        fp_log = path.splitext(self.__fp)[0] + '.log'
        try:
            with open(fp_log, 'a') as f:
                f.write(msg + os.linesep)
        except Exception as e:
            logger.error(f'Failed to write log message to file {fp_log}, {e}')
        logger.info(msg)

    @property
    def xml(self):
        with open(path.splitext(self.fp_input_file)[0] + '.xml', 'r') as f:
            xml = f.read()
        return xml

    @property
    def fp_input_file(self):
        return self.__fp

    @property
    def fp_safir_exe(self):
        return self.__fp_safir_exe

    @fp_input_file.setter
    def fp_input_file(self, fp: str):
        if path.exists(fp) and path.isfile(fp):
            self.__fp = fp
        else:
            raise ValueError

    @fp_safir_exe.setter
    def fp_safir_exe(self, fp: str):
        if path.exists(fp) and path.isfile(fp):
            self.__fp_safir_exe = fp
        else:
            raise ValueError

    @staticmethod
    def safir_single_run(fp_safir_exe: str, fp_in: str, fp_stdout: str = None):
        dir_in = os.path.dirname(fp_in)
        fn_in = os.path.basename(fp_in)

        if fn_in.endswith('.in'):
            fn_in = fn_in[:-3]

        # construct command
        cmd = f'{fp_safir_exe} {fn_in.rstrip(".in")}'

        if fp_stdout is not None:
            subprocess.run(args=cmd, cwd=dir_in, stdout=open(fp_stdout, 'w+'))
        else:
            subprocess.run(args=cmd, cwd=dir_in, stdout=open(os.devnull, 'w'))

    @staticmethod
    def update_params(fp_in: str, suffix: str = None, **kwargs):
        with open(fp_in, 'r') as f:
            safir_in = f.read()

        if len(kwargs) > 0:
            safir_in_new = safir_in.format(**kwargs)
        else:
            safir_in_new = safir_in

        fn_name, fn_suffix = os.path.splitext(os.path.basename(fp_in))

        i = 0
        while True:
            if i > 99:
                raise ValueError

            if suffix is not None:
                fn_in_new = f'{fn_name}{suffix}{fn_suffix}'
            else:
                fn_in_new = f'{fn_name}_{i:02d}{fn_suffix}'

            fp_in_new = os.path.join(os.path.dirname(fp_in), fn_in_new)

            if os.path.exists(fp_in_new):
                i += 1
                continue
            else:
                with open(fp_in_new, 'w+') as f:
                    f.write(safir_in_new)
                return fp_in_new


class Thermal2D(Thermal2DRun, Thermal2DPPXML):
    def __init__(self):
        super().__init__()


def safir_single_run(fp_safir_exe: str, fp_in: str, fp_stdout: str = None):
    dir_in = os.path.dirname(fp_in)
    fn_in = os.path.basename(fp_in)

    if fn_in.endswith('.in'):
        fn_in = fn_in[:-3]

    # construct command
    cmd = f'{fp_safir_exe} {fn_in.rstrip(".in")}'

    if fp_stdout is not None:
        subprocess.run(args=cmd, cwd=dir_in, stdout=open(fp_stdout, 'w+'))
    else:
        subprocess.run(args=cmd, cwd=dir_in, stdout=open(os.devnull, 'w'))


def batch_run_worker(args: List) -> List:
    def worker(
            cmd: str,
            cwd: str,
            fp_stdout: str = None,
            timeout_seconds: int = 1 * 60,
    ) -> List:
        try:
            if fp_stdout:
                subprocess.call(cmd, cwd=cwd, timeout=timeout_seconds, stdout=open(fp_stdout, 'w+'))
            else:
                subprocess.call(cmd, cwd=cwd, timeout=timeout_seconds, stdout=open(os.devnull, 'w'))
            return [cmd, 'Success']
        except subprocess.TimeoutExpired:
            return [cmd, 'Timed out']

    kwargs, q = args
    result = worker(**kwargs)
    q.put(1)
    return result


def batch_run(list_kwargs_in: List[Dict], func_mp: Callable = batch_run_worker, n_proc: int = 1, dir_work: str = None,
              qt_progress_signal=None):
    # ------------------------------------------
    # prepare variables used for multiprocessing
    # ------------------------------------------
    m, p = mp.Manager(), mp.Pool(n_proc, maxtasksperchild=1000)
    q = m.Queue()
    jobs = p.map_async(func_mp, [(dict_, q) for dict_ in list_kwargs_in])
    n_simulations = len(list_kwargs_in)

    # ---------------------
    # multiprocessing start
    # ---------------------
    while True:
        if jobs.ready():
            if qt_progress_signal:
                qt_progress_signal.emit(100)
            break  # complete
        else:
            if qt_progress_signal:
                qt_progress_signal.emit(int(q.qsize() / n_simulations * 100))
            time.sleep(1)  # in progress

    # --------------------------------------------
    # pull results and close multiprocess pipeline
    # --------------------------------------------
    p.close()
    p.join()
    mp_out = jobs.get()
    time.sleep(0.5)

    # ----------------------
    # save and print summary
    # ----------------------
    if dir_work:
        out = mp_out
        len_1 = int(max([len(' '.join(i[0])) for i in out]))
        summary = '\n'.join([f'{" ".join(i[0]):<{len_1}} - {i[1]:<{len_1}}' for i in out])
        print(summary)
        with open(os.path.join(dir_work, 'summary.txt'), 'w+') as f:
            f.write(summary)

    return mp_out


if __name__ == '__main__':
    model = Thermal2DPPXML()
    fp = r'C:\Users\IanFu\Desktop\!MMC Trinity\01 analysis\trial_01\validation.gid\validation.XML'
    with open(fp, 'r') as f:
        model.xml = f.read()
    model.get_nodes_temp([1, 2, 3])
