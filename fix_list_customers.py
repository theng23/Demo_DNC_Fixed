"""Chạy một lần trong thư mục chứa ask_dnc.py để sửa truy vấn liệt kê khách hàng."""

from pathlib import Path


INSERT = r'''        # DNC_LIST_ALL_CUSTOMERS_FIX
        import unicodedata

        list_query = unicodedata.normalize("NFD", question.casefold().replace("đ", "d"))
        list_query = "".join(c for c in list_query if unicodedata.category(c) != "Mn")
        if (
            re.search(r"\b(liet ke|danh sach|hien thi|xem|in)\b", list_query)
            and re.search(r"\b(tat ca|toan bo|het)\b", list_query)
            and re.search(r"\b(khach hang|customers?|customer_id)\b", list_query)
            and not re.search(r"\b(dnc|other|result|kh\d+|call\d+)\b", list_query)
        ):
            customer_file = Path(__file__).resolve().with_name("document_dnc_demo.txt")
            customer_document = customer_file.read_text(encoding="utf-8-sig")
            customer_ids = set(re.findall(
                r"^\s*CALL\d+\s*\|\s*(KH\d+)\s*\|\s*(?:DNC|OTHER)\s*$",
                customer_document, re.I | re.M,
            ))
            customer_ids = sorted({value.upper() for value in customer_ids},
                                  key=lambda value: (int(value[2:]), value))
            if not customer_ids:
                raise ValueError("Không tìm thấy dòng dữ liệu cuộc gọi trong document_dnc_demo.txt.")
            print(f"{len(customer_ids)} khách hàng trong dữ liệu giả lập ({customer_file.name}):")
            print("\n".join(customer_ids))
            continue

'''


def main():
    target = Path(__file__).resolve().with_name("ask_dnc.py")
    original = target.read_bytes()
    code = original.decode("utf-8-sig").replace("\r\n", "\n")
    if "# DNC_LIST_ALL_CUSTOMERS_FIX" in code:
        print("ask_dnc.py đã có bản sửa này; không cần ghi lại.")
        return

    anchors = [
        "        prompt, sources = prepare(question)\n",
        '        document = path.read_text(encoding="utf-8-sig")\n',
    ]
    matches = [anchor for anchor in anchors if code.count(anchor) == 1]
    if len(matches) != 1:
        raise ValueError("Phiên bản ask_dnc.py khác dự kiến; chưa thay đổi file. Hãy gửi nội dung file để sửa đúng vị trí.")

    updated = code.replace(matches[0], INSERT + matches[0], 1)
    compile(updated, str(target), "exec")
    backup = target.with_name("ask_dnc.before_list_customers.py")
    if not backup.exists():
        backup.write_bytes(original)
    target.write_text(updated, encoding="utf-8-sig")
    print("Đã sửa ask_dnc.py. Bản sao: ask_dnc.before_list_customers.py.")
    print("Chạy: python .\\ask_dnc.py")


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError, SyntaxError) as error:
        print("Lỗi:", error)
        raise SystemExit(1)

