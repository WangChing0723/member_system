# member_system

## 使用方法：
這是一個關於申辦會員的系統，可以透過[此網站](http://20.24.70.9:3000)來進行操作，
主畫面上可以進行 1.註冊帳號 2.登入系統 兩種操作。
登入系統後可以進行查詢其他會員的姓名或是更新您的名字
(此系統會同步變更資料庫中的資料)

## 專案架構：
![image](https://user-images.githubusercontent.com/99674906/167289207-6aa5153b-fdb6-4787-8340-6b91f4675e72.png)

此專案主要目的是練習、展現 Python 後端技能，並使用 Azure 進行雲端部署。首先，在雲端建立 Azure VM，作業系統為 REHL8，並利用 Linux 指令安裝相關套件。再來，將 Python 後端程式跑在此機器上，當成服務的 server，並將此 procress 丟在背景執行。另外，透過 Azure Database for MySQL 設計、建立資料庫，儲存會員相關資料，同時也可以避免 Azure VM 出現問題時，資料庫可以正常提供資料。最後，對連線設定 Network Security 來確保其安全性。
