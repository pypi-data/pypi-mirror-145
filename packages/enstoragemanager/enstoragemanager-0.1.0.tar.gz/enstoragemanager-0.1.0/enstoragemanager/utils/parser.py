import argparse


def main_parser():
    # core
    parser = argparse.ArgumentParser()
    parser.add_argument("--geotagger", default=False, action="store_true", help="")
    parser.add_argument("--downsample", default=False, action="store_true", help="")

    # downsampler
    parser.add_argument(
        "--cfolder",
        required=False,
        help="folder to store compressed images",
        default="./compressed",
    )
    # geotagger
    parser.add_argument("--cvalue", required=False, default=5)
    parser.add_argument("--sfolder", default="original")
    parser.add_argument("--dfolder", default="sorted")
    parser.add_argument("--kmz", default="src/python/enimagegeotagger/maps/final.kmz")

    # storage
    parser.add_argument("--copydestination", required=False, default="original")
    parser.add_argument("--mntpoint", default="/mnt")
    parser.add_argument("--cfunc", default="copy")
    return parser
