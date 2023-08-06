""" Define and retrieve all command line options.
"""

import argparse


def get_command_line_arguments(version: str):
    """build, parse and return command line arguments

    Args:
        version (str): the current program version

    Returns:
        the parsed command line arguments
    """

    program_name = "mdpeditor"
    description = (
        "Compiles an .mdp file from preset .mdp parameter blocks"
        " and user settings. To learn more about available parameters"
        " use --explain. ")

    epilog = """Examples:
    mdpeditor --explain help
    \tShows available pre-defined parameter blocks

    mdpeditor force_field.charmm nsteps=100
    \tCompiles the pre-defined block force_field.charmm and
    \tsets "nsteps = 100" in the output
    """

    parser = argparse.ArgumentParser(
        description=description,
        prog=program_name,
        add_help=False,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(dest="compile",
                        nargs="*",
                        metavar="tokens",
                        help="use 'help' to learn about tokens")

    parser.add_argument(
        "--merge-duplicates",
        dest="merge_right",
        action='store_true',
        default=False,
        help="allow duplicate parameters by overwriting previously set"
        " parameters")

    parser.add_argument("--output",
                        nargs='?',
                        const='compiled.mdp',
                        type=argparse.FileType('w'),
                        help="write the compiled parameters to an .mdp file"
                        " (instead of command line)",
                        metavar="compiled.mdp")

    parser.add_argument(
        "--explain",
        dest="explain",
        nargs=1,
        metavar="explain",
        help="explain an .mdp parameter or parameter block",
    )

    parser.add_argument("-h",
                        "--help",
                        action="help",
                        help="show this help message and exit")

    parser.add_argument("--version",
                        action="version",
                        version=(f"{program_name} {version}"))

    return parser.parse_args()
