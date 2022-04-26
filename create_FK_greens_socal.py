#!/usr/bin/env python

import os
import numpy as np
from mtuq import read
from mtuq.util import fullpath
from mtuq.util.cap import parse_station_codes


def create_FK_greens():
    '''Create Greens' function associated with data by using FK. '''

    path_data = fullpath('/home/jovyan/scoped/pysep/20200404015318920/*.[zrt]')
    path_weights = fullpath('/home/jovyan/scoped/pysep/20200404015318920/weights.dat')
    event_id = '20200404015318920'

    # user specified searching depth in km
    # searching_depths = np.array([5, 11, 18])       # eg: at 5, 11, 18 km.
    searching_depths = np.arange(8, 13, 1)       # eg: from 8 to 13 km with interval of 1 km.

    # set model parameters.
    fk_command    = 'fk.pl'
    model_name    = 'socal'
    model_type    = 'f'
    npts          = 512         # must be 2^n
    dt            = 0.1
    src_type      = ['0', '2']  # 0-Explosion source, 2-Double-couple source
    is_sr_dist_degree = False

    searching_depths = np.ceil(searching_depths)
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

    # create the Greens function
    for d in searching_depths:
        for s_type in src_type:
            cmd_str = "%s -M%s/%d/%s -N%d/%.4f -S%s " % (fk_command, model_name, d, model_type, npts, dt, s_type)
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

