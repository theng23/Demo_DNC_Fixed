# Demo DNC RAG Local - Ollama + Qwen

Dự án này là một bản demo chạy trên Windows, minh họa mô hình Retrieval-Augmented Generation (RAG) với dữ liệu nội bộ lưu dưới dạng file `.txt`. Mục tiêu là tìm đoạn văn bản liên quan, ghép ngữ cảnh và gửi prompt cho mô hình AI local như Ollama + Qwen, giúp bạn thử nghiệm AI trên máy cá nhân mà không cần phụ thuộc hoàn toàn vào Copilot.

## Mục tiêu

Demo này giúp bạn hiểu và thử nghiệm các bước sau:

- đọc tài liệu local bằng Python
- tách nội dung thành các chunk / đoạn văn bản nhỏ
- tìm kiếm thông tin theo từ khóa hoặc chủ đề
- gom ngữ cảnh phù hợp để tạo prompt
- kiểm tra nhanh các câu hỏi liên quan đến DNC, khách hàng, cuộc gọi giả lập

## Giới thiệu tổng quan

Repo này chứa các script Python chính như sau:

- `ai_search_copilot_windows.py`: điểm vào chính, thực hiện retrieval + augmentation và mặc định gọi mô hình local qua Ollama. Script cũng hỗ trợ tùy chọn `--copilot` cho trải nghiệm dùng Copilot API nếu bạn đã cấu hình quyền.
- `read_document.py`: đọc tài liệu, tách chunk và trích xuất nội dung liên quan
- `generate_dnc_demo.py`: tạo dữ liệu demo mẫu cho DNC
- `test_ai_search_copilot_windows.py`: kiểm thử logic retrieval và prompt

Các file dữ liệu demo bao gồm:

- `document_dnc_demo.txt`
- `Ticket_DNC_DEMO.txt`
- `Tai_lieu_DNC_DEMO.txt`

## Kiến trúc demo

Workflow của project như sau:

1. đọc file tài liệu `.txt`
2. chia nội dung thành các chunk
3. tìm các đoạn phù hợp với câu hỏi
4. tạo prompt có ngữ cảnh
5. gửi prompt đến mô hình AI local hoặc provider khác
6. trả lời theo ngôn ngữ tiếng Việt, dựa trên tài liệu nguồn

## Yêu cầu hệ thống

- Python 3.10+
- Windows 10/11
- Pip để cài đặt package

Cài đặt dependency:

```powershell
python -m pip install -r requirements_windows.txt
```

## Chạy demo cơ bản

Ví dụ 1:

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?"
```

Ví dụ 2:

```powershell
python .\ai_search_copilot_windows.py --question "Application sau DNC có bắt buộc cùng Ops không?"
```

Quy trình chạy sẽ gồm:

1. đọc tài liệu từ thư mục local
2. tách nội dung thành các đoạn nhỏ
3. tìm các chunk phù hợp với câu hỏi
4. xây dựng prompt kèm ngữ cảnh
5. xuất kết quả để bạn copy sang Copilot web hoặc gửi qua API nếu đã cấu hình quyền truy cập

## Chạy local với Ollama + Qwen

Đây là cách chạy chính của project hiện tại.

### Bước 1: Cài Ollama

Tải và cài đặt Ollama từ trang chính thức, sau đó mở terminal và chạy:

```powershell
ollama pull qwen2.5:3b
```

Hoặc thay model theo ý bạn nếu muốn dùng phiên bản khác.

### Bước 2: Khởi động model

```powershell
ollama run qwen2.5:3b
```

### Bước 3: Chạy dự án

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?"
```

Lúc này dự án sẽ:

- đọc file tài liệu local
- tìm đoạn liên quan
- xây dựng prompt có context
- gọi model local Ollama để trả lời

> Nếu bạn đang dùng Copilot, hệ thống vẫn có tùy chọn `--copilot`, nhưng với workflow hiện tại, Ollama + Qwen là cách chạy chuẩn và ổn định nhất.

Hướng dẫn liên quan tới đăng nhập / token / cấu hình Azure nếu cần dùng Copilot cũ vẫn có trong:

- `README_LOGIN_WINDOWS.md`
- `BAT_DAU.md`

## Kiểm tra nhanh

```powershell
python -m unittest -v
```

## Lưu ý quan trọng

- Đây là dữ liệu demo giả lập, không phải dữ liệu chính thức của công ty.
- Chế độ mặc định của project là retrieval + augmentation local.
- Generation có thể chạy trên mô hình local qua Ollama + Qwen hoặc các provider AI khác tùy cấu hình.
- Logic tìm kiếm hiện nay dựa trên từ khóa và chunk local, chưa dùng vector database hay embedding.
- Luôn kiểm tra lại nguồn dữ liệu và kết quả AI trước khi dùng cho mục đích thực tế.

## Cấu trúc thư mục chính

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
├── TRAINING_15P.md
└── ...
```

## Ứng dụng thực tế

Project này phù hợp để học và demo các kỹ năng sau:

- RAG trên file local
- prompt engineering cho mô hình local như Qwen qua Ollama
- xử lý dữ liệu dạng tài liệu nội bộ
- xây dựng nền tảng AI Search có kiểm soát nguồn dữ liệu

## Kết luận

Đây là một demo nhẹ, dễ hiểu và phù hợp để làm nền tảng cho các dự án AI Search hoặc hệ thống hỏi đáp dựa trên tài liệu nội bộ. Nếu cần, bạn có thể tiếp tục mở rộng thành phiên bản web, hệ thống search nâng cao hoặc tích hợp backend API.
