from kocrawl.answerer.base_answerer import BaseAnswerer


class EcoAnswerer(BaseAnswerer):

    def eco_form(self,result: dict) -> str:
        msg = '일상에서 실천할 수 있는 저탄소 실천 방법에 대해 알려드릴께요! 😄 {slogan} \n {way}\n'.format(slogan = result['slogan'], way = result['way'])

        return msg