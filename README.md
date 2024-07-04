## 簡介

### 開發動機

每逢暑假總是會和朋友一起相約出遊，但每次出遊往往都會因為選定時間、行程安排等等因素一再延後，因此我想開法一款能解決所有困擾的APP，讓一群人出去玩不用再切換APP，省去溝通上的不便！

### APP功能介紹

首先進入頁面後會分成三個部分：

1. Pick the Date：透過kivymd.uix.pickers內建的MDDatePicker可以展示出行事曆，使用者只需要選擇日期按下確定後，便可以進行投票，最終會在螢幕上顯示前四名。
2. Have the Plane：使用者可以按下螢幕右下角的加號➕新增文字來說明行程，而每個MDCard都可以個別修改和刪除，中間的回復按鈕可以清除當前的所有行程。
3. Split the Bill：使用者可以按下螢幕右下角的加號➕依照指示填寫花費、成員和備註，最後可以按下中間帳單來確定最後每個人應該支付多少錢。

## 開發過程遇到的問題與解決方法

1.在設計主頁面時，因為我的icon大小都設定為正方形，而我自己在main.py內定義ImageButton讓照片即為圖片，但這樣會導致我的畫面的位置設計不如預期，且按鈕觸發的位置也不正確，因此我選擇在期望的位置放置icon，但改用Button和icon重疊的方式，並將Button的背景設為透明，以此來達到預期的效果。

2.增加MDCard可以修改的功能時，我沒有設定全域變數來紀錄MDCard是否有被修改，導致我在測試時每次修改都會變成新增一張MDCard，而非更改原本的內容，因此最後則創建editing_card來紀錄。

## 未來展望

目前的APP開發尚未完成多人連線，未來希望能夠研究出如何藉由傳送連結給達到多人使用的目的，以及能夠讓其他用戶分享自己的行程！
