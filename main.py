# main.py
import asyncio
from ChatOpenAI import ChatOpenAI
import os
# os.environ['HTTP_PROXY']="http://172.22.112.1:7890"
# os.environ['HTTPS_PROXY']="http://172.22.112.1:7890"



async def main():
    llm = ChatOpenAI("deepseek-chat", system_prompt="你是一个帮助测试的助手")
    prompt = "你好，请简单介绍一下你自己。"

    try:
        res = await llm.chat(prompt)
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
