import argparse
from pathlib import Path
from ai_search_copilot_windows import ask_local_llm
from read_document import make_chunks, retrieve, build_prompt

parser = argparse.ArgumentParser()
parser.add_argument("--question")
args = parser.parse_args()

question = (args.question or input("Câu hỏi: ")).strip()
if not question:
    raise SystemExit()

try:
    path = Path(__file__).resolve().parent / "document_dnc_demo.txt"
    document = path.read_text(encoding="utf-8-sig")
    matches = retrieve(question, make_chunks(document))

    if not matches:
        print("Chưa tìm thấy thông tin phù hợp trong tài liệu.")
    else:
        prompt = build_prompt(question, matches, path.name)
        prompt += (
            "\n\nYÊU CẦU TRÌNH BÀY: "
            "Trả lời trực tiếp bằng đúng một câu ngắn trên một dòng. "
            "Giữ ID nguồn hỗ trợ câu trả lời. "
            "Không nhắc lại câu hỏi, không thêm tiêu đề. "
            "Không giải thích các mục không liên quan. "
            "Chỉ nêu thông tin còn thiếu nếu người dùng hỏi đến thông tin đó."
        )
        answer = ask_local_llm(prompt)
        print(" ".join(answer.split()))
except (OSError, ValueError, RuntimeError) as error:
    print("Lỗi:", error)
