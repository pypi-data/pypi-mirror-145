""" Allow to access the contents of pre-defined mdp parameter blocks"""
import importlib.resources
import configparser
import io

from collections import OrderedDict


def formatted_blocks() -> str:
    """Reformat blockname strings so that their hierarchy is easy to grasp
    """
    blocks = available_parameter_blocks()
    prefixes = [len(blockname.split(".")[0]) for blockname in blocks]
    longest_prefix = max(prefixes)
    previous_prefix = ""
    for index, blockname in enumerate(blocks):
        current_prefix = blockname.split(".")[0]

        # overwrite block prefix with whitespace if following block
        # with the same prefix
        if current_prefix == previous_prefix:
            blocks[index] = " " * len(
                previous_prefix) + blockname[len(previous_prefix):]

        # prepend spaces so that blocks are aligned at the dot
        blocks[index] = " " * (longest_prefix -
                               len(current_prefix)) + blocks[index]

        # add a newline if we change the block level
        if current_prefix != previous_prefix:
            blocks[index] = "\n" + blocks[index]

        previous_prefix = current_prefix

    return "\n".join(blocks)


def available_parameter_blocks():
    """
    List of available parameter blocks in the package resource
    """

    blocks = []

    # the mdp blocks are stored as a sub-package with non-python data
    # in nested folders like default/parameters.mdp
    mdpblock_package_contents = importlib.resources.contents(__package__)

    for package_content in mdpblock_package_contents:

        # go through all subfolders
        if not importlib.resources.is_resource(__package__, package_content):
            # look for .mdp files
            for block in importlib.resources.contents(__package__ + "." +
                                                      package_content):
                if block[-4:] == ".mdp":
                    blocks += [package_content + "." + block[:-4]]
    blocks.sort()

    return blocks


def default_parameter_block():
    """
    Return a parameter block that has all parameters set to default values
    """

    return read_parameter_block("default.parameters")


def read_parameter_block(block):
    """
    Read a list of specified parameter blocks as a mapping to an OrderedDict.
    """

    return mdp_string_to_ordered_dict(_parameter_block_as_string(block))


def description_string(block: str) -> str:
    """Return a string with a self-description of a parameter block
    """
    description = ""
    # print the first lines of the parameter file that are prepended with
    # a semicolon, omitting the semicolon
    block_as_string = _parameter_block_as_string(block)
    for line in block_as_string.splitlines():
        if len(line) > 0 and (line[0] == ';'):
            description += line[1:] + "\n"
        else:
            return description

    return description


def _parameter_block_as_string(block_name):
    """
    Return an .mdp parameter block from the package resources
    """

    return importlib.resources.read_text(
        __package__ + "." + block_name.split(".")[0],
        block_name.split(".")[1] + ".mdp")


def mdp_string_to_ordered_dict(mdp_string: str) -> OrderedDict:
    """
    Convert a string in .mdp format to an OrderedDict via configparser

    Values are treated as strings, comments are stripped.

    Args:
        mdp_string (string): Input string in .mdp format (key = value)

    Returns:
        OrderedDict: A dict with the parameters in order
    """

    # add a section heading to satisfy configparser
    mdp_string = "[parameters]\n" + mdp_string
    # provide this string as a file for configparser to read
    mdp_string_as_file = io.StringIO(mdp_string)

    config = configparser.ConfigParser(comment_prefixes=[";"],
                                       inline_comment_prefixes=[";"])
    config.read_file(mdp_string_as_file)

    return OrderedDict(config['parameters'])
