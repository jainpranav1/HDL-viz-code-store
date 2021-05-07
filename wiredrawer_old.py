import gatematrix as gm
import queue
import numpy as np
import time

def sum1(a, b):
    return [a[0]+b[0], a[1]+b[1]]

def equal1(a, b):
    if (a[0] == b[0]) and (a[1] == b[1]):
        return True
    else:
        return False

def short_path(start, end, matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    paths = queue.Queue()
    paths.put([start])
    add = [start]


    # if "start" is left of "end", then move "right" is chosen
    # elif, "start" is right of "end", then move "left" is chosen
    # else, a path is generated manually
    hor_mot = []
    if start[1] < end[1]:
        hor_mot = [0, 1]
    elif start[1] > end[1]:
        hor_mot = [0, -1]
    else:
        print("lol")
        sp_path = []
        for g in range(start[0], end[0] + 1):
            sp_path.append([g, start[1]])
        return sp_path

    # if "start" is above "end", then move "down" is chosen
    # elif, "start" is below "end", move "up" is chosen
    # else, a path is generated manually
    if start[0] < end[0]:
        vert_mot = [1, 0]
    elif start[0] > end[0]:
        vert_mot = [-1, 0]
    else:
        ind = -1
        for z in reversed(range(start[1], end[1] + 1)):
            if matrix[start[0]][z] != -1:
                ind = z + 1
                break

        sp_path = []
        low_track = True
        for s in range(start[1], end[1] + 1):
            if s < ind:
                if low_track:
                    if matrix[start[0]][s] == -1:
                        sp_path.append([start[0], s])
                    else:
                        low_track = False
                        sp_path.append([start[0] - 1, s - 1])
                        sp_path.append([start[0] - 1, s])
                else:
                    if matrix[start[0] - 1][s] == -1:
                        sp_path.append([start[0] - 1, s])
                    else:
                        low_track = True
                        sp_path.append([start[0], s - 1])
                        sp_path.append([start[0], s])
            else:
                if low_track:
                    sp_path.append([start[0], s])
                else:
                    low_track = True
                    sp_path.append([start[0] - 1, s])
                    sp_path.append([start[0], s])

        return sp_path

    while not equal1(add[-1], end):
        if paths.empty():
            print("Error: No Path")
            return [[None, None]]

        add = paths.get()

        # iterates through moves
        moves = [sum1(add[-1], hor_mot), sum1(add[-1], vert_mot)]
        for n in moves:
            if (n[0] < num_rows) and (n[1] < num_cols) and (n[0] >= 0) and (n[1] >= 0):
                if matrix[n[0], n[1]] == -1:
                    new = add.copy()
                    new.append(n)
                    paths.put(new)

    return add

path = r"C:\Users\prana\Desktop\CSCE_312\P5Codes\P5Codes\Pranav-Jain-727009500\CPU.hdl"
gmatrix, phdl = gm.gate_matrix(path)

gmatrix[0:6, 3:7] = gmatrix[0:6, 3:7] - 1
gmatrix[6:10, 5:7] = gmatrix[6:10, 5:7] - 1
gmatrix[19:, 3:7] = gmatrix[19:, 3:7] - 1
gmatrix[15:19, 5:7] = gmatrix[15:19, 5:7] - 1


num_rows = len(gmatrix)
num_cols = len(gmatrix[0])

start = time.time()

'''
# list of overall chip's outputs
ov_out = []
for p in phdl["outputs"]:
    ov_out.append(p["name"])

end_dic = {}
# stores end points on end_dic dictionary
for p in phdl["parts"]:
    for k in p["external"]:
        if k["inout"] == "in":
            if k["name"] in end_dic:
                end_dic[k["name"]].append(p["coord"])
            else:
                end_dic[k["name"]] = [p["coord"]]


# adds coordinates for each wire
for p in phdl["parts"]:
    for k in p["external"]:
        if (k["inout"] == "out") and (k["name"] not in ov_out):
            for end in end_dic[k["name"]]:
                new_start = sum1(p["coord"], [0, 1])
                new_end = sum1(end, [0, -1])
                print("start end", new_start, new_end)
                path = short_path(new_start, new_end, gmatrix)
                print("path", path)
                path.append(end)
                if "path" in k:
                    k["path"].append(path)
                else:
                    k["path"] = [path]
'''

end = time.time()

total = end - start

print(total)

path = short_path([13, 2], [9, 2], gmatrix)
print(path)

for i in path:
    gmatrix[i[0]][i[1]] = 100

print(gmatrix)
print(phdl)
