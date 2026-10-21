# AI Chatbot: LLM, RAG và cách hoạt động

## 1. AI Chatbot được tạo ra như thế nào?

AI Chatbot là một ứng dụng giúp người dùng đặt câu hỏi và nhận câu trả lời dưới dạng tự nhiên, giống như trò chuyện với một trợ lý. Một chatbot thông thường có 3 phần chính:

1. Nhận câu hỏi từ người dùng
2. Xử lý ngữ nghĩa và tìm thông tin phù hợp
3. Trả lời dựa trên ngôn ngữ tự nhiên

Với chatbot hiện đại, phần lớn hệ thống sử dụng mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời. Nhưng LLM chỉ giỏi trong việc dự đoán và viết câu, không phải lúc nào cũng biết đúng sự thật nếu không có dữ liệu nguồn rõ ràng.

Vì thế, nhiều chatbot cần thêm một lớp truy xuất thông tin để tìm dữ liệu liên quan trước khi trả lời.

---

## 2. LLM là gì?

LLM là viết tắt của Large Language Model, nghĩa là mô hình ngôn ngữ lớn.

LLM là một mô hình AI được huấn luyện trên khối lượng dữ liệu rất lớn, có khả năng:

- hiểu ngôn ngữ tự nhiên
- trả lời câu hỏi
- tóm tắt văn bản
- dịch thuật
- viết nội dung
- suy luận logic cơ bản

Ví dụ: Qwen, GPT, Llama, Mistral đều là các LLM.

Tuy nhiên, LLM có một hạn chế quan trọng:

- nó có thể “nói rất chắc chắn nhưng không đúng”
- nó không biết mọi thứ trong thời gian thực
- nó có thể tưởng tượng thông tin nếu thiếu nguồn

Vì vậy, khi dùng chatbot cho doanh nghiệp, người ta thường không để LLM tự đoán quá nhiều. Thay vào đó, người ta cho mô hình truy xuất thông tin trước rồi mới trả lời.

---

## 3. RAG là gì?

RAG là viết tắt của Retrieval-Augmented Generation.

Nó có nghĩa là:

- Tìm kiếm (Retrieval): tìm các tài liệu hoặc đoạn văn bản liên quan
- Bổ sung ngữ cảnh (Augmentation): đưa đoạn văn bản đó vào prompt
- Tạo câu trả lời (Generation): cho LLM đọc ngữ cảnh và trả lời

RAG giúp chatbot:

- trả lời dựa trên dữ liệu thật của doanh nghiệp
- nói rõ nguồn thông tin
- giảm nguy cơ “suy luận sai”
- dễ kiểm tra khi câu trả lời sai hoặc thiếu căn cứ

Ví dụ đơn giản:

- Người dùng hỏi: “DNC_CALLS và DNC_CUSTOMERS khác nhau thế nào?”
- Hệ thống tìm trong tài liệu kỹ thuật, FAQ, ticket nội bộ
- Chọn những đoạn liên quan nhất
- Đưa các đoạn ấy vào prompt
- LLM dựa trên chúng để trả lời

---

## 4. LLM + RAG trong AI Chatbot sẽ như thế nào?

Một chatbot tích hợp LLM + RAG thường hoạt động theo luồng sau:

1. Người dùng nhập câu hỏi
2. Hệ thống tìm kiếm trong kho dữ liệu nội bộ
3. Lấy ra các đoạn văn bản phù hợp
4. Ghép chúng thành ngữ cảnh
5. Gửi kèm câu hỏi cho LLM
6. LLM trả lời dựa trên dữ liệu đã cung cấp
7. Hệ thống hiển thị câu trả lời kèm nguồn hoặc ID đoạn tài liệu

### Ví dụ mô hình luồng

```text
Người dùng
   ↓
Câu hỏi
   ↓
Tìm kiếm trong tài liệu / FAQ / ticket / knowledge base
   ↓
Chọn các đoạn liên quan
   ↓
Provide context to LLM
   ↓
LLM trả lời theo ngữ cảnh
   ↓
Hiển thị câu trả lời + nguồn
```

Điểm mạnh của mô hình này là:

- đúng hơn so với LLM thuần
- dễ kiểm tra nguồn
- phù hợp cho doanh nghiệp, nơi cần căn cứ rõ ràng

---

## 5. Tại sao cần RAG nếu đã có LLM?

Vì LLM đơn thuần giống như một người giỏi nói nhưng không có sổ tay. Nếu ta hỏi về quy định nội bộ, báo cáo, tài liệu kỹ thuật, hoặc dữ liệu riêng của công ty, LLM có thể không biết. RAG giải quyết vấn đề này bằng cách cho mô hình đọc dữ liệu thật trước khi phản hồi.

RAG giúp thay đổi từ:

- “AI nói theo suy nghĩ của mình”

sang:

- “AI trả lời dựa trên tài liệu chính thức đã được cung cấp”

---

## 6. Demo với Ticket DNC

Dưới đây là các câu hỏi demo dùng cho tài liệu giả lập DNC.

Mục tiêu là không chỉ hỏi AI mà còn train cách suy nghĩ: xem nguồn có đủ không, có cần xác nhận thêm không, và câu trả lời có dựa trên tài liệu không.

### Ví dụ câu hỏi demo

1. DNC_CALLS khác DNC_CUSTOMERS thế nào?
2. Nếu một khách hàng có 3 cuộc gọi DNC, liệu tính là 3 hay 1?
3. Application sau DNC có bắt buộc phải đi cùng Ops không?
4. Một ticket có thể chứa nhiều loại DNC khác nhau không?
5. Nếu một dữ liệu không rõ trong tài liệu, chatbot nên trả lời như thế nào?
6. Khi không tìm thấy thông tin, chatbot cần nêu gì?
7. Nếu tài liệu chỉ nói “pending” hoặc “chưa xác nhận”, AI có được trả lời chắc chắn không?
8. Đoạn nào trong tài liệu xác nhận định nghĩa chính thức?

---

## 7. Bài tập cho mọi người

Hãy trả lời các câu hỏi dưới đây bằng suy nghĩ của bạn, sau đó so sánh với tài liệu demo:

### Câu hỏi 1

Một khách hàng có 2 cuộc gọi DNC, có phải là 2 khách hàng hay 1 khách hàng?

### Câu hỏi 2

Nếu trong tài liệu chỉ có “pending” thì AI có nên trả lời chắc chắn hay không?

### Câu hỏi 3

Tại sao cần có context và source ID khi hỏi AI?

### Câu hỏi 4

Nếu AI trả lời không có căn cứ, ta nên làm gì?

### Câu hỏi 5

RAG khác với LLM thuần ở điểm nào?

### Câu hỏi 6

Một chatbot doanh nghiệp tốt nên có những đặc tính gì?

### Câu hỏi 7

Khi dữ liệu không đủ, câu trả lời phù hợp nhất là gì?

### Câu hỏi 8

Nếu bạn là người xây dựng chatbot cho nội bộ, bạn sẽ lưu dữ liệu ở đâu và cho AI xem những gì?

---

## 8. Kết luận

LLM rất mạnh trong việc hiểu và tạo ngôn ngữ. Nhưng để xây dựng AI Chatbot thực tế, không thể chỉ dựa trên mô hình ngôn ngữ. Cần có:

- dữ liệu nguồn
- truy xuất thông tin
- ngữ cảnh rõ ràng
- kiểm chứng và xác nhận nguồn

RAG là giải pháp giúp AI chatbot trả lời dựa trên tài liệu thật, chứ không chỉ “nói theo cảm tính”.

Đây cũng là cách mà project Demo_DNC_Fixed đang minh họa: dùng tài liệu nội bộ làm nguồn, chọn đoạn liên quan, và cho LLM trả lời có căn cứ.

---

## 9. Gợi ý cho buổi thảo luận

Sau khi đọc tài liệu này, hãy đặt ra thêm nhiều câu hỏi liên quan đến:

- định nghĩa dữ liệu
- mâu thuẫn giữa tài liệu và thực tế
- độ tin cậy của nguồn
- cách AI nên phản hồi khi dữ liệu thiếu
- cách kiểm tra trước khi dùng thông tin cho quyết định chính thức

Mỗi câu hỏi đều là một cơ hội để hiểu rõ hơn về cách AI chatbot hoạt động và tại sao RAG lại quan trọng.
