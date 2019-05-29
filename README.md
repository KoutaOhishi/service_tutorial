# service_tutorial

## Serviceについて
- ROSの通信方式の一つ
- 1対１の双方向通信  
  - client(要求) と server(応答)
  - topic通信は単方向通信（pub/sub)
- 同期的処理
  - serverはclientから要求があった時だけ処理を行い、結果をclientに返す
  - clientはserverからの応答があるまで次の処理に進めない
  - 情報の受け渡しが確実に行われる
  - 処理が終わるとclientとserverの通信は切れる
- topic通信との使い分け（個人的見解）
  - センサから得られる情報を扱う処理はtopic通信で行う
    - 情報の更新頻度が高いから
  - それ以外はservice通信で書くのがbetter

## Setup
```
cd ~/catkin_ws/src/

git clone https://github.com/KoutaOhishi/service_tutorial.git

git clone https://gitlab.com/TeamSOBITS/text_to_speech.git

chmod 755 service_tutorial/src/*

chmod 755 text_to_speech/src/*

sh text_to_speech/install.sh

cd ../

catkin_make

```

## Tutorial
### Clientをpythonで書く！
#### ①Serverの起動
まずはじめに、text_to_speechのserverを起動する。
```
roslaunch text_to_speech tts_google.launch
```

#### ②起動中のServiceを確認
別の端末を開いて、`rosservice list`と実行し、どんなサービスがmasterに登録されているかを確認する。
```
<実行結果>
/rosout/get_loggers
/rosout/set_logger_level
/speech_word ← 今回使うのはこれ！
/text_to_speech_node/get_loggers
/text_to_speech_node/set_logger_level
```

#### ③Serviceの型の確認
`rosservice type /speech_word`と実行し、 */speech_word* のサービスの型を確認する。

```
<実行結果>
text_to_speech/TextToSpeech
```

#### ④型の中身を確認
`rossrv show text_to_speech/TextToSpeech`と実行し、型の中身を確認する。
```
<実行結果>
string text ← clientからserverに送る情報
---
bool result ← serverからclientに送る情報

```

text_to_speechでは、clientが発話させたい文字列をserverに送り、  
serverは発話が終了したらclientにresultを返す。

#### ⑤端末からserverに情報を送ってみる
pythonのプログラムを書く前に、まずは端末側からserverに発話させたい文字列を送ってみる。  
以下のコマンドを実行する。(tab補完を使うと便利）
```
rosservice call /speech_word "text: 'Hello world.'"

<実行結果>
result: True
```
発話が終わってから`result: True`が返ってくるのが重要。  

#### ⑥pythonでclientを書いてみる
client側をpythonで書いてみましょう。  
キーボード入力から文字列を受け取り、  その文字列を、serverに送るプログラムを書いてください。  
プログラムは`service_tutorial/src/tts_client.py`に書いてください。  
解答例は`service_tutorial/src/SAMPLE_tts_client.py`に書いてます。  
プログラムが書けたら以下のコマンドを実行してclientを起動してください。
```
rosrun service_tutorial tts_client.py
```


### Serverをpythonで書く！
#### ①Serverの起動
今回作るServiceのイメージを掴むために、SAMPLEのプログラムを起動する。  
以下のコマンドを実行する。  
```
roslaunch service_tutorial count_down.launch
```

#### ②端末からserverに情報を送ってみる
別の端末を開き、以下のコマンドを実行する。
```
rosservice call /count_down "second: 5"

<実行結果>
flag: True
```
5秒経ってから`flag: True`が返ってきたはず。  

ちなみに、server側では以下の通りの実行結果になっている。  
```
[INFO] [xxxxxxxxxx.xxxxxx]: count_down_server ON
[INFO] [xxxxxxxxxx.xxxxxx]: 4
[INFO] [xxxxxxxxxx.xxxxxx]: 3
[INFO] [xxxxxxxxxx.xxxxxx]: 2
[INFO] [xxxxxxxxxx.xxxxxx]: 1
[INFO] [xxxxxxxxxx.xxxxxx]: Finish
```
上記のように、clientから数字を受け取ったらカウントダウンをする処理をserver側で書いてもらいます。

#### ③Serviceの型の確認
今回使うServiceの型はあらかじめ用意してある。  
端末で`rosservice type /count_down`と実行する。  
```
<実行結果>
service_tutorial/CountDown
```

#### ④型の中身を確認
端末で`rossrv show service_tutorial/CountDown`と実行する。
```
<実行結果>
int8 second
---
bool flag

```

#### ⑤serverをpythonで書いてみる
server側をpythonで書いてみましょう。  
clientから送られてきた秒数カウントダウンを行い、カウントが0になったら、clientにTrueと返してください。  
プログラムは`service_tutorial/src/count_down_server.py`に書いてください。  
解答例は`service_tutorial/src/SAMPLE_count_down_server.py`に書いてます。  
プログラムが書けたらすべての端末を閉じた後、以下のコマンドを実行してください。
```
#端末１
roscore

#端末2(serverの起動)
rosrun service_tutorial count_down_server.py

#端末３（serverに情報を送る）
rosservice call /count_down "second: 7"
```
