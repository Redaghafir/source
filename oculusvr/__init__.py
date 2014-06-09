import ctypes, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import platform
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        unix_lib_dirs_list = ['/lib', '/usr/lib', '/lib64', '/usr/lib64']
        if sys.platform.startswith('linux'):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            bitage = platform.architecture()[0]
            if bitage.startswith('32'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu']
            elif bitage.startswith('64'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']
            else:
                # guess...
                unix_lib_dirs_list += glob.glob('/lib/*linux-gnu')
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

###############################################################################
#                                                                             #
# Begin libraries                                                             #
#                                                                             #
###############################################################################
import struct

suffix = "-x86"
prefix = "win32"
file = "OVR_C.dll"
if 64 == 8 * struct.calcsize("P"):
    suffix = "-x86-64"
if ("linux" in sys.platform):
    file = "libOVR_C.so"
    prefix = "linux"
elif ("darwin" in sys.platform):
    file = "libOVR_C.dylib"
    prefix = "darwin"

libfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), prefix + suffix, file)
_libs["OVR_C"] = load_library(libfile)

# 1 libraries

# No modules

GLuint = c_uint # OVR_CAPI.h: 26

uintptr_t = POINTER(c_uint) # OVR_CAPI.h: 27

ovrBool = c_char # OVR_CAPI.h: 35

# OVR_CAPI.h: 55
class struct_ovrVector2i_(Structure):
    pass

struct_ovrVector2i_.__slots__ = [
    'x',
    'y',
]
struct_ovrVector2i_._fields_ = [
    ('x', c_int),
    ('y', c_int),
]

vector2i = struct_ovrVector2i_ # OVR_CAPI.h: 55

# OVR_CAPI.h: 59
class struct_ovrSizei_(Structure):
    pass

struct_ovrSizei_.__slots__ = [
    'w',
    'h',
]
struct_ovrSizei_._fields_ = [
    ('w', c_int),
    ('h', c_int),
]

sizei = struct_ovrSizei_ # OVR_CAPI.h: 59

# OVR_CAPI.h: 64
class struct_ovrRecti_(Structure):
    pass

struct_ovrRecti_.__slots__ = [
    'Pos',
    'Size',
]
struct_ovrRecti_._fields_ = [
    ('Pos', vector2i),
    ('Size', sizei),
]

recti = struct_ovrRecti_ # OVR_CAPI.h: 64

# OVR_CAPI.h: 70
class struct_ovrQuatf_(Structure):
    pass

struct_ovrQuatf_.__slots__ = [
    'x',
    'y',
    'z',
    'w',
]
struct_ovrQuatf_._fields_ = [
    ('x', c_float),
    ('y', c_float),
    ('z', c_float),
    ('w', c_float),
]

quat = struct_ovrQuatf_ # OVR_CAPI.h: 70

# OVR_CAPI.h: 74
class struct_ovrVector2f_(Structure):
    pass

struct_ovrVector2f_.__slots__ = [
    'x',
    'y',
]
struct_ovrVector2f_._fields_ = [
    ('x', c_float),
    ('y', c_float),
]

vec2 = struct_ovrVector2f_ # OVR_CAPI.h: 74

# OVR_CAPI.h: 78
class struct_ovrVector3f_(Structure):
    pass

struct_ovrVector3f_.__slots__ = [
    'x',
    'y',
    'z',
]
struct_ovrVector3f_._fields_ = [
    ('x', c_float),
    ('y', c_float),
    ('z', c_float),
]

vec3 = struct_ovrVector3f_ # OVR_CAPI.h: 78

# OVR_CAPI.h: 82
class struct_ovrMatrix4f_(Structure):
    pass

struct_ovrMatrix4f_.__slots__ = [
    'M',
]
struct_ovrMatrix4f_._fields_ = [
    ('M', (c_float * 4) * 4),
]

mat4 = struct_ovrMatrix4f_ # OVR_CAPI.h: 82

# OVR_CAPI.h: 88
class struct_ovrPosef_(Structure):
    pass

struct_ovrPosef_.__slots__ = [
    'Orientation',
    'Position',
]
struct_ovrPosef_._fields_ = [
    ('Orientation', quat),
    ('Position', vec3),
]

pose = struct_ovrPosef_ # OVR_CAPI.h: 88

# OVR_CAPI.h: 99
class struct_ovrPoseStatef_(Structure):
    pass

struct_ovrPoseStatef_.__slots__ = [
    'Pose',
    'AngularVelocity',
    'LinearVelocity',
    'AngularAcceleration',
    'LinearAcceleration',
    'TimeInSeconds',
]
struct_ovrPoseStatef_._fields_ = [
    ('Pose', pose),
    ('AngularVelocity', vec3),
    ('LinearVelocity', vec3),
    ('AngularAcceleration', vec3),
    ('LinearAcceleration', vec3),
    ('TimeInSeconds', c_double),
]

pose_state = struct_ovrPoseStatef_ # OVR_CAPI.h: 99

# OVR_CAPI.h: 110
class struct_ovrFovPort_(Structure):
    pass

struct_ovrFovPort_.__slots__ = [
    'UpTan',
    'DownTan',
    'LeftTan',
    'RightTan',
]
struct_ovrFovPort_._fields_ = [
    ('UpTan', c_float),
    ('DownTan', c_float),
    ('LeftTan', c_float),
    ('RightTan', c_float),
]

fov_port = struct_ovrFovPort_ # OVR_CAPI.h: 110

enum_anon_1 = c_int # OVR_CAPI.h: 125

ovrHmd_None = 0 # OVR_CAPI.h: 125

ovrHmd_DK1 = 3 # OVR_CAPI.h: 125

ovrHmd_DKHD = 4 # OVR_CAPI.h: 125

ovrHmd_CrystalCoveProto = 5 # OVR_CAPI.h: 125

ovrHmd_DK2 = 6 # OVR_CAPI.h: 125

ovrHmd_Other = (ovrHmd_DK2 + 1) # OVR_CAPI.h: 125

ovrHmdType = enum_anon_1 # OVR_CAPI.h: 125

enum_anon_2 = c_int # OVR_CAPI.h: 155

ovrHmdCap_Present = 1 # OVR_CAPI.h: 155

ovrHmdCap_Available = 2 # OVR_CAPI.h: 155

ovrHmdCap_LowPersistence = 128 # OVR_CAPI.h: 155

ovrHmdCap_LatencyTest = 256 # OVR_CAPI.h: 155

ovrHmdCap_DynamicPrediction = 512 # OVR_CAPI.h: 155

ovrHmdCap_NoVSync = 4096 # OVR_CAPI.h: 155

ovrHmdCap_NoRestore = 16384 # OVR_CAPI.h: 155

ovrHmdCap_Writable_Mask = 4992 # OVR_CAPI.h: 155

ovrHmdCaps = enum_anon_2 # OVR_CAPI.h: 155

enum_anon_3 = c_int # OVR_CAPI.h: 166

ovrSensorCap_Orientation = 16 # OVR_CAPI.h: 166

ovrSensorCap_YawCorrection = 32 # OVR_CAPI.h: 166

ovrSensorCap_Position = 64 # OVR_CAPI.h: 166

ovrSensorCaps = enum_anon_3 # OVR_CAPI.h: 166

enum_anon_4 = c_int # OVR_CAPI.h: 175

ovrDistortionCap_Chromatic = 1 # OVR_CAPI.h: 175

ovrDistortionCap_TimeWarp = 2 # OVR_CAPI.h: 175

ovrDistortionCap_NoSwapBuffers = 4 # OVR_CAPI.h: 175

ovrDistortionCap_Vignette = 8 # OVR_CAPI.h: 175

ovrDistortionCaps = enum_anon_4 # OVR_CAPI.h: 175

enum_anon_5 = c_int # OVR_CAPI.h: 186

ovrEye_Left = 0 # OVR_CAPI.h: 186

ovrEye_Right = 1 # OVR_CAPI.h: 186

ovrEye_Count = 2 # OVR_CAPI.h: 186

ovrEyeType = enum_anon_5 # OVR_CAPI.h: 186

# OVR_CAPI.h: 190
class struct_ovrHmdStruct(Structure):
    pass

hmd = POINTER(struct_ovrHmdStruct) # OVR_CAPI.h: 190

# OVR_CAPI.h: 232
class struct_ovrHmdDesc_(Structure):
    pass

struct_ovrHmdDesc_.__slots__ = [
    'Handle',
    'Type',
    'ProductName',
    'Manufacturer',
    'HmdCaps',
    'SensorCaps',
    'DistortionCaps',
    'Resolution',
    'WindowsPos',
    'DefaultEyeFov',
    'MaxEyeFov',
    'EyeRenderOrder',
    'DisplayDeviceName',
    'DisplayId',
]
struct_ovrHmdDesc_._fields_ = [
    ('Handle', hmd),
    ('Type', ovrHmdType),
    ('ProductName', String),
    ('Manufacturer', String),
    ('HmdCaps', c_uint),
    ('SensorCaps', c_uint),
    ('DistortionCaps', c_uint),
    ('Resolution', sizei),
    ('WindowsPos', vector2i),
    ('DefaultEyeFov', fov_port * ovrEye_Count),
    ('MaxEyeFov', fov_port * ovrEye_Count),
    ('EyeRenderOrder', ovrEyeType * ovrEye_Count),
    ('DisplayDeviceName', String),
    ('DisplayId', c_int),
]

hmd_desc = struct_ovrHmdDesc_ # OVR_CAPI.h: 232

enum_anon_6 = c_int # OVR_CAPI.h: 252

ovrStatus_OrientationTracked = 1 # OVR_CAPI.h: 252

ovrStatus_PositionTracked = 2 # OVR_CAPI.h: 252

ovrStatus_PositionConnected = 32 # OVR_CAPI.h: 252

ovrStatus_HmdConnected = 128 # OVR_CAPI.h: 252

ovrStatusBits = enum_anon_6 # OVR_CAPI.h: 252

# OVR_CAPI.h: 270
class struct_ovrSensorState_(Structure):
    pass

struct_ovrSensorState_.__slots__ = [
    'Predicted',
    'Recorded',
    'Temperature',
    'StatusFlags',
]
struct_ovrSensorState_._fields_ = [
    ('Predicted', pose_state),
    ('Recorded', pose_state),
    ('Temperature', c_float),
    ('StatusFlags', c_uint),
]

sensor_state = struct_ovrSensorState_ # OVR_CAPI.h: 270

# OVR_CAPI.h: 281
class struct_ovrSensorDesc_(Structure):
    pass

struct_ovrSensorDesc_.__slots__ = [
    'VendorId',
    'ProductId',
    'SerialNumber',
]
struct_ovrSensorDesc_._fields_ = [
    ('VendorId', c_short),
    ('ProductId', c_short),
    ('SerialNumber', c_char * 24),
]

sensor_desc = struct_ovrSensorDesc_ # OVR_CAPI.h: 281

# OVR_CAPI.h: 313
class struct_ovrFrameTiming_(Structure):
    pass

struct_ovrFrameTiming_.__slots__ = [
    'DeltaSeconds',
    'ThisFrameSeconds',
    'TimewarpPointSeconds',
    'NextFrameSeconds',
    'ScanoutMidpointSeconds',
    'EyeScanoutSeconds',
]
struct_ovrFrameTiming_._fields_ = [
    ('DeltaSeconds', c_float),
    ('ThisFrameSeconds', c_double),
    ('TimewarpPointSeconds', c_double),
    ('NextFrameSeconds', c_double),
    ('ScanoutMidpointSeconds', c_double),
    ('EyeScanoutSeconds', c_double * 2),
]

frame_timing = struct_ovrFrameTiming_ # OVR_CAPI.h: 313

# OVR_CAPI.h: 330
class struct_ovrEyeRenderDesc_(Structure):
    pass

struct_ovrEyeRenderDesc_.__slots__ = [
    'Eye',
    'Fov',
    'DistortedViewport',
    'PixelsPerTanAngleAtCenter',
    'ViewAdjust',
]
struct_ovrEyeRenderDesc_._fields_ = [
    ('Eye', ovrEyeType),
    ('Fov', fov_port),
    ('DistortedViewport', recti),
    ('PixelsPerTanAngleAtCenter', vec2),
    ('ViewAdjust', vec3),
]

eye_render_desc = struct_ovrEyeRenderDesc_ # OVR_CAPI.h: 330

enum_anon_7 = c_int # OVR_CAPI.h: 354

ovrRenderAPI_None = 0 # OVR_CAPI.h: 354

ovrRenderAPI_OpenGL = (ovrRenderAPI_None + 1) # OVR_CAPI.h: 354

ovrRenderAPI_Android_GLES = (ovrRenderAPI_OpenGL + 1) # OVR_CAPI.h: 354

ovrRenderAPI_D3D9 = (ovrRenderAPI_Android_GLES + 1) # OVR_CAPI.h: 354

ovrRenderAPI_D3D10 = (ovrRenderAPI_D3D9 + 1) # OVR_CAPI.h: 354

ovrRenderAPI_D3D11 = (ovrRenderAPI_D3D10 + 1) # OVR_CAPI.h: 354

ovrRenderAPI_Count = (ovrRenderAPI_D3D11 + 1) # OVR_CAPI.h: 354

ovrRenderAPIType = enum_anon_7 # OVR_CAPI.h: 354

# OVR_CAPI.h: 369
class struct_ovrRenderAPIConfig_(Structure):
    pass

struct_ovrRenderAPIConfig_.__slots__ = [
    'API',
    'RTSize',
    'Multisample',
    'PlatformData',
]
struct_ovrRenderAPIConfig_._fields_ = [
    ('API', ovrRenderAPIType),
    ('RTSize', sizei),
    ('Multisample', c_int),
    ('PlatformData', uintptr_t * 8),
]

ovrRenderAPIConfig = struct_ovrRenderAPIConfig_ # OVR_CAPI.h: 369

# OVR_CAPI.h: 385
class struct_ovrTexture_(Structure):
    pass

struct_ovrTexture_.__slots__ = [
    'API',
    'TextureSize',
    'RenderViewport',
    'TexId',
    'PlatformData',
]
struct_ovrTexture_._fields_ = [
    ('API', ovrRenderAPIType),
    ('TextureSize', sizei),
    ('RenderViewport', recti),
    ('TexId', GLuint),
    ('PlatformData', uintptr_t * 7),
]

texture = struct_ovrTexture_ # OVR_CAPI.h: 385

# OVR_CAPI.h: 622
class struct_ovrDistortionVertex_(Structure):
    pass

struct_ovrDistortionVertex_.__slots__ = [
    'Pos',
    'TimeWarpFactor',
    'VignetteFactor',
    'TexR',
    'TexG',
    'TexB',
]
struct_ovrDistortionVertex_._fields_ = [
    ('Pos', vec2),
    ('TimeWarpFactor', c_float),
    ('VignetteFactor', c_float),
    ('TexR', vec2),
    ('TexG', vec2),
    ('TexB', vec2),
]

ovrDistortionVertex = struct_ovrDistortionVertex_ # OVR_CAPI.h: 622

# OVR_CAPI.h: 632
class struct_ovrDistortionMesh_(Structure):
    pass

struct_ovrDistortionMesh_.__slots__ = [
    'pVertexData',
    'pIndexData',
    'VertexCount',
    'IndexCount',
]
struct_ovrDistortionMesh_._fields_ = [
    ('pVertexData', POINTER(ovrDistortionVertex)),
    ('pIndexData', POINTER(c_ushort)),
    ('VertexCount', c_uint),
    ('IndexCount', c_uint),
]

ovrDistortionMesh = struct_ovrDistortionMesh_ # OVR_CAPI.h: 632

# OVR_CAPI.h: 421
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovr_Initialize'):
        continue
    ovr_Initialize = _lib.ovr_Initialize
    ovr_Initialize.argtypes = []
    ovr_Initialize.restype = ovrBool
    break

# OVR_CAPI.h: 422
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovr_Shutdown'):
        continue
    ovr_Shutdown = _lib.ovr_Shutdown
    ovr_Shutdown.argtypes = []
    ovr_Shutdown.restype = None
    break

# OVR_CAPI.h: 427
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_Detect'):
        continue
    ovrHmd_Detect = _lib.ovrHmd_Detect
    ovrHmd_Detect.argtypes = []
    ovrHmd_Detect.restype = c_int
    break

# OVR_CAPI.h: 433
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_Create'):
        continue
    ovrHmd_Create = _lib.ovrHmd_Create
    ovrHmd_Create.argtypes = [c_int]
    ovrHmd_Create.restype = hmd
    break

# OVR_CAPI.h: 434
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_Destroy'):
        continue
    ovrHmd_Destroy = _lib.ovrHmd_Destroy
    ovrHmd_Destroy.argtypes = [hmd]
    ovrHmd_Destroy.restype = None
    break

# OVR_CAPI.h: 438
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_CreateDebug'):
        continue
    ovrHmd_CreateDebug = _lib.ovrHmd_CreateDebug
    ovrHmd_CreateDebug.argtypes = [ovrHmdType]
    ovrHmd_CreateDebug.restype = hmd
    break

# OVR_CAPI.h: 444
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetLastError'):
        continue
    ovrHmd_GetLastError = _lib.ovrHmd_GetLastError
    ovrHmd_GetLastError.argtypes = [hmd]
    if sizeof(c_int) == sizeof(c_void_p):
        ovrHmd_GetLastError.restype = ReturnString
    else:
        ovrHmd_GetLastError.restype = String
        ovrHmd_GetLastError.errcheck = ReturnString
    break

# OVR_CAPI.h: 452
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetEnabledCaps'):
        continue
    ovrHmd_GetEnabledCaps = _lib.ovrHmd_GetEnabledCaps
    ovrHmd_GetEnabledCaps.argtypes = [hmd]
    ovrHmd_GetEnabledCaps.restype = c_uint
    break

# OVR_CAPI.h: 456
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_SetEnabledCaps'):
        continue
    ovrHmd_SetEnabledCaps = _lib.ovrHmd_SetEnabledCaps
    ovrHmd_SetEnabledCaps.argtypes = [hmd, c_uint]
    ovrHmd_SetEnabledCaps.restype = None
    break

# OVR_CAPI.h: 472
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_StartSensor'):
        continue
    ovrHmd_StartSensor = _lib.ovrHmd_StartSensor
    ovrHmd_StartSensor.argtypes = [hmd, c_uint, c_uint]
    ovrHmd_StartSensor.restype = ovrBool
    break

# OVR_CAPI.h: 475
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_StopSensor'):
        continue
    ovrHmd_StopSensor = _lib.ovrHmd_StopSensor
    ovrHmd_StopSensor.argtypes = [hmd]
    ovrHmd_StopSensor.restype = None
    break

# OVR_CAPI.h: 477
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_ResetSensor'):
        continue
    ovrHmd_ResetSensor = _lib.ovrHmd_ResetSensor
    ovrHmd_ResetSensor.argtypes = [hmd]
    ovrHmd_ResetSensor.restype = None
    break

# OVR_CAPI.h: 484
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetSensorState'):
        continue
    ovrHmd_GetSensorState = _lib.ovrHmd_GetSensorState
    ovrHmd_GetSensorState.argtypes = [hmd, c_double]
    ovrHmd_GetSensorState.restype = sensor_state
    break

# OVR_CAPI.h: 488
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetSensorDesc'):
        continue
    ovrHmd_GetSensorDesc = _lib.ovrHmd_GetSensorDesc
    ovrHmd_GetSensorDesc.argtypes = [hmd, POINTER(sensor_desc)]
    ovrHmd_GetSensorDesc.restype = ovrBool
    break

# OVR_CAPI.h: 495
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetDesc'):
        continue
    ovrHmd_GetDesc = _lib.ovrHmd_GetDesc
    ovrHmd_GetDesc.argtypes = [hmd, POINTER(hmd_desc)]
    ovrHmd_GetDesc.restype = None
    break

# OVR_CAPI.h: 502
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetFovTextureSize'):
        continue
    ovrHmd_GetFovTextureSize = _lib.ovrHmd_GetFovTextureSize
    ovrHmd_GetFovTextureSize.argtypes = [hmd, ovrEyeType, fov_port, c_float]
    ovrHmd_GetFovTextureSize.restype = sizei
    break

# OVR_CAPI.h: 544
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_ConfigureRendering'):
        continue
    ovrHmd_ConfigureRendering = _lib.ovrHmd_ConfigureRendering
    ovrHmd_ConfigureRendering.argtypes = [hmd, POINTER(ovrRenderAPIConfig), c_uint, fov_port * 2, eye_render_desc * 2]
    ovrHmd_ConfigureRendering.restype = ovrBool
    break

# OVR_CAPI.h: 555
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_BeginFrame'):
        continue
    ovrHmd_BeginFrame = _lib.ovrHmd_BeginFrame
    ovrHmd_BeginFrame.argtypes = [hmd, c_uint]
    ovrHmd_BeginFrame.restype = frame_timing
    break

# OVR_CAPI.h: 561
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_EndFrame'):
        continue
    ovrHmd_EndFrame = _lib.ovrHmd_EndFrame
    ovrHmd_EndFrame.argtypes = [hmd]
    ovrHmd_EndFrame.restype = None
    break

# OVR_CAPI.h: 571
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_BeginEyeRender'):
        continue
    ovrHmd_BeginEyeRender = _lib.ovrHmd_BeginEyeRender
    ovrHmd_BeginEyeRender.argtypes = [hmd, ovrEyeType]
    ovrHmd_BeginEyeRender.restype = pose
    break

# OVR_CAPI.h: 579
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_EndEyeRender'):
        continue
    ovrHmd_EndEyeRender = _lib.ovrHmd_EndEyeRender
    ovrHmd_EndEyeRender.argtypes = [hmd, ovrEyeType, pose, POINTER(texture)]
    ovrHmd_EndEyeRender.restype = None
    break

# OVR_CAPI.h: 606
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetRenderDesc'):
        continue
    ovrHmd_GetRenderDesc = _lib.ovrHmd_GetRenderDesc
    ovrHmd_GetRenderDesc.argtypes = [hmd, ovrEyeType, fov_port]
    ovrHmd_GetRenderDesc.restype = eye_render_desc
    break

# OVR_CAPI.h: 642
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_CreateDistortionMesh'):
        continue
    ovrHmd_CreateDistortionMesh = _lib.ovrHmd_CreateDistortionMesh
    ovrHmd_CreateDistortionMesh.argtypes = [hmd, ovrEyeType, fov_port, c_uint, POINTER(ovrDistortionMesh)]
    ovrHmd_CreateDistortionMesh.restype = ovrBool
    break

# OVR_CAPI.h: 649
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_DestroyDistortionMesh'):
        continue
    ovrHmd_DestroyDistortionMesh = _lib.ovrHmd_DestroyDistortionMesh
    ovrHmd_DestroyDistortionMesh.argtypes = [POINTER(ovrDistortionMesh)]
    ovrHmd_DestroyDistortionMesh.restype = None
    break

# OVR_CAPI.h: 653
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetRenderScaleAndOffset'):
        continue
    ovrHmd_GetRenderScaleAndOffset = _lib.ovrHmd_GetRenderScaleAndOffset
    ovrHmd_GetRenderScaleAndOffset.argtypes = [fov_port, sizei, recti, vec2 * 2]
    ovrHmd_GetRenderScaleAndOffset.restype = None
    break

# OVR_CAPI.h: 660
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetFrameTiming'):
        continue
    ovrHmd_GetFrameTiming = _lib.ovrHmd_GetFrameTiming
    ovrHmd_GetFrameTiming.argtypes = [hmd, c_uint]
    ovrHmd_GetFrameTiming.restype = frame_timing
    break

# OVR_CAPI.h: 665
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_BeginFrameTiming'):
        continue
    ovrHmd_BeginFrameTiming = _lib.ovrHmd_BeginFrameTiming
    ovrHmd_BeginFrameTiming.argtypes = [hmd, c_uint]
    ovrHmd_BeginFrameTiming.restype = frame_timing
    break

# OVR_CAPI.h: 670
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_EndFrameTiming'):
        continue
    ovrHmd_EndFrameTiming = _lib.ovrHmd_EndFrameTiming
    ovrHmd_EndFrameTiming.argtypes = [hmd]
    ovrHmd_EndFrameTiming.restype = None
    break

# OVR_CAPI.h: 675
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_ResetFrameTiming'):
        continue
    ovrHmd_ResetFrameTiming = _lib.ovrHmd_ResetFrameTiming
    ovrHmd_ResetFrameTiming.argtypes = [hmd, c_uint]
    ovrHmd_ResetFrameTiming.restype = None
    break

# OVR_CAPI.h: 680
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetEyePose'):
        continue
    ovrHmd_GetEyePose = _lib.ovrHmd_GetEyePose
    ovrHmd_GetEyePose.argtypes = [hmd, ovrEyeType]
    ovrHmd_GetEyePose.restype = pose
    break

# OVR_CAPI.h: 687
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetEyeTimewarpMatrices'):
        continue
    ovrHmd_GetEyeTimewarpMatrices = _lib.ovrHmd_GetEyeTimewarpMatrices
    ovrHmd_GetEyeTimewarpMatrices.argtypes = [hmd, ovrEyeType, pose, mat4 * 2]
    ovrHmd_GetEyeTimewarpMatrices.restype = None
    break

# OVR_CAPI.h: 696
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrMatrix4f_Projection'):
        continue
    ovrMatrix4f_Projection = _lib.ovrMatrix4f_Projection
    ovrMatrix4f_Projection.argtypes = [fov_port, c_float, c_float, ovrBool]
    ovrMatrix4f_Projection.restype = mat4
    break

# OVR_CAPI.h: 702
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrMatrix4f_OrthoSubProjection'):
        continue
    ovrMatrix4f_OrthoSubProjection = _lib.ovrMatrix4f_OrthoSubProjection
    ovrMatrix4f_OrthoSubProjection.argtypes = [mat4, vec2, c_float, c_float]
    ovrMatrix4f_OrthoSubProjection.restype = mat4
    break

# OVR_CAPI.h: 707
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovr_GetTimeInSeconds'):
        continue
    ovr_GetTimeInSeconds = _lib.ovr_GetTimeInSeconds
    ovr_GetTimeInSeconds.argtypes = []
    ovr_GetTimeInSeconds.restype = c_double
    break

# OVR_CAPI.h: 710
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovr_WaitTillTime'):
        continue
    ovr_WaitTillTime = _lib.ovr_WaitTillTime
    ovr_WaitTillTime.argtypes = [c_double]
    ovr_WaitTillTime.restype = c_double
    break

# OVR_CAPI.h: 719
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_ProcessLatencyTest'):
        continue
    ovrHmd_ProcessLatencyTest = _lib.ovrHmd_ProcessLatencyTest
    ovrHmd_ProcessLatencyTest.argtypes = [hmd, c_ubyte * 3]
    ovrHmd_ProcessLatencyTest.restype = ovrBool
    break

# OVR_CAPI.h: 723
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetLatencyTestResult'):
        continue
    ovrHmd_GetLatencyTestResult = _lib.ovrHmd_GetLatencyTestResult
    ovrHmd_GetLatencyTestResult.argtypes = [hmd]
    if sizeof(c_int) == sizeof(c_void_p):
        ovrHmd_GetLatencyTestResult.restype = ReturnString
    else:
        ovrHmd_GetLatencyTestResult.restype = String
        ovrHmd_GetLatencyTestResult.errcheck = ReturnString
    break

# OVR_CAPI.h: 727
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetMeasuredLatencyTest2'):
        continue
    ovrHmd_GetMeasuredLatencyTest2 = _lib.ovrHmd_GetMeasuredLatencyTest2
    ovrHmd_GetMeasuredLatencyTest2.argtypes = [hmd]
    ovrHmd_GetMeasuredLatencyTest2.restype = c_double
    break

# OVR_CAPI.h: 763
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetFloat'):
        continue
    ovrHmd_GetFloat = _lib.ovrHmd_GetFloat
    ovrHmd_GetFloat.argtypes = [hmd, String, c_float]
    ovrHmd_GetFloat.restype = c_float
    break

# OVR_CAPI.h: 766
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_SetFloat'):
        continue
    ovrHmd_SetFloat = _lib.ovrHmd_SetFloat
    ovrHmd_SetFloat.argtypes = [hmd, String, c_float]
    ovrHmd_SetFloat.restype = ovrBool
    break

# OVR_CAPI.h: 771
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetFloatArray'):
        continue
    ovrHmd_GetFloatArray = _lib.ovrHmd_GetFloatArray
    ovrHmd_GetFloatArray.argtypes = [hmd, String, POINTER(c_float), c_uint]
    ovrHmd_GetFloatArray.restype = c_uint
    break

# OVR_CAPI.h: 775
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_SetFloatArray'):
        continue
    ovrHmd_SetFloatArray = _lib.ovrHmd_SetFloatArray
    ovrHmd_SetFloatArray.argtypes = [hmd, String, POINTER(c_float), c_uint]
    ovrHmd_SetFloatArray.restype = ovrBool
    break

# OVR_CAPI.h: 781
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetString'):
        continue
    ovrHmd_GetString = _lib.ovrHmd_GetString
    ovrHmd_GetString.argtypes = [hmd, String, String]
    if sizeof(c_int) == sizeof(c_void_p):
        ovrHmd_GetString.restype = ReturnString
    else:
        ovrHmd_GetString.restype = String
        ovrHmd_GetString.errcheck = ReturnString
    break

# OVR_CAPI.h: 786
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'ovrHmd_GetArraySize'):
        continue
    ovrHmd_GetArraySize = _lib.ovrHmd_GetArraySize
    ovrHmd_GetArraySize.argtypes = [hmd, String]
    ovrHmd_GetArraySize.restype = c_uint
    break


# OVR_CAPI.h: 743
try:
    OVR_KEY_USER = 'User'
    OVR_KEY_NAME = 'Name'
    OVR_KEY_GENDER = 'Gender'
    OVR_KEY_PLAYER_HEIGHT = 'PlayerHeight'
    OVR_KEY_EYE_HEIGHT = 'EyeHeight'
    OVR_KEY_IPD = 'IPD'
    OVR_KEY_NECK_TO_EYE_HORIZONTAL = 'NeckEyeHori'
    OVR_KEY_NECK_TO_EYE_VERTICAL = 'NeckEyeVert'
    OVR_DEFAULT_GENDER = 'Male'
    OVR_DEFAULT_PLAYER_HEIGHT = 1.778
    OVR_DEFAULT_EYE_HEIGHT = 1.675
    OVR_DEFAULT_IPD = 0.064
    OVR_DEFAULT_NECK_TO_EYE_HORIZONTAL = 0.12
    OVR_DEFAULT_NECK_TO_EYE_VERTICAL = 0.12
except:
    pass

def ovrVec3ToTuple(v):
    return (v.x, v.y, v.z)

def ovrQuatToTuple(q):
    return (q.x, q.y, q.z, q.w)

def ovrMat4ToTuple(m):
    mm = []
    for i in range(0, 4):
        for j in range(0, 4):
            mm.append(m.M[j][i])
    return tuple(mm)


class Rift():
    @staticmethod
    def initialize():
        if (0 == ovr_Initialize()):
            raise SystemError("Unable to initialize the Oculus SDK")

    @staticmethod
    def shutdown():
        ovr_Shutdown()

    @staticmethod
    def detect():
        return ovrHmd_Detect()

    def __init__(self, index = 0, debug = False):
        if (debug != False):
            self.hmd = ovrHmd_CreateDebug(debug)
        else:
            self.hmd = ovrHmd_Create(index)

    def destroy(self):
        ovrHmd_Destroy(self.hmd)
        self.hmd = None

    def get_last_error(self):
        return ovrHmd_GetLastError(self.hmd);

    def get_enabled_caps(self):
        return ovrHmd_GetEnabledCaps(self.hmd);

    def set_enabled_caps(self, caps):
        return ovrHmd_SetEnabledCaps(self.hmd, caps);

    def start_sensor(self, supported_caps = 
                     ovrSensorCap_Orientation |
                     ovrSensorCap_YawCorrection |
                     ovrSensorCap_Position, 
                     required_caps = 0):
        if (0 == ovrHmd_StartSensor(self.hmd, supported_caps, required_caps)):
            raise SystemError("Unable to start the sensor")

    def stop_sensor(self):
        return ovrHmd_StopSensor(self.hmd)

    def reset_sensor(self):
        return ovrHmd_ResetSensor(self.hmd)

    def get_sensor_state(self, absTime = 0):
        return ovrHmd_GetSensorState(self.hmd, absTime)

    def get_sensor_desc(self):
        result = sensor_desc()
        if (0 == ovrHmd_GetSensorDesc(self.hmd, byref(result))):
            raise SystemError("Unable to fetch the sensor description")
        return result

    def get_desc(self):
        result = hmd_desc()
        if (0 == ovrHmd_GetDesc(self.hmd, byref(result))):
            raise SystemError("Unable to fetch the hmd description")
        return result

    def get_fov_texture_size(self, eye, fov_port, pixels_per_display_pixel = 1):
        return ovrHmd_GetFovTextureSize(self.hmd, eye, fov_port, pixels_per_display_pixel);

    def configure_rendering(self, config, fovPorts, 
                            distortion_caps = 
                            ovrDistortionCap_Chromatic |
                            ovrDistortionCap_TimeWarp |
                            ovrDistortionCap_NoSwapBuffers |
                            ovrDistortionCap_Vignette):
        result = [ eye_render_desc(), eye_render_desc() ]
        out_arr  = (eye_render_desc * 2)(*result)
        in_arr = (fov_port * 2)(*fovPorts)

        if (0 == ovrHmd_ConfigureRendering(self.hmd, byref(config), distortion_caps, in_arr, out_arr)):
            raise SystemError("Unable to configure rendering")
        return out_arr

    def begin_frame(self, frame_index = 0):
        return ovrHmd_BeginFrame(self.hmd, frame_index)

    def end_frame(self):
        return ovrHmd_EndFrame(self.hmd)

    def begin_eye_render(self, eye):
        self.pose = ovrHmd_BeginEyeRender(self.hmd, eye); 
        return self.pose

    def end_eye_render(self, eye, texture, pose = None):
        if (None == pose):
            pose = self.pose
        ovrHmd_EndEyeRender(self.hmd, eye, pose, byref(texture))

    def get_render_desc(self, eye, fov):
        return ovrHmd_GetRenderDesc(self.hmd, eye, fov)

    @staticmethod
    def get_perspective(fov, near, far, right_handed):
        return ovrMatrix4f_Projection(fov, near, far, '\x01' if right_handed else '\x00')

    @staticmethod
    def get_orthographic(perspective, scale, distance, eye_x_offset):
        return ovrMatrix4f_Projection(perspective, scale, distance, eye_x_offset)

    @staticmethod
    def get_time_in_seconds():
        ovr_GetTimeInSeconds()

    @staticmethod
    def wait_till_time(time_in_seconds):
        return ovr_WaitTillTime(time_in_seconds)

# TODO finish writing wrapper functionality for the functions used in 
# client-side distortion
#
# # OVR_CAPI.h: 642
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_CreateDistortionMesh'):
#         continue
#     ovrHmd_CreateDistortionMesh = _lib.ovrHmd_CreateDistortionMesh
#     ovrHmd_CreateDistortionMesh.argtypes = [hmd, ovrEyeType, fov_port, c_uint, POINTER(ovrDistortionMesh)]
#     ovrHmd_CreateDistortionMesh.restype = ovrBool
#     break
# 
# # OVR_CAPI.h: 649
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_DestroyDistortionMesh'):
#         continue
#     ovrHmd_DestroyDistortionMesh = _lib.ovrHmd_DestroyDistortionMesh
#     ovrHmd_DestroyDistortionMesh.argtypes = [POINTER(ovrDistortionMesh)]
#     ovrHmd_DestroyDistortionMesh.restype = None
#     break
# 
# # OVR_CAPI.h: 653
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetRenderScaleAndOffset'):
#         continue
#     ovrHmd_GetRenderScaleAndOffset = _lib.ovrHmd_GetRenderScaleAndOffset
#     ovrHmd_GetRenderScaleAndOffset.argtypes = [fov_port, sizei, recti, vec2 * 2]
#     ovrHmd_GetRenderScaleAndOffset.restype = None
#     break
# 
# # OVR_CAPI.h: 660
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetFrameTiming'):
#         continue
#     ovrHmd_GetFrameTiming = _lib.ovrHmd_GetFrameTiming
#     ovrHmd_GetFrameTiming.argtypes = [hmd, c_uint]
#     ovrHmd_GetFrameTiming.restype = frame_timing
#     break
# 
# # OVR_CAPI.h: 665
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_BeginFrameTiming'):
#         continue
#     ovrHmd_BeginFrameTiming = _lib.ovrHmd_BeginFrameTiming
#     ovrHmd_BeginFrameTiming.argtypes = [hmd, c_uint]
#     ovrHmd_BeginFrameTiming.restype = frame_timing
#     break
# 
# # OVR_CAPI.h: 670
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_EndFrameTiming'):
#         continue
#     ovrHmd_EndFrameTiming = _lib.ovrHmd_EndFrameTiming
#     ovrHmd_EndFrameTiming.argtypes = [hmd]
#     ovrHmd_EndFrameTiming.restype = None
#     break
# 
# # OVR_CAPI.h: 675
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_ResetFrameTiming'):
#         continue
#     ovrHmd_ResetFrameTiming = _lib.ovrHmd_ResetFrameTiming
#     ovrHmd_ResetFrameTiming.argtypes = [hmd, c_uint]
#     ovrHmd_ResetFrameTiming.restype = None
#     break
# 
# # OVR_CAPI.h: 680
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetEyePose'):
#         continue
#     ovrHmd_GetEyePose = _lib.ovrHmd_GetEyePose
#     ovrHmd_GetEyePose.argtypes = [hmd, ovrEyeType]
#     ovrHmd_GetEyePose.restype = pose
#     break
# 
# # OVR_CAPI.h: 687
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetEyeTimewarpMatrices'):
#         continue
#     ovrHmd_GetEyeTimewarpMatrices = _lib.ovrHmd_GetEyeTimewarpMatrices
#     ovrHmd_GetEyeTimewarpMatrices.argtypes = [hmd, ovrEyeType, pose, mat4 * 2]
#     ovrHmd_GetEyeTimewarpMatrices.restype = None
#     break

# # OVR_CAPI.h: 719
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_ProcessLatencyTest'):
#         continue
#     ovrHmd_ProcessLatencyTest = _lib.ovrHmd_ProcessLatencyTest
#     ovrHmd_ProcessLatencyTest.argtypes = [hmd, c_ubyte * 3]
#     ovrHmd_ProcessLatencyTest.restype = ovrBool
#     break
# 
# # OVR_CAPI.h: 723
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetLatencyTestResult'):
#         continue
#     ovrHmd_GetLatencyTestResult = _lib.ovrHmd_GetLatencyTestResult
#     ovrHmd_GetLatencyTestResult.argtypes = [hmd]
#     if sizeof(c_int) == sizeof(c_void_p):
#         ovrHmd_GetLatencyTestResult.restype = ReturnString
#     else:
#         ovrHmd_GetLatencyTestResult.restype = String
#         ovrHmd_GetLatencyTestResult.errcheck = ReturnString
#     break
# 
# # OVR_CAPI.h: 727
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetMeasuredLatencyTest2'):
#         continue
#     ovrHmd_GetMeasuredLatencyTest2 = _lib.ovrHmd_GetMeasuredLatencyTest2
#     ovrHmd_GetMeasuredLatencyTest2.argtypes = [hmd]
#     ovrHmd_GetMeasuredLatencyTest2.restype = c_double
#     break
# 
# # OVR_CAPI.h: 763
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetFloat'):
#         continue
#     ovrHmd_GetFloat = _lib.ovrHmd_GetFloat
#     ovrHmd_GetFloat.argtypes = [hmd, String, c_float]
#     ovrHmd_GetFloat.restype = c_float
#     break
# 
# # OVR_CAPI.h: 766
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_SetFloat'):
#         continue
#     ovrHmd_SetFloat = _lib.ovrHmd_SetFloat
#     ovrHmd_SetFloat.argtypes = [hmd, String, c_float]
#     ovrHmd_SetFloat.restype = ovrBool
#     break
# 
# # OVR_CAPI.h: 771
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetFloatArray'):
#         continue
#     ovrHmd_GetFloatArray = _lib.ovrHmd_GetFloatArray
#     ovrHmd_GetFloatArray.argtypes = [hmd, String, POINTER(c_float), c_uint]
#     ovrHmd_GetFloatArray.restype = c_uint
#     break
# 
# # OVR_CAPI.h: 775
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_SetFloatArray'):
#         continue
#     ovrHmd_SetFloatArray = _lib.ovrHmd_SetFloatArray
#     ovrHmd_SetFloatArray.argtypes = [hmd, String, POINTER(c_float), c_uint]
#     ovrHmd_SetFloatArray.restype = ovrBool
#     break
# 
# # OVR_CAPI.h: 781
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetString'):
#         continue
#     ovrHmd_GetString = _lib.ovrHmd_GetString
#     ovrHmd_GetString.argtypes = [hmd, String, String]
#     if sizeof(c_int) == sizeof(c_void_p):
#         ovrHmd_GetString.restype = ReturnString
#     else:
#         ovrHmd_GetString.restype = String
#         ovrHmd_GetString.errcheck = ReturnString
#     break
# 
# # OVR_CAPI.h: 786
# for _lib in _libs.itervalues():
#     if not hasattr(_lib, 'ovrHmd_GetArraySize'):
#         continue
#     ovrHmd_GetArraySize = _lib.ovrHmd_GetArraySize
#     ovrHmd_GetArraySize.argtypes = [hmd, String]
#     ovrHmd_GetArraySize.restype = c_uint
#     break
