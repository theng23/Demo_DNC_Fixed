# LLM + RAG cho AI Search — bản sửa từ Demo_DNC.7z

## Mở đúng bản

Giải nén ZIP vào folder mới. Mở folder có `ai_search_copilot_windows.py`, bấm thanh địa chỉ File Explorer, gõ `powershell`, Enter. Chạy:

```powershell
python .\ai_search_copilot_windows.py --version
```

Phải hiện **DNC LOCAL RAG v2**. Nếu chưa thấy, kiểm tra lại folder trước khi chạy tiếp.

## Demo với quyền hiện tại

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?"
```

- **[R] RETRIEVAL:** Python chia TXT thành 6 mục và chọn tối đa hai mục phù hợp. Câu đầu chọn [S2], [S3].
- **[A] AUGMENTATION:** ghép câu hỏi, chỉ dẫn và nguồn vào `prompt_copilot.txt`.
- **[G] GENERATION:** hiện rõ chưa gọi LLM trong Python; bạn chuyển prompt sang Copilot web để sinh câu trả lời thật.

```powershell
Get-Content .\prompt_copilot.txt -Raw | Set-Clipboard
```

Mở chat mới trong Copilot công ty, Ctrl+V rồi gửi. Đối chiếu nội dung và ID nguồn với các đoạn Python đã chọn. Không đính kèm thêm toàn bộ TXT vào chat trong bài test này.

Chạy các câu hỏi tiếp theo, copy lại prompt mới sau mỗi lần:

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS và DNC_CUSTOMERS trong dữ liệu minh họa bằng bao nhiêu? Giải thích KH001."

python .\ai_search_copilot_windows.py --question "Application sau DNC có bắt buộc cùng Ops không?"
```

Kỳ vọng đối chiếu: toàn bộ tập có 3 cuộc gọi/2 khách hàng; KH001 riêng có 2 cuộc gọi/1 khách hàng. Với Application, nguồn [S5] nêu chưa xác nhận cùng Ops. Đây là tiêu chí kiểm tra, không phải câu trả lời LLM đã chạy sẵn.

Không cần cài thêm thư viện, đăng nhập API hoặc tạo .venv trong chế độ này. Nếu bỏ `--question`, script hỏi bạn nhập câu hỏi trong terminal.

## Chọn nguồn local

`config.json` giữ các ID và URL bạn gửi, thêm `document_path` mặc định là `Ticket_DNC_DEMO.txt`. `file_urls` được giữ nhưng không dùng trong flow local. Không có config thì script vẫn đọc TXT mặc định cùng folder.

```powershell
python .\ai_search_copilot_windows.py --file "C:\duong-dan\Tai_lieu.txt" --question "Câu hỏi của bạn"
```

Đường dẫn tương đối được tính từ folder chứa script. Tài liệu trong gói là giả lập, không phải quy định chính thức của Home Credit.

## Gọi LLM tự động

Thêm `--copilot` sau khi có app registration riêng và quyền phù hợp. Xem `README_LOGIN_WINDOWS.md`. Cấu hình gửi lên đang dùng Client ID Azure CLI từng gặp AADSTS65002; code sẽ báo rõ và dừng trước auth, vẫn giữ prompt để dùng trên web.

`--dry-run` in payload với context local, không gọi API kể cả khi đi kèm `--copilot`.

## Các script sau khi sửa

- `ai_search_copilot_windows.py`: điểm chạy chính, hiện R/A/G, có tùy chọn Copilot API.
- `read_document.py`: chia mục, truy xuất từ khóa và ghép prompt; vẫn chạy độc lập được.
- `test_ai_search_copilot_windows.py`: unittest thực tế, đã thay bản bị chép nhầm nội dung chương trình chính.

Chạy kiểm tra bằng `python -m unittest -v`. Test API/auth dùng mock; chưa kiểm tra DPAPI, MFA hoặc câu trả lời Copilot thật trong tenant công ty.

## Giới hạn cần nói đúng

Retrieval là tìm từ khóa có chuẩn hóa dấu tiếng Việt, không có embedding/vector database. Mỗi mục đánh số là một chunk; nếu không có mục đánh số thì toàn file là một chunk. Điểm không phải độ tin cậy, và câu hỏi đồng nghĩa có thể tìm thiếu/sai nguồn.

Với chế độ mặc định, Python thực hiện retrieval + augmentation, Copilot web thực hiện generation sau thao tác dán prompt thủ công. Chưa tự động toàn bộ. LLM vẫn có thể trả lời sai hoặc dẫn ID sai, nên phải kiểm tra nguồn.

Câu `Bitcoin Ethereum` không có từ khóa trong tài liệu: báo `CHUA_DU_NGUON`, không gọi LLM và thay prompt cũ để tránh dùng nhầm nguồn.
