from EncounterRoller.lib.table_manager import TableManager
from EncounterRoller.lib.settings_manager import SettingsManager
from EncounterRoller.lib.xp import challenge_rating, multipliers, xp_table
from random import choices
import json

class EncounterBuilder(object):
    def __init__(self, settings:SettingsManager, table_manager:TableManager):
        self.settings = settings
        self.table_manager = table_manager
        with open (self.table_manager.table_path, 'r') as table_file:
            self.table = json.loads(table_file.read())
        self.encounters = {}

    def list_generators(self):
        for idx, generator_name in enumerate(filter(lambda g: g != 'universal_monsters', self.table), 1):
            print('{0}.\t{1}'.format(idx, generator_name))

    def calculate_xp_limits(self):
        return {
            # level_of_characters - 1 to offset for characters starting at level 1 and not level 0.
            difficulty: xp[self.settings.level_of_characters - 1] * self.settings.number_of_characters
            for difficulty, xp in xp_table.items()
        }

    def get_monster_xp(self, monster):
        return challenge_rating[monster['cr']]

    def list_xp_limits(self):
        for tier, limit in self.calculate_xp_limits().items():
            print('{0}:\t{1}'.format(tier, limit))

    def get_xp_multiplier(self, num_monsters):
        for multiplier in multipliers:
            if multiplier['min'] <= num_monsters <= multiplier['max']:
                return float(multiplier['mul'])
        raise Exception('We should never get here. ({0} monsters broke something important.'.format(num_monsters))

    def build(self, args):
        try:
            subtable_idx = int(args.subtable[0])
            subtable_name = list(self.table.keys())[subtable_idx]
        except:
            subtable_name = ' '.join(args.subtable)
        subtable_list = self.table[subtable_name]['monsters']
        universal = self.table['universal_monsters']
        monster_list = subtable_list + universal
        monster_weights = ([int(self.table[subtable_name]['weight'])] * len(subtable_list)) + [1] * len(universal)
        xp_limits = self.calculate_xp_limits()
        encounters = {}

        for tier in xp_limits.keys():
            limit = xp_limits[tier]
            total_xp = 0
            encounters[tier] = []

            for monster in choices(monster_list, monster_weights, k=1000):
                xp = self.get_monster_xp(monster)
                if xp <= limit:
                    if (total_xp + xp) * float(self.get_xp_multiplier(len(encounters[tier]) + 1)) < limit:
                        encounters[tier].append(monster)
                        total_xp += xp

        self.encounters = encounters
        return self

    def print_encounters(self):
        if not [self.encounters.keys()]:
            print('No encounters created.')
            exit()
        limits = self.calculate_xp_limits()

        for tier, encounter in self.encounters.items():
            multiplier = self.get_xp_multiplier(len(encounter))
            effective_xp = int(sum([self.get_monster_xp(m) for m in encounter]) * multiplier)
            print('{0} (Total Effective XP: {1}/Max XP: {2}):'.format(tier.title(), effective_xp, limits[tier]))

            for monster in encounter:
                monster_xp = self.get_monster_xp(monster)
                print('\t{0}\t(CR: {1})\n\t\tXP: {2}/Effective XP: {3}'.format(
                    monster['name'],
                    monster['cr'],
                    monster_xp,
                    int(monster_xp * multiplier)
                ))
            print()
                

            
