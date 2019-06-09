# does-it-rains-today-for-linebot

It posts whether it rains today to line bot.

![image](https://raw.githubusercontent.com/tsubasaogawa/does-it-rains-today-for-linebot/images/image.png)

## Requirements

- Dark Sky API Account
- LINEBot Account
- [LINEBot Publisher Layer](https://github.com/tsubasaogawa/linebot-publisher-layer)
- Environment Variables
  - CAN_POST_TO_LINE
    - Set empty not to post to line bot.
  - DARK_SKY_API_KEY
  - LINE_BOT_ACCESS_TOKEN
  - LINE_BOT_TO_ID
  - PRECIP_THRESHOLD_PERCENT
    - A threshold % whether it rains today or not. Default is 30%.
  - WEATHER_LATITUDE
  - WEATHER_LONGITUDE
