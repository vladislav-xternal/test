import requests
import customtkinter as ctk
from tkinter import messagebox
import webbrowser

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Text Generation")
root.geometry("800x600")

def generate_text():
    text = entry.get()
    auth_key = entry_auth.get()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    if not auth_key:
        messagebox.showwarning("Warning", "Please enter your authorization key.")
        return

    headers = {
        'Authorization': f'Bearer {auth_key}'
    }
    url = "https://api.edenai.run/v2/text/generation"
    payload = {
        "providers": "openai,cohere",
        "text": text,
        "temperature": 0.2
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        if 'openai' in result and 'generated_text' in result['openai']:
            generated_text = result['openai']['generated_text']
            label_result.delete(1.0, ctk.END)
            label_result.insert(ctk.END, generated_text)
        else:
            messagebox.showerror("Error", "Generated text not found in response.")
            label_result.delete(1.0, ctk.END)

    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
        label_result.delete(1.0, ctk.END)
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
        label_result.delete(1.0, ctk.END)

def open_url():
    url = "https://app.edenai.run/bricks/catalog/"
    webbrowser.open(url)

frame_input = ctk.CTkFrame(root, width=380, height=500)
frame_input.pack(side=ctk.LEFT, padx=20, pady=20, fill='both')

label = ctk.CTkLabel(frame_input, text="Enter Text:")
label.pack(pady=10)

entry = ctk.CTkEntry(frame_input, width=300)
entry.pack(pady=10)

button = ctk.CTkButton(frame_input, text="Generate Text", command=generate_text)
button.pack(pady=20)

label_result_title = ctk.CTkLabel(frame_input, text="Generated Text:")
label_result_title.pack(pady=10)

label_result = ctk.CTkTextbox(frame_input, width=500, height=350, wrap='word')
label_result.pack(pady=10)

frame_auth = ctk.CTkFrame(root, width=380, height=500)
frame_auth.pack(side=ctk.RIGHT, padx=20, pady=20, fill='both')

label_auth = ctk.CTkLabel(frame_auth, text="Enter Authorization Key:", width=300)
label_auth.pack(pady=10)

entry_auth = ctk.CTkEntry(frame_auth, width=300, show="*")
entry_auth.pack(pady=10)

button_open_url = ctk.CTkButton(frame_auth, text="Get Authorization Key", command=open_url)
button_open_url.pack(pady=10)

root.mainloop()
