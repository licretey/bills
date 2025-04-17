import os
from processors.alipay import AlipayProcessor
from processors.wechat import WechatProcessor
from config import DB_CONFIG
import psycopg2

PROCESSOR_MAP = {
    'alipay': AlipayProcessor,
    '微信支付': WechatProcessor
}
# 数据文件目录
DATA_DIR = "./data"

def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def main():
    conn = connect_db()
    for filename in os.listdir(DATA_DIR):
        for prefix, processor_cls in PROCESSOR_MAP.items():
            if filename.startswith(prefix):
                file_path = os.path.join(DATA_DIR, filename)
                print(f"使用 {processor_cls.__name__} 处理文件: {filename}")
                processor = processor_cls(conn, file_path)
                processor.run()
    conn.close()

if __name__ == "__main__":
    main()
