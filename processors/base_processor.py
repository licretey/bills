import os
import re
from datetime import datetime


class BaseProcessor:
    def __init__(self, conn, file_path):
        self.conn = conn
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.header_map = {}
        self.info = {
            'order_account': None,
            'file_start': None,
            'file_end': None,
            'file_export_time': None,
            'file_bills_count': None,
            'file_record_income': None,
            'file_record_income_count': None,
            'file_record_expense': None,
            'file_record_expense_count': None,
            'file_record_unknow_count': None,
            'file_record_unknow_total': None,
        }

    def connect_cursor(self):
        return self.conn.cursor()

    def parse_time(self, time_str):
        """尝试多种时间格式解析"""
        for fmt in ['%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M']:
            try:
                return datetime.strptime(time_str, fmt)
            except ValueError:
                continue
        return None

    def insert_data(self, data, columns):
        placeholders = ','.join(['%s'] * len(columns))
        query = f"INSERT INTO bill ({', '.join(columns)}) VALUES ({placeholders})"
        cursor = self.connect_cursor()
        try:
            cursor.execute(query, data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"插入失败: {e}\n数据: {data}")
        finally:
            cursor.close()

    def run(self):
        raise NotImplementedError("子类必须实现 run 方法")


    def parse_header_metadata(self, line):
        # 拼接后法便匹配校验
        line = ','.join(line).strip()
        lineRow = line.strip(",")
        # 微信昵称/支付宝账户
        if '微信昵称：' in line or '姓名：' in line:
            self.info['order_account'] = re.sub(r'^(微信昵称|姓名)：', '', lineRow).strip()
        if '支付宝账户：' in line:
            self.info['order_account'] = re.sub(r'^支付宝账户：', '', lineRow).strip()

        # 起止时间
        if '起始时间：' in line and '终止时间：' in line:
            match = re.findall(r'\[(.*?)\]', lineRow)
            if len(match) == 2:
                self.info['file_start'] = self.parse_time(match[0])
                self.info['file_end'] = self.parse_time(match[1])

        # 导出时间
        if '导出时间：' in line:
            match = re.search(r'\[(.*?)\]', lineRow)
            if match:
                self.info['file_export_time'] = self.parse_time(match.group(1))

        # 总交易笔数
        if re.match(r'^共\d+笔记录', line):
            match = re.search(r'^共(\d+)笔记录', lineRow)
            if match:
                self.info['file_bills_count'] = int(match.group(1))

        # 收入/支出/不计收支
        if '收入：' in line:
            match = re.findall(r'(\d+)笔\s+([\d.]+)元', lineRow)
            if match:
                self.info['file_record_income_count'] = int(match[0][0])
                self.info['file_record_income'] = float(match[0][1])
        if '支出：' in line:
            match = re.findall(r'(\d+)笔\s+([\d.]+)元', lineRow)
            if match:
                self.info['file_record_expense_count'] = int(match[0][0])
                self.info['file_record_expense'] = float(match[0][1])
        if '不计收支：' in line or '中性交易：' in line:
            match = re.findall(r'(\d+)笔\s+([\d.]+)元', lineRow)
            if match:
                self.info['file_record_unknow_count'] = int(match[0][0])
                self.info['file_record_unknow_total'] = float(match[0][1])