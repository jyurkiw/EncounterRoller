from EncounterRoller.lib.settings_manager import SettingsManager
from EncounterRoller.lib.template_json import template_json
import json
import os
import pathlib
import shutil

class TableManager(object):
    """Manage table files like Tizarus.json.
    This is not the monster data in the files. It's the files themselves.
    """
    def __init__(self, settings: SettingsManager):
        self.settings = settings
        self.tables_dir = os.path.join(settings.settings_path, 'tables')
        pathlib.Path(self.tables_dir).mkdir(parents=True, exist_ok=True)

    def get_all_tables(self):
        """Get all table files from storage and enumerate them for quick indexing.
        """
        return {
            i: { 'file': f, 'name': os.path.splitext(f)[0].replace('_', ' ').title() }
            for i, f in enumerate(os.listdir(self.tables_dir), 1)
        }

    def list_tables(self):
        """Print all tables to the terminal.
        """
        for idx, table in self.get_all_tables().items():
            print('{0}. {1}'.format(idx, table['name']))

    def save_table(self, file_path):
        """Save the passed file to storage.
        """
        file_path = self.get_table_file_name(True)
        shutil.copyfile(file_path,
            os.path.join(self.tables_dir, os.path.basename(file_path)))

    @property
    def table_path(self):
        return os.path.join(self.tables_dir, self.get_table_file_name(self.settings.current_table, True))
    
    def get_table_file_name(self, name, filename=False):
        """Get the file name of the passed table.
        Will accept either a name without the .json,
        or an index number.
        Returns the filename or the table name depending on
        the filename argument. If false, return the table name.
        If true, return the file name.
        """
        tables = self.get_all_tables()

        try:
            idx = int(name)
            if idx in tables:
                file = tables[idx]
            else:
                print('Didn\'t find {0} tables.'.format(idx))
                exit()
        except:
            file = next(filter(lambda f: f['name'] == name, tables.values()))
            if not file:
                print('Table {0} was not found.'.format(name))

        return file['file'] if filename else file['name']

    def manage_tables(self, args):
        """Manage table logic from the argument parser.
        """
        # Flag handling logic
        if args.new_table:
            # Create a new table file with starter template JSON structure.
            if args.name.endswith('.json'):
                file_name = args.name
            else:
                file_name = '{0}.json'.format(args.name).lower().replace(' ', '_')
            with open(file_name, 'w') as new_json:
                new_json.write(json.dumps(template_json, indent=4))
        elif args.save_table:
            # Save the passed table file to the table_dir.
            self.save_table(args.name)
        elif args.get_table:
            # Copy a table file from the table_dir to the local directory.
            file_name = self.get_table_file_name(args.name, True)
            shutil.copyfile(os.path.join(self.tables_dir, file_name), file_name)
        else:
            # Set table if all flags false
            table_name = self.get_table_file_name(args.name)
            self.settings.current_table = table_name
            