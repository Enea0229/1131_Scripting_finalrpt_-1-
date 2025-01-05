import sqlite3


class Database:
    def __init__(self, db_name="crypto_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    ## 幣種資訊表
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS crypto_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto TEXT NOT NULL,
            price REAL NOT NULL,
            change TEXT NOT NULL,
            volume TEXT NOT NULL,
            market_cap TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            note TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    ## 幣種資訊新增
    def insert_data(self, data):
        query = """
        INSERT INTO crypto_data (crypto, price, change, volume, market_cap, timestamp, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (
                data["crypto"],
                data["price"],
                data["change"],
                data["volume"],
                data["market_cap"],
                data["timestamp"],
                data.get("note", ""),
            ),
        )
        self.conn.commit()

    ## 幣種資訊取得
    def get_data(self, crypto):
        query = """
        SELECT crypto, price, change, volume, market_cap, timestamp, note
        FROM crypto_data
        WHERE crypto = ?
        ORDER BY timestamp DESC
        """
        cursor = self.conn.execute(query, (crypto,))
        return cursor.fetchall()

    ## 幣種資訊更新
    def update_data(self, crypto, timestamp, note):
        query = """
        UPDATE crypto_data
        SET note = ?
        WHERE crypto = ? AND timestamp = ?
        """
        self.conn.execute(query, (note, crypto, timestamp))
        self.conn.commit()

    ## 幣種資訊刪除
    def delete_data(self, crypto, timestamp):
        query = """
        DELETE FROM crypto_data
        WHERE crypto = ? AND timestamp = ?
        """
        self.conn.execute(query, (crypto, timestamp))
        self.conn.commit()

    def close(self):
        self.conn.close()
