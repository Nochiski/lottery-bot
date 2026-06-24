# 소개 

동행복권 사이트내에 계정에 예치금만 넣어두시면 이후 매주 로또와 연금복권을 구입하고 당첨을 체크하여 알려드려요!  

# 사용법 

![](./.github/images/check.png)

1. 레포지토리를 `fork` 합니다.
2. fork한 repo → **Settings → Secrets and variables → Actions → New repository secret** 으로 들어갑니다.
3. 아래 변수들을 **모두 Secret 으로** 등록합니다 (Variable 아님 — 워크플로우가 `secrets.` 로 읽습니다).
4. 매주 자동으로 로또·연금복권을 구매하고 당첨을 체크해 알림을 보냅니다 🎉

## 등록할 Secret

| Name | 값 | 필수 |
|---|---|---|
| `USERNAME` | 동행복권 아이디 | ✅ |
| `PASSWORD` | 동행복권 비밀번호 | ✅ |
| `COUNT` | 구매 수량 (예: `5`) | ✅ |
| `DISCORD_WEBHOOK_URL` | Discord 웹훅 URL | 알림 채널 중 택1 |
| `TELEGRAM_BOT_TOKEN` | 텔레그램 봇 토큰 | 알림 채널 중 택1 |
| `TELEGRAM_CHAT_ID` | 텔레그램 챗 아이디 | 텔레그램 사용 시 필수 |

> `USERNAME` / `PASSWORD` / `TELEGRAM_BOT_TOKEN` 은 민감정보이므로 반드시 Secret 으로 관리하세요. Name 은 표 그대로(대문자, 오타 금지) 입력해야 합니다.

# 알림 채널 

Discord, Telegram 으로 알림을 받을 수 있습니다 (둘 다 설정 시 동시 발송, 하나도 없으면 로그로만 출력).

- **Discord**: `DISCORD_WEBHOOK_URL` 만 등록하면 됩니다.
- **Telegram**: `TELEGRAM_BOT_TOKEN` 과 `TELEGRAM_CHAT_ID` 를 **모두** 등록해야 동작합니다.
  - **토큰**: [@BotFather](https://t.me/BotFather) 에서 봇 생성 시 발급. 노출되면 `/revoke` 로 즉시 재발급하세요.
  - **챗 아이디 얻는 법** (둘 중 하나)
    1. 봇에게 아무 메시지나 1개 보낸 뒤 `https://api.telegram.org/bot<TOKEN>/getUpdates` 를 열면 응답의 `"chat":{"id": ...}` 숫자가 챗 아이디 (메시지를 **먼저** 보내야 보임)
    2. 텔레그램에서 [@userinfobot](https://t.me/userinfobot) 에게 START → 답장으로 오는 `Id` 숫자

# Reference 
- https://github.com/roeniss/dhlottery-api
