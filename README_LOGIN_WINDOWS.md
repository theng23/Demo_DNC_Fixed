# Copilot API: phần LLM tự động, tùy chọn

Đọc BAT_DAU.md trước. Mặc định script dùng Python cho retrieval/augmentation và chuyển prompt thủ công sang Copilot web cho generation.

Sau khi IT cấp app registration riêng, license và quyền phù hợp:

```powershell
python -m pip install -r requirements_windows.txt
python .\ai_search_copilot_windows.py --question "DNC_CALLS khác DNC_CUSTOMERS thế nào?" --copilot
```

Nguồn được lấy từ TXT trên máy, gửi tối đa hai đoạn bằng additionalContext cho Chat API; không đọc URL SharePoint. Dù nguồn local, API vẫn yêu cầu app và quyền Microsoft Graph phù hợp.

App cần Mobile and desktop applications, redirect URI http://localhost, cùng đủ delegated permissions/consent: Sites.Read.All, Mail.Read, People.Read.All, OnlineMeetingTranscript.Read.All, Chat.Read, ChannelMessage.Read.All, ExternalItem.Read.All. Tài khoản cần license Copilot phù hợp. Client ID Azure CLI từng gặp AADSTS65002 không dùng cho luồng này; code sẽ dừng và giải thích.

Đăng nhập qua trình duyệt, MFA theo chính sách công ty. MSAL thử cache trước; nếu có nhiều tài khoản thì mở chọn tài khoản. Token cache lưu qua MSAL Extensions bằng Windows DPAPI tại %LOCALAPPDATA%\DNC-Copilot-Demo\<ma-app-tenant>.bin. Code không thu thập/lưu mật khẩu Microsoft, không fallback sang token dạng rõ. Phiên bị thu hồi hoặc chính sách thay đổi vẫn có thể cần đăng nhập lại.

API còn preview. Tắt web không khóa toàn bộ enterprise grounding vào nguồn local. Prompt yêu cầu chỉ dùng các đoạn đã cấp nhưng vẫn cần kiểm tra nội dung. ID [S...] do Python gán; context local có thể không có citation URL từ API. Mỗi lần chạy tạo conversation mới. Test auth/API dùng mock, chưa xác minh DPAPI/MFA/LLM thật trên tenant công ty.

Tham khảo:
https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api/ai-services/chat/copilotconversation-chat
https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api/ai-services/chat/copilotroot-post-conversations
https://learn.microsoft.com/en-us/entra/msal/python/getting-started/acquiring-tokens
https://github.com/AzureAD/microsoft-authentication-extensions-for-python
