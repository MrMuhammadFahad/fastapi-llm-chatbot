from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Config

MODEL_NAME = "Qwen/Qwen2-1.5B-Instruct"

# Load model & tokenizer

def load_model_and_tokenizer(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16
    )
    return tokenizer, model


tokenizer, model = load_model_and_tokenizer(MODEL_NAME)

# App init

app = FastAPI()

# Memory (chat history)

def init_messages():
    return [{"role": "system", "content": "You are a helpful assistant."}]


messages = init_messages()

# Request schema

class PromptRequest(BaseModel):
    prompt: str

# Core logic functions

def add_user_message(messages, prompt):
    messages.append({"role": "user", "content": prompt})
    return messages


def build_model_input(messages, tokenizer):
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    return inputs


def generate_response(inputs, model):
    output_ids = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True
    )
    return output_ids


def decode_response(output_ids, tokenizer):
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


def extract_assistant_reply(full_response: str):
    return full_response.split("assistant")[-1].strip()


def add_assistant_message(messages, reply):
    messages.append({"role": "assistant", "content": reply})
    return messages

# API endpoint

@app.post("/generate")
def generate(req: PromptRequest):
    global messages

    messages = add_user_message(messages, req.prompt)

    inputs = build_model_input(messages, tokenizer)

    output_ids = generate_response(inputs, model)

    full_response = decode_response(output_ids, tokenizer)

    assistant_reply = extract_assistant_reply(full_response)

    messages = add_assistant_message(messages, assistant_reply)

    return {"response": assistant_reply}