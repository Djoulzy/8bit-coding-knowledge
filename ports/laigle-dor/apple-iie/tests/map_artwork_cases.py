"""Host map-policy regressions; native paging/overlays are checked separately."""
from pathlib import Path
from tempfile import TemporaryDirectory
from tools.debug_map import export_maps
from tools.resources import row_offset


class MapArtworkTests:
    def map_artwork(self, world):
        with TemporaryDirectory(prefix='laigle-map-') as directory:
            dest=Path(directory)
            _,report=export_maps(world,dest,self.video)
            return (dest/'maps.bin').read_bytes(),report

    @staticmethod
    def map_set_field(world,number,field,value):
        offset=4*number+1+field//4;shift=2*(field%4)
        world[offset]=(world[offset]&~(3<<shift))|(value<<shift)

    def test_map_artwork_ignores_locks_and_merges_doors_with_grilles(self):
        baseline,report=self.map_artwork(self.world)
        modified=bytearray(self.world)
        from model.world import Room
        for number in range(64):
            r=Room.decode(self.world,number)
            for field in range(3):
                if r.fields[field] in (1,2):
                    self.map_set_field(modified,number,field,3-r.fields[field])
            for field in (6,7,8):
                self.map_set_field(modified,number,field,(r.fields[field]+1)%4)
        actual,changed=self.map_artwork(modified)
        self.assertEqual(actual,baseline,'door/grille types and locks must not change pixels')
        self.assertNotEqual(changed['directed_links'],report['directed_links'],
                            'raw source details remain available in metadata')
        self.assertEqual(report['legend']['door_types'],['Porte / grille','Arche'])

    def test_map_artwork_hides_furniture_and_floor_obstacles_but_keeps_fireplaces(self):
        baseline,report=self.map_artwork(self.world)
        modified=bytearray(self.world)
        from model.world import Room
        for number in range(64):
            offset=256+4*number
            if modified[offset]&7 != 1:
                modified[offset]&=248  # remove non-fireplace fixtures, keep treasure/state
            # Clear only the obstacle bit; preserve the secret-fireplace bit.
            field=Room.decode(self.world,number).fields[3]
            self.map_set_field(modified,number,3,field&1)
        actual,_=self.map_artwork(modified)
        self.assertEqual(actual,baseline,'furniture and floor obstacles have no map icon')
        for number in range(64):modified[256+4*number]&=248
        without_fireplaces,_=self.map_artwork(modified)
        self.assertNotEqual(without_fireplaces,baseline,'fireplaces must remain visible')
        self.assertTrue(any(c['furnishing']=='fireplace' for c in report['cells']))
        self.assertTrue(all(c['furnishing'] in (None,'fireplace') for c in report['cells']))
        self.assertEqual({c['room'] for c in report['cells'] if c['floor_obstacle']},
                         {6,13,28,38})
        self.assertNotIn('Escalier',report['legend']['icons'])
        self.assertNotIn('Coffre',report['legend']['icons'])
        self.assertNotIn('Meuble',report['legend']['icons'])
        self.assertEqual(report['legend']['room_types'],['Salle sombre','Salle eclairee'])

    def test_map_artwork_marks_secret_fireplaces_with_a_solid_right_pillar(self):
        def pixel(data,page,x,y):
            return (data[page*8192+row_offset(y)+x//7]>>(x%7))&1

        data,report=self.map_artwork(self.world)
        self.assertEqual({c['room'] for c in report['cells'] if c['secret']},
                         {0,11,38,49,51,63})
        self.assertEqual(report['cells'][63]['furnishing'],'fireplace',
                         'B2 397 overrides the packed room-63 furnishing')
        for c in report['cells']:
            if c['furnishing']!='fireplace':continue
            p,x,y=c['page'],c['x'],c['y'];ink=int(c['dark'])
            if c['secret']:
                for row in range(7):
                    for col in range(4,7):
                        self.assertEqual(pixel(data,p,x+3+col,y+12+row),ink,c['room'])
                # No detached mark on the left wall of the room.
                for row in range(15,18):
                    self.assertEqual(pixel(data,p,x+1,y+row),1-ink,c['room'])
            else:
                self.assertEqual(pixel(data,p,x+8,y+13),1-ink,c['room'])
        # All initial secret fireplaces are lit. A controlled dark room checks
        # the same solid pillar in white, without changing historical records.
        dark=bytearray(self.world);dark[0]&=252
        dark_data,dark_report=self.map_artwork(dark)
        c=dark_report['cells'][0]
        for row in range(7):
            for col in range(4,7):
                self.assertEqual(pixel(dark_data,c['page'],c['x']+3+col,c['y']+12+row),1)
        self.assertIn('Passage secret',report['legend']['icons'])
        self.assertEqual(set(report['footer']),{'y','room_byte_columns'})
