from kocrawl.answerer.base_answerer import BaseAnswerer


class RentAnswerer(BaseAnswerer):

    def rent_form(self, location: str, kinds: str, item: str, result: dict) -> str:
        """
        여행지 출력 포맷

        :param location: 지역
        :param place: 장소
        :param result: 데이터 딕셔너리
        :return: 출력 메시지
        """

        msg = self.rent_init.format(location=location, kinds=kinds, item=item)
        msg += '{location} 근처의 '

        msg = self._add_msg_from_dict(result,'near_name1', msg, '가장 가까운 장소는 {near_name1}이고,')
        msg = self._add_msg_from_dict(result,'near_address1', msg, '{near_address1}에 위치해 있어요! \n')
        msg = self._add_msg_from_dict(result, 'near_name2', msg, '둘째로 가까운 장소는 {near_name2}이고,')
        msg = self._add_msg_from_dict(result, 'near_address2', msg, '{near_address2}에 위치해 있어요!\n')
        msg = self._add_msg_from_dict(result, 'near_name3', msg, '세번째로 가까운 장소는 {near_name3}이고,')
        msg = self._add_msg_from_dict(result, 'near_address3', msg, '{near_address3}에 위치해 있어요!\n')
        msg = msg.format(location=location, near_name1=result['near_name1'], near_address1=result['near_address1'],
                         near_name2=result['near_name2'], near_address2=result['near_address2'],
                         near_name3=result['near_name3'], near_address3=result['near_address3'],)

        return msg