#从一些导入开始 - rich 是一个用于在终端中进行格式化文本输出的库
import os
from rich.console import Console
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv(override=True)

def show(text):
    try:
        Console().print(text)
    except Exception:
        print(text)

openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))


todos = []
completed = []

def get_todo_report() -> str:
    result = ""
    for index, todo in enumerate(todos):
        if completed[index]:
            result += f"Todo #{index + 1}: [green][strike]{todo}[/strike][/green]\n"
        else:
            result += f"Todo #{index + 1}: {todo}\n"
    show(result)
    return result

def create_todos(descriptions: list[str]) -> str:
    todos.extend(descriptions)
    completed.extend([False] * len(descriptions))
    return get_todo_report()

def mark_complete(index: int, completion_notes: str) -> str:
    if 1 <= index <= len(todos):
        completed[index - 1] = True
    else:
        return "No todo at this index."
    Console().print(completion_notes)
    return get_todo_report()

create_todos_json = {
    "name": "create_todos",
    "description": "从描述列表中添加新的待办事项并返回完整列表",
    "parameters": {
        "type": "object",
        "properties": {
            "descriptions": {
                'type': 'array',
                'items': {'type': 'string'},
                'title': 'Descriptions'
                }
            },
        "required": ["descriptions"],
        "additionalProperties": False
    }
}

mark_complete_json = {
    "name": "mark_complete",
    "description": "标记完成给定位置的待办事项（从 1 开始）并返回完整列表",
    "parameters": {
        'properties': {
            'index': {
                'description': '标记为完成的待办事项的从1开始的索引',
                'title': 'Index',
                'type': 'integer'
                },
            'completion_notes': {
                'description': '有关如何在控制台中完成待办事项的注释',
                'title': 'Completion Notes',
                'type': 'string'
                }
            },
        'required': ['index', 'completion_notes'],
        'type': 'object',
        'additionalProperties': False
    }
}

tools = [{"type": "function", "function": create_todos_json},
        {"type": "function", "function": mark_complete_json}]

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        #此处中文乱码
        results.append({"role": "tool","content": json.dumps(result,ensure_ascii=False),"tool_call_id": tool_call.id})
    return results

def loop(messages):
    done = False
    while not done:
        response = openai.chat.completions.create(model="gpt-5.2", messages=messages, tools=tools, reasoning_effort="none")
        finish_reason = response.choices[0].finish_reason
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    show(response.choices[0].message.content)


system_message = """
您需要解决一个问题，方法是使用待办事项工具规划一系列步骤，然后依次执行每个步骤。 
现在使用待办事项列表工具，创建计划，执行步骤，并回复解决方案。 
如果问题中未提供任何数量，请包括一个得出合理估计的步骤。 
以丰富的控制台标记提供您的解决方案，无需代码块。 
请勿询问用户问题或进行澄清； 仅在使用您的工具后回复答案。
"""
user_message = """"
一列火车于下午 2:00 从波士顿出发，时速 60 英里。 
另一辆火车于下午 3:00 从纽约出发，以 80 英里/小时的速度开往波士顿。 
他们什么时候见面？
"""
messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]


todos, completed = [], []

loop(messages)