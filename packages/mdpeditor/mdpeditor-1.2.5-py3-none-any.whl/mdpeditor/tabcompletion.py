""" Provide functionality to handle tab completion """
import readline

import mdpeditor.mdpblocks.process
import mdpeditor.mdpblocks.read


class PromptTabCompleter:
    """ Provide tab completion for the prompt """
    def __init__(self, blocks, parameter_keys):
        self.blocks = blocks
        self.parameter_keys = parameter_keys
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(" ")
        readline.set_completer(self.__complete_compile__)

    def __complete_compile__(self, text, state):
        """ add a = for parameters tab completion
        """
        results = [x + " " for x in self.blocks if x.startswith(text)] + [
            x + "=" for x in self.parameter_keys if x.startswith(text)
        ] + [None]
        return results[state]

    def __complete_explain__(self, text, state):
        """ provide tab completion for explain mode
        """
        results = [x + " " for x in self.blocks if x.startswith(text)] + [
            x + " " for x in self.parameter_keys if x.startswith(text)
        ] + [None]
        return results[state]

    def compile_mode(self):
        """set completion mode to compile mode (= after .mdp parameters)"""
        readline.set_completer(self.__complete_compile__)

    def explain_mode(self):
        """set completion mode to explain mode (no = after .mdp parameters)"""
        readline.set_completer(self.__complete_explain__)


def setup_tab_completion() -> PromptTabCompleter:
    """ Create a prompt tab completer with .mdp data loaded from modules """
    return PromptTabCompleter(
        mdpeditor.mdpblocks.read.available_parameter_blocks(),
        mdpeditor.explain.mdp_options_list() +
        mdpeditor.mdpblocks.process.tab_completion_hints())
