import re

from kocrawl.editor.base_editor import BaseEditor


class TermEditor(BaseEditor):
    def edit_term(self,results:dict):

        results['meaning'] = results['meaning'][9:-5]

        if "sim_meaning" in results.keys():
            results['sim_meaning'] = results['sim_meaning'][9:-5]
        return results
