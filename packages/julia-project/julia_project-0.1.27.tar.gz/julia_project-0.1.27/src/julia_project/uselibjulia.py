import ctypes
import shutil
import os
import subprocess

def load_libjulia(julia_path=None, project=None):
    # Find the Julia library
    if julia_path is None:
        julia_path = shutil.which("julia") or ''
    if project is None:
        project =  "."
    cmd = [julia_path, '--project='+project, '--history-file=no',
           '--startup-file=no', '-O0', '--compile=min', '-e',
           'import Libdl; print(abspath(Libdl.dlpath("libjulia")))']
    libjulia_path = subprocess.run(cmd, check=True, capture_output=True, encoding='utf8').stdout
    assert os.path.exists(libjulia_path)

    current_dir = os.getcwd()

    julia_toplevel = os.path.dirname(os.path.dirname(libjulia_path))
    bindir = os.path.realpath(os.path.join(julia_toplevel, "bin"))

    try:
        os.chdir(os.path.dirname(libjulia_path))
        libjulia = ctypes.PyDLL(libjulia_path, ctypes.RTLD_GLOBAL) # <-- avoids segfault
        libjulia.jl_init__threading.argtypes = []
        libjulia.jl_init__threading.restype = None
        libjulia.jl_init__threading()
        libjulia.jl_eval_string.argtypes = [ctypes.c_char_p]
        libjulia.jl_eval_string.restype = ctypes.c_void_p
    finally:
        os.chdir(current_dir)

    return libjulia


the_libjulia = load_libjulia()


def eval_str(code="", libjulia=the_libjulia):
    return libjulia.jl_eval_string(code.encode('utf8'))

def runcom():
    eval_str("import Pkg; Pkg.activate(\"../venv/julia_project/myjuliamod-1.7.2/\"); Pkg.instantiate()")
