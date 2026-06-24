import requests
import re
import html

class Notification:
    def __init__(self, telegram_bot_token: str = None, telegram_chat_id: str = None) -> None:
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id

    def send_lotto_buying_message(self, body: dict, webhook_url: str) -> None:
        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":  
            message = f"로또 구매 실패 (`{result.get('resultMsg', 'Unknown Error')}`) 남은잔액 : {body.get('balance', '확인불가')}"
            self._notify(webhook_url, message)
            return

        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body.get('balance', '확인불가')}\n```{lotto_number_str}```"
        self._notify(webhook_url, message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        # parse list without last number 3
        lotto_number = [x[:-1] for x in lotto_number]
        
        # remove alphabet and | replace white space  from lotto_number
        lotto_number = [x.replace("|", " ") for x in lotto_number]
        
        # lotto_number to string 
        lotto_number = '\n'.join(x for x in lotto_number)
        
        return lotto_number

    def send_win720_buying_message(self, body: dict, webhook_url: str) -> None:
        
        if body.get("resultCode") != '100':  
            message = f"연금복권 구매 실패 (`{body.get('resultMsg', 'Unknown Error')}`) 남은잔액 : {body.get('balance', '확인불가')}"
            self._notify(webhook_url, message)
            return       

        win720_round = body.get("round", "?")
        if win720_round == "?":
            try:
                 win720_round = body.get("saleTicket", "").split("|")[-2]
            except (IndexError, AttributeError, TypeError):
                 win720_round = "?"

        if not body.get("saleTicket"):
            win720_number_str = "번호 정보 없음"
        else:
            win720_number_str = self.make_win720_number_message(body.get("saleTicket"))

        message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body.get('balance', '확인불가')}\n```\n{win720_number_str}```"
        self._notify(webhook_url, message)

    def make_win720_number_message(self, win720_number: str) -> str:
        formatted_numbers = []
        for number in win720_number.split(","):
            formatted_number = f"{number[0]}조 " + " ".join(number[1:])
            formatted_numbers.append(formatted_number)
        return "\n".join(formatted_numbers)

    def send_lotto_winning_message(self, winning: dict, webhook_url: str) -> None:
        assert type(winning) == dict

        balance_str = winning.get('balance', '확인불가')
        try: 
            round = winning["round"]
            money = winning["money"]

            if winning["lotto_details"]:
                max_label_status_length = max(len(f"{line['label']} {line['status']}") for line in winning["lotto_details"])

                formatted_lines = []
                for line in winning["lotto_details"]:
                    line_label_status = f"{line['label']} {line['status']}".ljust(max_label_status_length)
                    line_result = line["result"]
    
                    formatted_nums = []
                    for num in line_result:
                        raw_num = re.search(r'\d+', num).group()
                        formatted_num = f"{int(raw_num):02d}"
                        if '✨' in num:
                            formatted_nums.append(f"[{formatted_num}]")
                        else:
                            formatted_nums.append(f" {formatted_num} ")
    
                    formatted_nums = [f"{num:>6}" for num in formatted_nums]
    
                    formatted_line = f"{line_label_status} " + " ".join(formatted_nums)
                    formatted_lines.append(formatted_line)
    
                formatted_results = "\n".join(formatted_lines)
            else:
                formatted_results = "상세 정보를 불러오지 못했습니다."

            is_winning = winning['money'] != "-" and winning['money'] != "0 원" and winning['money'] != "0"
            
            if is_winning:
                winning_message = f"로또 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 🎉 (남은잔액 : {balance_str})"
            else:
                winning_message = f"로또 *{winning['round']}회* - 다음 기회에... 🫠 (남은잔액 : {balance_str})"

            self._notify(webhook_url, f"```ini\n{formatted_results}```\n{winning_message}")
        except KeyError:
            message = f"로또 - 다음 기회에... 🫠 (남은잔액 : {balance_str})"
            self._notify(webhook_url, message)
            return

    def send_win720_winning_message(self, winning: dict, webhook_url: str) -> None:
        assert type(winning) == dict

        balance_str = winning.get('balance', '확인불가')
        try:
            if "win720_details" in winning and winning["win720_details"]:
                max_label_status_length = max(len(f"{line['label']} {line['status']}") for line in winning["win720_details"])
                formatted_lines = []
                for line in winning["win720_details"]:
                    line_label_status = f"{line['label']} {line['status']}".ljust(max_label_status_length)
                    formatted_lines.append(f"{line_label_status} {line['result']}")
                
                formatted_results = "\n".join(formatted_lines)
                message_content = f"```ini\n{formatted_results}```\n"
            else:
                message_content = ""

            is_winning = winning['money'] != "-" and winning['money'] != "0 원" and winning['money'] != "0"

            if is_winning:
                message = f"{message_content}연금복권 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 🎉 (남은잔액 : {balance_str})"
            else:
                 message = f"{message_content}연금복권 *{winning['round']}회* - 다음 기회에... 🫠 (남은잔액 : {balance_str})"

            self._notify(webhook_url, message)
        except KeyError:
            message = f"연금복권 - 다음 기회에... 🫠 (남은잔액 : {balance_str})"
            self._notify(webhook_url, message)

    def _notify(self, webhook_url: str, message: str) -> None:
        sent = False
        if webhook_url:
            self._send_discord_webhook(webhook_url, message)
            sent = True
        if self.telegram_bot_token and self.telegram_chat_id:
            self._send_telegram(message)
            sent = True
        if not sent:
            print(f"[Info] No notification channel configured. Message: {message}")

    def _send_discord_webhook(self, webhook_url: str, message: str) -> None:
        if not webhook_url:
            print(f"[Info] Webhook URL not found. Message: {message}")
            return

        payload = { "content": message }
        requests.post(webhook_url, json=payload, timeout=10)

    def _send_telegram(self, message: str) -> None:
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        html_message = self._to_telegram_html(message)
        res = requests.post(
            url,
            json={
                "chat_id": self.telegram_chat_id,
                "text": html_message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        if res.status_code != 200:
            # HTML 파싱 실패 시 원문 평문으로라도 전달 (알림 유실 방지)
            requests.post(
                url,
                json={ "chat_id": self.telegram_chat_id, "text": message },
                timeout=10,
            )

    def _to_telegram_html(self, message: str) -> str:
        # Discord 전용 표기를 텔레그램 HTML 로 변환
        message = message.replace(":moneybag:", "💰")

        parts = message.split("```")
        rendered = []
        for index, part in enumerate(parts):
            if index % 2 == 1:  # ``` ``` 코드블록 내부 → 등폭(monospace) 정렬 유지
                if "\n" in part:
                    first_line, rest = part.split("\n", 1)
                    if first_line.strip() and " " not in first_line.strip():
                        part = rest  # 'ini' 같은 언어 태그 줄 제거
                rendered.append(f"<pre>{html.escape(part, quote=False)}</pre>")
            else:
                escaped = html.escape(part, quote=False)
                escaped = re.sub(r"\*([^*\n]+)\*", r"<b>\1</b>", escaped)  # *강조* → 굵게
                rendered.append(escaped)
        return "".join(rendered)
