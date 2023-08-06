"""module storing the tekigo specific logging functions"""


import os, sys
import logging


def logging_start(out_dir):
    f_log = os.path.join(out_dir, f"tekigo_{os.getpid()}.log")
    logging.basicConfig(
        level=logging.INFO,
        # format="%(levelname)s - %(message)s",
        format="%(message)s",
        handlers=[
            logging.FileHandler(
                f_log, mode="w"
            ),  # set mode to "a" to append
            logging.StreamHandler(sys.stdout),
        ],
    )


def logging_banner(title):

    logging.info(f"\n\n======= {title} =========\n\n")


def logging_pyhip(
    hausdorff_distance,
    frozen_patch_list,
    max_spacing_gradient,
    periodic_adaptation,
):
    """log PyHIP parameters"""
    logging.info(f"   Hip specific arguments")
    logging.info(f"   max_spacing_gradient : {max_spacing_gradient}")
    if hausdorff_distance is not None:
        logging.info(f"   hausdorff_distance : {hausdorff_distance}")
    else:
        logging.info(f"   hausdorff_distance : (auto)")
    if frozen_patch_list:
        plist = "\n - ".join(frozen_patch_list)
        logging.info(f"   frozen_patch_list : \n - {plist}")
    if periodic_adaptation:
        logging.info(f"   periodic adaptation enabled")
    else:
        logging.info(f"   periodic adaptation disabled\n")


def logging_mesh(name, nnode, ncell, h_min):
    logging.info(f"   {name}:")
    logging.info(f"   Number of nodes     {nnode}")
    logging.info(f"   Number of cells     {ncell}")
    logging.info(f"   Minimal edge size   {h_min:1.5e}\n")


def logging_field(name, field):
    logging.info(f"   Field {name} : {field.min():1.4f}, {field.max():2.4f}\n")
