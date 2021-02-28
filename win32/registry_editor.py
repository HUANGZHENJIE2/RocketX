import win32api
import win32con




def set_start_up():
    subkeyHandle = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                         r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')
    (v, t) = win32api.RegQueryValueEx(subkeyHandle, "BaiduYunDetect")
    print(v)
    rocketXkey = win32api.RegCreateKeyEx(
        win32con.HKEY_CURRENT_USER,
       r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
        win32con.KEY_ALL_ACCESS,
       "RocketX"
    )
    # # winreg.SetValue(key, "MyNewKey", winreg.REG_SZ, "New")
    win32api.RegSetValueEx(
        win32con.HKEY_CURRENT_USER,
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
        "RocketX",win32con.REG_SZ,"1110")

    subkeyHandle = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                         r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')

    (v, t) = win32api.RegQueryValueEx(
        subkeyHandle,
        "RocketX")
    print(v)

if __name__ == '__main__':
    set_start_up()
