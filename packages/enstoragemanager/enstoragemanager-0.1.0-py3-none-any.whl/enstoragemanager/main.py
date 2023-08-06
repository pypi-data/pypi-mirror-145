from copy import Storage
from utils.parser import main_parser

if __name__ == "__main__":
    parser = main_parser()
    args = parser.parse_args()
    copier = Storage(
        mount_point=args.mntpoint,
        destination=args.copydestination,
        copy_function=args.cfunc,
    )
    if str(args.cfunc) == "copy":
        copier.copy_files()
        print("copied")
    else:
        copier.move_files()
        print("moved files")
