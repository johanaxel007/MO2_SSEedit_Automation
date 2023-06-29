from configparser import ConfigParser


class ConfigManager:
    configur = ConfigParser(allow_no_value=True, comment_prefixes="#")
    file = ''

    def __init__(self, file='settings.ini'):
        self.configur.read(file)
        self.file = file
        print(f'ConfigManager: "{self.file}" Initialized with ID: {id(self)}')

    def __repr__(self) -> str:
        return f"<ConfigManager: {self.file}>"

    @property
    def config(self):
        return self.configur

    def _write_config(self):
        with open(self.file, 'w', encoding="utf-8", errors="ignore") as configfile:
            self.configur.write(configfile)

    def update_field(self, section, field, value):
        self.configur.set(section, field, value)
        self._write_config()

    def delete_field(self, section, field):
        self.configur.remove_option(section, field)
        self._write_config()
