#!/usr/bin/env python

import os
import numpy as np
from mtuq import read
from mtuq.event import Origin
from mtuq.util import fullpath
from mtuq.util.cap import parse_station_codes


def create_FK_greens():
    '''Create Greens' function associated with data by using FK. '''

    path_data = fullpath('data/examples/20090407201255351/*.[zrt]')
    path_weights = fullpath('data/examples/20090407201255351/weights.dat')
    event_id = '20090407201255351'

    origin = Origin({
        'time': '2009-04-07T20:12:55.000000Z',
        'latitude': 61.454200744628906,
        'longitude': -149.7427978515625,
        'depth_in_m': 33033.599853515625,
        })

    # set model parameters.
    model_name    = 'socal'
    model_type    = 'f'
    npts          = 512
    dt            = 0.1
    src_type      = ['0', '2']  # 0-Explosion source, 2-Double-couple source
    is_sr_dist_degree = False

    src_depth = np.ceil(origin.depth_in_m/1000.0)   # in km
    # read the weight file
    station_id_list = parse_station_codes(path_weights)
    # read data
    data = read(path_data, format='sac',
                event_id=event_id,
                station_id_list=station_id_list,
                tags=['units:cm', 'type:velocity'])

    data.sort_by_distance()
    stations = data.get_stations()
    sr_dist = []
    for sta in stations:
        sr_dist.append(np.ceil(sta.sac.dist))

    for s_type in src_type:
        cmd_str = "fk.pl -M%s/%d/%s -N%d/%.4f -S%s " % (model_name, src_depth, model_type, npts, dt, s_type)
        # if source-receiver distance is degree, otherwise is km.
        if is_sr_dist_degree:
            cmd_str += '-D '
        # add source-receiver distance
        for sr_d in sr_dist:
            cmd_str += str(" %d " % sr_d)

        # create Green's function by using FK.
        os.system(cmd_str)

if __name__=='__main__':
    create_FK_greens()


# python ./create_fk_greens_socal.py
