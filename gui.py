import customtkinter as ctk
from PIL import Image
import threading  # <-- NEW: Allows us to run tasks in the background
import action 
import spech_to_text 
import routine

# --- Modern Theme Setup ---
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue")  

def User_send(event=None): 
    send = entry1.get()
    if not send.strip(): return  
    
    text.configure(state="normal")
    text.insert("end", "Me --> " + send + "\n")
    entry1.delete(0, "end")  
    
    bot = action.Action(send)
    if bot != None:
        text.insert("end", "Bot <-- " + str(bot) + "\n\n")
    
    text.configure(state="disabled")
    text.see("end") 
    
    if bot == "ok sir":
        root.destroy()          

# --- NEW: Background Thread Function ---
def process_voice_thread():
    # 1. Listen to the microphone (This no longer freezes the UI!)
    ask_val = spech_to_text.spech_to_text()
    
    # 2. If it heard something, update the chat
    if ask_val:
        text.configure(state="normal")
        text.insert("end", "Me --> " + ask_val + "\n") 
        
        bot_val = action.Action(ask_val)
        if bot_val != None:
           text.insert("end", "Bot <-- " + str(bot_val) + "\n\n")
           
        text.configure(state="disabled")
        text.see("end") 
        
        if bot_val == "ok sir":
            # Wait 1 second before destroying so user can read the goodbye
            root.after(1000, root.destroy) 
            return # Exit early so we don't try to configure a destroyed button
            
    # 3. Reset the button back to its original green state
    ask_btn.configure(
        text="🎤 Ask", 
        fg_color="#10B981", 
        text_color="white", 
        state="normal"
    )

# --- UPDATED: The Click Action ---
def ask():
    # 1. Instantly change button to visually indicate listening
    ask_btn.configure(
        text="🎤 Listening...", 
        fg_color="white",        # White background
        text_color="#10B981",    # Green text/icon
        state="disabled"         # Prevent double-clicking
    )
    
    # 2. Start the microphone on a separate background thread
    # daemon=True ensures the thread dies safely if you close the app early
    threading.Thread(target=process_voice_thread, daemon=True).start()

def clear_text():
    text.configure(state="normal")
    text.delete("1.0", "end")
    text.configure(state="disabled")

# --- Window Setup ---
root = ctk.CTk()
root.geometry("550x700")
root.title("Desktop Assistant")
root.resizable(False, False)

# --- 1. Header Section ---
header_frame = ctk.CTkFrame(root, fg_color="transparent")
header_frame.pack(pady=(25, 15))

try:
    img_data = Image.open("image/assitant.png")
    ctk_image = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(65, 65))
    image_label = ctk.CTkLabel(header_frame, image=ctk_image, text="")
    image_label.pack(side="left", padx=10)
except Exception as e:
    print("Image not found. Ensure 'image/assitant.png' exists.")

title_label = ctk.CTkLabel(header_frame, text="Desktop Assistant", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
title_label.pack(side="left", padx=10)

# --- 2. Chat Window ---
text = ctk.CTkTextbox(root, width=480, height=420, font=ctk.CTkFont(family="Segoe UI", size=14), corner_radius=15, border_width=2, border_color="#E5E7EB", fg_color="#F9FAFB")
text.pack(pady=10, padx=30, fill="both", expand=True)
text.configure(state="disabled")

# --- 3. Input Area ---
entry_frame = ctk.CTkFrame(root, fg_color="transparent")
entry_frame.pack(pady=10, padx=30, fill="x")

entry1 = ctk.CTkEntry(entry_frame, height=45, font=ctk.CTkFont(family="Segoe UI", size=14), corner_radius=20, placeholder_text="Type a message...", border_width=2, border_color="#E5E7EB")
entry1.pack(side="left", fill="x", expand=True, padx=(0, 10))

send_btn = ctk.CTkButton(entry_frame, text="Send", width=80, height=45, corner_radius=20, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), command=User_send)
send_btn.pack(side="right")

# --- 4. Bottom Action Buttons ---
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=(10, 25))

# The default button state is set here
ask_btn = ctk.CTkButton(btn_frame, text="🎤 Ask", width=120, height=45, corner_radius=20, fg_color="#10B981", text_color="white", hover_color="#059669", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), command=ask)
ask_btn.grid(row=0, column=0, padx=15)

clear_btn = ctk.CTkButton(btn_frame, text="Clear", width=120, height=45, corner_radius=20, fg_color="#EF4444", hover_color="#DC2626", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), command=clear_text)
clear_btn.grid(row=0, column=1, padx=15)

root.bind('<Return>', User_send)

# NEW: Start the background heartbeat before launching the UI
routine.run_in_background()

root.mainloop()