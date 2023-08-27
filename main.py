import os.path
import time
from subprocess import Popen

from pywinauto import Desktop, findbestmatch
from pywinauto.timings import wait_until

from utils.configmanager import ConfigManager
from utils.utils import read_file_to_list, write_list_to_file, escape_path, print_start, print_finished, print_dated


def read_or_create_file(_path):
    _contents = []
    if os.path.isfile(_path):
        _contents = read_file_to_list(_path)
    else:
        write_list_to_file(_path, [])
    # Remove empty strings
    _contents = [i for i in _contents if i]
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
            print_dated("Warning: Couldn't find the output window, waiting a little longer")

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
        print_dated("Done: Saving plugin")
        xedit_script_window.close()
    except TimeoutError:
        print_dated("Error: Timed out")
        time.sleep(2)
        xedit_script_window.close()


def settings_ini_create():
    if not os.path.exists("settings.ini"):
        ini = [r"[SETTINGS]",
               r"# Path to your plugin load order file: MO2 Users --> Show Open Folders menu --> Open Profile folder --> plugins.txt",
               r"plugins_path = K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt",
               r"# Path where a backup is created of your load order.",
               r"plugins_backup_path = K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt.bak",
               r"# Path to Mod Organizer 2 executable (exe).",
               r"mo2_executable_path = I:\!Tools\!Mod_Organizer_2\ModOrganizer.exe",
               r"# Path to xEdit executable (exe).",
               r"xedit_executable_path = I:\Games\Mod Organizer 2\Skyrim Special Edition\!Tools\SSEEdit\SSEEdit.exe",
               r"# Path to where xEdit should store its cache. (Optional)",
               r"xedit_cache_path = K:\Games\Mod Organizer 2\Skyrim Special Edition\mods\SSE Edit Data\SSEEdit Cache\\",
               r"# Path to where xEdit should store its plugin backups. (Optional)",
               r"xedit_backup_path = K:\Games\Mod Organizer 2\Skyrim Special Edition\mods\SSE Edit Data\SSEEdit Backups\\",
               r"# Name of the xEdit script to be run on each plugin.",
               r"xedit_script = WryeBashTagGenerator - Automated.pas",
               r"# Path to where the done plugins cache is stored. Any plugin in this file will be skipped.",
               r"cache_file_path = ./plugin_cache.txt",
               r"# Path to where the done plugins cache when using the whitelist is stored. Any plugin in this file will be skipped, even if it's in the whitelist.",
               r"cache_whitelist_file_path = ./plugin_cache_whitelist.txt",
               r"# Path to where the plugin whitelist is read from. When this file contains any plugin names, only these plugins will be processed.",
               r"whitelist_file_path = ./plugin_whitelist.txt",
               r"# Path to where the plugin blacklist is read from. Any plugin in this file will be skipped, even if it's in the whitelist.",
               r"blacklist_file_path = ./plugin_blacklist.txt"]
        write_list_to_file('settings.ini', ini)


if __name__ == '__main__':
    settings_ini_create()
    config_manager = ConfigManager()
    # --- Setup Variables ---
    plugins_path = config_manager.config.get('SETTINGS', 'plugins_path')
    plugins_backup_path = config_manager.config.get('SETTINGS', 'plugins_backup_path')
    mo2_executable_path = config_manager.config.get('SETTINGS', 'mo2_executable_path')
    xedit_executable_path = config_manager.config.get('SETTINGS', 'xedit_executable_path')
    xedit_cache_path = config_manager.config.get('SETTINGS', 'xedit_cache_path')
    xedit_backup_path = config_manager.config.get('SETTINGS', 'xedit_backup_path')
    xedit_script = config_manager.config.get('SETTINGS', 'xedit_script')
    cache_file_path = config_manager.config.get('SETTINGS', 'cache_file_path')
    cache_whitelist_file_path = config_manager.config.get('SETTINGS', 'cache_whitelist_file_path')
    whitelist_file_path = config_manager.config.get('SETTINGS', 'whitelist_file_path')
    blacklist_file_path = config_manager.config.get('SETTINGS', 'blacklist_file_path')

    plugins_raw = read_file_to_list(plugins_path)
    write_list_to_file(plugins_backup_path, plugins_raw)

    plugin_whitelist = read_or_create_file(whitelist_file_path)
    plugin_blacklist = read_or_create_file(blacklist_file_path)

    # Cache (Separate cache when whitelist is used)
    if not plugin_whitelist:
        plugin_cache = read_or_create_file(cache_file_path)
    else:
        plugin_cache = read_or_create_file(cache_whitelist_file_path)
        cache_file_path = cache_whitelist_file_path

    plugins = plugins_raw[1:]
    plugins_inactive = set_plugins_inactive(plugins)

    plugin_count = len(plugins_inactive)

    print_start(plugin_count, len(plugin_whitelist), len(plugin_blacklist), xedit_script)

    for index, plugin in enumerate(plugins_inactive):
        print_dated(f"{(index + 1):04d} / {plugin_count:04d} | {plugin}")
        # Check if whitelist is used
        if plugin_whitelist and plugin not in plugin_whitelist:
            print_dated(f"Warning: {plugin} is not in whitelist, skipping.\n")
            continue

        # Check if cached
        if plugin in plugin_cache:
            print_dated(f"Warning: {plugin} is in cache, skipping.\n")
            continue

        # Check if blacklisted
        if plugin in plugin_blacklist:
            print_dated(f"Warning: {plugin} is blacklisted, skipping.\n")
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
                command = f'"{escape_path(mo2_executable_path)}" run "{escape_path(xedit_executable_path)}" -a "'
                if xedit_cache_path:
                    command += f'-C:\\"{escape_path(xedit_cache_path)}\\" '
                if xedit_backup_path:
                    command += f'-B:\\"{escape_path(xedit_backup_path)}\\" '
                command += f'-script:\\"{xedit_script}\\" -autoload""'
                start_xedit(command)
                return True
            except Exception:  # This still allows to exit by CTRL + C
                print_dated(f"Error: xEdit failure | Try {(retries + 1)} / 3")
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

    print_finished()
