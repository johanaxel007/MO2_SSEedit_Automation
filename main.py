import time
from subprocess import Popen
import os.path

from pywinauto import Desktop, findbestmatch
from pywinauto.timings import wait_until

from utils import read_file_to_list, write_list_to_file


def read_or_create_file(_path):
    _contents = []
    if os.path.isfile(_path):
        _contents = read_file_to_list(_path)
    else:
        write_list_to_file(_path, [])
    return _contents


def set_plugins_inactive(_plugins: list):
    for _plugin_index, _plugin in enumerate(_plugins):
        _plugins[_plugin_index] = str.lstrip(_plugin, '*')
    return _plugins


def set_plugin_active(_plugins: list, _plugin_index: int):
    _plugins[_plugin_index] = '*' + plugin
    return _plugins


def set_plugin_inactive(_plugins: list, _plugin_index: int):
    _plugins[_plugin_index] = str.lstrip(plugin, '*')
    return _plugins


def start_xedit(shortcut: str):
    def ensure_finished():
        text = ""
        try:
            text = xedit_script_window.Edit.get_value()
        except findbestmatch.MatchError:
            print("Warning: Couldn't find the output window, waiting a but longer")

        quit_index = text.rfind('You can close this application now.')
        return quit_index > 0

    Popen(shortcut, shell=True)
    xedit_script_window = Desktop(backend="uia").SSEScript
    xedit_script_window.wait('visible', 60)
    xedit_script_window.window(title="Module Selection", control_type="Window").OKButton.click()

    time.sleep(5)

    try:
        wait_until(240, 2, ensure_finished)
        time.sleep(5)
        xedit_script_window.close()
    except TimeoutError:
        print("Error: Timed out")
        time.sleep(2)
        xedit_script_window.close()


if __name__ == '__main__':
    plugins_path = r"K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt"
    plugins_backup_path = r"K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt.bak"
    xedit_shortcut = r'I:\!Tools\!Mod_Organizer_2\ModOrganizer.exe "moshortcut://Skyrim Special Edition:SSEEdit - Write Bash Tags"'
    cache_file_path = r'./plugin_cache.txt'
    cache_whitelist_file_path = r'./plugin_cache_whitelist.txt'
    whitelist_file_path = r'./plugin_whitelist.txt'
    blacklist_file_path = r'./plugin_blacklist.txt'

    plugins_raw = read_file_to_list(plugins_path)
    write_list_to_file(plugins_backup_path, plugins_raw)

    plugin_whitelist = read_or_create_file(whitelist_file_path)
    plugin_blacklist = read_or_create_file(blacklist_file_path)

    # Cache (Separate cache when whitelist is used)
    if len(plugin_whitelist) == 0:
        plugin_cache = read_or_create_file(cache_file_path)
    else:
        plugin_cache = read_or_create_file(cache_whitelist_file_path)
        cache_file_path = cache_whitelist_file_path

    plugins = plugins_raw[1:]
    plugins_inactive = set_plugins_inactive(plugins)

    plugin_count = len(plugins_inactive)

    for index, plugin in enumerate(plugins_inactive):
        print(f"{(index + 1):04d} / {plugin_count:04d} | {plugin}")
        # Check if whitelist is used
        if len(plugin_whitelist) != 0 and plugin not in plugin_whitelist:
            print(f"Warning: {plugin} is not in whitelist, skipping.\n")
            continue

        # Check if cached
        if plugin in plugin_cache:
            print(f"Warning: {plugin} is in cache, skipping.\n")
            continue

        # Check if blacklisted
        if plugin in plugin_blacklist:
            print(f"Warning: {plugin} is blacklisted, skipping.\n")
            plugin_cache.append(plugin)
            write_list_to_file(cache_file_path, plugin_cache)
            continue

        # Generate bash tags
        plugins_active = set_plugin_active(plugins_inactive, index)
        write_list_to_file(plugins_path, plugins_active)

        # Try to start
        def try_again(retries=0):
            if retries >= 3: return False
            try:
                start_xedit(xedit_shortcut)
                return True
            except:
                print(f"Error: xEdit failure | Try {(retries + 1)} / 3")
                retries += 1
                try_again(retries)


        if not try_again(): continue
        time.sleep(5)

        # Reset plugin file
        plugins_active = set_plugin_inactive(plugins_inactive, index)
        write_list_to_file(plugins_path, plugins_inactive)
        time.sleep(1)

        # Write plugin to cache
        plugin_cache.append(plugin)
        write_list_to_file(cache_file_path, plugin_cache)
        time.sleep(2)
        print()

    # Restore original plugin.txt file
    write_list_to_file(plugins_path, plugins_raw)
