import customtkinter as ctk
import ollama
from llm_axe import OnlineAgent, OllamaChat

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

    # Show user input
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

send_btn = ctk.CTkButton(app, text="Send", command=send_message)
send_btn.pack(padx=10, pady=(0, 20))

entry.bind("<Return>", lambda e: send_message())

app.mainloop()
