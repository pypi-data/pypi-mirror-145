'''This Python code is an automatically generated wrapper
for Fortran code made by 'fmodpy'. The original documentation
for the Fortran source code follows.


'''

import os
import ctypes
import platform
import numpy

# --------------------------------------------------------------------
#               CONFIGURATION
# 
_verbose = True
_fort_compiler = "gfortran"
_shared_object_name = "fmath." + platform.machine() + ".so"
_this_directory = os.path.dirname(os.path.abspath(__file__))
_path_to_lib = os.path.join(_this_directory, _shared_object_name)
_compile_options = ['-fPIC', '-shared', '-O3', '-lblas', '-llapack']
_ordered_dependencies = ['fmath.f90', 'fmath_c_wrapper.f90']
# 
# --------------------------------------------------------------------
#               AUTO-COMPILING
#
# Try to import the existing object. If that fails, recompile and then try.
try:
    clib = ctypes.CDLL(_path_to_lib)
except:
    # Remove the shared object if it exists, because it is faulty.
    if os.path.exists(_shared_object_name):
        os.remove(_shared_object_name)
    # Compile a new shared object.
    _command = " ".join([_fort_compiler] + _compile_options + ["-o", _shared_object_name] + _ordered_dependencies)
    if _verbose:
        print("Running system command with arguments")
        print("  ", _command)
    # Run the compilation command.
    import subprocess
    subprocess.run(_command, shell=True, cwd=_this_directory)
    # Import the shared object file as a C library with ctypes.
    clib = ctypes.CDLL(_path_to_lib)
# --------------------------------------------------------------------


class fmath:
    ''''''

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine ORTHOGONALIZE
    
    def orthogonalize(self, a, lengths=None, rank=None):
        '''! Orthogonalize and normalize column vectors of A with pivoting.'''
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_int(a.shape[0])
        a_dim_2 = ctypes.c_int(a.shape[1])
        
        # Setting up "lengths"
        if (lengths is None):
            lengths = numpy.zeros(shape=(a.shape[1]), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(lengths), numpy.ndarray)) or
              (not numpy.asarray(lengths).flags.f_contiguous) or
              (not (lengths.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'lengths' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            lengths = numpy.asarray(lengths, dtype=ctypes.c_float, order='F')
        lengths_dim_1 = ctypes.c_int(lengths.shape[0])
        
        # Setting up "rank"
        rank_present = ctypes.c_bool(True)
        if (rank is None):
            rank_present = ctypes.c_bool(False)
            rank = ctypes.c_int()
        else:
            rank = ctypes.c_int(rank)
    
        # Call C-accessible Fortran wrapper.
        clib.c_orthogonalize(ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(lengths_dim_1), ctypes.c_void_p(lengths.ctypes.data), ctypes.byref(rank_present), ctypes.byref(rank))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return a, lengths, (rank.value if rank_present else None)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine SVD
    
    def svd(self, a, s=None, vt=None, rank=None, steps=None, bias=None):
        '''! Compute the singular values and right singular vectors for matrix A.'''
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_int(a.shape[0])
        a_dim_2 = ctypes.c_int(a.shape[1])
        
        # Setting up "s"
        if (s is None):
            s = numpy.zeros(shape=(min(a.shape[0],a.shape[1])), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(s), numpy.ndarray)) or
              (not numpy.asarray(s).flags.f_contiguous) or
              (not (s.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 's' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            s = numpy.asarray(s, dtype=ctypes.c_float, order='F')
        s_dim_1 = ctypes.c_int(s.shape[0])
        
        # Setting up "vt"
        if (vt is None):
            vt = numpy.zeros(shape=(min(a.shape[0],a.shape[1]), min(a.shape[0],a.shape[1])), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(vt), numpy.ndarray)) or
              (not numpy.asarray(vt).flags.f_contiguous) or
              (not (vt.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'vt' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            vt = numpy.asarray(vt, dtype=ctypes.c_float, order='F')
        vt_dim_1 = ctypes.c_int(vt.shape[0])
        vt_dim_2 = ctypes.c_int(vt.shape[1])
        
        # Setting up "rank"
        rank_present = ctypes.c_bool(True)
        if (rank is None):
            rank_present = ctypes.c_bool(False)
            rank = ctypes.c_int()
        else:
            rank = ctypes.c_int(rank)
        
        # Setting up "steps"
        steps_present = ctypes.c_bool(True)
        if (steps is None):
            steps_present = ctypes.c_bool(False)
            steps = ctypes.c_int()
        else:
            steps = ctypes.c_int(steps)
        if (type(steps) is not ctypes.c_int): steps = ctypes.c_int(steps)
        
        # Setting up "bias"
        bias_present = ctypes.c_bool(True)
        if (bias is None):
            bias_present = ctypes.c_bool(False)
            bias = ctypes.c_float()
        else:
            bias = ctypes.c_float(bias)
        if (type(bias) is not ctypes.c_float): bias = ctypes.c_float(bias)
    
        # Call C-accessible Fortran wrapper.
        clib.c_svd(ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(s_dim_1), ctypes.c_void_p(s.ctypes.data), ctypes.byref(vt_dim_1), ctypes.byref(vt_dim_2), ctypes.c_void_p(vt.ctypes.data), ctypes.byref(rank_present), ctypes.byref(rank), ctypes.byref(steps_present), ctypes.byref(steps), ctypes.byref(bias_present), ctypes.byref(bias))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return s, vt, (rank.value if rank_present else None)

fmath = fmath()

