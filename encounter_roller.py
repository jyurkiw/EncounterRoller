from EncounterRoller.lib.settings_manager import SettingsManager
from EncounterRoller.lib.table_manager import TableManager
from EncounterRoller.lib.encounter_builder import EncounterBuilder
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

# Generate Encounters
encounters = subparsers.add_parser('gen', help='Generate one or more encounters.')
encounters.add_argument('subtable', nargs='*', type=str, help='The subtable to gen with.')
encounters.set_defaults(op='generate_encounter')

# List Generators
generators = subparsers.add_parser('generators', help='List encounter generators.')
generators.set_defaults(op='list_generators')

# Xp limits
xp_limits = subparsers.add_parser('xp', help='List modified xp limits.')
xp_limits.set_defaults(op='list_xp_limits')

args = main_parser.parse_args()

settings = SettingsManager()

# if arg op logic
# TODO: Get rid of the if-else logic. Use function calls in set_defaults instead,
# and put the function calls into the lib directory where they belong.
if args.op == 'list_loaded_options':
    pass
elif args.op == 'config':
    settings.set(args)
    print(settings)
elif args.op == 'table':
    TableManager(settings).manage_tables(args)
elif args.op == 'list_tables':
    TableManager(settings).list_tables()
elif args.op == 'list_generators':
    EncounterBuilder(settings, TableManager(settings)).list_generators()
elif args.op == 'generate_encounter':
    EncounterBuilder(settings, TableManager(settings)).build(args).print_encounters()
elif args.op == 'list_xp_limits':
    EncounterBuilder(settings, TableManager(settings)).list_xp_limits()

print(args)