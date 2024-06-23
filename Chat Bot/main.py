import json #read jason file
from difflib import get_close_matches #best match question
import tkinter as tk
from tkinter import scrolledtext, messagebox

def load_knowledge_base(file_path: str) -> dict: #ta5od el data eli fe el jason hat2raha w b3den trg3ha lldata
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict): #34an lw aflt el brnamg w get fat7to tani yb2a 3amel save llegabat abl kda fe el jason bta3y ma3od4 ad5l m3loma m3loma lawl mara
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2) # el egaba eli hat2olha ayn kant heya ehh hat2raha w hatd5lha gwa el jason file bta3y

def find_best_match(user_question: str, questions: list[str]) -> str | None: # zy get close match fo2 kda yama hatrg3 string mn file jason ya m4 hatrg3 haga 5als
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) # el so2al eli el user bys2alo bt1arno bba2y el as2la eli fo2 kda 3ndy  cutoff 0.6 nsbt el t4abhoh 3ndy fe eo s2al
    return matches[0] if matches else None # el e5tyarat el mwgoda 3ndi heya index zero none lw ma3nde4 so2al nsbt t4abog 0.6 hay2olo 3lmni el egabt el so2al dah

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None: # ha5od ahsan egabat mt5zna fe file jason yama hyrg3 string yama hyrg3 none
    for q in knowledge_base["questions"]: # hloop fe el jason ha4of ahsan so2l mwgod bsy8t el jason ba3d ma tegb el so2al rg3ly ahsan egaba mwgoda 3ndk
        if q["question"] == question:
            return q["answer"]

def submit_question():
    user_input = entry.get() #had5lo el so2al w hafdl ad5l fe as2la
    if user_input.lower() == 'quit': #lw katbtlo quit hay3ml zy break kda haytl3 mn el infinty loop eli hoa feha yo3tbr w ha5rog mn el brnamg
        root.quit()
        return

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]]) #ha3ml loop w ageb ahsan egaba mwgoda 3ndi llso2al dag ahsan sy8a hytl3ly egabto

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base) #hy5o4 hna ygeb best match fe el knowlage based
        chat_log.insert(tk.END, f"You: {user_input}\n")#If best_match is found: The bot retrieves the answer from the knowledge base and updates the chat log with the user’s input and the bot’s response.
        chat_log.insert(tk.END, f"Bot: {answer}\n\n")
    else:
        chat_log.insert(tk.END, f"You: {user_input}\n") #If best_match is not found: The bot updates the chat log to indicate it doesn’t know the answer and prompts the user with a message box to teach the bot the correct answer.
        chat_log.insert(tk.END, "Bot: I don't know the answer, can you teach me?\n\n")
        messagebox.showinfo("Teach Bot", "I don't know the answer. Please provide the answer or skip.")

def teach_answer():
    user_input = entry.get() #haytlop mni el input
    new_answer = answer_entry.get() #had5lo el egaba
    if new_answer.lower() != "skip": #lw m4 skip
        knowledge_base["questions"].append({"question": user_input, "answer": new_answer}) #hayd5lha fe el jasoon
        save_knowledge_base("knowledge_base.json", knowledge_base) #w hy3mlha save fe el knowlage based
        chat_log.insert(tk.END, f"Bot: Thank you! I have learned a new response.\n\n")
    else:
        chat_log.insert(tk.END, "Bot: Skipped learning new response.\n\n") #lw la fe el chatbot hy3li skipp mn el so2al
    answer_entry.delete(0, tk.END)

knowledge_base = load_knowledge_base('knowledge_base.json')

root = tk.Tk() # export llmktaba
root.title("Chat Bot") #title
root.geometry("500x400") #msa7t el app length width 100+100 center of program on pc
root.configure(bg="#001f3f")#color of program

chat_frame = tk.Frame(root, bg="#001f3f") #frame for systen
chat_frame.pack(pady=10) #padd 10 pixels vertically

chat_log = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=15, bg="#003366", fg="white") #wrap=tk.WORD,ensures text wraps at word boundaries.
chat_log.pack() # ScrolledText widget

entry_frame = tk.Frame(root, bg="#001f3f")
entry_frame.pack(pady=5)

entry_label = tk.Label(entry_frame, text="You: ", bg="#001f3f", fg="white") #bg back ground color
entry_label.grid(row=0, column=0, padx=5) #padx=5 adds horizontal padding between grid cells.

entry = tk.Entry(entry_frame, width=40, bg="#00509e", fg="white") #fg text color
entry.grid(row=0, column=1, padx=5)

submit_button = tk.Button(entry_frame, text="Submit", command=submit_question, bg="#0074d9", fg="white") # function submit mn fo2
submit_button.grid(row=0, column=2, padx=5)

answer_label = tk.Label(entry_frame, text="Answer: ", bg="#001f3f", fg="white")
answer_label.grid(row=1, column=0, padx=5)

answer_entry = tk.Entry(entry_frame, width=40, bg="#00509e", fg="white")
answer_entry.grid(row=1, column=1, padx=5)

teach_button = tk.Button(entry_frame, text="Teach", command=teach_answer, bg="#0074d9", fg="white") # function teach answer mn fo2
teach_button.grid(row=1, column=2, padx=5)

root.mainloop()
