# pyupbit_autotrade

pyupbit autotrade project
위 모델의 경우, 골든 크로스 전략을 코인 거래의 성격에 맞게 분 단위로 함축시켜, 순간적으로 값이 엄청나게 오르는 상황을 체크하고 매수/매도 할 수 있도록 한 모델입니다.

main함수를 실행시키면 자동 거래(모의)를 시작할 것입니다.

실제 돈으로 거래하고자 하는 경우, pyupbit access key와 secret key를 발급받아 main함수의 올바른 부분에 넣어주고,

 auto_trader(btc_tickers,1.05,1.02,1.01,access_key, secret_key) # Default, Test 이 함수를 주석처리(맨 앞에 #)해주시고, 
실행시키는 함수를 주석처리 되어있는 
#pyupbit_util_realtrade.auto_trader(btc_tickers,1.05,1.02,1.01,access_key, secret_key)  이 함수의 주석을 삭제해주면(맨 앞 # 삭제) 됩니다.

다만 매도 타이밍이 여러 구현 방법을 시도해봤지만 매우 좋지 않아서, 매수만 자동화하고 매도를 직접 하는 편이 좋습니다.(현재 그렇게 되도록 되어있습니다.)
