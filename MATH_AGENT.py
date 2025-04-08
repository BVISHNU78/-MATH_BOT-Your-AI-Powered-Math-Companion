import customtkinter as ctk
import ollama
from llm_axe import OnlineAgent, OllamaChat
from customtkinter import CTkInputDialog
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x600")
app.title("🤖 MATH_BOT")

model_name = "mistral:latest"
llm = OllamaChat(model=model_name)
online_agent = OnlineAgent(llm=llm)

messages = [
    {"role": "system", "content": "hello what can I do?"},
    {"role": "user", "content": "hello my name is MATH_BOT"}
]

response = ollama.chat(model=model_name, messages=messages)
bot_reply = response["message"]["content"]
messages.append({"role": "assistant", "content": bot_reply})

frame = ctk.CTkFrame(master=app)
frame.pack(padx=10, pady=10, fill="both", expand=True)

chatbox = ctk.CTkTextbox(frame, wrap="word", font=("Arial", 14))
chatbox.pack(padx=10, pady=10, fill="both", expand=True)
chatbox.insert("end", f"🤖 MATH_BOT: {bot_reply}\n")
chatbox.configure(state="disabled")

entry = ctk.CTkEntry(app, placeholder_text="Type your message...")
entry.pack(padx=10, pady=(0, 10), fill="x")

def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    chatbox.configure(state="normal")
    chatbox.insert("end", f"🧑 You: {user_input}\n")
    chatbox.see("end")
    entry.delete(0, "end")
    messages.append({"role": "user", "content": user_input})

    if "search" in user_input.lower():
        query = f"Find reliable information about {user_input} from trusted sources."
        search_result = online_agent.search(query)
        summary_prompt = f"Summarize this search result in simple words: {search_result}"
        response = ollama.chat(model=model_name, messages=[{"role": "user", "content": summary_prompt}])
        bot_reply = response['message']['content']
        chatbox.insert("end", f"🔎 MATH_BOT: {bot_reply}\n")
    else:
        response = ollama.chat(model=model_name, messages=messages)
        bot_reply = response["message"]["content"]
        chatbox.insert("end", f"🤖 MATH_BOT: {bot_reply}\n")
        messages.append({"role": "assistant", "content": bot_reply})

    chatbox.configure(state="disabled")
    chatbox.see("end")

def generate_story():
    input_dialog = CTkInputDialog(text="Enter a title or prompt for the math story:", title="📘 Math Story Prompt")
    user_prompt = input_dialog.get_input()

    if not user_prompt:
        return  

    math_texts = [msg["content"] for msg in messages if msg["role"] in ["user", "assistant"]]
    combined = "\n".join(math_texts)

    story_prompt = (
        f"Using this conversation filled with math questions and answers:\n\n{combined}\n\n"
        f"Create a short, fun story based on this. Instruction: {user_prompt}"
    )

    story_response = ollama.chat(model=model_name, messages=[{"role": "user", "content": story_prompt}])
    story = story_response["message"]["content"]


    chatbox.configure(state="normal")
    chatbox.insert("end", f"📘 MATH_BOT (Story Mode):\n{story}\n\n")
    chatbox.configure(state="disabled")
    chatbox.see("end")


send_btn = ctk.CTkButton(app, text="Send", command=send_message)
send_btn.pack(padx=10, pady=(0, 10))

story_btn = ctk.CTkButton(app, text="📘 Generate Story", command=generate_story)
story_btn.pack(padx=10, pady=(0, 20))

entry.bind("<Return>", lambda e: send_message())

app.mainloop()
