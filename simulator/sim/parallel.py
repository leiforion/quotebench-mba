"""Process-level parallelism for the independent DES replications.

The DES runs are CPU-bound and independent (different seeds/variants), so the
right tool is multiple processes, not asyncio/threads (which cannot run Python
bytecode concurrently under the GIL and would give no speedup on this workload).
Each task returns a small picklable result (a LaneEconomics), so inter-process
transfer is cheap even though each DES holds tens of thousands of records.

pmap preserves task order and logs progress as tasks complete. jobs<=1 (or a
single task) runs serially in-process, which keeps profiling and debugging
simple and avoids pool start-up cost.
"""
import os

from .runlog import log


def default_jobs(n_tasks):
    """Sensible worker count: cap at task count and available cores, and leave
    one core free on larger machines. Override with SIM_JOBS."""
    env = os.environ.get("SIM_JOBS")
    if env:
        try:
            return max(1, int(env))
        except ValueError:
            pass
    cores = os.cpu_count() or 1
    return max(1, min(n_tasks, cores - 1 if cores > 2 else cores))


def pmap(worker, tasks, jobs=None, desc="task"):
    """Map worker over tasks (in task order). Logs '<desc> k/n' as each lands."""
    tasks = list(tasks)
    n = len(tasks)
    if n == 0:
        return []
    jobs = jobs if jobs is not None else default_jobs(n)
    jobs = min(jobs, n)

    if jobs <= 1:
        out = []
        for i, t in enumerate(tasks, 1):
            out.append(worker(t))
            log(f"{desc} {i}/{n} done")
        return out

    from concurrent.futures import ProcessPoolExecutor, as_completed
    log(f"{desc}: {n} tasks across {jobs} processes")
    results = [None] * n
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(worker, t): i for i, t in enumerate(tasks)}
        done = 0
        for fut in as_completed(futs):
            i = futs[fut]
            results[i] = fut.result()
            done += 1
            log(f"{desc} {done}/{n} done")
    return results
