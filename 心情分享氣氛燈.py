import network #引入network模組,用於網絡連接
import ledstrip #引入ledstrip模組,用於控制1ed燈的特效
from umqtt.robust import MQTTClient #引入MQTTClient模組,用於在物聯網(IoT)中進行通訊的模組

#建立一個字節變數來存儲 LED 燈帶的動畫效果
led_strip_effect = b'0'
#設定條燈腳位為 4,燈珠數量為 15
ledstrip.setup(4,15)

#連線到無線網路
sta_if = network.WLAN(network.STA_IF)#創建一個WLAN 物件,設定為 station 模式,以連接到無線網路
sta_if.active(True)#激活 WLAN 介面
sta_if.connect("無線網路基地台","無線網路密碼")#連接到指定的無線網路

#循環測試網路直到網路連線成功
while not sta_if.isconnected():
    pass
print("控制板已連線")

# 創建一個 MQTT 客戶端物件,用來連接到 Adafruit IO 服務
client = MQTTClient(
    client_id="",
    server="io.adafruit.com",
    user="AIO 帳號",
    password="AIO 金端",
    ssl=False)

#定義一個函數,該函數在收到MQTT消息時被調用,並將消息內容設定為 LED 燈帶的動畫效果
def get_cmd(topic, msg):
    # 宣告使用全域變數 led_strip_effect
    global led_strip_effect
    print(topic,msg)
    #設定條燈特效項目
    led_strip_effect = msg
    
client.connect()#使 MQTT 客戶端與 Adafruit IO 服務進行連接
client.set_callback(get_cmd)#設定 MQTT 客戶端接收消息時的回調函數
#訂閱 Adafruit IO 上的特定主題。在這裡,該主題是“AIO 帳號/feeds/mood"
client.subscribe(client.user.encode() + b"/feeds/mood");

# 在無限循環中,持續檢查並處理 MQTT 消息
while True:
    client.check_msg()#檢查是否有新的MQTT消息。如果有,則調用先前設定的回調函數 get_cmd
    if led_strip_effect == b'o':
        ledstrip.clear()
    elif led_strip_effect == b'1':
        #rainbow_cycle(間隔毫秒時間)
        ledstrip.rainbow_cycle(5)
    elif led_strip_effect == b'2':
        #cycle(r,g,b,間隔毫秒時間)
        ledstrip.cycle(123, 0, 20, 100)
    elif led_strip_effect == b'3':
        #bounce(r,g,b,間隔毫秒時間)
        ledstrip. bounce(23, 20, 128, 50)
