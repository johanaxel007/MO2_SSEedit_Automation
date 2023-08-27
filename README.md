#  xEdit: Per plugin script apply automation for MO2

## Getting started
### Requirements
- Python 3.10 (Other versions should also work, but has only been tested on 3.10)
- xEdit v4.0.4+ or any of its variations (SSEedit, FNVedit, ...)
- Mod Organiser 2 (Vortex or stand alone should also work, see `plugins_path` and `xedit_shortcut` in [Project setup](#project-setup))

### Warnings & acknowledges
The script was made for my personal use, bugs may exist and I may or may not fix them. From my usage the code is stable but still, use at your own risk.

It can and probably will mess up your active plugin state for your load order, so it's best to manually **create a back-up** of this.  

To automate the Wrye Bash tag generation, I have used a modified version of [WryeBashTagGenerator](https://github.com/fireundubh/WryeBashTagGenerator) from fireundubh. The modified version skips the options pop-up and always writes the tags to the plugin header.  

    For WryeBashTagGenerator script version 1.6.4.7:
        Set line 113 (g_AddTags) to True
        Commenting out lines 136 to 141 (ShowPrompt) by prefixing // to the code

### Project setup
1. Create a Python venv: `python -m venv venv`
	

2. Activate the venv using the following command
    - `.\venv\Scripts\Activate`
	

3. Install the dependencies: `pip install -r requirements.txt`


4. Set up the variables in `settings.ini` (default values shown):
   - plugins_path = `K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt`
     - Path to your plugin load order file
       - For MO2 users:
         1. Show Open Folders menu
         2. Open Profile folder
         3. plugins.txt

   - plugins_backup_path = `K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt.bak`
     - Path where a backup is created of your load order.

   - mo2_executable_path = `I:\!Tools\!Mod_Organizer_2\ModOrganizer.exe`
     - Path to Mod Organizer 2 executable (exe).

   - xedit_executable_path = `I:\Games\Mod Organizer 2\Skyrim Special Edition\!Tools\SSEEdit\SSEEdit.exe`
     - Path to xEdit executable (exe).

   - xedit_cache_path = `K:\Games\Mod Organizer 2\Skyrim Special Edition\mods\SSE Edit Data\SSEEdit Cache\`
     - Path to where xEdit should store its cache. (Optional)

   - xedit_backup_path = `K:\Games\Mod Organizer 2\Skyrim Special Edition\mods\SSE Edit Data\SSEEdit Backups\`
     - Path to where xEdit should store its plugin backups. (Optional)

   - xedit_script = `WryeBashTagGenerator - Automated.pas`
     - Name of the xEdit script to be run on each plugin.
   
   - cache_file_path = `./plugin_cache.txt`
     - Path to where the done plugins cache is stored, by default it's in the same directory as the python script.
     - You can safely delete this file as a new empty one will be generated when missing.
     - **WARNING**: Any plugin in this file will be skipped. You can safely delete this file as a new empty one will be generated when missing.
 
   - cache_whitelist_file_path = `./plugin_cache_whitelist.txt`
     - Path to where the done plugins cache when using the whitelist is stored, by default it's in the same directory as the python script.
     - **WARNING**: Any plugin in this file will be skipped, even if it's in the whitelist. You can safely delete this file as a new empty one will be generated when missing.
 
   - whitelist_file_path = `./plugin_whitelist.txt`
     - Path to where the plugin whitelist is read from, by default it's in the same directory as the python script.
	 - **INFO**: The following commands can help generate this file, change the path to where your plugin whitelist file is stored.
		- **CMD**: `dir /b *.esl *.esp *.esm >> "I:\Games\Mod Organizer 2\!Tools\_Projects\MO2_SSEedit_Automation\plugin_whitelist.txt"`
		- **Powershell**: `(dir .\ | where {$_.extension -in ".esl", ".esp", ".esm"}).name | Out-File "I:\Games\Mod Organizer 2\!Tools\_Projects\MO2_SSEedit_Automation\plugin_whitelist.txt" -Append`
     - **WARNING**: When this file contains any plugin names, only these plugins will be processed. You can safely delete this file as a new empty one will be generated when missing.
 
   - blacklist_file_path = `./plugin_blacklist.txt`
     - Path to where the plugin blacklist is read from, by default it's in the same directory as the python script.
     - The blacklist I use is given as an example.
     - **WARNING**: Any plugin in this file will be skipped, even if it's in the whitelist. You can safely delete this file as a new empty one will be generated when missing.


5. Run the code:
   - `python .\main.py` in a console window
   - The code should now be running, xEdit windows should pop up to run the script, do not close these manually unless they are stuck for 5+ minutes.
   - It's best to not use your computer when this script is running.


### Ideas
- Add elapsed time metric when script finishes