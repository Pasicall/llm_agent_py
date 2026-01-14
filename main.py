from MCPClient import MCPClient
import asyncio
from ChatOpenAI import ChatOpenAI
import os
from Agent import Agent
from logTitle import logTitle
from EmbeddingRetriver import EmbeddingRetriver

current_dir = os.getcwd()
fetchMCP = MCPClient("fetch", command="uvx",args=['mcp-server-fetch'])
fileMCP = MCPClient("file", command='npx',args=['-y','@modelcontextprotocol/server-filesystem',current_dir])
emb_model = os.getenv("EMBEDDING_MODEL")

TASK = f"""
        告诉我 Chelsey Dietrich 的信息,先从我给你的文件中中找到相关信息,信息在 knowledge 目录下,总结后创作一个关于她的故事
        把故事和她的基本信息保存到{current_dir}/antonette.md,输出一个漂亮md文件
        """

async def main():
    context = await retriveContext()
    agent = Agent("deepseek-chat",[fetchMCP,fileMCP])
    await agent.init()
    logTitle("init Agent finish")
    #response = await agent.invoke('爬取 https://jsonplaceholder.typicode.com/users 的内容，在 ${currentDir}/knowledge 中，每个人创建一个md文件，保存基本信息')
    response = await agent.invoke('你是什么模型')
    return response

async def retriveContext():
    #RAG
    embeddingRetriver = EmbeddingRetriver(model = emb_model)
    knowledgeDir = os.path.join(current_dir,'knowledge')
    for file in os.listdir(knowledgeDir):
        with open(os.path.join(knowledgeDir,file),'r',encoding='utf-8') as f:
            text = f.read()
            await embeddingRetriver.embedDocument(text)
    
    context = await embeddingRetriver.retrive(TASK,3)
    return context

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        print(result)
    except KeyboardInterrupt:
        pass
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise

    

