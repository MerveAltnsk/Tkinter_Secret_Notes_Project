from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import base64

#apply cryptography with vigenere ciphher

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt_notes():
    title = input_title_entry.get()
    message = input_text.get("1.0", END)
    master_secret = key_entry.get()

    if len(message) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error", message="Please fill all fields")
    else:
        # Encryption
        message_encrypted = encode(master_secret, message)

        try:
            with open("MySecret.txt", "a") as data_file:        # dosyayı a append modunda açıyoruz ki w write olsaydı 1 tane açılabilirdi append de üstüne devamlı açabiliyoruz
                data_file.write(f"\n{title} \n {message_encrypted}")
        except FileNotFoundError:
            with open("MySecret.txt", "w") as data_file:        # ilk defa çalıştırılacağı w yazabiliriz içi boş olduğu için ne yazdıysak o yazılacak sonra dosyayı bulduğunda üsteki çalışacak append ile devamm edip yazılacak
                data_file.write(f"\n{title} \n {message_encrypted}")
        finally:
            input_title_entry.delete(0, END)
            input_text.delete("1.0", END)
            key_entry.delete(0, END)

# Decrypt notes
def decrypt_notes():
    message_encrypted = input_text.get("1.0", END)
    master_secret = key_entry.get()

    if len(message_encrypted) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            input_text.delete("1.0", END)
            input_text.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please make sure of encrypted info.")

FONT = ("Verdana", 16, "normal")
window = Tk()
window.title("Secret Notes")
window.config(padx=100, pady=100)

# UI

#photo = PhotoImage(file = "image4.png")
#canvas = Canvas(width=256, height=256)
#canvas.create_image(128, 128, image=photo)
#canvas.pack()

try:
    image = Image.open("image4.png")
    resized_image = image.resize((100, 100))
    photo = ImageTk.PhotoImage(resized_image)
    photoLabel = Label(image=photo)
    photoLabel.pack()
except Exception as e:
    print(f"Error loading image: {e}")

input_title_label = Label(text='Enter your title', font=FONT)
input_title_label.pack(pady=(20))

input_title_entry = Entry(width=30)
input_title_entry.pack(pady=(5))

text_label = Label(text='Enter your secret', font=FONT)
text_label.pack(pady=(20))

input_text = Text(width=40, height=20)
input_text.pack(pady=(20))

key_label = Label(text='Enter master key', font=FONT)
key_label.pack(pady=(20, 5))

key_entry = Entry(width=30)
key_entry.pack(pady=(5))

save_button = Button(text='Save & Encrypt', command=save_and_encrypt_notes)
save_button.pack(pady=(10, 5))  # Üstte 10, altta 5 birim boşluk

decrypt_button = Button(text='Decrypt', command=decrypt_notes)
decrypt_button.pack(pady=(5, 20))  # Üstte 5, altta 20 birim boşluk

# Run the Tkinter main loop inside try-except
try:
    window.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
