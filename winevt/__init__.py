import winevt.settings as settings

#
# Load up whichever way we can
#

# Assume it's in-line unless we get otherwise
out_of_line = False

try:
    from ._winevt import ffi, lib as evtapi
    # Loading inline, these will be the same
    kernel32 = evtapi
    out_of_line = True

except:
    # In-line mode
    from .winevt_build import ffibuilder
    ffi = ffibuilder()
    evtapi = ffi.dlopen("Wevtapi.dll")
    kernel32 = ffi.dlopen("Kernel32.dll")

# Init settings if we haven't yet
if settings.callbacks == None:
    settings.init()

#
# Some Enums
#

FORMAT_MESSAGE_ALLOCATE_BUFFER  = 0x00000100
FORMAT_MESSAGE_ARGUMENT_ARRAY   = 0x00002000
FORMAT_MESSAGE_FROM_HMODULE     = 0x00000800
FORMAT_MESSAGE_FROM_STRING      = 0x00000400
FORMAT_MESSAGE_FROM_SYSTEM      = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS   = 0x00000200
FORMAT_MESSAGE_MAX_WIDTH_MASK   = 0x000000FF

#
# Helper functions
#

def get_last_error():
    """ Get the last error value, then turn it into a nice string. Return the string. """
    error_id = kernel32.GetLastError()
    
    # No actual error
    if error_id == 0:
        return None

    # Gonna need a string pointer
    buf = ffi.new("LPWSTR")

    chars = kernel32.FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, ffi.NULL, error_id , 0, buf, 0, ffi.NULL)

    return ffi.string(ffi.cast("char **",buf)[0][0:chars]).decode('utf-8').strip("\r\n")


def uses_inline():
    return not out_of_line
