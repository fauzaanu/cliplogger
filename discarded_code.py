import ctypes.wintypes

user32 = ctypes.windll.user32


def wnd_proc(hwnd, msg, wParam, lParam):
    if msg == 0x031D:
        print("Clipboard contents changed!")
    return user32.DefWindowProcW(hwnd, msg, wParam, lParam)


class WNDCLASS(ctypes.Structure):
    _fields_ = [("style", ctypes.c_uint),
                ("lpfnWndProc", ctypes.c_void_p),
                ("cbClsExtra", ctypes.c_int),
                ("cbWndExtra", ctypes.c_int),
                ("hInstance", ctypes.c_void_p),
                ("hIcon", ctypes.c_void_p),
                ("hCursor", ctypes.c_void_p),
                ("hbrBackground", ctypes.c_void_p),
                ("lpszMenuName", ctypes.c_void_p),
                ("lpszClassName", ctypes.c_void_p)]


wnd_class = WNDCLASS()
wnd_class.lpfnWndProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p,
                                           ctypes.c_void_p)(wnd_proc)
wnd_class.hInstance = user32.GetModuleHandleW(None)
wnd_class.lpszClassName = "MyClipboardListener".encode('utf-8')
atom = user32.RegisterClassW(ctypes.byref(wnd_class))
hwnd = user32.CreateWindowExW(0, atom, "My Clipboard Listener", 0, 0, 0, 0, 0, None, None,
                              user32.GetModuleHandleW(None), None)
user32.AddClipboardFormatListener(hwnd)
msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
    user32.TranslateMessage(ctypes.byref(msg))
    user32.DispatchMessageW(ctypes.byref(msg))
