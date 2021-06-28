from EncounterRoller.lib.settings_manager import SettingsManager
from EncounterRoller.lib.table_manager import TableManager
import argparse

settings = SettingsManager()

# Main parser
main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers()
main_parser.set_defaults(op='list_loaded_options')

# Subcommand parsers
# Config
config = subparsers.add_parser('config', help='Configure the Encounter Roller.')
config.add_argument('--num_characters', '-n', type=int, help='The number of PCs.')
config.add_argument('--party_level', '-l', type=int, help='The average party level')
config.set_defaults(op='config')

# Set Table
table = subparsers.add_parser('table', help='Table management.')
table_action_group = table.add_mutually_exclusive_group()
table_action_group.add_argument('--new_table', '-n', action="store_true", help='Create new table file for editing.')
table_action_group.add_argument('--save_table', '-s', action="store_true", help='Save a table file.')
table_action_group.add_argument('--get_table', '-g', action="store_true", help='Get a table file for editing.')
table.add_argument('name', nargs='?', type=str, help='Set the current table.')
table.set_defaults(op='table')

# List Tables
tables = subparsers.add_parser('tables', help='List tables.')
tables.set_defaults(op='list_tables')

args = main_parser.parse_args()

settings = SettingsManager()

# if arg op logic

if args.op == 'list_loaded_options':
    pass
elif args.op == 'config':
    settings.set(args)
    print(settings)
elif args.op == 'table':
    TableManager(settings).manage_tables(args)
elif args.op == 'list_tables':
    TableManager(settings).list_tables()

print(args)