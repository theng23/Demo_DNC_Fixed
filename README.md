# Demo_DNC_Fixed

Dự án này là một demo Windows cho mô hình Retrieval-Augmented Generation (RAG) đơn giản, dùng dữ liệu tài liệu local (`.txt`) để tìm đoạn liên quan, ghép ngữ cảnh và tạo prompt cho Microsoft Copilot/LLM.

Mục tiêu của demo là minh họa cách:

- đọc tài liệu local bằng Python
- chia tài liệu thành các chunk / đoạn nội dung
- tìm kiếm thông tin dựa trên từ khóa
- chuẩn bị prompt có ngữ cảnh cho Copilot
- hỗ trợ kiểm tra nhanh các câu hỏi về DNC / khách hàng / cuộc gọi giả lập

## 1. Giới thiệu

Repo này chứa các script Python để:

- `ai_search_copilot_windows.py`: điểm vào chính, xử lý retrieval + augmentation và có thể gửi prompt lên Copilot API nếu đã cấu hình Azure app registration
- `read_document.py`: đọc, tách chunk và rút trích nội dung liên quan
- `generate_dnc_demo.py`: tạo dữ liệu demo DNC mẫu
- `test_ai_search_copilot_windows.py`: kiểm thử tự động cho logic retrieval và prompt

Dữ liệu demo được lưu trong:

- `document_dnc_demo.txt`
- `Ticket_DNC_DEMO.txt`
- `Tai_lieu_DNC_DEMO.txt`

## 2. Yêu cầu

- Python 3.10+
- Windows 10/11
- Pip để cài dependencies

Cài đặt:

```powershell
python -m pip install -r requirements_windows.txt
```

## 3. Chạy demo cơ bản

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?"
```

Hoặc:

```powershell
python .\ai_search_copilot_windows.py --question "Application sau DNC có bắt buộc cùng Ops không?"
```

Script sẽ:

1. đọc tài liệu local
2. tách đoạn văn bản theo mục
3. tìm chunk phù hợp với câu hỏi
4. tạo prompt chuẩn bị cho Copilot
5. xuất nội dung cho bạn copy sang Copilot web hoặc gửi qua API nếu đã cấu hình quyền truy cập

## 4. Tự động gửi lên Copilot

Nếu bạn đã có Azure app registration và quyền phù hợp, có thể dùng chế độ Copilot API:

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?" --copilot
```

Chi tiết đăng nhập / quyền / token cache được mô tả trong:

- `README_LOGIN_WINDOWS.md`
- `BAT_DAU.md`

## 5. Kiểm tra nhanh

```powershell
python -m unittest -v
```

## 6. Lưu ý quan trọng

- Đây là dữ liệu demo giả lập, không phải dữ liệu chính thức của công ty.
- Chế độ mặc định của project là retrieval + augmentation local, còn generation được thực hiện bằng Copilot web hoặc API sau khi đã có quyền truy cập.
- Logic tìm kiếm dựa trên từ khóa và chunk local, không phải vector database hay embedding.
- Cần kiểm tra lại source và kết quả AI trước khi dùng cho mục đích thực tế.

## 7. Cấu trúc thư mục chính

```text
Demo_DNC_Fixed/
├── ai_search_copilot_windows.py
├── ask_dnc.py
├── ask_dnc.before_loop.py
├── ask_dnc.before_rag_fix.py
├── BAT_DAU.md
├── config.json
├── document_dnc_demo.txt
├── generate_dnc_demo.py
├── prompt_copilot.txt
├── read_document.py
├── README.md
├── README_LOGIN_WINDOWS.md
├── requirements_windows.txt
├── test_ai_search_copilot_windows.py
├── Ticket_DNC_DEMO.txt
├── Tai_lieu_DNC_DEMO.txt
└── TRAINING_15P.md
```

## 8. Mục đích phát triển

Demo này phù hợp để học cách:

- RAG trên file local
- prompt engineering cho Copilot
- xử lý dữ liệu dạng tài liệu nội bộ
- chuẩn bị nền tảng cho hệ thống AI Search có kiểm soát nguồn dữ liệu

Nếu bạn muốn, mình có thể tiếp tục mở rộng project thành phiên bản có giao diện web, search nâng cao hoặc tích hợp backend API.
