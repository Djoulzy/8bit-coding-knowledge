"""Source-backed 40-column panels, stored once in unused low auxiliary RAM."""
import re
import textwrap
from tools.common import digest, write_json

TEXT_SECTOR = 224


def literals(source, block, wanted):
    result = {}; address = 0x0501
    while set(wanted) - result.keys():
        header = source.read(address, 4, block)
        next_address = int.from_bytes(header[:2], 'little')
        number = int.from_bytes(header[2:], 'little')
        if next_address <= address:
            raise ValueError('Missing BASIC text lines: %s' % (set(wanted) - result.keys()))
        if number in wanted:
            body = source.read(address + 4, next_address - address - 4, block)
            result[number] = [v.decode('ascii') for v in re.findall(rb'"([^"\r\n]*)"', body)]
        address = next_address
    return result


def export_panels(source, dest):
    intro_lines = [1620, 1630, 1650, 1660, 1670, 1680, 1685, 1687]
    b1 = literals(source, 1, intro_lines + [1515, 1520, 1530, 1540, 1550, 1560, 1570])
    b2 = literals(source, 2, [3005, 3010, 3015, 13000, 13010, 13015, 13020, 13030, 13035])
    def clean(s):return ' '.join(s.split())
    panels = {}
    def panel(name, rows):
        for row, col, text in rows:
            if not 0 <= row < 24 or col < 0 or col + len(text) > 40:
                raise ValueError('Panel does not fit: %s %r' % (name, (row, col, text)))
        panels[name] = rows
    def center(row, text):return row, (40-len(text))//2, text
    rows = [center(0, "L'Aigle d'Or")]; row = 2
    for group in [[1620, 1630], [1650, 1660, 1670, 1680], [1685, 1687]]:
        paragraph = clean(' '.join(s for n in group for s in b1[n]))
        for text in textwrap.wrap(paragraph, 36):
            rows.append((row, 2, text)); row += 1
        row += 1
    rows.append(center(23, 'Une touche: suite    H / ?: aide'))
    panel('intro', rows)
    panel('exterior', [center(1, 'Exterieur du chateau'),
          (7, 5, clean(b2[3010][0])), (10, 5, clean(b2[3010][1])),
          (13, 5, clean(b2[3015][0])), (16,5,'4. Reprendre avec un code'),
          center(23, 'H / ?: commandes')])
    def offer(line):
        label, price = clean(b2[line][0]).split(':')
        return label.strip().ljust(18) + ': ' + price.strip()
    panel('merchant', [center(2, clean(b2[13000][0])),
          (6, 4, offer(13010)), (7, 7, clean(b2[13015][0])),
          (9, 4, offer(13020)), (11, 4, offer(13030)),
          (13, 4, offer(13035)), (16, 4, clean(b2[13035][1])),
          (18, 3, "Pieces d'or: 00000"), (20, 3, 'Achat ? (0-4)'),
          center(23, 'H / ?: commandes')])
    panel('inventory', [center(1, 'Inventaire'), (3, 2, 'En main : Vide'),
          (5, 2, 'Provisions'), (5, 22, 'Equipement'),
          (7, 2, 'Fioles'), (9, 2, 'Torches'), (11, 2, 'Cordes'),
          (13, 2, 'Pieds de biche'),
          (7, 22, 'Clef en fer'), (9, 22, 'Clef en or'),
          (11, 22, 'Bague'), (13, 22, 'Aigle (plomb)'),
          center(15, 'Objets de quete'),
          (17, 2, 'Livre'), (17, 22, 'Diamant'),
          (19, 2, "Aigle d'or"), (19, 22, 'Parchemins'), (19, 36, '0/3'),
          center(22, 'Espace / Entree / Echap : retour'), center(23, 'H / ? : aide')])
    commands = [clean(s) for n in [1515, 1520, 1530, 1540, 1550] for s in b1[n]][:12]
    commands[1] = 'Espace: Arret, position neutre'
    rows = [center(1, 'Commandes')]
    rows += [(3+i, 2, s) for i, s in enumerate(commands)]
    rows += [(15, 2, 'T: Allumer une torche'), (16, 2, 'H / ?: Cette aide'),
             (17, 2, 'C: Code de reprise'),
             (18, 2, 'Objet en main:'), (19, 2, '0: Vide             1: Torche'),
             (20, 2, '2: Clef en fer      3: Clef en or'),
             (21, 2, '4: Fiole            5: Pied de biche'),
             center(23, 'Une touche: retour')]
    panel('help', rows)
    panel('name', [center(4, "L'Aigle d'Or"), center(7, "Comment t'appelles-tu ?"),
          (10, 7, 'Nom: ______'), center(13, 'Six caracteres au maximum'),
          center(15, 'Entree pour continuer'), center(16, 'Retour arriere pour corriger'),
          center(23, '?: Commandes')])
    panel('debug', [center(1, 'Menu de test'),
          (4, 3, '1: Tous les objets (9 consommables)'),
          (6, 3, '2: Teleportation'),
          (7, 3, '3: Carte du chateau'),
          (9, 3, 'Salle actuelle: 00'),
          (12, 3, 'Destination: __  (0-63)'),
          (14, 3, '2 puis numero et Entree'),
          (15, 3, 'Retour arriere: corriger'),
          center(23, 'Echap / Ctrl+D: retour au jeu')])
    panel('code_save', [center(2,'Code de reprise'),
          center(5,'Piece et inventaire uniquement'),
          center(7,'Notez les 18 caracteres ci-dessous :'),
          (9,10,'______-______-______'),
          center(12,'Le nom sera saisi au prochain depart.'),
          center(15,'Or, force et salles ne sont pas sauves.'),
          center(20,'Espace / Entree / Echap : retour'), center(23,'H / ? : aide')])
    panel('code_load', [center(2,'Reprendre une aventure'),
          center(5,'Saisissez les 18 caracteres du code.'),
          (9,10,'______-______-______'),
          center(12,'Le nom saisi au debut sera conserve.'),
          center(15,'Or, force et salles : nouvelle partie.'),
          center(18,'Entree : reprendre'), center(19,'Retour arriere : effacer'),
          center(22,'Echap: annuler   H / ?: aide')])
    # Preserve the existing compact end-screen layout, using the shared AUX
    # text engine instead of 480 padded MAIN bytes.
    for name, first, second in [
            ('dead', 'Vous avez perdu', 'Votre aventure est terminee'),
            ('win', 'Vous avez reuni les trois objectifs', 'Victoire'),
            ('depart', 'Fin du voyage', 'Vous quittez le chateau')]:
        panel(name, [(4,0,"L'Aigle d'Or             Or:00000"), (8,0,first), (9,0,second),
                     (10,0,'O ou Entree: nouvel essai')])
    data = bytearray(); offsets = {}
    for name, rows in panels.items():
        offsets[name] = len(data)
        for row, col, text in rows:
            data.extend([row, col]); data.extend(text.encode('ascii')); data.append(0)
        data.append(255)
    if len(data) > 0xC00:raise ValueError('Text archive exceeds AUX $1400-$1FFF')
    (dest/'text-panels.bin').write_bytes(data)
    report = {'bytes':len(data), 'sha256':digest(data), 'disk_sector':TEXT_SECTOR,
              'aux_start':'$1400', 'panels':panels, 'offsets':offsets,
              'source_b1_lines':sorted(b1), 'source_b2_lines':sorted(b2),
              'adaptations':'source letter case retained, whitespace/reflow, 24 rows; Apple help keys/T command; spaced two-column inventory and hidden development menu are new target text'}
    write_json(dest/'text-panels.json', report)
    names = [None, 'exterior', 'merchant', 'inventory', None, 'dead', 'win', 'depart', 'name', None, 'help', 'intro', 'debug', None, None, None, 'code_save', 'code_load']
    lines = ['.segment "TEXTASSETS"', 'text_assets: .incbin "text-panels.bin"', '.segment "RODATA"']
    for part in ['lo', 'hi']:
        lines += ['text_panel_%s: .byte ' % part + ','.join(
            ('<' if part=='lo' else '>')+'(text_assets+%d)'%offsets[n] if n else '0' for n in names)]
    return lines, report
