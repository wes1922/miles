# 🌍 Global Airlines Award Hub - 航空資料庫修改說明書

`all_airlines_web.html` 設計上將所有的「航空放票規則」集中在程式碼上方的一個名為 `const airlines = [ ... ]` 的設定陣列中。

如果您未來發現航空公司的放票規則有變更（例如：原本提早 360 天突然改成 355 天），您可以直接用任何文字編輯器（如記事本、VS Code）打開這個 HTML 檔案，找到大約第 170 行的 `const airlines` 區塊，照著以下參數規則進行修改即可完美套用。

---

## 🛠️ 基礎結構與格式

每一家航空公司都是被大括號 `{}` 包起來的物件，並由多個屬性（參數）所組成。
以下是一個典型的航空資料庫條目：

```javascript
{ 
  alliance: "星空聯盟 (Star Alliance)", 
  id: "br", 
  name: "EVA Air 長榮航空", 
  days: 360, 
  confirmed: true, 
  partnerConfirmed: false, 
  tz: "Asia/Taipei", 
  hour: 8,
  note: "如果有特殊提醒可以寫在這裡"
}
```

---

## 📖 參數完整對照表

所有可用的參數如下，分為「必填」與「選填（外家專用）」：

### 核心 / 自家航班參數 (必填)

| 參數名稱 | 資料型態 | 意義與用途 | 填寫範例 |
| :--- | :--- | :--- | :--- |
| **`alliance`** | 字串 (String) | **所屬聯盟名稱**。<br/>這決定了它在下拉式選單中會被分配在哪個分類標題下。 | `"星空聯盟 (Star Alliance)"` |
| **`id`** | 字串 (String) | **內部票號代碼**。<br/>系統產生的 `.ics` 行事曆檔名會用到它，請保持英文小寫。 | `"br"` 或 `"jl"` |
| **`name`** | 字串 (String) | **顯示名稱**。<br/>使用者在網頁上看到的名字。 | `"All Nippon Airways (ANA)"`|
| **`days`** | 數字 (Int) | **「自家執飛」提早放票天數**。<br/>請確認是提早幾天（如 360 或 355）。 | `360` |
| **`tz`** | 字串 (String) | **總部所在地時區 (Timezone)**。<br/>請填入標準 IANA 時區格式，系統會自動處理當地的夏令時間(DST)。如果統一用格林威治標準時間則填 `"UTC"`。 | `"Asia/Tokyo"`, `"America/New_York"`, `"UTC"` |
| **`hour`** | 數字 (0-23) | **「自家執飛」放票整點時間**。<br/>該時區當地的 24 小時制時間。例如早上 9 點請填 9；凌晨 0 點請填 0。 | `9` (代表早上 9 點)<br/>`0` (代表凌晨 0 點) |
| **`confirmed`** | 邏輯值 (Boolean) | **「自家執飛」是否已實測驗證**。<br/>填寫 `true` 會亮綠燈✅；填 `false` 則會亮紅燈⚠️字樣顯示「尚未確認精確時間 (約略推估)」。 | `true` 或 `false` |

---

### 外家 / 聯盟夥伴航班參數 (進階選填)

為因應某些航空公司「自家航班」與「聯盟夥伴航班」的放票規則與時間**完全不同**，本系統特別為外家（Partner）配置了獨立的覆蓋參數。

> 💡 **注意事項：** 如果您「沒有」寫入這些 partner 參數，系統會自動「繼承」上方自家航班的設定 (`days`, `tz`, `hour`) 給外家區塊。

| 參數名稱 | 資料型態 | 意義與用途 | 填寫範例 |
| :--- | :--- | :--- | :--- |
| **`partnerDays`** | 數字 (Int) | **「外家/夥伴航班」提早放票天數**。<br/>例如 ANA 自家是 355 天，但夥伴票是 356 天，這裡就填 356。 | `356` |
| **`partnerTz`** | 字串 (String) | **「外家/夥伴航班」的基準時區**。<br/>若跟自家放票時區不同才需填寫。 | `"America/New_York"` |
| **`partnerHour`** | 數字 (0-23) | **「外家/夥伴航班」的放票整點時間**。<br/>若跟自家不同才需設定，例如自家 9 點，外家 0 點。 | `0` |
| **`partnerConfirmed`**| 邏輯值 (Boolean)| **「外家/夥伴航班」是否已實測驗證**。<br/>填寫 `true` 會在外家卡片亮綠燈✅；`false` 則亮紅燈⚠️。 | `true` 或 `false` |

---

### 輔助文字參數 (選填)

| 參數名稱 | 資料型態 | 意義與用途 | 填寫範例 |
| :--- | :--- | :--- | :--- |
| **`note`** | 字串 (HTML) | **💡 深度經驗與規律 板塊**。<br/>設定後會在網頁上顯示一個黑底黃字的詳細解說區塊（支援基礎 HTML 標籤如 `<br/>` 或 `<strong>`）。 | `"部分外家如AA放票時間不一樣<br/>請注意。"` |
| **`icsDesc`** | 字串 (String) | **自訂行事曆備註**。<br/>使用者下載的 `.ics` 行事曆中，備註欄位的客製化文字。換行必須打雙斜線 `\\n`，否則會導致 HTML 解析錯誤。 | `"頭等艙：2張\\n商務：1張"` |

---

## 🛠️ 修改實戰範例

### 範例一：修改華航的放票時間
假設華航 (CI) 宣佈將放票時間從 **早上 8 點** 改為 **早上 9 點**，天數變成 **355天**。
1. 尋找程式碼 `id: "ci"` 那一行：
   ```javascript
   { alliance: "天合聯盟...", id: "ci", name: "China Airlines 中華航空", days: 361, confirmed: true, partnerConfirmed: false, tz: "Asia/Taipei", hour: 8 }
   ```
2. 修改 `days` 與 `hour` 的數值：
   ```javascript
   { alliance: "天合聯盟...", id: "ci", name: "China Airlines 中華航空", days: 355, confirmed: true, partnerConfirmed: false, tz: "Asia/Taipei", hour: 9 }
   ```

### 範例二：為國泰 (CX) 加入外家航班的獨立時間
假設國泰航空 (CX) 的自家其實是 360 天早上 8 點，但夥伴航班確認是 355 天的 0 點釋出。
可以在原代碼後面手動補上 `partnerDays` 與 `partnerHour`：
```javascript
{ 
  alliance: "寰宇一家 (Oneworld)", 
  id: "cx", 
  name: "Cathay Pacific Asia Miles", 
  days: 360, 
  confirmed: false, 
  tz: "Asia/Hong_Kong", 
  hour: 8,
  
  // ▼ 以下是您自己為外站新增的參數
  partnerConfirmed: true, 
  partnerDays: 355, 
  partnerHour: 0 
}
```

修改完畢後只要「儲存檔案 (Ctrl+S)」，再去瀏覽器「重新整理 (F5)」網頁，強大的系統引擎就會自動根據您設定的新規則，把時區、日期全部完美計算並更新在介面上！
