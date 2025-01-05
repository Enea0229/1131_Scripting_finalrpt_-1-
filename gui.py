import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import simpledialog
import webbrowser  # 用於打開瀏覽器
from scraper import get_crypto_data, get_news
from database import Database
from datetime import datetime

#pip install ttkbootstrap

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle

class CryptoApp:
    def __init__(self):
        print("[INFO] Starting CryptoApp with Metro UI theme...")
        self.root = ttkb.Window(themename="flatly")  # 選擇主題
        self.root.title("Crypto 資訊系統")
        self.database = Database()

        # 設定全局字體
        self.empty_font = ("Arial", 18)
        self.table_content_font = ("新細明體", 18)  # 修改字體為新細明體  #修改1
        self.table_header_font = ("Arial", 22, "bold")
        self.label_font = ("Arial", 28)
        self.dropdown_font = ("Arial", 18)
        self.button_font = ("Arial", 18)

        # 分頁相關變數
        self.news_per_page = 5
        self.current_page = 1

        # 設置行列權重
        self.root.grid_rowconfigure(6, weight=1)  # 修改行數為 6    # 修改1
        self.root.grid_columnconfigure((0, 1, 3), weight=1)  # 修改列數為 (0, 1, 3)  # 修改1
        self.root.grid_columnconfigure(2, weight=15)  # 修改第 2 列權重為 15  # 修改1

        # 定義 Combobox 樣式
        self.dropdown_style = ttkb.Style()
        self.dropdown_style.configure(
            "MetroDropdown.TCombobox",
            arrowsize=15,  # 調整下拉箭頭大小
            padding=[5, 5, 5, 5],  # 控制內部填充，影響寬度
            font=self.dropdown_font,   # 字體大小
        )

        # 定義 Treeview 樣式
        self.table_style = ttkb.Style()
        self.table_style.configure(
            "MetroTable.Treeview",
            font=self.table_content_font,  # 表格內容字體大小
            rowheight=70,                  # 修改行高為 70  # 修改1
        )
        self.table_style.configure(
            "MetroTable.Treeview.Heading",
            font=self.table_header_font,  # 表格標題字體大小
            background="#3498db",         # 標題背景顏色
            foreground="white",           # 標題文字顏色
        )

        #定義按鈕樣式(紫色)
        self.btn_style = ttkb.Style()
        self.btn_style.configure(
            "MetroButton.Purple.TButton",  # 自定義樣式名稱
            font=self.button_font,         # 調整字體大小
            padding=[10, 5],               # 控制按鈕內部填充
            background="#7b4f9d",          # 標題背景顏色
            foreground="white",            # 標題文字顏色
            borderwidth=0,                 # 移除邊框
        )
        self.btn_style.map(
            "MetroButton.Purple.TButton",
            background=[("active", "#dd0af5")],  # 滑鼠懸停時的顏色
        )

        #定義按鈕樣式(綠色)
        self.btn_style = ttkb.Style()
        self.btn_style.configure(
            "MetroButton.Green.TButton",  # 自定義樣式名稱
            font=self.button_font,        # 調整字體大小
            padding=[10, 5],              # 控制按鈕內部填充
            background="#393",            # 標題背景顏色
            foreground="white",           # 標題文字顏色
            borderwidth=0,                # 移除邊框
        )
        self.btn_style.map(
            "MetroButton.Green.TButton",
            background=[("active", "#3cdb07")],  # 滑鼠懸停時的顏色
        )

        #定義按鈕樣式(紅色)
        self.btn_style = ttkb.Style()
        self.btn_style.configure(
            "MetroButton.Red.TButton",  # 自定義樣式名稱
            font=self.button_font,        # 調整字體大小
            padding=[10, 5],              # 控制按鈕內部填充
            background="#f00505",            # 標題背景顏色
            foreground="white",           # 標題文字顏色
            borderwidth=0,                # 移除邊框
        )
        self.btn_style.map(
            "MetroButton.Red.TButton",
            background=[("active", "#f5ca0a")],  # 滑鼠懸停時的顏色
        )

        # 建立介面
        self.create_widgets()

    def create_widgets(self):
        print("[INFO] Setting up GUI widgets...")

        # 設置標籤，用於說明選擇幣種
        self.select_label = ttkb.Label(
            self.root,
            text="請選擇幣種：",
            font=self.label_font,
            bootstyle=SECONDARY,
        )
        self.select_label.grid(row=0, column=0, padx=30, pady=30, sticky="e")  # 修改1

        # 下拉選單
        self.crypto_var = ttkb.StringVar(value="BTC")
        cryptos = ["BTC", "ETH", "DOGE", "BNB", "SUI", "SOL"]
        self.crypto_dropdown = ttkb.Combobox(
            self.root,
            values=cryptos,
            textvariable=self.crypto_var,
            font=self.dropdown_font,
            bootstyle=PRIMARY,
        )
        self.crypto_dropdown.grid(row=0, column=1, padx=10, pady=30, sticky="w")  # 修改1

        # 搜尋按鈕
        self.search_button = ttkb.Button(
            self.root,
            text="搜尋",
            command=self.fetch_data,
            style="MetroButton.Purple.TButton",  # 套用自訂樣式
        )
        self.search_button.grid(row=0, column=2, columnspan=2, padx=10, pady=30, sticky="w")  # 修改1

        # 資料庫搜尋按鈕
        self.search_database_button = ttkb.Button(
            self.root,
            text="資料庫搜尋",
            command=self.open_search_window,
            style="MetroButton.Purple.TButton",  # 套用自訂樣式
        )
        self.search_database_button.grid(row=0, column=4, padx=30, pady=30, sticky="w")  # 修改1

        self.result_table = ttkb.Treeview(
            self.root,
            columns=("幣種", "價格", "漲跌", "24H成交量", "市值"),
            show="headings",
            height=1,
            bootstyle=INFO,
            style="MetroTable.Treeview",  # 套用自訂樣式
        )

        for col in ("幣種", "價格", "漲跌", "24H成交量", "市值"):
            self.result_table.heading(col, text=col)
            self.result_table.column(col, anchor="center")
            self.result_table.grid(
                row=1, column=0, columnspan=5, padx=30, pady=10, sticky="ew"  # 修改1
            )

        # 插入空行
        self.empty_label = ttkb.Label(self.root, text="", font=self.empty_font)
        self.empty_label.grid(row=2, column=0, columnspan=1)  # 修改1

        # 備註標籤
        self.note_label = ttkb.Label(
            self.root,
            text="備註",
            font=self.label_font,
            bootstyle=SECONDARY,
        )
        self.note_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        # 備註輸入
        self.note_entry = ttkb.Entry(self.root, width=50, font=self.empty_font)
        self.note_entry.grid(row=3, column=1, columnspan=2, padx=50, pady=10, sticky="ew")  # 修改1

        # 新增按鈕
        self.add_button = ttkb.Button(
            self.root,
            text="新增",
            command=self.add_to_database,
            style="MetroButton.Purple.TButton",  # 套用自訂樣式
        )
        self.add_button.grid(row=3, column=3, padx=10, pady=10, sticky="w")  # 修改1

        # 插入空行
        self.empty_label = ttkb.Label(self.root, text="", font=self.empty_font)
        self.empty_label.grid(row=4, column=0, columnspan=1)  # 佔用一整行

        # 最新新聞標籤
        self.news_label = ttkb.Label(
            self.root,
            text="最新新聞",
            font=self.label_font,
            bootstyle=DARK,
        )
        self.news_label.grid(row=5, column=0, columnspan=5)  # 修改1

        # 新聞列表
        self.news_table = ttkb.Treeview(
            self.root,
            columns=("標題", "連結", "日期"),
            show="headings",
            height=5,
            style="MetroTable.Treeview",  # 套用自訂樣式
        )
        self.news_table.heading("標題", text="標題")
        self.news_table.heading("連結", text="連結")
        self.news_table.heading("日期", text="日期")
        self.news_table.column("標題", width=700, anchor="w")  # 修改1
        self.news_table.column("連結", width=30, anchor="w")   # 修改1
        self.news_table.column("日期", width=20, anchor="center") # 修改1
        self.news_table.grid(
            row=6, column=0, columnspan=5, padx=30, pady=10, sticky="nsew" # 修改1
        )

        self.news_table.bind("<Button-1>", self.on_news_click)

        # 上一頁按鈕
        self.prev_button = ttkb.Button(
            self.root,
            text="上一頁",
            command=self.show_prev_page,
            style="MetroButton.Green.TButton",  # 套用自訂樣式
        )
        self.prev_button.grid(row=7, column=1, padx=10, pady=10)  # 修改1

        # 下一頁按鈕
        self.next_button = ttkb.Button(
            self.root,
            text="下一頁",
            command=self.show_next_page,
            style="MetroButton.Green.TButton",  # 套用自訂樣式
        )
        self.next_button.grid(row=7, column=2, columnspan=2, padx=10, pady=30)  # 修改1

    def fetch_data(self):
        crypto = self.crypto_var.get()
        if not crypto:
            print("[WARNING] No cryptocurrency selected!")
            return

        print(f"[INFO] Fetching data for selected cryptocurrency: {crypto}")
        data = get_crypto_data(crypto)
        self.result_table.delete(*self.result_table.get_children())
        self.result_table.insert(
            "",
            "end",
            values=(data["name"], data["price"], data["change"], data["volume"], data["market_cap"]), # 修改1
        )

        self.news_data = get_news(crypto)
        self.current_page = 1
        self.display_news()

    def display_news(self):
        self.news_table.delete(*self.news_table.get_children())
        start_index = (self.current_page - 1) * self.news_per_page
        end_index = start_index + self.news_per_page
        for news in self.news_data[start_index:end_index]:
            self.news_table.insert(
                "", "end", values=(news["title"], news["link"], news["time"]) # 修改1
            )

    def show_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_news()

    def show_next_page(self):
        if self.current_page < (len(self.news_data) + self.news_per_page - 1) // self.news_per_page:
            self.current_page += 1
            self.display_news()

    def add_to_database(self):
        selected_item = self.result_table.focus()
        if not selected_item:
            print("[WARNING] No row selected for adding to database!")
            return

        values = self.result_table.item(selected_item, "values")
        note = self.note_entry.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "crypto": values[0],
            "price": values[1],
            "change": values[2],
            "volume": values[3],
            "market_cap": values[4],
            "timestamp": timestamp,
            "note": note,
        }

        self.database.insert_data(data)
        print(f"[INFO] Data added to database: {data}")

    def open_search_window(self):
        search_window = ttkb.Toplevel(self.root)  # 使用 ttkbootstrap 的 Toplevel
        search_window.title("資料庫搜尋")
        search_window.configure(bg="white")  # 直接設置背景色

        # 設定行列權重，確保控件填滿窗口
        search_window.grid_rowconfigure(2, weight=1)  # 第三行分配可用空間
        search_window.grid_columnconfigure(0, weight=1)
        search_window.grid_columnconfigure(1, weight=1)
        search_window.grid_columnconfigure(2, weight=1)
        search_window.grid_columnconfigure(3, weight=1)

        # 搜尋標籤
        search_label = ttkb.Label(
            search_window,
            text="輸入幣種名稱:",
            font=self.label_font,
            bootstyle="DARK",
        )
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # 搜尋輸入框
        search_entry = ttkb.Entry(search_window, font=self.dropdown_font)
        search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 搜尋按鈕
        search_button = ttkb.Button(
            search_window,
            text="搜尋",
            style="MetroButton.Purple.TButton",  # 自定義按鈕樣式
            command=lambda: self.perform_search(search_window, search_entry),
        )
        search_button.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="w")

    def perform_search(self, search_window, search_entry):
        # 清空之前的結果
        for widget in search_window.winfo_children():
            if isinstance(widget, ttkb.Treeview):
                widget.destroy()

        crypto = search_entry.get()
        if not crypto:
            print("[WARNING] No cryptocurrency entered for search!")
            return

        # 搜尋 database
        records = self.database.get_data(crypto)
        if not records:
            print(f"[INFO] No records found for {crypto}")
            return

        # 幣種資訊
        result_table = ttkb.Treeview(
            search_window,
            columns=("幣種", "價格", "漲跌", "24H成交量", "市值", "時間", "備註"),
            show="headings",
            bootstyle="info",
            style="MetroTable.Treeview",  # 套用自訂樣式
        )

        # 設置列標題和寬度
        result_table.heading("幣種", text="幣種")
        result_table.column("幣種", width=0, anchor="center")

        result_table.heading("價格", text="價格")
        result_table.column("價格", width=200, anchor="center")

        result_table.heading("漲跌", text="漲跌")
        result_table.column("漲跌", width=30, anchor="center")

        result_table.heading("24H成交量", text="24H成交量")
        result_table.column("24H成交量", width=150, anchor="center")

        result_table.heading("市值", text="市值")
        result_table.column("市值", width=150, anchor="center")

        result_table.heading("時間", text="時間")
        result_table.column("時間", width=250, anchor="center")

        result_table.heading("備註", text="備註")
        result_table.column("備註", width=150, anchor="e")

        result_table.grid(
            row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew"
        )

        for record in records:
            result_table.insert("", "end", values=record)

            # 編輯備註
            def edit_record():
                selected_item = result_table.focus()
                if not selected_item:
                    print("[WARNING] No row selected for editing!")
                    return

                values = result_table.item(selected_item, "values")
                new_note = tk.simpledialog.askstring(
                    "編輯備註", "輸入新的備註:", parent=search_window
                )
                if new_note is not None:
                    self.database.update_data(values[0], values[5], new_note)
                    print(
                        f"[INFO] Updated record for {values[0]} with new note: {new_note}"
                    )
                    # 更新
                    result_table.item(selected_item, values=(*values[:-1], new_note))

            # 刪除備註
            def delete_record():
                selected_item = result_table.focus()
                if not selected_item:
                    print("[WARNING] No row selected for deletion!")
                    return

                values = result_table.item(selected_item, "values")
                self.database.delete_data(values[0], values[5])
                print(f"[INFO] Deleted record for {values[0]} at {values[5]}")
                result_table.delete(selected_item)

            # 編輯按鈕
            edit_button = ttkb.Button(
                search_window,
                text="編輯",
                style="MetroButton.Green.TButton",  # 套用自訂樣式
                command=edit_record,
            )
            edit_button.grid(row=3, column=0, columnspan=2, padx=400, pady=10)

            # 刪除按鈕
            delete_button = ttkb.Button(
                search_window,
                text="刪除",
                style="MetroButton.Red.TButton",  # 套用自訂樣式
                command=delete_record,
            )
            delete_button.grid(row=3, column=2, columnspan=2, padx=400, pady=10)

    def on_news_click(self, event):
        region = self.news_table.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.news_table.identify_column(event.x)
        row_id = self.news_table.identify_row(event.y)

        if column == "#2":
            item = self.news_table.item(row_id)
            link = item["values"][1]
            if link:
                webbrowser.open(link)
                print(f"[INFO] Opened link: {link}")

    def run(self):
        print("[INFO] Running the GUI application...")
        self.root.mainloop()

if __name__ == "__main__":
    app = CryptoApp()
    app.run()
