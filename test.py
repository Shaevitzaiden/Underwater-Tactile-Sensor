#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


def get_grid_points(dims, deltas, border_offset):
        # Be careful with the x_dim+dx and y_dim+dy for any non perfectly divisible dimensions by the deltas
        dx, dy = deltas
        x_dim, y_dim = dims
        x_offset, y_offset = [3+12.65, 3+6.23]
        x_range = np.arange(start=border_offset, stop=x_dim+dx-border_offset, step=dx)
        y_range = np.arange(start=border_offset, stop=y_dim+dy-border_offset, step=dy)
        target_points = []
        for i in range(y_range.shape[0]):
            for j in range(x_range.shape[0]):
                target_points.append((round(x_range[j]+x_offset-x_dim/2,1), round(y_range[i]+y_offset-y_dim/2,1)))
        return target_points


if __name__ == "__main__":
    a  = np.arange(15)
    print(a)
    a = a.reshape((5,3))
    print(np.max(a, axis=1))
    