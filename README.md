# 安裝說明

## 安裝 Python
1. 從 [python.org](https://www.python.org/downloads/) 下載並安裝 Python。

## 克隆倉庫
```sh
git clone https://github.com/hazasi/MouseMacro.git
cd MouseMacro
```
## 安裝必要元件
```pip install pyautogui keyboard psutil pywin32 pynput```

## 執行程式
```python mouse_automation.py```

```
使用控制台菜單與自動化腳本互動：
F7 - 開始記錄鼠標點擊
F8 - 停止記錄
F9 - 列出記錄的動作
F10 - 播放記錄的動作
F11 - 將記錄的動作保存到 actions.json
F12 - 從 actions.json 加載動作
F4 - 停止播放
按照螢幕上的控制台菜單進行其他選項的操作
```

## 錄製說明:
1. 使用 F7 開始錄製動作，建議操作慢一些。
2. 操作完成按下F8可停止錄製。
3. 然後按下 F11 或 選項5 儲存。 檔案預設Action.json 

## 掛卡錄製參考:
* 上級摩天，錄製過程包含把隊伍拉到定點，約10幾秒結束，可以先按下 F8 先結束錄製。
* 錄製結束後，請先注意你打的時間，將這個時間請換算秒數，將其設定為 間隔時間 interval。
* 間隔時間，建議額外多15~20秒。 出卡片會慢一些。
* 最後再將你的錄製按下 F11進行存檔。
## 修改說明
程式架構本身使用標準元件，套用OS層級的鍵盤綁定；可以直接看程式碼。可變鎖定的目標可作用於其他。

