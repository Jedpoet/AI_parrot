# parrot_ai.py


def get_parrot_response(user_text: dict) -> str:
    # 1. 取得 API Key (提示：可以用環境變數)
    # 2. 組裝 Prompt
    # 3. 呼叫 API
    # 4. 解析 JSON 回應

    return f"請將以下這句話改成用：{user_text["mood"]}的心情呈現：{user_text["input"]}"
