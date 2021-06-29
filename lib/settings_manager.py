from genericpath import exists
import json
import os
import pathlib

class SettingsManager(object):
    PCS_NUM = 'pcs_num'
    PCS_LEVEL = 'pcs_level'
    ENC_NUM = 'enc_num'
    CURRENT_TABLE = 'cur_tbl'

    def __init__(self):
        # Detect linux/mac vs windows. Fuck solaris.
        if os.name == 'posix':
            self.settings_path = os.path.expanduser(os.path.join('~', '.5eERrc'))
        if os.name == 'nt':
            self.settings_path = os.path.expanduser(os.path.join('~', 'AppData', 'Local', 'EncounterRoller5e'))
        
        self.settings_file_path = os.path.join(self.settings_path, 'settings.json')
        self.tables_file_path = os.path.join(self.settings_path, 'tables')

        settings = self.read_settings_file()

        self._num_characters = settings[SettingsManager.PCS_NUM]
        self._level_characters = settings[SettingsManager.PCS_LEVEL]
        self._encounter_num = settings[SettingsManager.ENC_NUM]
        self._current_table = settings[SettingsManager.CURRENT_TABLE]

    def read_settings_file(self):
        """Read settings file and return parsed contents.
        """
        if not os.path.exists(self.settings_file_path):
            self.write_settings_file({
                SettingsManager.PCS_NUM: 5,
                SettingsManager.PCS_LEVEL: 1,
                SettingsManager.ENC_NUM: 1,
                SettingsManager.CURRENT_TABLE: None
            })
        with open(self.settings_file_path, 'r') as settings_file:
            settings = json.loads(settings_file.read())
        return settings

    def write_settings_file(self, settings):
        """Write out modified settings data to settings file.
        """
        pathlib.Path(self.settings_path).mkdir(parents=True, exist_ok=True)
        with open(self.settings_file_path, 'w') as settings_file:
            settings_file.write(json.dumps(settings, indent=4))

    def set_setting(self, key, value):
        """Set and save a setting.
        It would be more efficient to make all changes and then write once,
        but this is simple, it works, and it's incredibly durable.
        """
        settings = self.read_settings_file()
        settings[key] = value
        self.write_settings_file(settings)

    @property
    def number_of_characters(self):
        return self._num_characters

    @number_of_characters.setter
    def number_of_characters(self, value):
        self._num_characters = value
        self.set_setting(SettingsManager.PCS_NUM, value)

    @property
    def level_of_characters(self):
        return self._num_characters

    @level_of_characters.setter
    def level_of_characters(self, value):
        self._level_characters = value
        self.set_setting(SettingsManager.PCS_LEVEL, value)

    @property
    def number_of_encounters(self):
        return self._num_characters

    @number_of_encounters.setter
    def number_of_encounters(self, value):
        self._encounter_num = value
        self.set_setting(SettingsManager.ENC_NUM, value)

    @property
    def current_table(self):
        return self._current_table

    @current_table.setter
    def current_table(self, value):
        self._current_table = value
        self.set_setting(SettingsManager.CURRENT_TABLE, value)

    def set(self, args):
        """Handle the set operation from the command line.
        """
        if args.num_characters:
            self.number_of_characters = args.num_characters
        if args.party_level:
            self.level_of_characters = args.party_level

    def __str__(self) -> str:
        return '\nNumber of Characters:\t{0}\nCharacter Level:\t{1}\nCurrent Table:\t\t{2}'.format(
            self.number_of_characters,
            self.level_of_characters,
            self._current_table
        )