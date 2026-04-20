1. 在倉庫模組(WM)中，在什麼情況下,才會開立庫存移轉單(Transfer Order)？

    (A) 產品出貨給顧客的時候(Post Goods Issue)

    (B) 當有物品從倉庫轉移(Transfer)的時候

    (C) 採購收貨時(Post Goods Receipt)

    (D) 產品出貨給顧客又退回的時候(Post Goods Return)

2. 在倉庫模組(WM)中，將檢驗中(Stock in Quality Inspection)的庫存轉移到未限制庫存(Unrestricted-use)，是屬於？

    (A) 移轉過帳(Transfer Posting)

    (B) 庫存移轉(Stock Transfer)

    (C) 二者皆非

    (D) 二者皆是

3. 下列何者不是倉庫模組(WM)的主數據(Master Data)？

    (A) 批號主數據(Batch Master Data)

    (B) 危險物品主數據(Hazard Master Data)

    (C) 供應商主數據(Vendor Master Data)

    (D) 儲存格主數據(Storage Bin Master Data)

4. 下列何者是倉庫模組(WM)的主數據(Master Data)？

    (A) 批號主數據(Batch Master Data)

    (B) 危險物品主數據(Hazard Master Data)

    (C) 儲存格主數據(Storage Bin Master Data)

    (D) 以上皆是

5. 在庫存管理的級別中，那一種級別可以整合供應鏈管理(SCM)

    (A) 庫存管理(Inventory Management)

    (B) 倉庫管理(Warehouse Management)

    (C) 擴展型的倉庫管理(Excended Warehouse Management)

    (D) 以上皆是

6. 在倉庫模組中(WM)，最小的儲存單位是？

    (A) 檢貨區域(Picking Area)

    (B) 儲存段(Storage Section)

    (C) 倉庫編號(Warehouse Number)

    (D) 儲存格(Storage Bin)

7. 針對庫存管理(Inventory Management)與倉庫管理(Warehouse Management)的描述，何是錯誤的？

    (A) 庫存管理(Inventory Management)是以儲存地點(Storage Location)來標明存放位置

    (B) 倉庫管理(Warehouse Management)是以格位(Bin)來標明存放位置

    (C) 庫存管理(Inventory Management)是以儲存地點(Storage Location)及格位(Bin)來標明存放位置

    (D) 使用 EWM(Extended Warehouse Management)可以實行更細化的管理

8. 在倉庫模組中(WM)，T-CODE MMBE可以查詢庫存餘額，而庫存餘額的顯示級別有六種，下列那些屬於其級別？

    (A) 集團(Client)

    (B) 公司代碼(Company Code)

    (C) 工廠(Plant)

    (D) 以上皆是

9. 在倉庫模組中(WM)，T-CODE MMBE可以查詢庫存餘額，而庫存餘額的顯示級別有六種，下列那些屬於其級別？

    (A) 儲存地點(Storage Location)

    (B) 特殊庫存(Special Stock)

    (C) 批號(Batch)

    (D) 以上皆是

10. 在倉庫模組中(WM)，何者是發貨(Issue)或收貨(Receipt)的暫存區？

    (A) 檢貨區域(Picking Area)

    (B) 儲存段(Storage Section)

    (C) 保留區(Allocation Zone)

    (D) 儲存格(Storage Bin)

11. 在倉庫模組中(WM)，庫存移轉(Stock Transfer)模式中，那些會產生財會憑証(Accounting Document)？

    (A) Stock to Stock

    (B) Storage Loc. to Storage Loc.

    (C) Company Code to Company Code

    (D) Material to Material

12. 在倉庫模組中(WM)，庫存移轉(Stock Transfer)的步驟描述，何者錯誤？

    (A) 可以是一步式(One Step)

    (B) 可以是二步式(Two Step)

    (C) 二步式(Two Step)若只有一個移動類型(Movement Type) 形同是一步式(One Step)

    (D) 二步式(Two Step)就會有二個移動類型 Movement Type

13. 在倉庫模組中(WM)，庫存移轉(Stock Transfer)模式中，那些一定不會有財會憑証(Accounting Document)？

    (A) Stock to Stock

    (B) Storage Loc. to Storage Loc.

    (C) Company Code to Company Code

    (D) Plant to Plant

14. 在 SAP 倉儲模組(WM)中，針對倉庫號碼(Warehouse Number)的描述何者是錯誤的？

    (A) 倉庫號碼(Warehouse Number)可以跨工廠

    (B) 倉庫號碼(Warehouse Number)不可以跨公司代碼

    (C) 倉庫號碼(Warehouse Number)可以包含多個儲存地點(Storage Location)

    (D) 倉庫號碼(Warehouse Number)是倉庫管理模組(WM)的重要組織結構

15. 在 SAP 倉儲模組(WM)中，針對倉庫號碼(Warehouse Number)的描述何者是錯誤的？

    (A) 一個倉庫號碼(Warehouse Number)必須連結至少一個儲存地點(Storage Location)

    (B) 倉庫號碼(Warehouse Number)可連結到跨工廠的儲存地點(Storage Location)

    (C) 一個儲存地點(Storage Location)能夠對應到多個倉庫號碼(Warehouse Number)

    (D) 不是所有的儲存地點(Storage Location)都需要對應到倉庫號碼(Warehouse Number)

16. 出貨點（Shipping Points）與工廠(Plant)的關係是？

    (A) 一對多

    (B) 一對一

    (C) 多對一

    (D) 多對多


解答與詳細解析

1. (B) 庫存移轉單(Transfer Order)是 WM 模組中用於倉庫內物品實體移動的指令，只有當物品在倉庫內發生移轉(Transfer)時才會開立；PGI 和 PGR 是 MM/SD 的操作，不會直接產生 WM 移轉單。

2. (A) 將庫存從一種狀態轉換到另一種狀態(如品檢中 → 未限制使用)，稱為移轉過帳(Transfer Posting)；庫存移轉(Stock Transfer)是指物料在不同地點間的實體移動。

3. (C) WM 模組的主數據包含批號主數據、危險物品主數據、儲存格主數據等；供應商主數據屬於 MM/FI 模組，不是 WM 的主數據。

4. (D) WM 模組的主數據包含批號主數據(Batch)、危險物品主數據(Hazardous Materials)、儲存格主數據(Storage Bin)，以上皆是。

5. (C) 三種庫存管理級別中，只有擴展型倉庫管理(EWM - Extended Warehouse Management)可以整合供應鏈管理(SCM)，提供更細化的多廠區、自動化倉庫管理功能。

6. (D) WM 組織結構由大到小為：倉庫編號(Warehouse Number) → 儲存區(Storage Type) → 儲存段(Storage Section) → 儲存格(Storage Bin)；儲存格是最小的單位。

7. (C) 庫存管理(Inventory Management)只以儲存地點(Storage Location)標明位置，不使用格位(Bin)；只有倉庫管理(WM)才使用格位精確定位；選項(C)將兩者混淆，故為錯誤描述。

8. (D) T-CODE MMBE 庫存顯示的六個級別包含：集團(Client)、公司代碼、工廠等，上述選項均屬其中，以上皆是。

9. (D) MMBE 庫存顯示的六個級別中也包含儲存地點、特殊庫存、批號等視圖，以上皆是。

10. (C) 保留區(Allocation Zone / Goods Receipt Zone)是 WM 中用於暫存待收或待發貨物的區域，為發貨與收貨的緩衝暫存區。

11. (C) 庫存移轉中，只有跨公司代碼(Company Code to Company Code)的移轉才會觸發會計憑証，因為涉及不同法人實體間的資產轉移；同倉存、跨儲存地點、同物料種類轉換不產生財務分錄。

12. (C) 二步式庫存移轉(Two Step)必定有兩個移動類型(Movement Type)，分別對應移出與移入；若只有一個 Movement Type 則是一步式(One Step)，選項(C)描述邏輯相反，故為錯誤。

13. (B) 同公司代碼內的跨儲存地點(Storage Loc. to Storage Loc.)移轉，物料仍在同一法人實體內，不涉及會計帳務，一定不產生財會憑証。

14. (B) 倉庫號碼(Warehouse Number)實際上可以跨公司代碼配置，選項(B)的描述「不可以跨公司代碼」是錯誤的；其他選項均為正確描述。

15. (C) 一個儲存地點(Storage Location)只能對應到一個倉庫號碼(Warehouse Number)，不能對應多個；選項(C)描述錯誤。

16. (D) 出貨點(Shipping Points)與工廠(Plant)的關係是多對多(Many to Many)，一個工廠可以有多個出貨點，一個出貨點也可以服務多個工廠。
