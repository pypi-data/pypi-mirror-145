
from kocrawl.answerer.base_answerer import BaseAnswerer


class TermAnswerer(BaseAnswerer):

    def term_form(self,result: dict) -> str:
        msg = '{term}의 뜻은 다음과 같아요!\n{meaning}\n'.format(term = result['term'], meaning = result['meaning'])
        if "sim_meaning" in result.keys():
            msg += '비슷한 단어인 {sim_term}에 대해서도 알아볼까요?\n{sim_meaning}\n'.format(sim_term = result['sim_term'], sim_meaning = result['sim_meaning'])
        return msg
