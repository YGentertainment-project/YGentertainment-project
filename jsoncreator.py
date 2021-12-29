filepath = 'weverse.csv'

with open(filepath, 'r', encoding='utf-8') as file:
    artist_lines = file.readlines()

for line in artist_lines:
    line = line.strip()
    artist, url = line.split(',')

    print('"{}": "{}",'.format(artist, url))
