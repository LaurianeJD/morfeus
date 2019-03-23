import argparse
from steriplus import BuriedVolume, read_gjf, read_xyz

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        "Steriplus program to calculate buried volume")
    parser.add_argument(
        'file', type=str, help='Input file, either .xyz, .gjf or .com')
    parser.add_argument(
        'atom1', type=int, help='Index of central metal atom (starting from 1)')
    parser.add_argument(
        '--density', type=float, help='Density of sphere grid', default=0.001)
    parser.add_argument(
        '--exclude', type=int, nargs="+",
        help='List of atoms to exclude from the calculation', required=True)
    parser.add_argument(
        "--include_hs", help="Include H atoms (default: False)",
        action='store_true')
    parser.add_argument(
        '--radii', type=str, help='Radii type: "crc", "bondi" (default)',
        choices=["bondi", "crc"], default="bondi")
    parser.add_argument(
        '--radii_scale', type=float,
        help='Radii scale factor (default 1.17)', default=1.17)
    parser.add_argument(
        '-r', '--radius', type=float,
        help='Radius of probe sphere', default=3.5)
    parser.add_argument(
        "--steric_map", type=int, nargs="+",
        help="Draw steric map with specified atoms to define z axis",)

    args = parser.parse_args()

    file = args.file
    if file[-4:] == ".xyz":
        elements, coordinates = read_xyz(file)
    elif file[-4:] == ".gjf" or file[-4:] == ".com":
        elements, coordinates = read_gjf(file)
    else:
        print("No valid input file. Use .xyz or .gjf/.com")
        return

    radii_type = args.radii
    radii_scale = args.radii_scale
    radius = args.radius
    density = args.density
    include_hs = args.include_hs
    exclude = args.exclude

    atom_1 = args.atom1

    bv = BuriedVolume(elements, coordinates, atom_1, exclude_list=exclude,
                      include_hs=include_hs, radius=radius,
                      radii_type=radii_type, radii_scale=radii_scale,
                      density=density)
    bv.print_report()
    if args.steric_map:
        bv.plot_steric_map(args.steric_map, "steric_map.png")

if __name__ == "__main__":
    main()