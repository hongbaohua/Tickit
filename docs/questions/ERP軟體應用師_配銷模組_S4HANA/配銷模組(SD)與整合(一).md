# 配銷模組(SD)與整合(一)

> **參考資料來源**：`S4HANA配銷_Reference76_202502.pdf` (第 1-38 題)

1. 客戶產品價格條件 (VK11, Condition type = PR00 )，主要是建立哪些內容，下列何者為非？
    (A) 價格 ( Price )
    (B) 折扣 ( Discount )
    (C) 運費 ( Freight )
    (D) 貿易條件 (Trade Term )。

2. 組成客戶產品價格條件( VK11 )有四個要素，不包含哪一個？
    (A) 客戶 ( Customer )
    (B) 物料 ( Material )
    (C) 產品部 ( Division )
    (D) 銷售組織 ( Sale Org. )。

3. 檢貨作業時，要填入倉庫號碼 ( warehouse number )是被指派(assign)給何者？
    (A) 工廠( plant )與儲存地點( storage location )
    (B) 儲存地點( storage location )
    (C) 工廠( plant )
    (D) 銷售組織 ( Sale Org. )。

4. 銷售組織( sales org. ) 與工廠( Plant ) 的關係是？
    (A) 多對一
    (B) 一對多
    (C) 不必設定
    (D) 多對多。

5. 在配銷模組中客戶訂單 (sales order , VA01) 的主檔資料有許多，但不包含下列哪一項？
    (A) 客戶 ( Customer )
    (B) 物料( Material )
    (C) 銷售組織 ( Sale Org. )
    (D) 輸出( Output )。

6. 在配銷模組(SD)中，哪一步驟會與獲利分析(Profitability analysis)整合？
    (A) 建立出貨通知單(Create an outbound delivery)
    (B) 建立銷貨發票(Generating an invoice)
    (C) 建立銷貨訂單(Generating a Sales Order)
    (D) 建立庫存移轉單(Create a Transfer Order)。

7. 在配銷模組(SD)中，建立商業夥伴時(Business partner)，必須先選擇何者？
    (A) 商業夥伴角色(Business partner role)
    (B) 商業夥伴類型(Business partner type)
    (C) 夥伴功能(partner function)
    (D) 科目群組(Account group)。

8. 在配銷模組(SD)流程中，銷售區域(Sales area)不包含下列何者？
    (A) 工廠(Plant)
    (B) 銷售通路(Distribution channel)
    (C) 銷售組織(Sales Organization)
    (D) 產品部 ( Division )。

9. 在配銷模組(SD)流程中，下列何者是銷售區域(Sales area)的一部份？
    (A) 工廠(Plant)
    (B) 銷售通路(Distribution channel)
    (C) 公司代碼(Company Code)
    (D) 儲存地點 (Storage Location)。

10. 在配銷模組(SD)流程中，當發貨時(Post Goods Issue)會影響一連串的動作，請問不包含下列哪一項？
    (A) 產生財會憑証(an accounting journal entry is created)
    (B) 庫存數量更新(Inventory quantities are updated)
    (C) 待開發票清單更新(the billing due list is updated)
    (D) 產生銷項發票(an invoice is created)。

11. 在配銷模組(SD)流程中，銷售組織(Sales Organization)與公司代碼(Company Code)的關係是？
    (A) 一對多
    (B) 多對一
    (C) 一對一
    (D) 多對多。

12. 下列何者不是配銷模組(SD)的主檔資料？
    (A) 客戶主檔資料(Customer Master Data)
    (B) 物料主檔資料(Material Master Data)
    (C) 客戶價格條件主檔資料(Condition Master Data)
    (D) 物料類型主檔資料(Material Type Master Data)。

13. 配銷模組(SD)中，客戶主檔資料包含三視圖，不包括下列哪一項？
    (A) 工廠資料(Plant Data)
    (B) 一般性資料(General Data)
    (C) 集團層級資料(Client Data)
    (D) 公司代碼資料(Company Code Data)。

14. 在配銷模組(SD)中，客戶價格條件主檔資料(Condition master data)會包含許多事項，但不包含？
    (A) 重量折扣
    (B) 貿易條件(Trade terms)
    (C) 數量折扣
    (D) 淨額折扣。

15. 在配銷模組(SD)流程中，哪些屬於售前活動(Pre-sales Activities)？
    (A) 建立詢價單(Create an Inquiries)
    (B) 客戶付款(Receipt of Customer Payment)
    (C) 檢查庫存可用量(Check Availability)
    (D) 開立發票(Create a Customer Invoice Issue)。

16. 在配銷模組(SD)流程中，銷貨訂單(sales order)，是由三個部份所組成，而產品資訊是建立在哪個部份？
    (A) 表頭(Header)
    (B) 表身(Line Items)
    (C) 排程(Schedule Lines)
    (D) 表尾(Footer)。

17. 在配銷模組(SD)流程中，開立客戶發票的模式中(Billing Methods)，若多張訂單(Sales Order)開立一張發票，稱為何種開立方式？
    (A) 集體開立(Collective Invoicing)
    (B) 分割開立(Split Invoicing)
    (C) 依出貨單開立(Delivery Based Invoicing)
    (D) 完全開立(Complete Invoicing)。

18. 在配銷模組中(SD)，組織層次中的工廠(Plant)，可以有多個功用，但不可能代表以下何者？
    (A) 製造工廠(manufacturing facility)
    (B) 儲存格(Storage Bin)
    (C) 倉庫(Warehouse)
    (D) 物流中心(Distribution Center)。

19. 在配銷模組(SD)流程中，開立發票(Create a Customer Invoice)，會產生哪一項財會憑証(Accounting Document)？
    (A) 借：銀行存款(Bank) 貸：應收帳款(A/R)
    (B) 借：銷貨成本(COGS) 貸：存貨(Inventory)
    (C) 借：應收帳款(A/R) 貸：銷貨收入(Sales Income)
    (D) 借：應收帳款(A/R) 貸：存貨(Inventory)。

20. 在物料文件中，移動類型 101，主要的是在描述何種狀況？
    (A) 採購單(Purchase order)的收貨(Receipt)
    (B) 採購單(Purchase order)的退回(Return)
    (C) 客戶訂單(Sales order)的發貨(Issue)
    (D) 客戶訂單(Sales order)的退回(Return)。

21. 當採購收貨時(Goods Receipt for Purchase Order)，對系統而言會發生一連串的影響，請問不包含下列哪個動作？
    (A) 產生物料帳憑証(Material Document is Created)
    (B) 產生財會憑証(Accounting Document is Created)
    (C) 產生管理會計憑証(Controlling Document is Created)
    (D) 更新庫存數量(Stock Quantities are Updated)。

22. 建立採購單(Purchase Order)的方式有很多種，下列描述何者正確？
    (A) 複製採購單(Reference a Purchase Order)
    (B) 直接新增 (Without Reference)
    (C) 複製報價單(Reference a RFQ/Quotation)
    (D) 以上皆是。

23. 在採購循環中(Purchasing process)，下列動作哪一步驟是與財會(FI)模組相關？
    (A) 建立採購單(Create Purchase Order)
    (B) 建立供應商(Create New Vendor)
    (C) 收到供應商的發票(Create Invoice Receipt from Vendor)
    (D) 評估報價單的價格(Evaluate Quotations on Price)。

24. 當採購收貨時(Goods Receipt for Purchase Order)，對資產負債表會產生變化，請問下列何者正確？
    (A) 借：存貨(Inventory) 貸：應付帳款(Account Payable)
    (B) 借：應付帳款(Account Payable) 貸：存貨(Inventory)
    (C) 借：存貨(Inventory) 貸：預計應付帳款(GR/IR)
    (D) 借：預計應付帳款(GR/IR) 貸：存貨(Inventory)。

25. 當收到供應商發票時( Invoice Receipt from Vendor)，對資產負債表會產生變化，請問下列何者正確？
    (A) 借：存貨(Inventory)貸：應付帳款(Account Payable)
    (B) 借：應付帳款(Account Payable) 貸：存貨(Inventory)
    (C) 借：預計應付帳款(GR/IR) 貸：應付帳款(Account Payable)
    (D) 借：預計應付帳款(GR/IR) 貸：應付帳款(Account Payable)。

26. 供應商(Vendor)主檔資料會被哪個模組使用到？
    (A) 財會模組(FI)
    (B) 物料模組(MM)
    (C) 財會模組(FI)與物料模組(MM)
    (D) 配銷模組(SD)。

27. 物料(Material)主檔資料會被哪個模組使用到？
    (A) 製造模組(PP)
    (B) 物料模組(MM)
    (C) 配銷模組(SD)
    (D) 以上皆是。

28. 在 S/4HANA 之中，物料模組會與雲端哪個模組緊密結合？
    (A) SUCCESSFACTORS
    (B) FIELDGLASS
    (C) ARIBA
    (D) CONCUR。

29. 物料帳(Material Ledger)，可以推出物料的實際成本與九大差異，在 S/4HANA 之中如何啟動此模組？
    (A) 已自動啟用
    (B) 要請顧問公司啟用
    (C) 要請 SAP 原廠啟用
    (D) 由用戶自行選擇是否啟用。

30. 針對採購組織(Purchasing Organization) 與採購群組的描述，何者是錯誤的？
    (A) 與供應商談價是屬於採購群組的工作
    (B) 一個企業可以有多個採購組織
    (C) 採購群組不一定是公司內部的實體單位
    (D) 評估供應商是採購組織的工作。

31. 採購模組(MM)，不包含哪些主檔資料( Master Data )？
    (A) 供應商主檔(Vendor Master)
    (B) 物料主檔(Material Master)
    (C) 採購訊息記錄(Purchasing Information Record)
    (D) 物料類型(Material Type)。

32. 下列哪個物料類型是屬於製成品？
    (A) ROH
    (B) HALB
    (C) FERT
    (D) HALB。

33. 以收貨為基礎的發票驗證(Goods-receipt-based Invoice Verification)，系統代表的意義為何？
    (A) 物料多次送達，但只有一次發票驗證，且以採購單的數量為驗證依據
    (B) 物料分幾次送達，就有幾次發票驗證，且以採購單數量為驗證依據
    (C) 物料一次送達，但有多次發票驗證，且以採購單的數量為驗證依據
    (D) 物料分幾次送達，就有幾次發票驗證，且以物料送達數量為驗證依據。

34. 以採購單為基礎的發票驗證(Purchase-order-based Invoice Verification)，系統代表的意義為何？
    (A) 物料分幾次送達，就有幾次發票驗證，且以物料送達數量為驗證依據
    (B) 物料多次送達，但只有一次發票驗證，且以採購單的數量為驗證依據
    (C) 物料一次送達，但有多次發票驗證，且以物料送達數量為驗證依據
    (D) 物料多次送達，但只有一次發票驗證，且以物料送達數量為驗證依據。

35. 當採購收貨時(MIGO)，下列敘述何者錯誤？
    (A) 貨物已確認送達
    (B) 預計應付帳款已產生(GR/IR)
    (C) 貨物狀態都是可使用(unrestricted use)
    (D) 採購單的狀態會更新。

36. 當建立採購單時，如果有填成本中心(cost center)，則下列何者正確？
    (A) 料號要填成本中心
    (B) 料號不可以填
    (C) 料號一定要填
    (D) 料號可填可不填。

37. 採購模組不會和哪個模組產生直接的關聯？
    (A) QM 品檢模組
    (B) WM 倉儲管理
    (C) FI 財務模組
    (D) SD 配銷模組。

38. 建立採購單時，何時要指定成本物件(COST OBJECT)，例如 成本中心？
    (A) 購買物料時(Material)
    (B) 購買服務時( service)
    (C) 依主管的要求
    (D) 不可以指定。

---
## 解析與補充

1. **(D)** 客戶價格條件（VK11）主要包含價格、折扣、運費、稅金等，貿易條件（Trade Term）屬主檔基本資料或訂單抬頭資料。
2. **(C)** VK11 四要素：客戶、物料、銷售組織、銷售通路。產品部（Division）通常包含在銷售區域中，但非 VK11 直接定義要素。
3. **(A)** 倉庫號碼（Warehouse Number）是指派給「工廠+儲存地點」的組合。
4. **(B)** 一個銷售組織可以對應多個工廠。
5. **(D)** 輸出（Output）是單據產生的結果，非主檔資料。客戶、物料、組織均為主檔。
6. **(B)** 開立發票（Billing）會將收入與成本過帳到獲利分析（CO-PA）。
7. **(B)** 建立 BP 時必須先決定其類型（人、組織、群組）。
8. **(A)** 銷售區域（Sales Area）= 銷售組織 + 通路 + 產品別。工廠不屬於銷售區域定義。
9. **(B)** 銷售通路是銷售區域的三大組成之一。
10. **(D)** 發貨（PGI）更新庫存與財會，但發票（Invoice）是下一個獨立步驟。
11. **(B)** 多個銷售組織可歸屬於一個公司代碼。
12. **(D)** 物料類型是分類屬性，非獨立主數據。
13. **(A)** 客戶主檔視圖：一般資料（集團）、公司代碼資料、銷售區域資料。不含工廠資料。
14. **(B)** 價格條件包含各式折扣與附加費，貿易條件非屬價格條件內容。
15. **(A)** 售前活動包含詢價（Inquiry）與報價。
16. **(B)** 產品/物料資訊位於訂單的表身（Line Items）。
17. **(A)** 多合一稱為集體開立（Collective Invoicing）。
18. **(B)** 儲存格（Storage Bin）是 WM 模組單位，工廠層級較高。
19. **(C)** 銷貨發票分錄：借：應收帳款、貸：銷貨收入。
20. **(A)** 101 是採購收貨最常用的移動類型。
21. **(C)** 收貨通常產生物料文件與會計文件，不一定會產生管理會計（CO）文件，除非涉及成本中心分配。
22. **(D)** 採購單可由多種來源參照建立。
23. **(C)** 收到發票涉及負債增加與預計應付沖銷，屬 FI 範疇。
24. **(C)** 採購收貨：借：存貨、貸：預計應付帳款(GR/IR)。
25. **(C/D)** 收到發票：借：預計應付帳款(GR/IR)、貸：應付帳款(AP)。
26. **(C)** 供應商資料由採購（物料模組）與會計（財會模組）共用。
27. **(D)** 物料主檔是所有物流與製造模組的核心。
28. **(C)** SAP Ariba 是專門的雲端採購與供應鏈協作平台。
29. **(A)** S/4HANA 規定必須啟用物料帳。
30. **(A)** 談判與合約簽署是「採購組織」的責任，而非「採購群組」。
31. **(D)** 物料類型是屬性，非獨立主檔。
32. **(C)** FERT (Fertigerzeugnis) 代表成品。
33. **(D)** 以收貨為基礎：每筆收貨對應一筆發票驗證。
34. **(B)** 以採購單為基礎：不論分幾次收貨，最終對應採購單總量驗證。
35. **(C)** 收貨時可進入不同狀態（如檢驗中），不一定直接是可使用。
36. **(B)** 購買消耗性物料（填成本中心）時，通常不需輸入料號（或料號不影響庫存）。
37. **(D)** 採購與銷售在流程上無直接連動，除非是轉售或特殊情境。
38. **(B)** 購買非庫存服務時，必須指定受益的成本物件。

---
## 補充/舊有題庫參考

*   **[原11]** 在倉庫模組(WM)中，最小的儲存單位是：儲存格 (Storage Bin)。
*   **[原19]** 在 S/4HANA 之中，物料文件(Material Document) 被儲存在那個資料表：MATDOC。
*   **[原25]** 庫存管理(IM)是以儲存地點(Storage Location)來標明存放位置，倉庫管理(WM)是以格位(Bin)來標明。
*   **[原38]** 倉庫號碼(Warehouse Number)可以跨工廠，但不可跨公司代碼。
