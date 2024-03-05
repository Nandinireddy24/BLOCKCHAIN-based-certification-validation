from tkinter import *
from tkinter.filedialog import askopenfilename
from Blockchain import Blockchain
from hashlib import sha256
import os

main = Tk()
main.title("Blockchain Based Certificate Verification")
main.geometry("1300x1200")

global filename

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def saveCertificate():
    global filename
    text.delete('1.0', END)
    filename = askopenfilename(initialdir="certificate_templates")
    with open(filename, "rb") as f:
        bytes = f.read()
    f.close()
    roll_no = tf1.get()
    name = tf2.get()
    contact = tf3.get()
    if len(roll_no) > 0 and len(name) > 0 and len(contact) > 0:
        digital_signature = sha256(bytes).hexdigest()
        data = roll_no + "#" + name + "#" + contact + "#" + digital_signature
        blockchain.add_new_transaction(data)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain) - 1]
        text.insert(END, "Blockchain Previous Hash : " + str(b.previous_hash) + "\nBlock No : " + str(b.index) + "\nCurrent Hash : " + str(b.hash) + "\n")
        text.insert(END, "Certificate Digital Signature : " + str(digital_signature) + "\n\n")
        blockchain.save_object(blockchain, 'blockchain_contract.txt')
    else:
        text.insert(END, "Please Enter Roll No")

def verifyCertificate():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir="certificate_templates")
    with open(filename, "rb") as f:
        bytes = f.read()
    f.close()
    digital_signature = sha256(bytes).hexdigest()
    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[3] == digital_signature:
                text.insert(END, "Uploaded Certificate Validation Successful\n")
                text.insert(END, "Details extracted from Blockchain after Validation\n\n")
                text.insert(END, "Roll No : " + arr[0] + "\n")
                text.insert(END, "Student Name : " + arr[1] + "\n")
                text.insert(END, "Contact No : " + arr[2] + "\n")
                text.insert(END, "Digital Sign : " + arr[3] + "\n")
                flag = False
                break
    if flag:
        text.insert(END, "Verification failed or certificate modified")

font = ('times', 15, 'bold')
# Rest of the title and font settings...

# Rest of the label and entry fields...

saveButton = Button(main, text="Save Certificate with Digital Signature", command=saveCertificate)
# Rest of the button placements and font settings...

verifyButton = Button(main, text="Verify Certificate", command=verifyCertificate)
# Rest of the button placements and font settings...

font1 = ('times', 13, 'bold')
text = Text(main, height=15, width=120)
# Rest of the text widget settings...

main.config(bg='brown')
main.mainloop()
