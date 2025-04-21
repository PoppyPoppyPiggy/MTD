# modules/attacker.py
import random
from config import HONEYPOT_LURE_PROB, DECOY_CONFUSE_PROB

class Attacker:
    def __init__(self):
        # 공격자가 최신 방어자 정보를 가지고 있는지 여부
        self.current_info = True

    def choose_target(self, defender_state):
        """
        공격 대상 선택 (defender_state에서 현재 실제 자산/허니팟/디코이 정보를 참고 가능)
        defender_state 예시: {
            "real_ip": <현재 실제 자산 IP>,
            "honeypot_ip": <허니팟 IP or None>,
            "decoy_ips": [<디코이 IP 목록>],
            "last_shuffle": <마지막 셔플 tick>
        }
        """
        # 만약 최근 셔플로 정보가 무효화되었다면, 첫 공격은 잘못된 대상으로 갈 수 있음
        if not self.current_info:
            # 허니팟이 존재하면 이전 IP로 허니팟이 위치한 것으로 가정
            if defender_state.get("honeypot_ip") is not None:
                # 이전 정보를 따라 공격 -> 사실상 허니팟으로 유입
                target = "honeypot"
            else:
                # 이전 정보를 따라 공격 -> 존재하지 않는 곳으로 공격 (실패)
                target = None
            # 한 번 시행 후에는 공격자가 새로운 정보를 얻었다고 가정
            self.current_info = True
            return target

        # 현재 정보를 가지고 공격 대상을 확률적으로 선택
        rand_val = random.random()
        if defender_state.get("honeypot_ip") and rand_val < HONEYPOT_LURE_PROB:
            return "honeypot"
        elif defender_state.get("decoy_ips") and rand_val < HONEYPOT_LURE_PROB + DECOY_CONFUSE_PROB:
            # 디코이가 존재하고, rand가 허니팟+디코이 구간에 속하면 디코이 선택
            # 여러 디코이가 있으면 무작위 하나 선택
            return ("decoy", random.choice(defender_state["decoy_ips"]))
        else:
            return "real"

    def attack(self, defender):
        """
        방어자의 상태를 참고하여 공격 실행. defender는 Defender 객체.
        attack 결과를 문자열로 반환: "real", "honeypot", "decoy", or "fail"
        """
        state = defender.get_state()
        target_choice = self.choose_target(state)

        if target_choice is None:
            # 공격이 아예 실패 (존재하지 않는 표적)
            return "fail"
        if target_choice == "real":
            # 실제 자산 공격 성공
            return "real"
        if target_choice == "honeypot":
            # 허니팟에 공격이 도달
            return "honeypot"
        if isinstance(target_choice, tuple) and target_choice[0] == "decoy":
            # 특정 디코이(target_choice[1])를 공격 -> 디코이에 걸림
            return "decoy"
