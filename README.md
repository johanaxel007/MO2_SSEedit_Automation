#  xEdit: Per plugin script apply automation for MO2

## Getting started
### Requirements
- Python 3.10 (Other versions should also work, but has only been tested on 3.10)

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


4. Set up the variables in `main.py` (default values shown):
   - plugins_path = `r"K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt"`
     - Path to your load order file (in MO2):
       1. Show Open Folders menu
       2. Open Profile folder
       3. plugins.txt

   - plugins_backup_path = `r"K:\Games\Mod Organizer 2\Skyrim Special Edition\profiles\Default\plugins.txt.bak"`
     - Path where a backup is created of your load order.

   - xedit_shortcut = `r'I:\!Tools\!Mod_Organizer_2\ModOrganizer.exe "moshortcut://Skyrim Special Edition:SSEEdit - Write Bash Tags"'`
     - Executable or MO2 shortcut to xEdit, this is wat's executed for each plugin.
       - My MO2 shortcut arguments: `-autoload -IKnowWhatImDoing -C:"K:\Games\Mod Organizer 2\Skyrim Special Edition\mods\SSE Edit Data\SSEEdit Cache\" -B:"K:\Games\Mod Organizer 2\Skyrim Special Edition\mods\SSE Edit Data\SSEEdit Backups\" -script:"WryeBashTagGenerator - Automated.pas"`
       - `-autoload` and `-script` are the two things that made this work.
       
   - cache_file_path = `r'./plugin_cache.txt'`
     - Path to where the done plugins cache is stored, by default it's in the same directory as the python script.
     - You can safely delete this file as a new empty one will be generated when missing.
     - **WARNING**: Any plugin in this file will be skipped. You can safely delete this file as a new empty one will be generated when missing.
     
   - cache_whitelist_file_path = `r'./plugin_cache_whitelist.txt'`
     - Path to where the done plugins cache when using the whitelist is stored, by default it's in the same directory as the python script.
     - **WARNING**: Any plugin in this file will be skipped, even if it's in the whitelist. You can safely delete this file as a new empty one will be generated when missing.
     
   - whitelist_file_path = `r'./plugin_whitelist.txt'`
     - Path to where the plugin whitelist is read from, by default it's in the same directory as the python script.
     - **INFO**: `dir /b *.esl *.esp *.esm > plugin_list.txt` can help generate this file, copy the output it gives into the whitelist file.
     - **WARNING**: When this file contains any plugin names, only these plugins will be processed. You can safely delete this file as a new empty one will be generated when missing.
     
   - blacklist_file_path = `r'./plugin_blacklist.txt'`
     - Path to where the plugin blacklist is read from, by default it's in the same directory as the python script.
     - The blacklist I use is given as an example.
     - **WARNING**: Any plugin in this file will be skipped, even if it's in the whitelist. You can safely delete this file as a new empty one will be generated when missing.


5. Run the code:
   - `python .\main.py` in a console window
   - The code should now be running, xEdit windows should pop up to run the script, do not close these manually unless they are stuck for 5+ minutes.
   - It's best to not use your computer when this script is running.
