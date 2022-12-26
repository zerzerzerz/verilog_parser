from copy import deepcopy
import torch
import dgl

def construct_cell_graph(cells:list, pin2index:dict, fanin_or_fanout:dict):
    src = []
    dst = []
    for cell in cells:
        n_pin = len(cell['pins'])
        cell_class = cell['cell_class']
        for i in range(n_pin):
            for j in range(i+1,n_pin):
                pin_a = cell['pins'][i][0]
                pin_b = cell['pins'][j][0]
                pin_name_a = f"{cell['cell_name']}.{pin_a}"
                pin_name_b = f"{cell['cell_name']}.{pin_b}"
                a_is_fanout = pin_a in fanin_or_fanout[cell_class]['output']
                b_is_fanout = pin_b in fanin_or_fanout[cell_class]['output']

                if a_is_fanout and b_is_fanout:
                    continue
                elif not a_is_fanout and not b_is_fanout:
                    continue
                elif a_is_fanout and not b_is_fanout:
                    src.append(pin2index[pin_name_b])
                    dst.append(pin2index[pin_name_a])
                elif not a_is_fanout and b_is_fanout:
                    src.append(pin2index[pin_name_a])
                    dst.append(pin2index[pin_name_b])
                else:
                    raise RuntimeError
    return src, dst


def construct_net_graph(inter_connections:dict, pin2index:dict):
    src = []
    dst = []
    for wire_name, v in inter_connections.items():
        # if this is PI/PO, continue
        if wire_name in pin2index.keys():
            continue
        assert len(v['driver']) == 1
        for sink in v['sink']:
            src.append(pin2index[v['driver'][0]])
            dst.append(pin2index[sink])
    return src, dst


def construct_graph(
    cells:list, 
    inter_connections:dict, 
    pin2index:dict, 
    fanin_or_fanout:dict,
):
    res = {}
    res[('node','net_out','node')] = construct_net_graph(inter_connections, pin2index)
    res[('node','cell_out','node')] = construct_cell_graph(cells, pin2index, fanin_or_fanout)
    res[('node','net_in','node')] = deepcopy(res[('node','net_out','node')])[::-1]
    return dgl.heterograph(res)
