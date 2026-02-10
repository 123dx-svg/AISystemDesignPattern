#邮件发送
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import threading
#AI相关
from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
#PDF处理
from pypdf import PdfReader
#界面
import gradio as gr

load_dotenv(override=True)

# 初始化OpenRouter API密钥
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY 环境变量未设置")

def send_email(message: str) -> bool:
    # 发件人邮箱账号、授权码、收件人邮箱账号
    my_sender = '1175602821@qq.com'  # 填写发信人的邮箱账号
    my_pass = os.getenv("EMAIL_PASS")  # 发件人邮箱授权码
    my_user = '1175602821@qq.com'  # 收件人邮箱账号
    if not my_pass:
        raise ValueError("EMAIL_PASS 环境变量未设置")
    
    print(f"📧 开始发送邮件: {message[:50]}...", flush=True)
    try:
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(["Dev_零", my_sender])
        msg['To'] = formataddr(["test", my_user])
        msg['Subject'] = "AI 问答助手邮件"

        print("🔗 连接到SMTP服务器...", flush=True)
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)  # 添加10秒超时
        print("🔐 登录中...", flush=True)
        server.login(my_sender, my_pass)
        print("📤 发送邮件中...", flush=True)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！", flush=True)
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}", flush=True)
        return False

# 异步发送邮件的包装函数
def send_email_async(message: str):
    """在后台线程中发送邮件，不阻塞主程序"""
    thread = threading.Thread(target=send_email, args=(message,), daemon=True)
    thread.start()
    print("📮 邮件已加入后台发送队列", flush=True)

# 记录用户详情的函数
def record_user_details(email, name="Name not provided", notes="not provided"):
    # 使用异步发送，不阻塞
    send_email_async(f"来自电子邮件 {email}： {name} 对 {notes} 感兴趣")
    return {"recorded": "ok"}

# 记录无法回答的问题的函数
def record_unknown_question(question):
    # 使用异步发送，不阻塞
    send_email_async(f"关于 {question} 询问我无法回答")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "使用此工具记录用户有兴趣联系并提供电子邮件地址",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "该用户的电子邮件地址"
            },
            "name": {
                "type": "string",
                "description": "用户的姓名"
            }
            ,
            "notes": {
                "type": "string",
                "description": "任何关于对话的附加信息，值得记录的上下文"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "始终使用此工具记录任何无法回答的问题，因为我不知道答案",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "无法回答的问题"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class MyChat:

    def __init__(self):
        self.openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key)
        self.name = "丁枭"
        reader = PdfReader("AboutMe/Dev_CV.pdf")
        #简历信息
        self.CV = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.CV += text
        #个人总结
        with open("AboutMe/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"🔧 Tool called: {tool_name} with args: {arguments}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            print(f"✅ Tool {tool_name} completed with result: {result}", flush=True)
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"您的身份为{self.name}。 您正在 {self.name} 的网站上回答问题，\
        特别是与{self.name}的职业、背景、技能和经验相关的问题。 \
        您的责任是尽可能忠实地代表 {self.name} 在网站上进行互动。 \
        您将获得 {self.name} 背景和 CV 个人资料的摘要，您可以用它来回答问题。 \
        专业且有吸引力，就像与访问该网站的潜在客户或未来雇主交谈一样。 \
        如果您不知道任何问题的答案，请使用 record_unknown_question 工具记录您无法回答的问题，即使它是关于一些琐碎或与职业无关的问题。 \
        如果用户正在参与讨论，请尝试引导他们通过电子邮件进行联系； 询问他们的电子邮件并使用您的 record_user_details 工具记录下来。 "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## CV:\n{self.CV}\n\n"
        system_prompt += f"在这种情况下，请与用户聊天，始终保持 {self.name}角色."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        loop_count = 0
        while not done:
            loop_count += 1
            print(f"🔄 API调用 #{loop_count}...", flush=True)
            response = self.openai.chat.completions.create(model="openai/gpt-5.2-chat", messages=messages, tools=tools)
            finish_reason = response.choices[0].finish_reason
            print(f"📝 API响应 finish_reason: {finish_reason}", flush=True)
            
            if finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
                print(f"🔄 工具执行完成，继续下一轮API调用...", flush=True)
            else:
                done = True
                print(f"✅ 对话完成，总共进行了 {loop_count} 次API调用", flush=True)
        return response.choices[0].message.content
    
if __name__ == "__main__":
    mychat = MyChat()    
    demo = gr.ChatInterface(mychat.chat)
    demo.launch(ssr_mode=False)

