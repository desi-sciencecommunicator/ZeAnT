def collect_blocks(color_i, parameters):
    '''collect cells across all blocks'''

    import os
    import h5py
    import numpy as np
    from types import SimpleNamespace
    from voluseg._tools.constants import hdf
    # REMOVED: pyspark imports, SparkSession setup, sc, accum_data class
    # from voluseg._tools.evenly_parallelize import evenly_parallelize

    # set up spark
    # import pyspark
    # from pyspark.sql.session import SparkSession
    # spark = SparkSession.builder.getOrCreate()
    # sc = spark.sparkContext

    p = SimpleNamespace(**parameters)

    dir_cell = os.path.join(p.dir_output, 'cells', str(color_i))

    fullname_volmean = os.path.join(p.dir_output, 'volume%d'%(color_i))
    with h5py.File(fullname_volmean+hdf, 'r') as file_handle:
        block_valids = file_handle['block_valids'][()]

    # class accum_data(pyspark.accumulators.AccumulatorParam):
    #     '''define accumulator class'''

    #     def zero(self, val0):
    #         return [[]] * 4

    #     def addInPlace(self, val1, val2):
    #         return [val1[i] + val2[i] for i in range(4)]

    # # cumulate collected cells
    # if p.parallel_clean:
    #     cell_data = sc.accumulator([[]] * 4, accum_data())

    # REMOVED: accum_data class and sc.accumulator

    def add_data(ii):                          # ii directly, not tuple_ii[1]
        try:
            cell_block_id = []
            cell_xyz = []
            cell_weights = []
            cell_timeseries = []

            fullname_block = os.path.join(dir_cell, 'block%05d'%(ii))
            with h5py.File(fullname_block+hdf, 'r') as file_handle:
                for ci in range(file_handle['n_cells'][()]):
                    cell_block_id.append(ii)
                    cell_xyz.append(file_handle['/cell/%05d/xyz'%(ci)][()])
                    cell_weights.append(file_handle['/cell/%05d/weights'%(ci)][()])
                    cell_timeseries.append(file_handle['/cell/%05d/timeseries'%(ci)][()])

            return [cell_block_id, cell_xyz, cell_weights, cell_timeseries]

        except KeyError:
            print('block %d is empty.'%ii)
        except IOError:
            print('block %d does not exist.'%ii)

    # if p.parallel_clean:
    #     evenly_parallelize(np.argwhere(block_valids).T[0]).foreach(add_data)
    #     cell_block_id, cell_xyz, cell_weights, cell_timeseries = cell_data.value
    
    # REMOVED: if p.parallel_clean branch entirely
    # Sequential collection, cleaned up from the else branch:
    
    idx_block_valids = np.argwhere(block_valids).T[0]
    results = [add_data(ii) for ii in idx_block_valids if add_data(ii) is not None]

    # Note: call add_data once per ii and filter None (failed blocks)
    results = list(filter(None, [add_data(ii) for ii in idx_block_valids]))
    cell_block_id = [ii for r in results for ii in r[0]]
    cell_xyz      = [v  for r in results for v  in r[1]]
    cell_weights  = [v  for r in results for v  in r[2]]
    cell_timeseries = [v for r in results for v in r[3]]

    # valids_tuple = zip([[]]*len(idx_block_valids), idx_block_valids)
    # cell_block_id, cell_xyz, cell_weights, cell_timeseries = list(zip(*map(add_data, valids_tuple)))
    # cell_block_id = [ii for bi in cell_block_id for ii in bi]
    # cell_xyz = [xyzi for ci in cell_xyz for xyzi in ci]
    # cell_weights = [wi for ci in cell_weights for wi in ci]
    # cell_timeseries = [ti for ci in cell_timeseries for ti in ci]

    # # convert lists to arrays
    # cn = len(cell_xyz)
    # cell_block_id = np.array(cell_block_id)
    # cell_lengths = np.array([len(i) for i in cell_weights])
    # cell_xyz_array = np.full((cn, np.max(cell_lengths), 3), -1, dtype=int)
    # cell_weights_array = np.full((cn, np.max(cell_lengths)), np.nan)
    # for ci, li in enumerate(cell_lengths):
    #     cell_xyz_array[ci, :li] = cell_xyz[ci]
    #     cell_weights_array[ci, :li] = cell_weights[ci]
    # cell_timeseries_array = np.array(cell_timeseries)

    # return cell_block_id, cell_xyz_array, cell_weights_array, cell_timeseries_array, cell_lengths

    # convert lists to arrays (unchanged)
    cn = len(cell_xyz)
    cell_block_id = np.array(cell_block_id)
    cell_lengths = np.array([len(i) for i in cell_weights])
    cell_xyz_array = np.full((cn, np.max(cell_lengths), 3), -1, dtype=int)
    cell_weights_array = np.full((cn, np.max(cell_lengths)), np.nan)
    for ci, li in enumerate(cell_lengths):
        cell_xyz_array[ci, :li] = cell_xyz[ci]
        cell_weights_array[ci, :li] = cell_weights[ci]
    cell_timeseries_array = np.array(cell_timeseries)

    return cell_block_id, cell_xyz_array, cell_weights_array, cell_timeseries_array, cell_lengths
