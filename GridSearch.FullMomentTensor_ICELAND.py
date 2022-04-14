#!/usr/bin/env python

import os
import numpy as np

from mtuq import read, open_db, download_greens_tensors
from mtuq.event import Origin
from mtuq.graphics import plot_data_greens2, plot_beachball, plot_misfit_lune
from mtuq.grid import FullMomentTensorGridSemiregular
from mtuq.grid_search import grid_search
from mtuq.misfit import Misfit
from mtuq.process_data import ProcessData
from mtuq.util import fullpath, merge_dicts, save_json
from mtuq.util.cap import parse_station_codes, Trapezoid



if __name__=='__main__':
    #
    # Carries out grid search over all moment tensor parameters
    #
    # USAGE
    #   mpirun -n <NPROC> python GridSearch.FullMomentTensor.py
    #


    path_data=    fullpath('pysep/20140825161903000/*.[zrt]')
    path_weights= fullpath('pysep/20140825161903000/weights.dat')
    event_id=     '20140825161903000'
    model=        'ak135'


    #
    # Body and surface wave measurements will be made separately
    #

    process_bw = ProcessData(
        filter_type='Bandpass',
        freq_min= 0.1,
        freq_max= 0.333,
        pick_type='taup',
        taup_model=model,
        window_type='body_wave',
        window_length=25.,
        capuaf_file=path_weights,
        )

    process_sw = ProcessData(
        filter_type='Bandpass',
        freq_min=0.025,
        freq_max=0.0625,
        pick_type='taup',
        taup_model=model,
        window_type='surface_wave',
        window_length=150.,
        capuaf_file=path_weights,
        )


    #
    # For our objective function, we will use a sum of body and surface wave
    # contributions
    #

    misfit_bw = Misfit(
        norm='L2',
        time_shift_min=-4.,
        time_shift_max=+4.,
        time_shift_groups=['ZR'],
        )

    misfit_sw = Misfit(
        norm='L2',
        time_shift_min=-15.,
        time_shift_max=+15.,
        time_shift_groups=['ZR','T'],
        )


    #
    # User-supplied weights control how much each station contributes to the
    # objective function
    #

    station_id_list = parse_station_codes(path_weights)


    #
    # Next, we specify the moment tensor grid and source-time function
    #

    grid = FullMomentTensorGridSemiregular(
        npts_per_axis=15,
        magnitudes=[4.6])

    wavelet = Trapezoid(
        magnitude=4.6)


    #
    # Origin time and location will be fixed. For an example in which they
    # vary, see examples/GridSearch.DoubleCouple+Magnitude+Depth.py
    #
    # See also Dataset.get_origins(), which attempts to create Origin objects
    # from waveform metadata
    #

    origin = Origin({
        'time': '2014-08-25T16:19:03.000000Z',
        'latitude': 64.612,
        'longitude': -17.472,
        'depth_in_m': 5000.0,
        })


    from mpi4py import MPI
    comm = MPI.COMM_WORLD


    #
    # The main I/O work starts now
    #

    if comm.rank==0:
        print('Reading data...\n')
        data = read(path_data, format='sac',
            event_id=event_id,
            station_id_list=station_id_list,
            tags=['units:cm', 'type:velocity'])


        data.sort_by_distance()
        stations = data.get_stations()


        print('Processing data...\n')
        data_bw = data.map(process_bw)
        data_sw = data.map(process_sw)


        print('Reading Greens functions...\n')
        greens = download_greens_tensors(stations, origin, model)

        print('Processing Greens functions...\n')
        greens.convolve(wavelet)
        greens_bw = greens.map(process_bw)
        greens_sw = greens.map(process_sw)


    else:
        stations = None
        data_bw = None
        data_sw = None
        greens_bw = None
        greens_sw = None


    stations = comm.bcast(stations, root=0)
    data_bw = comm.bcast(data_bw, root=0)
    data_sw = comm.bcast(data_sw, root=0)
    greens_bw = comm.bcast(greens_bw, root=0)
    greens_sw = comm.bcast(greens_sw, root=0)


    #
    # The main computational work starts now
    #

    if comm.rank==0:
        print('Evaluating body wave misfit...\n')

    results_bw = grid_search(
        data_bw, greens_bw, misfit_bw, origin, grid)

    if comm.rank==0:
        print('Evaluating surface wave misfit...\n')

    results_sw = grid_search(
        data_sw, greens_sw, misfit_sw, origin, grid)



    if comm.rank==0:

        results = results_bw + results_sw

        # array index corresponding to minimum misfit
        idx = results.idxmin('source')

        best_source = grid.get(idx)
        lune_dict = grid.get_dict(idx)
        mt_dict = grid.get(idx).as_dict()


        #
        # Generate figures and save results
        #

        print('Generating figures...\n')

        plot_data_greens2(event_id+'FMT_waveforms.png',
            data_bw, data_sw, greens_bw, greens_sw, process_bw, process_sw,
            misfit_bw, misfit_sw, stations, origin, best_source, lune_dict)


        plot_beachball(event_id+'FMT_beachball.png',
            best_source, stations, origin)


        plot_misfit_lune(event_id+'FMT_misfit.png', results)
        plot_misfit_lune(event_id+'FMT_misfit_mt.png', results, show_mt=True)
        plot_misfit_lune(event_id+'FMT_misfit_tradeoff.png', results, show_tradeoffs=True)

        print('Saving results...\n')

        merged_dict = merge_dicts(lune_dict, mt_dict, origin,
            {'M0': best_source.moment(), 'Mw': best_source.magnitude()})


        # save best-fitting source
        save_json(event_id+'FMT_solution.json', merged_dict)


        # save misfit surface
        results.save(event_id+'FMT_misfit.nc')


        print('\nFinished\n')
