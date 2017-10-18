import h5py
import numpy as np
import os

file_list = ['data_format2_20170717_20170915.h5', 'data_format2_20170918_20170922.h5',
             'data_format2_20170925_20170929.h5', 'data_format2_20171009_20171013.h5']

def combine(originalFile, newFile):
    original_data = h5py.File(originalFile, 'a')
    new_data = h5py.File(newFile, 'r')
    new_data_keys = list(new_data.keys())
    for i in range(0, new_data_keys.__len__()):
        time = new_data_keys[i]
        data_matrix = np.array(new_data[time][:])
        original_data.create_dataset(time, data=data_matrix)
    original_data.close()
    new_data.close()


def combine_all(fileList, newFileName):
    newFile = h5py.File(newFileName, 'w')
    newFile.close()
    for f in fileList:
        combine(newFileName, f)


if __name__ == '__main__':
    # Path of this file
    local_path = os.path.dirname(os.path.abspath(__file__))
    # Path of dataset
    local_data_path = local_path + '/Data/'
    # Name of new file
    newFileName = 'latestData.h5'
    # Creat new file, combine data from file_list into new file
    combine_all([local_data_path + e for e in file_list], local_data_path + newFileName)

    # Test new file
    data = h5py.File(local_data_path + newFileName, 'r')
    data_keys = list(data.keys())
    print (data_keys)


