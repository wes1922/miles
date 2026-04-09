# 哩程機票自動監控爬蟲實作計畫 (JAL/ANA 定時查票系統)

這是一個全新的背景程式專案，目的是建立一個可以模擬真人登入並自動查詢日本航空 (JAL) 與全日空 (ANA) 哩程機位狀態的爬蟲系統，並具備定時 (每小時一次) 的執行能力。

## 目標核心功能
1. 支援帳號密碼登入機制 (針對常客計畫)。
2. 自動化進入查票頁面，填入目標航線 (東京 TYO <-> 洛杉磯 LAX)。
3. 每小時固定觸發查詢最新可訂位日期 (例如 JAL 的 360 天後、ANA 的 355/356天後)。
4. (後續可擴充) 發現有機位時立即發送提醒。

## User Review Required
> [!WARNING]
> 開發航空公司爬蟲面臨重大挑戰與風險，請使用者務必詳閱並確認以下事項：
> 1. **帳號封禁風險**：航空公司（尤其是日系航空公司）對於自動化腳本抓取資料的容忍度極低。如果被系統偵測到是爬蟲，**有機率會直接封鎖甚至停權您的哩程帳號**。在正式帳號測試前需極度謹慎。
> 2. **反爬蟲機制 (Anti-Bot)**：目前的航空公司官網多數引進了強大的防護機制（如 Cloudflare, reCAPTCHA, 或行為分析）。簡單的 Python Requests 無法登入，我們必須使用 `Playwright` 搭配真實瀏覽器模擬，甚至需要人工介入解鎖一次驗證碼。
> 3. **需要本機長期掛機環境**：若要「每小時執行一次」，必須要在有一台不關機的電腦上執行 Cron job 或 Windows 工作排程器。
> 
> **請問是否同意上述風險，且要在本機電腦安裝並執行 Playwright 爬蟲專案？**
> 如果同意，我們將會開啟隱形瀏覽器實作登入查票邏輯。

## Proposed Changes
這將是一個獨立的 Python 專案，檔案將建立在原有的 `專案1` 資料夾內。

### 核心爬蟲腳本
#### [NEW] [award_flight_scraper.py](file:///c:/Users/cma76164/.gemini/antigravity/brain/6f45c9ed-1de0-4264-b1fb-269ae9aafcd7/專案1/award_flight_scraper.py)
- 載入 `playwright` 模組。
- 建立 `login_jal()` 與 `login_ana()` 函數。
- 建立輸入航段資訊 (TYO-LAX) 查票的 `search_flights()` 函數。
- 整合 `schedule` 模組以達到每小時 `01` 分定時執行的排程環圈。

### 依賴環境檔案
#### [NEW] [requirements.txt](file:///c:/Users/cma76164/.gemini/antigravity/brain/6f45c9ed-1de0-4264-b1fb-269ae9aafcd7/專案1/requirements.txt)
- 將宣告所需的依賴項：`playwright`, `schedule`, `python-dotenv` (用於安全存儲帳號密碼)。

#### [NEW] [.env.example](file:///c:/Users/cma76164/.gemini/antigravity/brain/6f45c9ed-1de0-4264-b1fb-269ae9aafcd7/專案1/.env.example)
- 環境變數範例檔，用於讓使用者填入 `JAL_USERNAME`, `JAL_PASSWORD` 等機敏資訊，避免將帳號密碼寫死在程式碼中。

## Verification Plan

### Automated Tests
目前無自動化測試。需要使用者先在終端機安裝依賴項目：
`pip install -r requirements.txt`
`playwright install`

### Manual Verification
1. 程式將設計為在開發模式下開啟「可見模式的瀏覽器 (Headless=False)」。
2. 使用者在終端機執行 `python award_flight_scraper.py --test`。
3. 觀察瀏覽器自動彈出，前往 JAL 或 ANA 登入頁。
4. 觀察輸入帳號密碼以及遇到反爬蟲驗證時的行為。
5. 確認是否能成功印出「東京-洛杉磯」搜尋回傳的最新機位日期結果。
