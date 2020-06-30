import os
import subprocess
from typing import List, Dict, Callable
import multiprocessing as mp
import time


def safir_batch_run_worker(args: List) -> List:
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


def safir_batch_run(
        list_kwargs_in: List[Dict],
        func_mp: Callable = safir_batch_run_worker,
        n_proc: int = 1,
        dir_work: str = None,
        qt_progress_signal=None
):

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
