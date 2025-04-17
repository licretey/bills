import csv
from .base_processor import BaseProcessor



class AlipayProcessor(BaseProcessor):
    FILE_FROM = "alipay"
    COLUMN_MAP = {
        "交易时间": "transaction_time",
        "交易分类": "transaction_category",
        "交易对方": "counterparty",
        "对方账号": "counterparty_account",
        "商品说明": "product_description",
        "收/支": "income_or_expense",
        "金额": "amount",
        "收/付款方式": "payment_method",
        "交易状态": "transaction_status",
        "交易订单号": "transaction_id",
        "商家订单号": "merchant_order_id",
        "备注": "remarks"
    }

    def run(self):
        with open(self.file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader, start=1):
                if "交易时间" in row:
                    self.header_map = {col: idx for idx, col in enumerate(row)}
                    continue
                elif not self.header_map:
                    self.parse_header_metadata(row)
                    continue  # 跳过非数据区

                try:
                    values = []
                    for key in self.COLUMN_MAP.keys():
                        raw = row[self.header_map.get(key, '')].strip()
                        if key == "交易时间":
                            values.append(self.parse_time(raw))
                        elif key == "金额":
                            values.append(float(raw) if raw else None)
                        else:
                            values.append(raw)
                    values += [self.file_name, self.FILE_FROM] + list(self.info.values())
                    self.insert_data(values, list(self.COLUMN_MAP.values()) + ["file_name", "file_from"] + list(self.info.keys()))
                except Exception as e:
                    print(f"解析错误 at line {i}: {e}")