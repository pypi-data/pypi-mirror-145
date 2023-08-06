from .autoencoder import *
from .genetic_algorithm import *

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Fonctions de l'interface graphique

def start_algo():
    ''''''
    global window2
    window2 = tk.Toplevel(window)
    # window.withdraw()
    window.iconify()
    window2.title("Robot Portrait")
    window2.geometry("1000x650")
    window2.resizable(height=False, width=False)
    window2.configure(bg='white')
    #global iteration
    #iteration = 0
    contenu_window(z)


def contenu_window(z):
    TextFrame = tk.LabelFrame(
        window2, width=window_width, height=0.19*window_height, bg="white")
    # TextFrame.grid(row=0,column=0,columnspan=5,sticky=tk.NW)
    # TextFrame.configure(bg = 'white') # A changer
    TextFrame.place(x=0, rely=0)
    TextFrame.pack()

    '''Title=tk.Label(TextFrame, text="Robot Portrait",height= 1, width=65, fg="black")
    #fontTitle=tkFont.Font(size=16)
    Title.configure(font=("Helvetica",20,"underline"))
    Title.place(relx=0.2,rely=0.1)'''

    ToDo = tk.Label(TextFrame, text="Choose between 1 and 4 images that most represent the suspect.\n You can select an image by clicking on the associated button. Once an image is selected, the button will turn blue. When you are done with the selection, click on the 'next' button. \n Then,  the program will propose you other images generated from the ones that you have selected. \n If you think there is one image representing exactly the suspect, you can click on 'The selected image corresponds to the criminal', and the program will display the chosen image and end", wraplength=900, bg="white", width=window_width)
    # fontTitle=tkFont.Font(size=16)
    ToDo.configure(font=("Helvetica", 12))
    ToDo.place(relx=0.5, rely=0.5)
    ToDo.pack()

    nbr_columns = 5

    global suspects
    suspects = []

    ImageFrame1 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame1.configure(bg="grey")
    ImageFrame1.place(x=0, rely=0.19)

    ImageFrame2 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame2.configure(bg="grey")
    ImageFrame2.place(relx=0.2, rely=0.19)

    ImageFrame3 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame3.configure(bg="grey")
    ImageFrame3.place(relx=0.4, rely=0.19)

    ImageFrame4 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame4.configure(bg="grey")
    ImageFrame4.place(relx=0.6, rely=0.19)

    ImageFrame5 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame5.configure(bg="grey")
    ImageFrame5.place(relx=0.8, rely=0.19)

    ImageFrame6 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame6.configure(bg="grey")
    ImageFrame6.place(relx=0, rely=0.57)

    ImageFrame7 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame7.configure(bg="grey")
    ImageFrame7.place(relx=0.2, rely=0.57)

    ImageFrame8 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame8.configure(bg="grey")
    ImageFrame8.place(relx=0.4, rely=0.57)

    ImageFrame9 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame9.configure(bg="grey")
    ImageFrame9.place(relx=0.6, rely=0.57)

    ImageFrame10 = tk.LabelFrame(
        window2, width=0.2*window_width, height=0.38*window_height, bg="white")
    # ImageFrame10.configure(bg="grey")
    ImageFrame10.place(relx=0.8, rely=0.57)

    Frame_bas = tk.LabelFrame(
        window2, width=window_width, height=0.05*window_height, bg="white")
    # ImageFrame10.configure(bg="grey"),
    Frame_bas.place(relx=0, rely=0.95)

    # Buttons

    Button1 = tk.Button(ImageFrame1, command=lambda: [returnperson(
        0), ChangeColor(Button1)], text="Person 1", width=15)
    Button1.place(relx=0.2, rely=0.85)
    # Button1.pack(side="top")

    Button2 = tk.Button(ImageFrame2, command=lambda: [returnperson(
        1), ChangeColor(Button2)], text="Person 2", width=15)
    Button2.place(relx=0.2, rely=0.85)

    Button3 = tk.Button(ImageFrame3, command=lambda: [returnperson(
        2), ChangeColor(Button3)], text="Person 3", width=15)
    Button3.place(relx=0.2, rely=0.85)

    Button4 = tk.Button(ImageFrame4, command=lambda: [returnperson(
        3), ChangeColor(Button4)], text="Person 4", width=15)
    Button4.place(relx=0.2, rely=0.85)

    Button5 = tk.Button(ImageFrame5, command=lambda: [returnperson(
        4), ChangeColor(Button5)], text="Person 5", width=15)
    Button5.place(relx=0.2, rely=0.85)

    Button6 = tk.Button(ImageFrame6, command=lambda: [returnperson(
        5), ChangeColor(Button6)], text="Person 6", width=15)
    Button6.place(relx=0.2, rely=0.85)

    Button7 = tk.Button(ImageFrame7, command=lambda: [returnperson(
        6), ChangeColor(Button7)], text="Person 7", width=15)
    Button7.place(relx=0.2, rely=0.85)

    Button8 = tk.Button(ImageFrame8, command=lambda: [returnperson(
        7), ChangeColor(Button8)], text="Person 8", width=15)
    Button8.place(relx=0.2, rely=0.85)

    Button9 = tk.Button(ImageFrame9, command=lambda: [returnperson(
        8), ChangeColor(Button9)], text="Person 9", width=15)
    Button9.place(relx=0.2, rely=0.85)

    Button10 = tk.Button(ImageFrame10, command=lambda: [returnperson(
        9), ChangeColor(Button10)], text="Person 10", width=15)
    Button10.place(relx=0.2, rely=0.85)

    print("Iteration", iteration)

    L_frame = [ImageFrame1, ImageFrame2, ImageFrame3, ImageFrame4, ImageFrame5,
               ImageFrame6, ImageFrame7, ImageFrame8, ImageFrame9, ImageFrame10]
    z2 = np.array(reconstruct_image_from_latent_vectors(decoder, z))
    print(len(z2))
    list_images = list_to_images(z2)
    Images(list_images, L_frame)
    #iteration += 1

    # while iteration < nbre_iter :
    button_next = tk.Button(Frame_bas, text=">>NEXT", fg="black", bg="white",
                            height=1, width=8, command=lambda: [add_1(), ask_confirmation(z)])
    button_next.place(relx=0.9, rely=0.2)
    bouton_fin = tk.Button(Frame_bas, text="I have found my suspect", command=lambda: [
                           ask_confirmation_end(z), set_iteration()], bg="white")
    bouton_fin.place(relx=0.37, rely=0.2)
    bouton = tk.Button(Frame_bas, text="QUIT", command=lambda: [
                       set_iteration(), fermer_tout()])
    bouton.pack()
    bouton.place(relx=0.05, rely=0.2)

    if iteration == (nbre_iter_max-1):
        messagebox.showwarning(
            "Last iteration", "This is the last iteration, you have to choose only one image that will be the one of the suspect")
        button_next.destroy()
    window2.mainloop()


def fermer_tout():
    ''''''
    for c in window2.winfo_children():
        c.destroy()
    for c in window.winfo_children():
        c.destroy()
    window.destroy()


def end_algo(z, suspects):
    ''''''
    window3 = tk.Toplevel(window2)
    window2.withdraw()
    window3.title("Robot Portrait")
    window3.configure(bg='white')
    window3.geometry("450x550")
    window3.resizable(height=False, width=False)
    texte = tk.Label(window3, anchor='center', text="Here is your suspect !", font=(
        'Helvetica', 20, 'bold'), wraplength=700, bg="white")
    texte.pack()
    texte.place(x=225, y=70, anchor="center")
    bouton = tk.Button(window3, text="QUIT", command=fermer_tout)
    bouton.pack()
    bouton.place(x=225, y=470, anchor="center")
    # Dans le cas où le témoin arrête le programme avant la fin du nombre d'itération prévu
    z_selected = []
    for indice in suspects:
        z_selected.append(z[indice])
    L = np.array(reconstruct_image_from_latent_vectors(
        decoder, np.array(z_selected)))
    Im = list_to_images(L)
    image = Im[0]
    Im = image.resize((300, 300))
    Im.save('./suspects/image_suspect.png')
    Im = ImageTk.PhotoImage(Im, master=window3)
    Im_widget = tk.Label(window3, image=Im)
    Im_widget.image = Im
    Im_widget.place(x=225, y=270, anchor='center')
    messagebox.showinfo(
        "Save image", "The image has been save in the folder /suspects")
    window3.mainloop()
    # Afficher l'image choisie + bouton quit


# On crée la fenêtre
def welcome_window():
    ''''''
    global window
    window = tk.Tk()
    window.title("Robot Portrait")
    window.configure(bg='white')
    window.resizable(height=False, width=False)

    # On choisit les dimensions
    window.geometry("1000x650")
    global window_width
    window_width = 1000
    global window_height
    window_height = 650

    # On définit le texte de la première page
    texte1 = tk.Label(window, anchor='center', text="Welcome to our program to generate robot portraits and identify criminals !", font=(
        'Helvetica', 20, 'bold'), wraplength=700, bg="white")
    texte1.pack()
    texte1.place(x=500, y=200, anchor="center")
    texte2 = tk.Label(window, text="In a few seconds, 10 faces will be displayed on the screen and you will have to choose between 1 and 4 images that most look like the suspect that you have in mind ",
                      font='Helvetica', anchor='center', wraplength=500,  bg="white")
    texte2.pack()
    texte2.place(x=500, y=300, anchor="center")

    # On définit le bouton qui va permettre de démarrer le programme
    bouton1 = tk.Button(window, text="START", command=start_algo)
    bouton1.pack()
    bouton1.place(x=500, y=500, anchor="center")

    window.mainloop()


def ask_confirmation(z):
    ''''''
    ask_the_client = tk.messagebox.askyesno(
        "Your selection", "Did you select all the wanted files? [yes/no]")
    if ask_the_client == 1:
        next_step(z, suspects)
    else:
        contenu_window(z)


def ask_confirmation_end(z):
    ''''''
    ask_the_client = tk.messagebox.askyesno(
        "Your selection", "Did you select the suspect's image? [yes/no]")
    if ask_the_client == 1:
        if len(suspects) == 1:
            end_algo(z, suspects)
        else:
            messagebox.showwarning(
                "Wrong number of images selected", "You should select only one image")
            contenu_window(z)
    else:
        contenu_window(z)


def next_step(z, suspects):
    ''''''
    #iteration += 1
    print(iteration)
    while iteration < nbre_iter_max:
        # print(suspects)
        n = len(z)
        # print(n)
        z_selected = []
        for indice in suspects:
            #print("Liste_suspects", suspects)
            #print("z sélectionné par user", z[indice])
            z_selected.append(z[indice])
        #print("Z ( = avant la mutation)", z)
        #print("Z_selected", z_selected)
        #global z
        z = adjust_children(z_selected, prior)
        #print("Zmuté", z[7])
        suspects = []
        contenu_window(z)
    # Image choisie à enregistrer
    # window2.withdraw()
    # window.deiconify()
    # window.destroy()


def add_1():
    global iteration
    iteration += 1


def set_iteration():
    global iteration
    iteration = nbre_iter_max


def Images(list_images, Lframe):
    ImageFrame1 = Lframe[0]
    ImageFrame2 = Lframe[1]
    ImageFrame3 = Lframe[2]
    ImageFrame4 = Lframe[3]
    ImageFrame5 = Lframe[4]
    ImageFrame6 = Lframe[5]
    ImageFrame7 = Lframe[6]
    ImageFrame8 = Lframe[7]
    ImageFrame9 = Lframe[8]
    ImageFrame10 = Lframe[9]

    # new size for the images
    newsize = (150, 150)
    #list_images =os.listdir("/Users/yasminemayakamili/Desktop/4BIM/4BIMS2/Projet4BIM/InterfaceGraphique/generated_images")
    for i in range(10):
        #path= "D:/Noemie/Documents/Biosciences/4A-S2/Développement Logiciel - Projet 4BIM/Projet 4BIM/Code projet/generated_images" +'/'+list_images[i]
        # Im=Image.open(path)
        Im = list_images[i]
        Im = Im.resize(newsize)
        Im = ImageTk.PhotoImage(Im, master=window2)
        # i va de 0 à 9
        j = i+1
        if j == 1:
            Im_widget = tk.Label(ImageFrame1, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 2:
            Im_widget = tk.Label(ImageFrame2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 3:
            Im_widget = tk.Label(ImageFrame3, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 4:
            Im_widget = tk.Label(ImageFrame4, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 5:
            Im_widget = tk.Label(ImageFrame5, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 6:
            Im_widget = tk.Label(ImageFrame6, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 7:
            Im_widget = tk.Label(ImageFrame7, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 8:
            Im_widget = tk.Label(ImageFrame8, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 9:
            Im_widget = tk.Label(ImageFrame9, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)
        if j == 10:
            Im_widget = tk.Label(ImageFrame10, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(relx=0.1, rely=0.1)


def generation_init():
    ''''''
    z = generate_latent_vectors(prior, 10)
    z2 = np.array(reconstruct_image_from_latent_vectors(decoder, z))
    return z2


def list_to_images(L):
    ''''''
    list_images = []
    for image in L:
        pil_image = Image.fromarray((image*255).astype(np.uint8))
        list_images.append(pil_image)
    return list_images


def returnperson(x):
    suspects.append(x)


def ChangeColor(button):
    # if button["fg"]=="black":
    button.configure(fg="blue")


def run():
    this_dir, _ = os.path.split(__file__)

    prior = get_prior(num_modes=2, latent_dim=50)
    global encoder
    encoder = get_encoder(
        latent_dim=50, kl_regularizer=get_kl_regularizer(prior))
    global decoder
    decoder = get_decoder(latent_dim=50)

    encoder.load_weights(os.path.join(
        this_dir, "model_vae/VAE_encoder2"))
    decoder.load_weights(os.path.join(
        this_dir, "model_vae/VAE_decoder2"))

    # encoder.load_weights("./model_vae/encoder/saved_encoder")
    # decoder.load_weights("./model_vae/decoder/saved_decoder")

    global z
    #z = generation_init()
    z = generate_latent_vectors(prior, 10)
    #print("Zinit", z)

    global iteration
    iteration = 0

    global suspects
    suspects = []

    global nbre_iter_max
    nbre_iter_max = 5

    welcome_window()
