#!/usr/bin/env python3
import numpy as np


def get_grid_points(dims, deltas, border_offset):
        # Be careful with the x_dim+dx and y_dim+dy for any non perfectly divisible dimensions by the deltas
        dx, dy = deltas
        x_dim, y_dim = dims
        x_offset, y_offset = [9.42, 3] #9.42,3
        x_range = np.arange(start=border_offset, stop=x_dim+dx-border_offset, step=dx)
        print(x_range)
        y_range = np.arange(start=border_offset, stop=y_dim+dy-border_offset, step=dy)
        target_points = []
        for i in range(y_range.shape[0]):
            for j in range(x_range.shape[0]):
                target_points.append((x_range[j]+x_offset, y_range[i]+y_offset))
        return target_points


if __name__ == "__main__":
    print(get_grid_points((12.5,12.5),(0.5,0.5),0.5))