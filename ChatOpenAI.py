from openai import OpenAI
import dotenv
import os
from logTitle import logTitle

dotenv.load_dotenv()

class ChatOpenAI():
    def __init__(self,model_name : str , tools = [] , system_prompt : str = "",context: str = ""):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL")
        self.model = model_name
        self.tools = tools
        self.system_prompt = system_prompt
        self.context = context
        self.llm = OpenAI(api_key=api_key,base_url=base_url)
        self.message = []

    async def chat(self,prompt = None):
        logTitle(f"Chat")
        if(prompt):
            self.message.append({"role":"user", "content":prompt})

        stream = self.llm.chat.completions.create(
            model=self.model,
            messages=self.message,
            tools=self.getToolsDefinition(),
            stream=True
        )

        content = ""
        toolCalls = []

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                contentChunk = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
                content += contentChunk
            if delta.tool_calls:
                for toolCallChunk in delta.tool_calls:
                    #第一次收到toolCall
                    if(len(toolCalls) <= toolCallChunk.index):
                        toolCalls.append({id:"",function:{"name":"", "arguments": ""}})
                    currentCall = toolCalls[toolCallChunk.index]

                    if(toolCallChunk.id):
                        currentCall["id"] += toolCallChunk.id
                    if(toolCallChunk.function.name):
                        currentCall["function"]["name"] += toolCallChunk.function.name
                    if(toolCallChunk.function.arguments):
                        currentCall["function"]["arguments"] += toolCallChunk.function.arguments
                    
        self.message.append({
            "role": "assistant",
            "content": content,
            "tool_calls":[{"id": call["id"], "type":"function","function":call["function"]} for call in toolCalls] if toolCalls else None
        })

        return{
            "content": content,
            "toolCalls": toolCalls
        }
    def appendToolResult(self,toolCallId: str, toolOutput: str):
        self.message.append({
            "role": "tool",
            "content":toolOutput,
            "tool_call_id": toolCallId
        })

    def getToolsDefinition(self):
        return[
            {
                "type": "function",
                "function":{
                    "name": tool['name'],
                    "description": tool['description'],
                    "parameters": tool['inputSchema']
                }
            }for tool in self.tools
        ]

if __name__ == '__main__':
    prompt = "你是谁"
    llm = ChatOpenAI("deepseek-chat")
    res = llm.chat(prompt=prompt)
    print(res)
