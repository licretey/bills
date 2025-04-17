import csv
from .base_processor import BaseProcessor

class WechatProcessor(BaseProcessor):
    FILE_FROM = "wechat"
    COLUMN_MAP = {
        "交易时间": "transaction_time",
        "交易类型": "transaction_category",
        "交易对方": "counterparty",
        "对方账号": "counterparty_account",
        "商品": "product_description",
        "收/支": "income_or_expense",
        "金额(元)": "amount",
        "支付方式": "payment_method",
        "当前状态": "transaction_status",
        "交易单号": "transaction_id",
        "商户单号": "merchant_order_id",
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
                        if key == '对方账号':
                            values.append("/")
                            continue
                        raw = row[self.header_map.get(key, '')].strip()
                        if key == "交易时间":
                            values.append(self.parse_time(raw))
                        elif key == "金额(元)":
                            values.append(float(raw.replace('¥', '')) if raw else None)
                        elif key == "收/支":
                            if raw == "不计收支" or raw == "/":
                                raw = "不计收支"
                            values.append(raw)
                        else:
                            values.append(raw)
                    values += [self.file_name, self.FILE_FROM] + list(self.info.values())
                    self.insert_data(values, list(self.COLUMN_MAP.values()) + ["file_name", "file_from"] + list(self.info.keys()))
                except Exception as e:
                    print(f"解析错误 at line {i}: {e}")