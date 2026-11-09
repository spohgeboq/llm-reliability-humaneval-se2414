import multiprocessing
import traceback
import sys
import os

if sys.platform != "win32":
    try:
        multiprocessing.set_start_method("fork", force=True)
    except RuntimeError:
        pass


def _worker_exec(full_code: str, result_queue: multiprocessing.Queue):
    try:
        exec_globals = {
            "__name__": "__main__",
            "__builtins__": __builtins__,
        }
        exec(full_code, exec_globals)
        result_queue.put(("PASSED", ""))
    except AssertionError as ae:
        result_queue.put(("FAILED_ASSERTION", str(ae) or "Assertion failed"))
    except SyntaxError as se:
        result_queue.put(("SYNTAX_ERROR", f"{type(se).__name__}: {str(se)}"))
    except NameError as ne:
        result_queue.put(("NAME_ERROR", f"{type(ne).__name__}: {str(ne)}"))
    except (IndexError, KeyError) as ie:
        result_queue.put(("BOUNDARY_INDEX_ERROR", f"{type(ie).__name__}: {str(ie)}"))
    except Exception as e:
        result_queue.put(("RUNTIME_ERROR", f"{type(e).__name__}: {str(e)}"))


def execute_in_sandbox(candidate_code: str, test_code: str, entry_point: str, timeout: float = 3.0) -> dict:
    runnable = (
        "import math\n"
        "import re\n"
        "import sys\n"
        "import collections\n"
        "import itertools\n"
        "import functools\n"
        "import heapq\n"
        "from typing import List, Dict, Tuple, Set, Optional, Any, Union\n\n"
        f"{candidate_code}\n\n"
        f"{test_code}\n\n"
        f"check({entry_point})\n"
    )

    q = multiprocessing.Queue()
    proc = multiprocessing.Process(target=_worker_exec, args=(runnable, q))
    proc.start()
    proc.join(timeout=timeout)

    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=0.5)
        if proc.is_alive():
            try:
                os.kill(proc.pid, 9)
            except OSError:
                pass
        return {
            "status": "TIMEOUT",
            "passed": False,
            "details": f"Process exceeded watchdog timeout threshold of {timeout:.1f}s"
        }

    if not q.empty():
        status, details = q.get()
        return {
            "status": status,
            "passed": (status == "PASSED"),
            "details": details
        }
    else:
        return {
            "status": "RUNTIME_ERROR",
            "passed": False,
            "details": f"Process exited unexpectedly with code {proc.exitcode}"
        }
