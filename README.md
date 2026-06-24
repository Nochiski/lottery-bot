# 소개 

동행복권 사이트내에 계정에 예치금만 넣어두시면 이후 매주 로또와 연금복권을 구입하고 당첨을 체크하여 알려드려요!  

# 사용법 

![](./.github/images/check.png)

- 레포지토리를 `fork`  합니다. 
- Settings - Secrets - Add a new secret 메뉴로 들어갑니다
- 환경 변수들을 만들어 줍니다 (.env.sample 참조) 
- 매주 로또 및 연금복권 구매 및 당첨 과정을 자동으로 알려드려요 🎉

# 알림 채널 

Discord, Telegram 으로 알림을 받을 수 있습니다 (둘 다 설정 시 동시 발송).

- **Discord**: `DISCORD_WEBHOOK_URL` 만 등록하면 됩니다.
- **Telegram**: `TELEGRAM_BOT_TOKEN` 과 `TELEGRAM_CHAT_ID` 를 모두 등록해야 동작합니다.
  - 토큰: [@BotFather](https://t.me/BotFather) 에서 봇 생성 시 발급
  - 챗 아이디: 봇과 대화를 시작한 뒤 `https://api.telegram.org/bot<TOKEN>/getUpdates` 를 열면 `chat.id` 확인 가능

# Reference 
- https://github.com/roeniss/dhlottery-api
