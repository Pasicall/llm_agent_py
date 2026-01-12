from logTitle import logTitle
from ChatOpenAI import ChatOpenAI
import json

class Agent():
    def __init__(self,model, mcpClients, sysprompt="", context="") -> None:
        self.mcpClients = mcpClients
        self.model = model
        self.sys_prompt = sysprompt
        self.context = context
        self.llm = None
    
    async def init(self):
        logTitle('TOOLS')
        for mcp in self.mcpClients:
            await mcp.init()

        #收集所有tools
        all_tools = []
        for client in self.mcpClients:
            all_tools.extend(client.get_tools())

        self.llm = ChatOpenAI(self.model, system_prompt = self.sys_prompt, tools=all_tools, context=self.context)

    async def close(self):
        for mcp in self.mcpClients:
            try:
                await mcp.close()
            except Exception as e:
                print(f"Warning: Error closing MCP client:{e}")

    #实现任务循环调度
    async def invoke(self,prompt: str):
        if not self.llm:
            raise Exception('Agent not initialized')
        
        response = await self.llm.chat(prompt=prompt)
        while True:
            if (len(response['toolCalls'])>0):
                for tool_call in response['toolCalls']:
                    #查找处理该工具的MCP客户端
                    mcp = next(
                        (client for client in self.mcpClients if any(
                            t['name'] == tool_call['function']['name'] for t in client.get_tools()
                        )),
                        None
                    )

                    if mcp :
                        logTitle("TOOL USE")
                        print(f"Calling tool: {tool_call['function']['name']}")
                        print(f"Arguments: {tool_call['function']['arguments']}")


                        result = await mcp.call_tools(
                            tool_call['function']['name'],
                            json.loads(tool_call['function']['arguments'])
    
                        )

                        #数据清洗
                        result_str = ""
                        if hasattr(result,'content') and result.content:
                            result_dict = {
                                "content": result.content[0].text if result.content else "",
                                "isError": getattr(result,'ifError',False)
                            }
                            result_str = json.dumps(result_dict)
                        else:
                            result_str = str(result)

                        print(f"Result: {result_str}")
                        self.llm.appendToolResult(tool_call['id'],result_str)
                    else:
                        self.llm.appendToolResult(tool_call['id'],'Tool not found')

                response = await self.llm.chat()
                continue

            await self.close()
            return response['content']                        

    