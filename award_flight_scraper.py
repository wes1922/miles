import os
import time
import schedule
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# 載入環境變數
load_dotenv()

JAL_USERNAME = os.getenv("JAL_USERNAME")
JAL_PASSWORD = os.getenv("JAL_PASSWORD")
ANA_USERNAME = os.getenv("ANA_USERNAME")
ANA_PASSWORD = os.getenv("ANA_PASSWORD")

def check_jal_availability():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 開始執行 JAL 查票...")
    if not JAL_USERNAME or not JAL_PASSWORD:
        print("未設定 JAL_USERNAME 或 JAL_PASSWORD，跳過查詢。")
        return

    with sync_playwright() as p:
        # 使用持久化上下文可儲存 Session(登入狀態) 與 Cookies
        # 能大幅降低連續嘗試時被偵測為機器人的機率
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./playwright_profile_jal",
            headless=False, # 開啟介面，便於手動介入與登入
            slow_mo=1000    # 放慢動作速度，模擬真人點擊
        )
        page = browser.new_page()
        
        try:
            # 前往 JAL 英文版常客計畫頁面 (做範例測試用)
            page.goto("https://www.jal.co.jp/jp/en/jmb/")
            
            # ==========================================
            # TODO: 等待分析 JAL 最新 DOM 架構後再精確填入選擇器
            # 第一階段：必須由人工進行第一次的真實登入解鎖驗證碼
            # ==========================================
            print("請觀察瀏覽器：如果您尚未登入，請手動進行登入以儲存登入憑證。")
            page.wait_for_timeout(10000) # 給予10秒鐘彈性觀察時間

            # 將在這裡撰寫尋找 TYO -> LAX 的查詢邏輯
            print("JAL TYO-LAX 查票程式碼預留區。")

        except Exception as e:
            print(f"JAL 查詢過程發生錯誤: {e}")
        finally:
            print("關閉 JAL 瀏覽器...")
            browser.close()


def check_ana_availability():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 開始執行 ANA 查票...")
    if not ANA_USERNAME or not ANA_PASSWORD:
        print("未設定 ANA_USERNAME 或 ANA_PASSWORD，跳過查詢。")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./playwright_profile_ana",
            headless=False,
            slow_mo=1000
        )
        page = browser.new_page()
        
        try:
            page.goto("https://www.ana.co.jp/en/jp/")
            
            print("請觀察瀏覽器：如果您尚未登入 ANA，請手動登入以留下快取。")
            page.wait_for_timeout(10000)
            
            # 將在這裡撰寫尋找 TYO -> LAX 的查詢邏輯
            print("ANA TYO-LAX 查票程式碼預留區。")

        except Exception as e:
            print(f"ANA 查詢過程發生錯誤: {e}")
        finally:
            print("關閉 ANA 瀏覽器...")
            browser.close()


def job():
    print(f"=== 定時查票啟動: {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    check_jal_availability()
    check_ana_availability()
    print(f"=== 查票結束: {time.strftime('%Y-%m-%d %H:%M:%S')} ===")


def main():
    print("機票自動查票程式啟動中...")
    
    # 初次啟動時，先立刻手動執行一次流程
    # job()

    # 排程設定：每小時的 01 分執行
    schedule.every().hour.at(":01").do(job)
    
    print("排程已設定完成，未來將於每小時 01 分執行抓取。")
    print("等待中... (若要結束程式請按下 Ctrl+C)")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n偵測到中斷指令，退出程式。")
            break

if __name__ == "__main__":
    main()
