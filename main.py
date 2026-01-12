from MCPClient import MCPClient
import asyncio
from ChatOpenAI import ChatOpenAI
import os
from Agent import Agent
from logTitle import logTitle

current_dir = os.getcwd()
fetchMCP = MCPClient("fetch", command="uvx",args=['mcp-server-fetch'])
fileMCP = MCPClient("file", command='npx',args=['-y','@modelcontextprotocol/server-filesystem',current_dir])

async def main():
    agent = Agent("deepseek-chat",[fetchMCP,fileMCP])
    await agent.init()
    logTitle("init Agent finish")
    response = await agent.invoke('爬取 https://news.ycombinator.com/ 的内容，并且总结保存到${currentDir}的news.md文件中')
    return response

if __name__ == "__main__":
    result= asyncio.run(main())
    print(result)
