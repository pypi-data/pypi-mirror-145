""" Perform parameter calculations.

    Add new processing instructions for parameter blocks by adding to
    the processing_instructions dict.

    Note: This has to be kept in sync with how parameter block naming and
    discovery works in the provide package in this sub-module; ideally they
    would both share the discovery code.
"""
import itertools

import mdpeditor.mdpblocks.density_guided.vanilla


def tab_completion_hints():
    """ Provide tab completion hints for non-.mdp options
    """

    hints = [
        mdpeditor.mdpblocks.density_guided.vanilla.parameter_names().values(),
    ]

    # return the flattened result
    return list(itertools.chain(*hints))


def apply_instructions(parameters, block_names: str):
    """ Perform instructions by the parameter blocks
        Blocks may fill in a parameters that are needed by other blocks.

        Run through all blocks two times, being forgiving if
        keys are not found the first time, because they might be filled in
        by another block later.
    """
    processing_instructions = {
        'density_guided.vanilla':
        mdpeditor.mdpblocks.density_guided.vanilla.process,
    }

    # keep only the block names that have processing instructions
    block_names_to_process = [
        name for name in block_names if name in processing_instructions
    ]

    # try to evaluate all parameters by block-defined procedures, but don't do
    # anything if a key is not yet defined
    for block_name in block_names_to_process:
        processing_instructions[block_name](parameters)

    # during the second try, undefined parameters are an issue
    #   we collect errors across all blocks, report and then abort.
    error_message = ""
    for block_name in block_names_to_process:
        error = processing_instructions[block_name](parameters)
        if error:
            error_message += block_name + " ┐\n"
            spaces = " " * len(block_name)
            for (offending_parameter, reason) in error.items():
                error_message += spaces + " ├─ " + f"{offending_parameter}\n"
                error_message += spaces + "    " + f"  {reason}\n\n"

    if error_message:

        raise SystemExit("\nFix these issues, then try again:\n\n" +
                         error_message)
