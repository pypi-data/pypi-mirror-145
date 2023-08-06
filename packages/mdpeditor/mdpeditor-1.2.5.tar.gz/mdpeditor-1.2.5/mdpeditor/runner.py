""" Run the command line interface """
import sys

import importlib.metadata
from rich.console import Console

import mdpeditor.arguments
import mdpeditor.compile
import mdpeditor.explain
import mdpeditor.tabcompletion


def console_prompt_string(compile_mode: bool) -> str:
    """ put together the string that prompts the user for input """
    output_string = ("\nPress [bold][ENTER][/bold] to switch to ")

    if compile_mode:
        output_string += "normal"
    else:
        output_string += "--explain"

    output_string += " mode.\n"
    output_string += ("Press [bold][TAB][/bold] to list input options.\n")
    output_string += ("Press [bold][CTRL]+C[/bold] to exit, type "
                      "[bold]help[/] for more details on usage.")

    output_string += "\n>"

    if compile_mode:
        output_string += "[italic] mdpeditor[/] "
    else:
        output_string += "[italic] mdpeditor --explain[/] "

    return output_string


def run_interactive_prompt(console, version):
    """ start an interactive prompt"""

    # introductory message
    console.rule(f"mdpeditor {version}", style="")
    console.print(
        "Welcome to the interactive mode of mdpeditor!"
        "\n\nHere you"
        " can learn about .mdp parameters and parameter blocks "
        "and test different parameter combinations.\n\nFor production"
        " code in workflows, copy paste the prompt below"
        " and have a look at [bold]mdpeditor --help[/].\n")

    # set up tab completion
    completer = mdpeditor.tabcompletion.setup_tab_completion()

    merge_right = False

    line = ""
    compile_mode = False
    while line is not None or line == "end":
        # swap mode if only [Enter] was pressed
        # alter tab completion
        if line == "":
            compile_mode = not compile_mode
            if compile_mode:
                completer.compile_mode()
            else:
                completer.explain_mode()

        try:
            console.rule(style="")
            line = console.input(console_prompt_string(compile_mode))
            if line == "":
                continue
            if compile_mode:
                output = mdpeditor.compile.run_compile(line.split(),
                                                       merge_right)
            else:
                output = mdpeditor.explain.run_explain(line)
            console.rule(style="")
            console.print(output)

        # end gracefully when the user interrupts
        except KeyboardInterrupt:
            line = None
        except EOFError:
            line = None
        # do not exit like we do when running pure command line mode
        except SystemExit as error:
            console.print(error.__str__() + "\n")

    console.print("\n\nThanks for using mdpeditor!")

    console.print(
        "\nDiscuss .mdp parameters at "
        "https://gromacs.bioexcel.eu/tag/mdp-parameters",
        justify="right")

    console.print(
        "Report issues and suggestions for mdpeditor at "
        "https://gitlab.com/cblau/mdpeditor/-/issues",
        justify="right")

    console.print("\n:Copyright: 2021,2022  Christian Blau", justify="right")


def run():
    """ run the command line interface """

    # set up the console for printing
    console = Console()

    # derive the program version via git
    try:
        version = importlib.metadata.version("mdpeditor")
    except importlib.metadata.PackageNotFoundError:
        version = "Unknown"

    command_line_arguments = (mdpeditor.arguments.
                              get_command_line_arguments(version))

    if command_line_arguments.explain:
        output_string = mdpeditor.explain.run_explain(
            command_line_arguments.explain[0])
        console.print(output_string)
        return

    if not command_line_arguments.compile:
        run_interactive_prompt(console, version)
        return

    output_string = mdpeditor.compile.run_compile(
        command_line_arguments.compile, command_line_arguments.merge_right)

    if command_line_arguments.compile[0].strip() == "help":
        console.print(output_string)
        return

    mdpeditor.compile.print_annotated_output(console, output_string, version,
                                             sys.argv,
                                             command_line_arguments.output)
