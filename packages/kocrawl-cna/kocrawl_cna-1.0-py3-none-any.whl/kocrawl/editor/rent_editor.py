from kocrawl.editor.base_editor import BaseEditor
import re


class RentEditor(BaseEditor):

    def edit_rent(self, location: str, place: str, item:str, result: dict) -> dict:
        """
        join_dict를 사용하여 딕셔너리에 있는 string 배열들을
        하나의 string으로 join합니다.

        :param location: 지역
        :param place: 장소
        :param result: 데이터 딕셔너리
        :return: 수정된 딕셔너리
        """

        result = self.join_dict(result, 'near_name1')
        result = self.join_dict(result, 'near_address1')
        result = self.join_dict(result, 'near_name2')
        result = self.join_dict(result, 'near_address2')
        result = self.join_dict(result, 'near_name3')
        result = self.join_dict(result, 'near_address3')

        return result