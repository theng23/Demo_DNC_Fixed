import argparse
import re
from pathlib import Path
from ai_search_copilot_windows import ask_local_llm
from read_document import make_chunks, retrieve, build_prompt

parser = argparse.ArgumentParser()
parser.add_argument("--question")
args = parser.parse_args()

path = Path(__file__).resolve().parent / "document_dnc_demo.txt"

while True:
    try:
        question = (args.question or input("\nCâu hỏi: ")).strip()
        args.question = None
    except (KeyboardInterrupt, EOFError):
        break

    if question.casefold() in {"thoát", "thoat", "exit", "quit"}:
        break
    if not question:
        continue

    try:
        document = path.read_text(encoding="utf-8-sig")
        matches = retrieve(question, make_chunks(document))

        if not matches:
            print("Chưa tìm thấy thông tin phù hợp trong tài liệu.")
            continue

        prompt = build_prompt(question, matches, path.name)
        prompt += (
            "\n\nHẾT NGUỒN.\n"
            "YÊU CẦU TRÌNH BÀY: Trả lời trực tiếp bằng tiếng Việt. "
            "Nếu hỏi nhiều khách hàng, mỗi khách hàng một dòng riêng, "
            "bắt đầu bằng ID nguồn và mã khách hàng. "
            "Không gộp nhiều khách hàng vào cùng một dòng. "
            "Không nhắc lại câu hỏi, không thêm tiêu đề. "
            "Chỉ trình bày thông tin liên quan đến yêu cầu."
        )

        answer = ask_local_llm(prompt).strip()

        # Tách thêm khi model vẫn gộp các khách hàng trên một dòng.
        answer = re.sub(
            r"[ \t]+(?=\[S\d+\]\s*KH\d+\b)",
            "\n",
            answer,
        )
        print(answer)

    except (OSError, ValueError, RuntimeError) as error:
        print("Lỗi:", error)
