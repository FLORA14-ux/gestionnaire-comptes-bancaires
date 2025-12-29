import tkinter as tk
from tkinter import messagebox

 # Fenetre principale
def creer_interface_principale():
   
    fenetre = tk.Tk()
    fenetre.title("Gestionnaire de Comptes ancaires")
    fenetre.geometry("400x300")

    texte = tk.Label(fenetre, text="Bienvenue!", font=("Arial", 14))
    texte.pack(pady=20)

    sous_titre = tk.Label(fenetre, text="Choisissez une action :", font=("Arial", 12))
    sous_titre.pack(pady=10)

# Bouton 1
    btn_creer = tk.Button(fenetre, text="Creer un compte", font= ("Arial", 12),
                      bg="green", fg="white", width=25, command=ouvrir_formulaire_creation)
    btn_creer.pack(pady=10)
# Bouton 2
    btn_voir = tk.Button(fenetre, text="Voir mes comptes", font= ("Arial", 12),
                      bg="blue", fg="white", width=25, command=voir_comptes)
    btn_voir.pack(pady=10)
# Bouton 3
    btn_quitter = tk.Button(fenetre, text="Quitter", font= ("Arial", 12),
                      bg="red", fg="white", width=25, command=fenetre.quit)
    btn_quitter.pack(pady=10)

    fenetre.mainloop()

# Creation de compte
def ouvrir_formulaire_creation():
    fenetre_from = tk.Toplevel()
    fenetre_from.title("Creer un nouveau compte")
    fenetre_from.geometry("400x350")
    titre = tk.Label(fenetre_from, text="Nouveau Compte", font=("Arial", 14, "bold"))
    titre.pack(pady=15)

    # Champ du nom
    label_nom = tk.Label(fenetre_from, text="Nom du titulaire:", font=("Arial", 11))
    label_nom.pack(pady=5)
    entry_nom = tk.Entry(fenetre_from, font=("Arial", 11), width=30)
    entry_nom.pack(pady=5)

    # champ du type de compte
    label_type = tk.Label(fenetre_from, text="Type de compte:", font=("Arial", 11))
    label_type.pack(pady=5)
    type_compte = tk.StringVar(value="Courant")
    menu_type = tk.OptionMenu(fenetre_from, type_compte, "Courant", "Epargne")
    menu_type.config(font=("Arial", 11), width=27)
    menu_type.pack(pady=5)

    #champ du solde initial
    label_solde = tk.Label(fenetre_from, text="Solde initiale : ", font=("Arial", 11))
    label_solde.pack(pady=5)
    entry_solde = tk.Entry(fenetre_from, font=("Arial", 11), width=30)
    entry_solde.insert(0, "0")
    entry_solde.pack(pady=5)

    # Validation
    def valider_creation():
        nom=entry_nom.get()
        type_c=type_compte.get()
        solde=entry_solde.get()

        if nom =="":
            messagebox.showerror("Erreur", "Le nom du titulaire est obligatoire!")
            return
        try:
            solde=float(solde)
            if solde <0:
               messagebox.showerror("Erreur", "Le solde ne peut pas être negatif!")
               return
        except:
            messagebox.showerror("Erreur", "Le solde doit être un nombre!")
            return
        
        message = f"Compte créé ! \n\nTitulaire: {nom}\nType: {type_c}\nSolde initial: {solde} FCFA"
        messagebox.showinfo("Succès", message)
        fenetre_from.destroy()

    btn_valider = tk.Button(fenetre_from, text= "Créer le compte", font=("Arial", 12),
                        bg="green", fg="white", width=25, command=valider_creation)
    btn_valider.pack(pady=20)

# Pour annuler
    btn_annuler = tk.Button(fenetre_from, text="Annuler", font=("Arial", 12),
                        bg="gray", fg="white", width=25, command=fenetre_from.destroy)
    btn_annuler.pack(pady=5)

# Autres
def voir_comptes():
    messagebox.showinfo("Voir comptes", "Fonction en cours de développement...")

# Lancement 
if __name__ == "__main__":
 creer_interface_principale()