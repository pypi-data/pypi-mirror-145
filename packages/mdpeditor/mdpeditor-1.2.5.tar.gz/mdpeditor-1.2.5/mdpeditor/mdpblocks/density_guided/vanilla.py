""" Calculate parameters from external input for the vanilla settings
    in density guided simulations.
"""

# ensure consistent parameter naming for tab completion and processing
def parameter_names() -> dict:
    """Return the parameter names that this module sets

    Returns:
        dict: A dictionary with parameter names
    """

    return {
        "pixel-size": "pixel-size-in-nm",
        "reference-file-key-short": "reference-density-filename"
    }


def not_set_or_empty(dictionary, key) -> bool:
    """ Returns true if a key is not set or empty """
    return (key not in dictionary.keys() or not dictionary[key].strip())


def process(parameters):
    """ Set density guided simulation parameters from processing input

        Consume parameters that are not mdp options, but rather used to
        calculate these.

        Sets

            density-guided-simulation-gaussian-transform-spreading-width
            density-guided-simulation-reference-density-filename

        parameters : the full set of parameters, including non-mdp options
        block_name : allows error reporting.
    """

    errors = {}
    pixel_size_key = parameter_names()["pixel-size"]

    # set spreading width from pixel size if its not defined or empty
    width_key = "density-guided-simulation-gaussian-transform-spreading-width"
    if not_set_or_empty(parameters, width_key):
        try:
            parameters[width_key] = str(0.85 *
                                        float(parameters[pixel_size_key]))
            del parameters[pixel_size_key]
        except ValueError:
            errors[width_key] = ("use a real number instead of "
                                 f"{parameters[pixel_size_key]} when setting "
                                 "the spreading width with "
                                 f"{pixel_size_key}="
                                 f"{parameters[pixel_size_key]} ")
        except KeyError:
            errors[width_key] = ("unset, use " + f"{pixel_size_key}=YOURVALUE")
    else:
        if pixel_size_key in parameters:
            errors[width_key] = ("you have set a pixel size to determine the"
                                 "spreading width," +
                                 f" but {width_key} is already set to "
                                 f"{parameters[width_key]}")

    # handle the reference density file name
    reference_file_key = "density-guided-simulation-reference-density-filename"

    reference_file_key_short = (parameter_names()["reference-file-key-short"])

    if not_set_or_empty(parameters, reference_file_key):
        try:
            parameters[reference_file_key] = parameters[
                reference_file_key_short]
        except KeyError:
            errors[reference_file_key] = ("unset, use " +
                                          f"{reference_file_key_short}"
                                          f"=FILENAME")

    return errors
