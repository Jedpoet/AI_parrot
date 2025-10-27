# parrot_ai.py
import os
import google.generativeai as genai
import logging

# 停用 google-auth 的囉嗦日誌，讓輸出乾淨一點
logging.getLogger('google.auth').setLevel(logging.ERROR)


def get_parrot_response(user_text: dict) -> str:
    
    # 1. 取得 API Key (提示：可以用環境變數)
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "錯誤：找不到 'GEMINI_API_KEY' 環境變數。AI 鸚鵡無法啟動。"
        
        genai.configure(api_key=api_key)
    
    except Exception as e:
        return f"API Key 設定錯誤: {e}"

    # 2. 組裝 Prompt
    user_input = user_text["input"]
    mood = user_text["mood"] # 把 mood 先取出來
    
    # *** 【【【 這就是修改的關鍵！ 】】】 ***
    # 我們不再叫它「複述」，而是叫它「表演」
    prompt = f"""
    你是一個非常情緒化、很愛演的 AI 戲精。
    請你用「{mood}」的心情，對以下這句話所描述的「情境」，做出「極度誇張且戲劇化」的回應：
    
    「{user_input}」
    
    你的回應格式必須像舞台劇劇本一樣，包含：
    1.  用「（）」括號起來的動作、表情或情境描述。
    2.  充滿該情緒的台詞。

    範例（如果心情是 angry，原話是「撿到錢」）：
    （氣憤地跺腳，聲音大到幾乎是用吼的）「什麼『撿到錢』？！這種爛事怎麼会發生在我身上？！爛透了！」

    請注意：請「只回傳」你扮演的內容，不要包含任何額外的招呼語或解釋。
    """

    try:
        # 3. 呼叫 API
        
        # (使用你測試成功的模型名稱, 例如 'gemini-2.5-flash')
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        response = model.generate_content(prompt, safety_settings=safety_settings)

        # 4. 解析 JSON 回應
        
        # 檢查是否有回應內容
        if response.parts:
            ai_text = response.text.strip()
            # 在成功的回應前加上 (心情: xxx)
            return f"(心情: {mood}) {ai_text}"
        else:
            # AI 因安全設定等原因拒絕回答 (無法轉換)
            # 在回傳原話前，也加上 (心情: xxx)
            return f"(心情: {mood}) {user_input} (AI拒絕表演)"

    except Exception as e:
        # 處理 API 呼叫過程中可能發生的任何錯誤
        print(f"[AI 鸚鵡 API 呼叫失敗: {e}]")
        # 在回傳原話前，也加上 (心情: xxx)
        return f"(心情: {mood}) {user_input} (API呼叫失敗)"
