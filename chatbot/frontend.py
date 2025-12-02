from agents_config import triageAgent, dataRetrievalAgent, actionAgent
from agents import Runner
from agents.mcp import MCPServerStdio 
import streamlit as st
import os
import time
import asyncio, json
import logging
from logging import getLogger

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if "history" not in st.session_state:
    st.session_state.history = []

for message in st.session_state.history:
    type = message.get("role", None) or message.get("type", None)

    match type:
        case 'user': 
            with st.chat_message(type):
                st.markdown(message["content"])
        case 'assistant': 
            with st.chat_message(type):
                content_item = message["content"][0]

                if isinstance(content_item, dict) and "text" in content_item:
                    st.markdown(content_item["text"])
        case 'function_call': 
            if "transfer_to" not in message["name"]: 
                with st.chat_message(name="tool", avatar=":material/build:"):
                        st.markdown(f'LLM chamando tool {message["name"]}')
                        with st.expander("Visualizar argumentos"):
                            st.code(message["arguments"])
        case 'function_call_output':
            try:
                obj = json.loads(message['output'])
                with st.chat_message(name="tool", avatar=":material/data_object:"):
                    with st.expander("Visualizar resposta"):
                        st.code(obj["text"])
            except:
                continue

if "triageAgent" not in st.session_state:
    logger.info("loading triageAgent into session state")
    st.session_state.triageAgent = triageAgent 
    st.session_state.currentAgent = triageAgent

if "dataRetrievalAgent" not in st.session_state:
    logger.info("loading dataRetrievalAgent into session state")
    st.session_state.dataRetrievalAgent = dataRetrievalAgent

if "actionAgent" not in st.session_state:
    logger.info("loading actionAgent into session state")
    st.session_state.actionAgent = actionAgent

async def start_mcp():
    logger.info("starting MCP server and running agent")
    env = os.environ.copy()
    async with MCPServerStdio(params={
        "command": "mcp", 
        "args": ["run", "chatbot/server_mcp.py"], 
        "env": env
    }) as server:
        st.session_state.dataRetrievalAgent.mcp_servers = [server] 
        st.session_state.actionAgent.mcp_servers = [server] 

        result = await Runner.run(
            starting_agent=st.session_state.currentAgent, 
            input=st.session_state.history, 
            context=st.session_state.history
        )
       
        st.session_state.currentAgent = result.last_agent
        st.session_state.history = result.to_input_list()

prompt = st.chat_input("Digite sua pergunta:")

if prompt:
    # Exibe a mensagem do usuário na interface do chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Adiciona a mensagem do usuário ao histórico
    st.session_state.history.append({
        "role": "user", 
        "content": prompt
    })

    with st.spinner("Pensando..."):
        asyncio.run(start_mcp())
        st.rerun()

if "currentAgent" in st.session_state: 
    logger.info(f"Current agent: { st.session_state.currentAgent.name }")
