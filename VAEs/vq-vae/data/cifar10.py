import os
import sys
import numpy as np 

cifar_data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..','..', '..', 'cifar10-100-collection'))
sys.path.append(cifar_data_path)
from cifar10_data import data_iterator_cifar10

def cifar10_iterator(config, comm, train=True):
    '''
    Provide DataIterator with :py:class:`Cifar10DataSource`
    with_memory_cache and with_file_cache option's default value is all False,
    because :py:class:`Cifar10DataSource` is able to store all data into memory.

    '''
    data_iterator_ = data_iterator_cifar10(batch_size=config['train']['batch_size'], rng=np.random.RandomState(config['model']['rng']), 
                                      with_memory_cache=config['dataset']['with_memory_cache'], with_file_cache=config['dataset']['with_file_cache'])
    if comm.n_procs > 1:
        data_iterator_ = data_iterator_.slice(rng=None, num_of_slices=comm.n_procs, slice_pos=comm.rank)

    return data_iterator_