# LLM + RAG cho AI Search — buổi demo 15 phút

Mục tiêu: người nghe hiểu hệ thống tìm tài liệu rồi tạo câu trả lời có căn cứ, biết kiểm tra nguồn và nhận ra điều chưa xác nhận. Đây là training cho con người, không fine-tune trọng số mô hình.

## 0–3 phút: đặt vấn đề

“Một khách có hai cuộc gọi DNC thì đếm một hay hai? Mình cần biết đơn vị đếm và định nghĩa trong tài liệu. Hôm nay mình dùng kịch bản giả lập để minh họa cách AI hỗ trợ tra cứu.”

Giải thích LLM là phần tạo câu trả lời bằng ngôn ngữ. AI Search là trải nghiệm tìm kiếm/hỏi đáp; RAG là một cách xây dựng trải nghiệm đó bằng cách truy xuất thông tin liên quan rồi bổ sung vào context cho LLM. Không cần cố tạo một câu trả lời sai khi chưa có nguồn để chứng minh lợi ích của RAG.

## 3–5 phút: mở nguồn

Mở `Ticket_DNC_DEMO.txt`. Chỉ ba phần: định nghĩa chỉ số, bốn dòng dữ liệu và yêu cầu còn pending. Nói rõ tài liệu này là giả lập, không phải quy định chính thức của Home Credit.

## 5–10 phút: demo luồng chính

```powershell
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?"
```

Chỉ [R]: “Python chọn các mục liên quan trong tài liệu. Đây là retrieval. Bản demo dùng từ khóa, không dùng embedding.”

Chỉ [A]: “Python ghép câu hỏi với nguồn, thêm yêu cầu dẫn ID và nói rõ khi thiếu thông tin. Đây là augmentation.”

```powershell
Get-Content .\prompt_copilot.txt -Raw | Set-Clipboard
```

Dán vào chat mới của Copilot, gửi và chờ câu trả lời thật:

“Copilot dùng LLM để diễn đạt câu trả lời từ context mình vừa cấp. Đây là generation. Hôm nay mình chuyển prompt thủ công vì app Python chưa có quyền API.”

Mở prompt, đối chiếu [S2], [S3] với câu trả lời. Nếu thiếu nguồn, yêu cầu Copilot nêu ID thích hợp và tự kiểm tra lại. Các ID là mục TXT local, không phải link SharePoint.

Chạy lại với câu hỏi số lượng trong BAT_DAU.md. Copy prompt mới và đối chiếu 3 cuộc gọi/2 khách hàng; KH001 riêng có 2 cuộc gọi/1 khách hàng.

## 10–13 phút: nhận ra điều chưa biết

```powershell
python .\ai_search_copilot_windows.py --question "Application sau DNC có bắt buộc cùng Ops không?"
```

Copy prompt mới sang chat mới. Đối chiếu [S5]: tài liệu chưa xác nhận cùng Ops hay cửa sổ thời gian. Nếu AI tự đặt quy tắc, dùng ngay làm ví dụ vì sao có nguồn vẫn cần kiểm chứng.

## 13–15 phút: ứng dụng

“Team có thể dùng cách này để đọc FAQ, hiểu chỉ số báo cáo, tra cứu quy trình đã duyệt và chuẩn bị câu hỏi xác nhận business. Câu trả lời tốt phụ thuộc nguồn đúng, tìm đúng đoạn và LLM dùng nguồn đúng.”

Mời team nêu một loại tài liệu thường mất thời gian tra cứu. Không cần trình bày toàn bộ code hoặc phần đăng nhập trong 15 phút.

Chuẩn bị trước: chạy ba câu hỏi, mở Copilot và kiểm tra clipboard. Kết quả trong hướng dẫn là tiêu chí đối chiếu, không phải câu trả lời LLM đã chạy. Nếu không mở được Copilot thì chỉ demo được R/A; nói rõ phần G chưa chạy, không dùng câu trả lời ghi sẵn như kết quả trực tiếp.
