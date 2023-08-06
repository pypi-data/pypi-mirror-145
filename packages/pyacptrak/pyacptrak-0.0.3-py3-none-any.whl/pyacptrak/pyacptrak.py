import svgutils.compose as sc
import numpy as np
from IPython.display import display
from importlib import resources
from importlib.metadata import distribution
from typing import Final, List, Dict, TypeVar, Type, Sequence
from typeguard import typechecked
import xmltodict

version = distribution('pyacptrak').version

TSegment = TypeVar("TSegment", bound="Segment")
TTrack = TypeVar("TTrack", bound="Track")
TAssembly = TypeVar("TAssembly", bound="Assembly")

def get_resource(module: str, name: str) -> str:
    return resources.files(module).joinpath(name)

def get_class_elements(obj, extra='    '):
    return str(obj.__class__) + '\n' + '\n'.join(
        (extra + (str(item) + ' = ' +
                  (get_class_elements(obj.__dict__[item], extra + '    ') if hasattr(obj.__dict__[item], '__dict__') else str(
                      obj.__dict__[item])))
         for item in sorted(obj.__dict__)))

#Segment class
@typechecked
class Segment(object):
    def __init__(self, s: str) -> None:
        self._s = s.lower()
        self._figure = None
        if (self._s == 'aa'):
            self._info = {
                'name': None,
                'length': 660,
                'type': '8F1I01.AA66.xxxx-1',
                'description': 'ACOPOStrak straight segment'
            }
            self._svg = 'segment_aa.svg'
            self._img = {'tl': (0.0, 0.25),
                            'bl': (0.0, 10.74),
                            'tr': (66.0, 0.25),
                            'br': (66.0, 10.74),
                            'w': 66.0,
                            'h': 10.074,
                            'rs': 0.0,
                            're': 0.0}
        elif (self._s == 'ab'):
            self._info = {
                'name': None,
                'length': 450,
                'type': '8F1I01.AB2B.xxxx-1',
                'description': 'ACOPOStrak curve segment A'
            }
            self._svg = 'segment_ab.svg'
            self._img = {'tl': (0.0, 0.25),
                            'bl': (0.0, 9.98),
                            'tr': (44.6, 3.56),
                            'br': (40.89, 12.523),
                            'w': 44.6,
                            'h': 12.523,
                            'rs': 0.0,
                            're': 22.5}
        elif (self._s == 'ba'):
            self._info = {
                'name': None,
                'length': 450,
                'type': '8F1I01.BA2B.xxxx-1',
                'description': 'ACOPOStrak curve segment B'
            }
            self._svg = 'segment_ba.svg'
            self._img = {'tl': (0.0, 3.56),
                            'bl': (3.71, 12.523),
                            'tr': (44.6, 0.25),
                            'br': (44.6, 9.98),
                            'w': 44.6,
                            'h': 12.523,
                            'rs': 22.5,
                            're': 0.0}
        elif (self._s == 'bb'):
            self._info = {
                'name': None,
                'length': 240,
                'type': '8F1I01.BB4B.xxxx-1',
                'description': 'ACOPOStrak circular arc segment'
            }
            self._svg = 'segment_bb.svg'
            self._img = {'tl': (0.0, 2.59),
                            'bl': (4.35, 13.081),
                            'tr': (23.2, 2.59),
                            'br': (18.85, 13.081),
                            'w': 23.2,
                            'h': 13.081,
                            'rs': 22.5,
                            're': 22.5}
        else:
            raise ValueError('Segment not supported. Supported segments "AA", "AB", "BA" or "BB"')
    
    def info(self) -> Dict[str, any]:
        return {k: v for k, v in self._info.items() if v is not None}

    def plot(self, angle: float = 0) -> TSegment:
        angle %= 360.0

        w = self._img['w']
        h = self._img['h']
        
        nw = (abs(w*np.cos(np.deg2rad(angle))) + abs(h*np.cos(np.deg2rad(90+angle)))).round(3)
        nh = (abs(w*np.sin(np.deg2rad(angle))) + abs(h*np.sin(np.deg2rad(90+angle)))).round(3)
        nx = (nw - ((w*np.cos(np.deg2rad(angle))) + (h*np.cos(np.deg2rad(90+angle)))).round(3))/2
        ny = (nh - ((w*np.sin(np.deg2rad(angle))) + (h*np.sin(np.deg2rad(90+angle)))).round(3))/2
        
        self._figure = sc.Figure(str(nw) + 'mm', str(nh) + 'mm', sc.SVG(get_resource('pyacptrak', 'img/' + self._svg)).move(nx,ny).rotate(angle))
        
        display(self._figure)
        
        return self
    
    def save(self, name: str = 'Segment.svg') -> None:
        if not isinstance(name, str):
            raise TypeError('The "name" argument must be string')

        self._figure.save(name)
    
    def __add__(self, other: (TSegment|TTrack)) -> TTrack:
        if isinstance(other, Segment):
            return Track([self, other])
        elif isinstance(other, Track):
            new_track = [self]
            new_track += other.segment.copy()
            return Track(new_track)
        else:
            raise TypeError('Segments can only be added to  Segment or Track objects')
    
    def __mul__(self, other: int) -> TTrack:
        if isinstance(other, int):
            if other < 0:
                raise TypeError('Segments can only be multiplied by positive integers')
            l = list()
            for i in range(other):
                l.append(self.__class__(self._s))
            return Track(l)
        else:
            raise TypeError('Segments can only be multiplied by positive integers')
    
    __rmul__ = __mul__
    
#Track class
@typechecked
class Track(object):
    def __init__(self, segments: List[Segment], seg_prefix: str = 'gSeg_', seg_offset: int = 1):
        if seg_offset < 0:
            raise TypeError('The "seg_offset" argument must be a positive integer')

        self.segment = [Segment(seg._s) for seg in segments]
        self.seg_prefix = seg_prefix
        self.seg_offset = seg_offset
        
    def __add__(self, other: (TSegment|TTrack)) -> TTrack:
        new_track = self.segment.copy()
        if isinstance(other, Segment):
            new_track.append(other)
        elif isinstance(other, Track):
            other_track = self.__class__(other.segment, other.seg_prefix, other.seg_offset)
            new_track = new_track + other_track.segment
        else:
            raise TypeError('Tracks can only be added to Segment or Track objects')
        return Track(new_track)
    
    def __mul__(self, other: int) -> TTrack:
        if isinstance(other, int):
            if other < 0:
                raise TypeError('Tracks can only be multiplied by positive integers')
            new_track = self.segment.copy()
            new_track = new_track * other
            return Track(new_track)
        else:
            raise TypeError('Tracks can only be multiplied by positive integers')
    
    def __len__(self) -> int:
        return len(self.segment)
    
    def info(self, compact: bool = False) -> Dict[str, any]:
        for i, s in enumerate(self.segment):
            s._info['name'] = self.seg_prefix + str(i + self.seg_offset).zfill(3)
        return {
            'seg_prefix': self.seg_prefix,
            'seg_offset': self.seg_offset,
            'length': sum(s._info['length'] for s in self.segment),
            'segment': [s._info for s in self.segment] if not compact else 'The track has ' + str(len(self.segment)) + ' segments',
        }
    
    def plot(self, angle: float = 0) -> TTrack:
        angle %= 360.0

        xabs = self.segment[0]._img['tl'][0]
        yabs = self.segment[0]._img['tl'][1]
        rot = angle
        gap = 0.5
        xmax = 0.0
        ymax = 0.0
        xmin = 0.0
        ymin = 0.0

        asm = []
        for seg in self.segment:
            rot += seg._img['rs']
            xabs += (seg._img['tl'][1] * np.sin(np.deg2rad(rot)))
            yabs -= (seg._img['tl'][1] * np.cos(np.deg2rad(rot)))
            
            w = seg._img['w']
            h = seg._img['h']
            nw = [(w*np.cos(np.deg2rad(rot))).round(3), (h*np.cos(np.deg2rad(90+rot))).round(3)]
            nh = [(w*np.sin(np.deg2rad(rot))).round(3), (h*np.sin(np.deg2rad(90+rot))).round(3)]
            
            xmax = max(xmax, xabs, xabs + sum(x for x in nw if x > 0))
            ymax = max(ymax, yabs, yabs + sum(y for y in nh if y > 0))
            xmin = min(xmin, xabs, xabs + sum(x for x in nw if x < 0))
            ymin = min(ymin, yabs, yabs + sum(y for y in nh if y < 0))
    
            asm.append(sc.SVG(get_resource('pyacptrak', 'img/' + seg._svg)).move(round(xabs, 3), round(yabs, 3)).rotate(round(rot, 3)))
    
            xabs += ((seg._img['tr'][0] * np.cos(np.deg2rad(rot))) + (seg._img['tr'][1] * np.cos(np.deg2rad(rot + 90))) + (gap * np.cos(np.deg2rad(rot))))
            yabs += ((seg._img['tr'][0] * np.sin(np.deg2rad(rot))) + (seg._img['tr'][1] * np.sin(np.deg2rad(rot + 90))) + (gap * np.sin(np.deg2rad(rot))))
            rot +=  seg._img['re']
        
        nw = (abs(xmax) + abs(xmin))
        nh = (abs(ymax) + abs(ymin))
        nx = abs(xmin)
        ny = abs(ymin)
        
        self._figure = sc.Figure(str(nw) + 'mm', str(nh) + 'mm', *asm).move(nx, ny)

        display(self._figure)
        
        return self
    
    def save(self, name: str = 'Track.svg') -> None:
        self._figure.save(name)
    
    __rmul__ = __mul__
    
#Loop class
@typechecked
class Loop(Track):
    def __init__(self, l: int = 2, w: int = 1, **kwars) -> None:
        self._l = l
        self._w = w

        if (self._l < 2):
            raise ValueError('The length of the loop must be at least 2')
        elif (self._w < 1):
            raise ValueError('The width of the loop must be at least 1')
        else:
            if (self._w == 1):
                self._track = TRACK180 + ((self._l - 2) * TRACK0) + TRACK180 + ((self._l - 2) * TRACK0)
            else:
                self._track = TRACK90 + ((self._w - 2) * TRACK0) + TRACK90 + ((self._l - 2) * TRACK0) + TRACK90 + ((self._w - 2) * TRACK0) + TRACK90 + ((self._l - 2) * TRACK0)
        super().__init__(self._track.segment, **kwars)

    def __add__(self, other: (TSegment|TTrack)) -> TAssembly:
        if isinstance(other, Segment):
            new_track = Track([other])
            return Assembly([self, new_track])
        elif isinstance(other, Track):
            return Assembly([self, other])

    def __mul__(self, other: int) -> TAssembly:
        l = [self]
        return Assembly([ item for item in l for _ in range(other) ])

    __rmul__ = __mul__

    def save(self, name: str = 'Loop.svg') -> None:
        self._figure.save(name)

#Assembly class
@typechecked
class Assembly(object):
    def __init__(self, tracks: List[Track], name: str = 'gAssembly_1') -> None:
        self.name = name
        self.track = list()
        
        old_prefix = None
        for track in tracks:
            if old_prefix != track.seg_prefix:
                t_len = track.seg_offset
            self.track.append(Track(track.segment, track.seg_prefix, t_len))
            t_len += len(track)
            old_prefix = track.seg_prefix
    
    def info(self, compact: bool = False) -> Dict[str, any]:
        return {
            'name': self.name,
            'length': sum(t.info()['length'] for t in self.track),
            'track': [t.info() for t in self.track] if not compact else 'The assembly has ' + str(len(self.track)) + ' tracks',
        }
    
    def export(self):
        _grp_track = _mk_track_dict(self)
        _grp_segment = _mk_seg_dict()
        _grp_shuttle = _mk_sh_dict()
        _grp_visu = _mk_visu_dict()
        
        _asm_cfg = {
                            'Configuration': {
                                'Element': {
                                    '@ID': "gAssembly_1",
                                    '@Type': "assembly",
                                    'Group': [
                                        _grp_track,
                                        _grp_segment,
                                        _grp_shuttle,
                                        _grp_visu,
                                    ],
                                    'Selector': {
                                        '@ID': "Alarms",
                                        '@Value': 'None'
                                    }
                                }
                            }
                        }
        
        _asm_cfg_tree = xmltodict.unparse(_asm_cfg, pretty=True, full_document=False)

        _asm_cfg_file = 'AsmCfg.assembly'
        with open(_asm_cfg_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(b'<?AutomationStudio FileVersion="4.9"?>\n')
            f.write(b'<?pyacptrak version="'+ version + b'" author="Jorge Centeno"?>\n')
            f.write(_asm_cfg_tree.encode('utf-8'))
        
        print(f'{_asm_cfg_file} created successfully')
        
        _sh_cfg = _mk_sh_stereotype()
        _sh_cfg_tree = xmltodict.unparse(_sh_cfg, pretty=True, full_document=False)
        _sh_cfg_file = 'ShCfg.shuttlestereotype'
        with open(_sh_cfg_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(b'<?AutomationStudio FileVersion="4.9"?>\n')
            f.write(b'<?pyacptrak version="'+ version + b'" author="Jorge Centeno"?>\n')
            f.write(_sh_cfg_tree.encode('utf-8'))
        
        print(f'{_sh_cfg_file} created successfully')
        

#Controller parameter internal class for segment internal class
class _control_par(object):
    def __init__(self):
        self.pos_proportional_gain = 150
        self.speed_proportional_gain = 120
        self.ff_total_mass = 0.7
        self.ff_force_pos = 1.5
        self.ff_force_neg = 1.5
        self.ff_speed_force_factor = 1.4
    
    def __str__(self):
        return get_class_elements(self)

#Segment internal class for parameter class
class _segment(object):
    def __init__(self, sh):
        self.simulation = 'Off'
        self.elongation = 'Inactive'
        self.stop_reaction = 'Induction Halt'
        self.speed_filter = 'Not Used'
        self._controller = 'Medium'
        self._sh = sh
        self._sh.bind_to(self._update_control_par)
        self.control_par = _control_par()
    
    def __str__(self):
        return get_class_elements(self)
    
    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self, value):
        self._controller = value
        self._update_control_par(self._sh.model)
    
    def _update_control_par(self, model):
        _controller = ['soft', 'medium', 'hard']
        if self._controller.lower() not in _controller:
            raise ValueError(f'The controller mode is not valid, please configure one of the following values: {_controller}')
        
        if ((model == '8F1SA.102.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.102.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.102.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        
        elif ((model == '8F1SA.100.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.100.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.100.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        
        elif ((model == '8F1SA.106.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.106.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.106.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 200
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        
        elif ((model == '8F1SA.104.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.104.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.104.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 200
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        
        elif ((model == '8F1SA.203.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.8
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.203.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.8
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.203.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 180
            self.control_par.ff_total_mass = 0.8
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        
        elif ((model == '8F1SA.201.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 1.2
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.201.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 1.2
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.201.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 180
            self.control_par.ff_total_mass = 1.2
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        
        elif ((model == '8F1SA.308.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 600
            self.control_par.speed_proportional_gain = 200
            self.control_par.ff_total_mass = 2.5
            self.control_par.ff_force_pos = 3.0
            self.control_par.ff_force_neg = 3.0
            self.control_par.ff_speed_force_factor = 1.1
        elif ((model == '8F1SA.308.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 600
            self.control_par.speed_proportional_gain = 300
            self.control_par.ff_total_mass = 2.5
            self.control_par.ff_force_pos = 3.0
            self.control_par.ff_force_neg = 3.0
            self.control_par.ff_speed_force_factor = 1.1
        elif ((model == '8F1SA.308.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 600
            self.control_par.speed_proportional_gain = 400
            self.control_par.ff_total_mass = 2.5
            self.control_par.ff_force_pos = 3.0
            self.control_par.ff_force_neg = 3.0
            self.control_par.ff_speed_force_factor = 1.1
            
        else:
            raise ValueError(f'There is no shuttle with those characteristics: model = {model}, controller = {self._controller.capitalize()}')
        
        print('The control parameters have been updated')

#Shuttle stereotype internal class for shuttle class
class _sh_stereotype_par(object):
    def __init__(self):
        self.velocity = 4.0
        self.acceleration = 50.0
        self.deceleration = 50.0
        self.jerk = 0.02
        self.user_data = 0
        self.recontrol = 'Active'
    
    def __str__(self):
        return get_class_elements(self)

#Shuttle internal class for parameter class
class _shuttle(object):
    def __init__(self):
        self.count = 10
        self.convoy = 'Inactive'
        self.collision_distance = 0.002
        self.error_stop = 0.006
        self.stereotype = 'ShuttleStereotype_1'
        self.stereotype_par = _sh_stereotype_par()
        self._size = 50
        self._magnet_plate = 2
        self._magnet_type = 'Straight'
        self.model = '8F1SA.100.xxxxxx-x'
        self.collision_strategy = 'Constant'
        self.extent_front = 0.025
        self.extent_back = 0.025
        self.width = 0.046
        self._observers = []
        self.auto_dimensions = True
    
    def __str__(self):
        return get_class_elements(self)
        
    @property
    def size(self):
        return self._size
    
    @property
    def magnet_plate(self):
        return self._magnet_plate
    
    @property
    def magnet_type(self):
        return self._magnet_type
    
    @size.setter
    def size(self, value):
        _size = [50, 100, 244]
        if value not in _size:
            raise ValueError(f'The shuttle size is not valid, please configure one of the following values: {_size}')
            
        self._size = value
        self._update_model()
        
    @magnet_plate.setter
    def magnet_plate(self, value):
        _magnet_plate = [1, 2]
        if value not in _magnet_plate:
            raise ValueError(f'The magnet plate is not valid, please configure one of the following values: {_magnet_plate}')
        
        self._magnet_plate = value
        self._update_model()
        
    @magnet_type.setter
    def magnet_type(self, value):
        _magnet_type = ['straight', 'skewed']
        if value.lower() not in _magnet_type:
            raise ValueError(f'The magnet type is not valid, please configure one of the following values: {_magnet_type}')
        
        self._magnet_type = value
        self._update_model()
    
    def _update_model(self):
        if ((self.size == 50) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.03
            self.model = '8F1SA.102.xxxxxx-x'
        elif ((self._size == 50) and (self.magnet_plate == 2) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.046
            self.model = '8F1SA.100.xxxxxx-x'
        elif ((self._size == 50) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'skewed')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.03
            self.model = '8F1SA.106.xxxxxx-x'
        elif ((self._size == 50) and (self.magnet_plate == 2) and (self.magnet_type.lower() == 'skewed')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.046
            self.model = '8F1SA.104.xxxxxx-x'
        elif ((self._size == 100) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.05
                self.extent_back = 0.05
                self.width = 0.03
            self.model = '8F1SA.203.xxxxxx-x'
        elif ((self._size == 100) and (self.magnet_plate == 2) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.05
                self.extent_back = 0.05
                self.width = 0.046
            self.model = '8F1SA.201.xxxxxx-x'
        elif ((self._size == 244) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.122
                self.extent_back = 0.122
                self.width = 0.03
            self.model = '8F1SB.308.xxxxxx-x'
        else:
            raise ValueError(f'There is no shuttle with those characteristics size: {self._size}, magnetic plate: {self.magnet_plate}, magnet type {self.magnet_type}')
        
        for callback in self._observers:
            callback(self.model)
        
        if self.auto_dimensions:
            print(f'The shuttle model and dimensions have been updated: {self.model}')
        else:
            print(f'The shuttle model has been updated: {self.model}')
            
    def bind_to(self, callback):
        self._observers.append(callback)

#Visualization internal class for parameter class
class _visu(object):
    def __init__(self):
        self.task = 4

#Parameter internal class
class _param(object):
    def __init__(self):
        self.shuttle = _shuttle()
        self.segment = _segment(self.shuttle)
        self.visu = _visu()
        
    def __str__(self):
        return get_class_elements(self)
    
#Constant definition
PARAM: Final = _param()
TRACK0: Final = Track([Segment('aa')])
TRACK45: Final = Track([Segment('ab'), Segment('ba')])
TRACK90: Final = Track([Segment('ab'), Segment('bb'), Segment('ba')])
TRACK135: Final = Track([Segment('ab'), Segment('bb'), Segment('bb'), Segment('ba')])
TRACK180: Final = Track([Segment('ab'), Segment('bb'), Segment('bb'), Segment('bb'), Segment('ba')])

#Create track group dictionary
def _mk_track_dict(asm: Assembly):
    grp = []
    for i, track in enumerate(asm.track):
        if i < 1:
            selector = {
                            '@ID': 'Position',
                            '@Value': 'Absolute',
                            'Property': {
                                        '@ID': 'SegmentCountDirection',
                                        '@Value': 'RightToLeft'
                                    },
                            'Group': [
                                        {
                                            '@ID': 'Translation',
                                            'Property': [
                                                {
                                                    '@ID': 'X',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Y',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Z',
                                                    '@Value': '0.0'
                                                }
                                            ]
                                        },
                                        {
                                            '@ID': 'Orientation',
                                            'Property': [
                                                {
                                                    '@ID': 'Angle1',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Angle2',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Angle3',
                                                    '@Value': '0.0'
                                                }
                                            ]
                                        }
                                    ]
                        }
        else:
            selector = {
                            '@ID': 'Position',
                            '@Value': 'RelativeToOne',
                            'Group': [
                                    {
                                        '@ID': 'TrackSegmentPosition',
                                        "Property": [
                                            {
                                                '@ID': 'SegmentRef',
                                                '@Value': ''
                                            },
                                            {
                                                '@ID': 'PositionRelativeTo',
                                                '@Value': 'FromEnd'
                                            }
                                        ]
                                    },
                                    {
                                        '@ID': 'Base',
                                        'Property': {
                                            '@ID': 'SegmentRef',
                                            '@Value': ''
                                        }
                                    }
                                ]
                        }
        
        
        grp.append({
                    '@ID': 'Track['+ str(i+1) +']',
                    'Group': {
                                '@ID': 'Segments',
                                'Property': []
                             },
                    'Selector': selector,
                    })
        for j, seg in enumerate(track.info()['segment']):
            grp[i]['Group']['Property'].append({
                                        '@ID': 'SegmentRef[' + str(j+1) + ']',
                                        '@Value': seg['name'],
                                    })
        
    
    tracks = {
                '@ID': 'Tracks',
                    'Property': {
                        '@ID': 'TrackSeparation',
                        '@Value': '0.030'
                    },
                    'Group': grp}
    return tracks

#Create segment group dictionary
@typechecked
def _mk_seg_dict(param: _segment = PARAM.segment):
    _simulation = ['off', 'on']
    _elongation = ['inactive', 'active']
    _stop_reaction = ['induction halt']
    _speed_filter = ['not used']
    
    if param.simulation.lower() not in _simulation:
        raise ValueError(f'The segment simulation is not valid, please configure one of the following values: {_simulation}')
    
    if param.elongation.lower() not in _elongation:
        raise ValueError(f'The segment simulation is not valid, please configure one of the following values: {_elongation}')
    
    if param.stop_reaction.lower() not in _stop_reaction:
        raise ValueError(f'The segment simulation is not valid, please configure one of the following values: {_stop_reaction}')
    
    if param.speed_filter.lower() not in _speed_filter:
        raise ValueError(f'The segment simulation is not valid, please configure one of the following values: {_speed_filter}')
    
    return {
                "@ID": "CommonSegmentSettings",
                "Property": [
                    {
                        "@ID": "SegmentSimulationOnPLC",
                        "@Value": param.simulation.capitalize()
                    },
                    {
                        "@ID": "ElongationCompensation",
                        "@Value": param.elongation.capitalize()
                    },
                    {
                        "@ID": "ScopeOfErrorReaction",
                        "@Value": "Assembly"
                    },
                    {
                        "@ID": "ShuttleIdentificationTime",
                        "@Value": "0"
                    }
                ],
                "Selector": [
                    {
                        "@ID": "StopReaction",
                        "@Value": ''.join(x for x in param.stop_reaction.title() if not x.isspace()),
                    },
                    {
                        "@ID": "SpeedFilter",
                        "@Value": ''.join(x for x in param.speed_filter.title() if not x.isspace()),
                    }
                ],
                "Group": {
                    "@ID": "ControllerParameters",
                    "Group": {
                        "@ID": "DefaultParameter",
                        "Group": [
                            {
                                "@ID": "Controller",
                                "Group": [
                                    {
                                        "@ID": "Position",
                                        "Property": {
                                            "@ID": "ProportionalGain",
                                            "@Value": str(param.control_par.pos_proportional_gain),
                                        }
                                    },
                                    {
                                        "@ID": "Speed",
                                        "Property": [
                                            {
                                                "@ID": "ProportionalGain",
                                                "@Value": str(param.control_par.speed_proportional_gain),
                                            },
                                            {
                                                "@ID": "IntegrationTime",
                                                "@Value": "0.0"
                                            }
                                        ]
                                    },
                                    {
                                        "@ID": "FeedForward",
                                        "Property": [
                                            {
                                                "@ID": "TotalMass",
                                                "@Value": str(param.control_par.ff_total_mass),
                                            },
                                            {
                                                "@ID": "ForcePositive",
                                                "@Value": str(param.control_par.ff_force_pos),
                                            },
                                            {
                                                "@ID": "ForceNegative",
                                                "@Value": str(param.control_par.ff_force_neg),
                                            },
                                            {
                                                "@ID": "SpeedForceFactor",
                                                "@Value": str(param.control_par.ff_speed_force_factor),
                                            },
                                            {
                                                "@ID": "ForceLoad",
                                                "@Value": "0.0"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "@ID": "MovementErrorLimits",
                                "Property": [
                                    {
                                        "@ID": "PositionError",
                                        "@Value": "0.005"
                                    },
                                    {
                                        "@ID": "VelocityError",
                                        "@Value": "5.0"
                                    }
                                ]
                            },
                            {
                                "@ID": "Diverter",
                                "Property": {
                                    "@ID": "ForceOverride",
                                    "@Value": "1.0"
                                }
                            }
                        ]
                    },
                    "Selector": {
                        "@ID": "AdditionalParameterSets",
                        "@Value": "NotUsed"
                    }
                }
            }

def _mk_sh_stereotype(param: _shuttle = PARAM.shuttle):
    return {
                    'Configuration': {
                        'Element': {
                            '@ID': param.stereotype,
                            '@Type': 'shuttlestereotype',
                            'Property': [
                                {
                                    '@ID': 'MeasurementUnit',
                                    '@Value': '5067858'
                                },
                                {
                                    '@ID': 'MeasurementResolution',
                                    '@Value': '0.00001'
                                }
                            ],
                            'Selector': [
                                {
                                    '@ID': 'MovementLimits',
                                    '@Value': 'Internal',
                                    'Property': [
                                        {
                                            '@ID': 'VelocityIsReadOnly',
                                            '@Value': '0'
                                        },
                                        {
                                            '@ID': 'AccelerationIsReadOnly',
                                            '@Value': '0'
                                        },
                                        {
                                            '@ID': 'DecelerationIsReadOnly',
                                            '@Value': '0'
                                        },
                                        {
                                            '@ID': 'UpdateMode',
                                            '@Value': 'Immediately'
                                        }
                                    ],
                                    'Selector': [
                                        {
                                            '@ID': 'Velocity',
                                            'Property': {
                                                '@ID': 'Velocity',
                                                '@Value': str(param.stereotype_par.velocity)
                                            }
                                        },
                                        {
                                            '@ID': 'Acceleration',
                                            'Property': {
                                                '@ID': 'Acceleration',
                                                '@Value': str(param.stereotype_par.acceleration)
                                            }
                                        },
                                        {
                                            '@ID': 'Deceleration',
                                            'Property': {
                                                '@ID': 'Deceleration',
                                                '@Value': str(param.stereotype_par.deceleration)
                                            }
                                        }
                                    ]
                                },
                                {
                                    '@ID': 'JerkFilter',
                                    '@Value': 'Used',
                                    'Property': {
                                        '@ID': 'JerkTime',
                                        '@Value': str(param.stereotype_par.jerk)
                                    }
                                }
                            ],
                            'Group': [
                                {
                                    '@ID': 'UserData',
                                    'Property': {
                                        '@ID': 'Size',
                                        '@Value': str(param.stereotype_par.user_data)
                                    }
                                },
                                {
                                    '@ID': 'StateTransitions',
                                    'Property': {
                                        '@ID': 'AutomaticRecontrol',
                                        '@Value': param.stereotype_par.recontrol
                                    }
                                }
                            ]
                        }
                    }
                }

#Create shuttle group dictionary
@typechecked
def _mk_sh_dict(param: _shuttle = PARAM.shuttle):
    _convoy = ['inactive', 'active']
    _collision_strategy = ['constant', 'variable', 'advanced constant', 'advanced variable']
    
    if param.convoy.lower() not in _convoy:
        raise ValueError(f'The convoy is not valid, please configure one of the following values: {_convoy}')
    
    if param.collision_strategy.lower() not in _collision_strategy:
        raise ValueError(f'The collision strategy is not valid, please configure one of the following values: {_collision_strategy}')
        
    return {
                "@ID": "Shuttles",
                "Property": [
                    {
                        "@ID": "MaxShuttleCount",
                        "@Value": str(param.count),
                    },
                    {
                        "@ID": "MaxShuttleCommandCount",
                        "@Value": "0"
                    },
                    {
                        "@ID": "UseConvoys",
                        "@Value": param.convoy.capitalize(),
                    }
                ],
                "Group": [
                    {
                        "@ID": "DistanceReserve",
                        "Property": [
                            {
                                "@ID": "Collision",
                                "@Value": str(param.collision_distance),
                            },
                            {
                                "@ID": "ErrorStop",
                                "@Value": str(param.error_stop),
                            }
                        ]
                    },
                    {
                        "@ID": "ShuttleStereotypes",
                        "Property": {
                            "@ID": "ShuttleStRef[1]",
                            "Value": param.stereotype,
                        }
                    },
                    {
                        "@ID": "MagnetPlateConfigurations",
                        "Selector": {
                            "@ID": "ShuttleType[1]",
                            "@Value": param.model,
                        }
                    },
                    {
                        "@ID": "CollisionAvoidance",
                        "Selector": {
                            "@ID": "Strategy",
                            "@Value": ''.join(x for x in param.collision_strategy.title() if not x.isspace()),
                        },
                        "Group": {
                            "@ID": "MaximumModelDimensions",
                            "Group": [
                                {
                                    "@ID": "Length",
                                    "Property": [
                                        {
                                            "@ID": "ExtentToFront",
                                            "@Value": str(param.extent_front),
                                        },
                                        {
                                            "@ID": "ExtentToBack",
                                            "@Value": str(param.extent_back),
                                        }
                                    ]
                                },
                                {
                                    "@ID": "Width",
                                    "Property": {
                                        "@ID": "Width",
                                        "@Value": str(param.width),
                                    }
                                }
                            ]
                        }
                    }
                ]
            }

#Create visualization group dictionary
@typechecked
def _mk_visu_dict(param: _visu = PARAM.visu):
    _task = [1, 2, 3, 4, 5, 6, 7, 8]
    
    if param.task not in _task:
        raise ValueError(f'The task class is not valid, please configure one of the following values: {_task}')
        
    return {
                "@ID": "Visualization",
                "Property": [
                    {
                        "@ID": "MonitoringPv",
                        "@Value": "::Vis:Mon"
                    },
                    {
                        "@ID": "ProcessingTaskClass",
                        "@Value": str(param.task),
                    }
                ]
            }