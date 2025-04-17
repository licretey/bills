# bills
alipay and wechat bills import to pg from csv file



# 使用步骤
## 一 建立数据库并配置
### 1.1 建库建表

```sql
create table if not exists public.bill
(
    id                        integer default nextval('bill_id_seq'::regclass) not null
        primary key,
    transaction_time          timestamp,
    transaction_category      varchar(100),
    counterparty              varchar(100),
    product_description       text,
    income_or_expense         varchar(10),
    amount                    numeric(14, 4),
    payment_method            varchar(50),
    transaction_status        varchar(50),
    transaction_id            varchar(100),
    merchant_order_id         varchar(100),
    remarks                   text,
    counterparty_account      varchar(100),
    order_account             varchar(100),
    file_name                 varchar(100),
    file_from                 varchar(50),
    file_start                timestamp,
    file_end                  timestamp,
    file_export_time          timestamp,
    file_bills_count          integer,
    file_record_income        numeric(14, 4),
    file_record_expense       numeric(14, 4),
    file_record_unknow_count  integer,
    file_record_unknow_total  numeric(14, 4),
    file_record_income_count  integer,
    file_record_expense_count integer
);

comment on column public.bill.transaction_time is '交易时间+8时区';

comment on column public.bill.transaction_category is '交易分类';

comment on column public.bill.counterparty is '交易对方';

comment on column public.bill.product_description is '商品说明';

comment on column public.bill.income_or_expense is '收/支（可填：收入IN+、支出OUT-）';

comment on column public.bill.amount is '金额（支持两位小数）';

comment on column public.bill.payment_method is '收/付款方式';

comment on column public.bill.transaction_status is '交易状态';

comment on column public.bill.transaction_id is '交易订单号';

comment on column public.bill.merchant_order_id is '商家订单号';

comment on column public.bill.remarks is '备注';

comment on column public.bill.counterparty_account is '对方账号';

comment on column public.bill.order_account is '订单账号';

comment on column public.bill.file_name is '导入文件名称';

comment on column public.bill.file_from is '文件来源，如阿里，微信';

comment on column public.bill.file_start is '文件导出起始时间';

comment on column public.bill.file_end is '文件导出结束时间';

comment on column public.bill.file_export_time is '文件导出时间';

comment on column public.bill.file_bills_count is '文件记录总条数';

comment on column public.bill.file_record_income is '文件收入总额';

comment on column public.bill.file_record_expense is '文件支出总额';

comment on column public.bill.file_record_unknow_count is '文件不记收支条数';

comment on column public.bill.file_record_unknow_total is '文件不记收支总额';
```



### 1.2 配置config.py

## 二 下载数据到特定目录下
+ 如创建`data`目录
+ 将目录路径配置到main.py中

## 三 下载pg包

## 四 执行
`python main.py`