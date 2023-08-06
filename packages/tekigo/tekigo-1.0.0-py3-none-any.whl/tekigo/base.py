"""Base functions library for tekigo"""
import os.path as ospath
import logging
import numpy as np
import h5py

from tekigo.tools import approx_edge_from_vol_node

# The id of the line containing Metric quantity according to HIP
METRIC_NAME = "metric"


def update_h5_file(filename, parent_group, data_dict):
    """Update hdf5 file by adding a data dictionary to a parent group

    :param filename: the hdf5 file name
    :param parent_group: the parent group under which new datasests are appended
    :param data_dict: the data dictionary to append
    """
    if not ospath.isfile(filename):
        logging.warning(f"Creating void initial solution {filename}")
        with h5py.File(filename, "w") as h5f:
            h5f.create_group("Mesh")

    with h5py.File(filename, "r+") as h5f:
        if parent_group not in h5f:
            h5f.create_group(parent_group)

        for key in data_dict:
            if key in h5f[parent_group]:
                h5f[parent_group][key][...] = data_dict[key]
            else:
                h5f[parent_group][key] = data_dict[key]


def get_mesh_infos(mesh_f):
    with h5py.File(mesh_f, "r") as f_h:
        vol_node = f_h["VertexData"]["volume"][()]
        hmin = f_h["Parameters"]["h_min"][...][0]
        elem_type = list(f_h["Connectivity"].keys())[0]
        if elem_type == "tet->node":
            ncell = np.int_(f_h["Connectivity"]["tet->node"][...].shape[0] / 4)
        elif elem_type == "tri->node":
            ncell = np.int_(f_h["Connectivity"]["tri->node"][...].shape[0] / 3)
        else:
            raise ValueError("Unkown element type for computation of cell number")
    return hmin, ncell, vol_node


def metric_forecast(metric, mesh_file):
    with h5py.File(mesh_file, "r") as h5f:
        vol_node = h5f["VertexData"]["volume"][()]
    nnode_est = _estimate_nodes_number(metric)
    edge_est = metric * approx_edge_from_vol_node(vol_node)
    return nnode_est, edge_est


def filter_metric(vol_node, met_field, coarsen, nnode_max, min_vol):
    """Perform filtering on the metrics

    :param vol_node: the nodes volumes array
    :param met_field: the metric field to be filtered
    :param coarsen: boolean , allow coarsening or not
    :param nnode_max: limit the final number of nodes
    :param min_vol: limit the min volume


    :returns: - nnode_est : estimation of new number of nodes
              - met_field : metric field
    """

    if not coarsen:
        met_field = np.clip(met_field, None, 1.0)

    nnode_est = _estimate_nodes_number(met_field)
    msg = f"""
    |  _filter_metric
    |         coarsen  : {str(coarsen)}
    |       nnode_tgt  : {str(nnode_max)} 
    |          min_vol : {str(min_vol)}
    |  nnode_est start : {str(nnode_est)}

"""

    if nnode_est > nnode_max * 1.05:
        msg += "\n    | coarsen metric..."
        if coarsen:
            while nnode_est > nnode_max * 0.95:
                met_add = +0.025
                met_field += met_add
                nnode_est = _estimate_nodes_number(met_field)
                msg += f"\n    | nnodes {nnode_est} vs {nnode_max} (coarsening)"

        else:
            while nnode_est > nnode_max * 0.95:
                met_field = np.power(met_field, 0.8)
                nnode_est = _estimate_nodes_number(met_field)
                msg += f"\n    | nnodes {nnode_est} vs {nnode_max} (coarsening, clipped at 1)"

    elif nnode_est < nnode_max * 0.95:
        msg += "\n    | refine metric..."
        while nnode_est < nnode_max * 1.05:
            msg += f"\n    | nnodes {nnode_est} vs {nnode_max} (refining)"
            met_add = -0.025
            met_field += met_add
            nnode_est = _estimate_nodes_number(met_field)

    vol_est = _estimate_volume_at_node(vol_node, met_field)

    msg += "\n    | minimum forecasted volume"
    msg += f"\n    | before clipping :  {vol_est.min()}/{min_vol}"

    met_field_clean = np.where(
        vol_est > min_vol,
        met_field,
        np.power(min_vol / vol_node, 1.0 / 3.0),
    )
    vol_est = _estimate_volume_at_node(vol_node, met_field_clean)

    msg += f"\n    | after clipping : {vol_est.min()}/{min_vol}"

    nnode_est = _estimate_nodes_number(met_field_clean)

    logging.info(msg)
    return met_field_clean


def compute_metric(criteria, met_mix, n_node, max_refinement_ratio=0.6):
    r"""
        Calculate metric and estimates new number of nodes
        given refinement criteria and criteria choice method ('met_mix' parameter)

        :param criteria: a dictionary holding refinement criteria
        :type criteria: dict( )
        :param met_mix: type of metric mixing calculation method:

    if the criteria choice method is set on "average", the metric is computed as follows:

        .. math:: Metric = 1 - Rr_{max} < C >_i

        if the criteria choice method is set on "abs_max", the metric is computed as follows:

        .. math:: Metric = 1 - Rr_{max} \, C_i |_{ \tiny \displaystyle \max_{i \, \in \, C} | C_i |}

        with Metric and C (criteria) vectors of size n_nodes, Rr as Refinement ratio.

        :type met_mix: string
        :param n_node: current number of nodes
        :type n_node: integer
        :param max_refinement_ratio: refinement parameter for metric computation
        :type max_refinement_ratio: float

        :returns: metric field
    """
    met_field = np.ones(n_node) * 2.0
    if met_mix == "average":
        met_field = 0.0
        for crit in criteria:
            met_field = met_field + (1.0 - criteria[crit] * max_refinement_ratio)
        met_field = met_field / float(len(criteria))
    elif met_mix == "abs_max":
        max_crit = np.zeros(n_node)
        for crit in criteria:
            crit_value = criteria[crit] * max_refinement_ratio
            cond = np.abs(max_crit) > np.abs(crit_value)
            max_crit = np.where(cond, max_crit, crit_value)
        met_field = 1.0 - max_crit
    else:
        pass

    return met_field


# ------------------- PRIVATE -------------------
# internal methods
def _estimate_nodes_number(met_field):
    """Estimates nodes number given the metric field

    Parameters :
    ==========
    met_field_array : metric field
    vol_node : the nodes volumes array

    Returns :
    =======
    node_est : an estimation of the number of nodes
    """

    node_est = int(np.sum(1.0 / (met_field**3)))
    return node_est


def _estimate_volume_at_node(current_volume, met_field):
    """Estimates volume_at_nodes given the metric field

    Parameters :
    ==========
    met_field_array : metric field
    vol_node : the nodes volumes array

    Returns :
    =======
    node_est : an estimation of the number of nodes
    """

    volume_est = current_volume * met_field**3.0

    return volume_est
