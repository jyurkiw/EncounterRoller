from random import choice
import json
import argparse
import re

cr_reg = re.compile('.*\(CR\s(?P<cr>\d{1,2})\)')

parser = argparse.ArgumentParser()
parser.add_argument('terrain', type=str, default=False, help="Type of terrain to generate for.")
parser.add_argument('-n', type=int, default=False, help="Number of encounters to generate.")
parser.add_argument('--characters', type=int, default=False, help="Set the number of PCs.")
parser.add_argument('--level', type=int, default=False, help="Set the party level.")

args = parser.parse_args()

with open('path/to/args.json', 'r') as af:
    a = json.loads(af.read())
    characters = int(a['pc_num_characters'])
    level = int(a['pc_level'])
    num = int(a['num_encounters'])
    monster_file = a['monster_file']

with open ('path/to/{0}.json'.format(monster_file), 'r') as mf:
    monsters = json.loads(mf.read())

with open('path/to/XP.json', 'r') as xpf:
    xp = json.loads(xpf.read())


if args.terrain == 'list':
    terrains = [t for t in monsters.keys()]
    for t in [p for p in terrains if p != 'Universal']:
        print(t)
    exit()
elif args.terrain == 'set':
    if args.n: a['num_encounters'] = str(args.n)
    if args.characters: a['pc_num_characters'] = str(args.characters)
    if args.level: a['pc_level'] = str(args.level)
    with open('path/to/args.json', 'w') as af:
        af.write(json.dumps(a))

    print('Characters: {0} | Party Level: {1} | Encounters/Tier: {2}'.format(
        a['pc_num_characters'],
        a['pc_level'],
        a['num_encounters']))
    exit()
else:
    universal = monsters['Universal']
    
    if args.terrain not in monsters: print('did you type that right?')
    
    encounters = monsters[args.terrain]['Encounters'] + universal

    characters = int(num)
    level = int(level)
    
    # Calculate XP limits
    limits = {
        xp_key: xp[xp_key][level - 1] * characters
        for xp_key in [k for k in xp.keys() if k != 'CR' and k != 'Multipliers']
    }

    # Create encounter groups
    for limit, xp_limit in limits.items():
        print(limit + ':')
        curr_xp = 0
        num_enemies = 0

        while True:
            monster = choice(encounters)
            cr = int(cr_reg.match(monster).group('cr'))
            mxp = xp['CR'][cr - 1]
            curr_xp += mxp
            num_enemies += 1
            effective_xp = int(curr_xp * [float(m['mul']) for m in xp['Multipliers']
                if num_enemies >= m['min'] and num_enemies <= m['max']][0])


            if effective_xp <= xp_limit:
                print(monster)
            else:
                print()
                break

    print()