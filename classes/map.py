import h5py
import math
import numpy as np

class Map:
    def __init__(self, filename: str):
        self.no_data_value = None
        self.cell_size = None
        self.up_left = (0, float("inf"))
        self.down_right = (float("inf"), 0)
        self.dim = None
        self.filename = filename
        try:
            self.f = h5py.File(filename, "r")
            for dataset_name in self.f.keys():
                dataset = self.f[dataset_name]
                xinf = dataset.attrs["xinf"]
                yinf = dataset.attrs["yinf"]
                xsup = dataset.attrs["xsup"]
                ysup = dataset.attrs["ysup"]
                if self.no_data_value is None:
                    self.no_data_value = dataset.attrs["nodata_value"]
                elif self.no_data_value != dataset.attrs["nodata_value"]:
                    raise Exception("Different nodata values")
                if self.cell_size is None:
                    self.cell_size = dataset.attrs["cellsize"]
                elif self.cell_size != dataset.attrs["cellsize"]:
                    raise Exception("Different cell sizes")
                if self.up_left[1] > xinf:
                    self.up_left = (self.up_left[0], xinf)
                if self.up_left[0] < ysup:
                    self.up_left = (ysup, self.up_left[1])
                if self.down_right[1] < xsup:
                    self.down_right = (self.down_right[0], xsup)
                if self.down_right[0] > yinf:
                    self.down_right = (yinf, self.down_right[1])
            self.dim = (int((self.up_left[0] - self.down_right[0]) / self.cell_size) + 1, int((self.down_right[1] - self.up_left[1]) / self.cell_size) + 1,)
        except Exception as e:
            print("Problem trying to read the file: ", e)
            
    def umt_yx(self, y: int, x: int) -> np.float64:
        for dataset_name in self.f.keys():
            dataset = self.f[dataset_name]
            if y >= dataset.attrs["yinf"] and y < dataset.attrs["ysup"] and x >= dataset.attrs["xinf"] and x < dataset.attrs["xsup"]:
                i = int((dataset.attrs["ysup"] - y) / self.cell_size)
                j = int((x - dataset.attrs["xinf"]) / self.cell_size)
                return np.float64(dataset[i, j])
        return self.no_data_value

    def resize(self, factor: int, transform: callable, name: str):
        new_cell_size = self.cell_size * factor
        new_filename = name + '.hdf5'
        new_file = h5py.File(new_filename, 'w')
        for dataset_name in self.f.keys():
            dataset = self.f[dataset_name]
            new_nrows = math.ceil((dataset.attrs["ysup"] - dataset.attrs["yinf"]) / factor)
            new_ncolumns = math.ceil((dataset.attrs["xsup"] - dataset.attrs["xinf"]) / factor)
            new_file.create_dataset(dataset_name, (new_nrows, new_ncolumns), np.float64)
            for key , value in dataset.attrs.items():
                new_file[dataset_name].attrs[key] = value
            new_file[dataset_name].attrs["cellsize"] = new_cell_size
            for i in range(0, new_nrows):
                for j in range(0, new_ncolumns):
                    y_lower = i * factor 
                    y_upper = (i + 1) * factor 
                    x_lower = j * factor 
                    x_upper = (j + 1) * factor 
                    new_value = np.float64(transform(dataset[y_lower:y_upper, x_lower:x_upper]))
                    new_file[dataset_name][i, j] = new_value
        new_file.close()
        return Map(new_filename)