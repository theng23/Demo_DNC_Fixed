from collections import defaultdict
from pathlib import Path
import random
import shutil

NUM_CALLS = 1_000
NUM_CUSTOMERS = 300

if NUM_CUSTOMERS < 3 or NUM_CALLS < NUM_CUSTOMERS + 1:
    raise ValueError("Cần ít nhất 3 khách hàng và số cuộc gọi > số khách hàng.")

rng = random.Random(42)
rows = []

def add_call(customer, result=None):
    if result is None:
        result = "DNC" if rng.random() < 0.4 else "OTHER"
    rows.append((
        f"CALL{len(rows) + 1:02d}",
        f"KH{customer:03d}",
        result,
    ))

# Giữ nguyên bốn dòng ban đầu.
add_call(1, "DNC")
add_call(1, "DNC")
add_call(2, "DNC")
add_call(3, "OTHER")

# Đảm bảo mỗi khách hàng có ít nhất một cuộc gọi.
for customer in range(4, NUM_CUSTOMERS + 1):
    add_call(customer)

while len(rows) < NUM_CALLS:
    add_call(rng.randint(1, NUM_CUSTOMERS))

by_customer = defaultdict(list)
for row in rows:
    by_customer[row[1]].append(row)

dnc_rows = [row for row in rows if row[2] == "DNC"]
dnc_customers = {row[1] for row in dnc_rows}

# Kiểm tra tính nhất quán trước khi ghi.
assert len(rows) == NUM_CALLS
assert len({row[0] for row in rows}) == NUM_CALLS
assert len(by_customer) == NUM_CUSTOMERS
assert all(row[2] in {"DNC", "OTHER"} for row in rows)

parts = [
    "TÀI LIỆU GIẢ LẬP CHO TRAINING RAG — KHÔNG PHẢI QUY ĐỊNH CÔNG TY",
    "Mã tài liệu: DNC-DEMO. Phiên bản: DEMO-v2.",
    "Toàn bộ khách hàng và cuộc gọi đều là dữ liệu giả lập.",
    "",
    "1. Định nghĩa và phạm vi",
    "DNC_CALLS là số dòng cuộc gọi có RESULT = 'DNC'.",
    "DNC_CUSTOMERS là số CUSTOMER_ID khác nhau có ít nhất một cuộc gọi DNC.",
    "Một khách hàng có nhiều cuộc gọi DNC vẫn chỉ tính là một khách hàng DNC.",
    "TOTAL_CALLS đếm toàn bộ cuộc gọi, gồm cả DNC và OTHER.",
    "TOTAL_CUSTOMERS đếm toàn bộ khách hàng khác nhau.",
    "Không có dữ liệu khách hàng thật, lãi suất, hạn mức hoặc chính sách bán hàng.",
    "",
    "2. Tổng hợp số liệu của toàn bộ tập dữ liệu",
    "Đây là bảng tổng hợp đã được Python tính từ toàn bộ dữ liệu.",
    "Không được dùng số dòng của một đoạn truy xuất để suy ra tổng toàn bộ tập.",
    "CHI_SO | GIA_TRI | DON_VI",
    f"TOTAL_CALLS | {len(rows)} | cuộc gọi",
    f"TOTAL_CUSTOMERS | {len(by_customer)} | khách hàng",
    f"DNC_CALLS | {len(dnc_rows)} | cuộc gọi",
    f"DNC_CUSTOMERS | {len(dnc_customers)} | khách hàng",
    f"OTHER_CALLS | {len(rows) - len(dnc_rows)} | cuộc gọi",
    "",
]

# Mỗi khách hàng là một đoạn riêng để truy xuất.
for section, customer in enumerate(sorted(by_customer), start=3):
    calls = by_customer[customer]
    count_dnc = sum(row[2] == "DNC" for row in calls)
    parts.extend([
        f"{section}. Khách hàng {customer}",
        f"CUSTOMER_ID = {customer}.",
        f"Khách hàng này có {len(calls)} cuộc gọi, gồm {count_dnc} cuộc gọi DNC.",
        "CALL_ID | CUSTOMER_ID | RESULT",
        *(" | ".join(row) for row in calls),
        "",
    ])

base = Path(__file__).resolve().parent
target = base / "document_dnc_demo.txt"
backup = base / "document_dnc_demo.before_scale.txt"

if target.exists() and not backup.exists():
    shutil.copy2(target, backup)

target.write_text("\n".join(parts), encoding="utf-8-sig")

print(
    f"Đã tạo {target}: {len(rows):,} cuộc gọi; "
    f"{len(by_customer):,} khách hàng; "
    f"DNC_CALLS={len(dnc_rows):,}; "
    f"DNC_CUSTOMERS={len(dnc_customers):,}."
)

