import tkinter as tk
from tkinter import messagebox
from compte import Compte, sauvegarder_comptes, charger_comptes

# Liste globale pour stocker tous les comptes
liste_comptes = []


def creer_interface_principale():
    """Crée la fenêtre principale avec le menu"""
    
    global liste_comptes
    
    # Charger les comptes existants au démarrage
    liste_comptes = charger_comptes()
    
    fenetre = tk.Tk()
    fenetre.title("Gestionnaire de Comptes Bancaires")
    fenetre.geometry("400x500")
    
    texte = tk.Label(fenetre, text="🏦 Bienvenue!", font=("Arial", 14, "bold"))
    texte.pack(pady=20)
    
    sous_titre = tk.Label(fenetre, text="Choisissez une action :", font=("Arial", 12))
    sous_titre.pack(pady=10)
    
    # Bouton 1 : Créer un compte
    btn_creer = tk.Button(fenetre, text="➕ Créer un compte", font=("Arial", 12),
                          bg="green", fg="white", width=25, command=ouvrir_formulaire_creation)
    btn_creer.pack(pady=10)
    
    # Bouton 2 : Voir mes comptes
    btn_voir = tk.Button(fenetre, text="📋 Voir mes comptes", font=("Arial", 12),
                         bg="blue", fg="white", width=25, command=voir_comptes)
    btn_voir.pack(pady=10)
    
    # Bouton 3 : Opérations
    btn_operations = tk.Button(fenetre, text="💰 Effectuer une opération", font=("Arial", 12),
                               bg="orange", fg="white", width=25, command=ouvrir_operations)
    btn_operations.pack(pady=10)
    
    # Bouton 4 : Quitter
    btn_quitter = tk.Button(fenetre, text="❌ Quitter", font=("Arial", 12),
                            bg="red", fg="white", width=25, command=fenetre.quit)
    btn_quitter.pack(pady=10)
    
    fenetre.mainloop()


def ouvrir_formulaire_creation():
    """Ouvre une nouvelle fenêtre pour créer un compte"""
    
    fenetre_form = tk.Toplevel()
    fenetre_form.title("Créer un nouveau compte")
    fenetre_form.geometry("400x350")
    
    titre = tk.Label(fenetre_form, text="📝 Nouveau Compte", font=("Arial", 14, "bold"))
    titre.pack(pady=15)
    
    # Champ du nom
    label_nom = tk.Label(fenetre_form, text="Nom du titulaire:", font=("Arial", 11))
    label_nom.pack(pady=5)
    entry_nom = tk.Entry(fenetre_form, font=("Arial", 11), width=30)
    entry_nom.pack(pady=5)
    
    # Champ du type de compte
    label_type = tk.Label(fenetre_form, text="Type de compte:", font=("Arial", 11))
    label_type.pack(pady=5)
    type_compte = tk.StringVar(value="Courant")
    menu_type = tk.OptionMenu(fenetre_form, type_compte, "Courant", "Épargne")
    menu_type.config(font=("Arial", 11), width=27)
    menu_type.pack(pady=5)
    
    # Champ du solde initial
    label_solde = tk.Label(fenetre_form, text="Solde initial (FCFA):", font=("Arial", 11))
    label_solde.pack(pady=5)
    entry_solde = tk.Entry(fenetre_form, font=("Arial", 11), width=30)
    entry_solde.insert(0, "0")
    entry_solde.pack(pady=5)
    
    # Validation
    def valider_creation():
        global liste_comptes
        
        nom = entry_nom.get()
        type_c = type_compte.get()
        solde = entry_solde.get()
        
        if nom == "":
            messagebox.showerror("Erreur", "Le nom du titulaire est obligatoire!")
            return
        
        try:
            solde = float(solde)
            if solde < 0:
                messagebox.showerror("Erreur", "Le solde ne peut pas être négatif!")
                return
        except:
            messagebox.showerror("Erreur", "Le solde doit être un nombre!")
            return
        
        # CRÉER VRAIMENT LE COMPTE
        nouveau_compte = Compte(nom, type_c, solde)
        liste_comptes.append(nouveau_compte)
        
        # SAUVEGARDER DANS JSON
        sauvegarder_comptes(liste_comptes)
        
        message = f"Compte créé !\n\n{nouveau_compte}"
        messagebox.showinfo("Succès", message)
        fenetre_form.destroy()
    
    btn_valider = tk.Button(fenetre_form, text="✅ Créer le compte", font=("Arial", 12),
                            bg="green", fg="white", width=25, command=valider_creation)
    btn_valider.pack(pady=20)
    
    # Pour annuler
    btn_annuler = tk.Button(fenetre_form, text="❌ Annuler", font=("Arial", 12),
                            bg="gray", fg="white", width=25, command=fenetre_form.destroy)
    btn_annuler.pack(pady=5)


def voir_comptes():
    """Affiche la liste des comptes"""
    global liste_comptes
    
    if len(liste_comptes) == 0:
        messagebox.showinfo("Mes comptes", "Aucun compte enregistré pour le moment.")
        return
    
    # Créer une fenêtre pour afficher les comptes
    fenetre_liste = tk.Toplevel()
    fenetre_liste.title("Liste des comptes")
    fenetre_liste.geometry("500x400")
    
    titre = tk.Label(fenetre_liste, text="📋 Mes Comptes", font=("Arial", 14, "bold"))
    titre.pack(pady=15)
    
    # Zone de texte avec scrollbar
    frame = tk.Frame(fenetre_liste)
    frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    
    text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, font=("Courier", 10), wrap="word")
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_widget.yview)
    
    # Afficher les comptes
    for i, compte in enumerate(liste_comptes, 1):
        text_widget.insert("end", f"\n{'='*50}\n")
        text_widget.insert("end", f"COMPTE #{i}\n")
        text_widget.insert("end", f"{'='*50}\n")
        text_widget.insert("end", f"Numéro      : {compte.numero_compte}\n")
        text_widget.insert("end", f"Titulaire   : {compte.titulaire}\n")
        text_widget.insert("end", f"Type        : {compte.type_compte}\n")
        text_widget.insert("end", f"Solde       : {compte.solde} FCFA\n")
        text_widget.insert("end", f"Créé le     : {compte.date_creation}\n")
        text_widget.insert("end", f"Transactions: {len(compte.transactions)}\n")
    
    text_widget.config(state="disabled")
    
    # Bouton fermer
    btn_fermer = tk.Button(fenetre_liste, text="Fermer", font=("Arial", 11),
                           bg="gray", fg="white", width=20, command=fenetre_liste.destroy)
    btn_fermer.pack(pady=10)


def ouvrir_operations():
    """Ouvre la fenêtre des opérations bancaires"""
    global liste_comptes
    
    if len(liste_comptes) == 0:
        messagebox.showwarning("Attention", "Aucun compte disponible.\nCréez d'abord un compte !")
        return
    
    # Créer la fenêtre d'opérations
    fenetre_op = tk.Toplevel()
    fenetre_op.title("Opérations bancaires")
    fenetre_op.geometry("500x600")
    
    titre = tk.Label(fenetre_op, text="💰 Opérations Bancaires", font=("Arial", 14, "bold"))
    titre.pack(pady=15)
    
    # --- Sélection du compte ---
    label_selection = tk.Label(fenetre_op, text="Sélectionnez un compte :", font=("Arial", 11))
    label_selection.pack(pady=5)
    
    # Liste déroulante avec les comptes
    comptes_noms = [f"{c.numero_compte} - {c.titulaire} ({c.solde} FCFA)" for c in liste_comptes]
    compte_selectionne = tk.StringVar(value=comptes_noms[0] if comptes_noms else "")
    
    menu_comptes = tk.OptionMenu(fenetre_op, compte_selectionne, *comptes_noms)
    menu_comptes.config(font=("Arial", 10), width=40)
    menu_comptes.pack(pady=5)
    
    # Fonction pour obtenir le compte sélectionné
    def get_compte_selectionne():
        selection = compte_selectionne.get()
        numero = selection.split(" - ")[0]
        for c in liste_comptes:
            if c.numero_compte == numero:
                return c
        return None
    
    # --- Affichage du solde ---
    label_solde = tk.Label(fenetre_op, text="", font=("Arial", 12, "bold"), fg="darkblue")
    label_solde.pack(pady=10)
    
    def actualiser_solde():
        compte = get_compte_selectionne()
        if compte:
            label_solde.config(text=f"Solde actuel : {compte.solde} FCFA")
    
    actualiser_solde()
    
    # Actualiser le solde quand on change de compte
    compte_selectionne.trace("w", lambda *args: actualiser_solde())
    
    # --- Séparateur ---
    separator = tk.Label(fenetre_op, text="─" * 50)
    separator.pack(pady=10)
    
    # --- DÉPÔT ---
    label_depot = tk.Label(fenetre_op, text="💵 DÉPÔT", font=("Arial", 12, "bold"), fg="green")
    label_depot.pack(pady=5)
    
    label_montant_depot = tk.Label(fenetre_op, text="Montant à déposer (FCFA) :", font=("Arial", 10))
    label_montant_depot.pack(pady=3)
    
    entry_depot = tk.Entry(fenetre_op, font=("Arial", 11), width=20)
    entry_depot.pack(pady=3)
    
    def faire_depot():
        compte = get_compte_selectionne()
        if not compte:
            messagebox.showerror("Erreur", "Aucun compte sélectionné")
            return
        
        try:
            montant = float(entry_depot.get())
            succes, message = compte.deposer(montant)
            
            if succes:
                sauvegarder_comptes(liste_comptes)
                messagebox.showinfo("Succès", message)
                actualiser_solde()
                entry_depot.delete(0, tk.END)
                # Actualiser la liste déroulante
                comptes_noms_new = [f"{c.numero_compte} - {c.titulaire} ({c.solde} FCFA)" for c in liste_comptes]
                menu_comptes['menu'].delete(0, 'end')
                for nom in comptes_noms_new:
                    menu_comptes['menu'].add_command(label=nom, command=tk._setit(compte_selectionne, nom))
            else:
                messagebox.showerror("Erreur", message)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide !")
    
    btn_depot = tk.Button(fenetre_op, text="✅ Effectuer le dépôt", font=("Arial", 11),
                         bg="green", fg="white", width=25, command=faire_depot)
    btn_depot.pack(pady=5)
    
    # --- Séparateur ---
    separator2 = tk.Label(fenetre_op, text="─" * 50)
    separator2.pack(pady=10)
    
    # --- RETRAIT ---
    label_retrait = tk.Label(fenetre_op, text="💸 RETRAIT", font=("Arial", 12, "bold"), fg="red")
    label_retrait.pack(pady=5)
    
    label_montant_retrait = tk.Label(fenetre_op, text="Montant à retirer (FCFA) :", font=("Arial", 10))
    label_montant_retrait.pack(pady=3)
    
    entry_retrait = tk.Entry(fenetre_op, font=("Arial", 11), width=20)
    entry_retrait.pack(pady=3)
    
    def faire_retrait():
        compte = get_compte_selectionne()
        if not compte:
            messagebox.showerror("Erreur", "Aucun compte sélectionné")
            return
        
        try:
            montant = float(entry_retrait.get())
            succes, message = compte.retirer(montant)
            
            if succes:
                sauvegarder_comptes(liste_comptes)
                messagebox.showinfo("Succès", message)
                actualiser_solde()
                entry_retrait.delete(0, tk.END)
                # Actualiser la liste déroulante
                comptes_noms_new = [f"{c.numero_compte} - {c.titulaire} ({c.solde} FCFA)" for c in liste_comptes]
                menu_comptes['menu'].delete(0, 'end')
                for nom in comptes_noms_new:
                    menu_comptes['menu'].add_command(label=nom, command=tk._setit(compte_selectionne, nom))
            else:
                messagebox.showerror("Erreur", message)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide !")
    
    btn_retrait = tk.Button(fenetre_op, text="✅ Effectuer le retrait", font=("Arial", 11),
                           bg="red", fg="white", width=25, command=faire_retrait)
    btn_retrait.pack(pady=5)
    
    # --- Séparateur ---
    separator3 = tk.Label(fenetre_op, text="─" * 50)
    separator3.pack(pady=10)
    
    # --- HISTORIQUE ---
    def voir_historique_compte():
        compte = get_compte_selectionne()
        if not compte:
            messagebox.showerror("Erreur", "Aucun compte sélectionné")
            return
        
        if len(compte.transactions) == 0:
            messagebox.showinfo("Historique", "Aucune transaction pour ce compte.")
            return
        
        # Fenêtre historique
        fenetre_hist = tk.Toplevel()
        fenetre_hist.title(f"Historique - {compte.numero_compte}")
        fenetre_hist.geometry("600x400")
        
        titre_hist = tk.Label(fenetre_hist, text=f"📜 Historique de {compte.titulaire}", 
                             font=("Arial", 13, "bold"))
        titre_hist.pack(pady=10)
        
        # Zone de texte
        frame_hist = tk.Frame(fenetre_hist)
        frame_hist.pack(pady=10, padx=10, fill="both", expand=True)
        
        scrollbar_hist = tk.Scrollbar(frame_hist)
        scrollbar_hist.pack(side="right", fill="y")
        
        text_hist = tk.Text(frame_hist, yscrollcommand=scrollbar_hist.set, 
                           font=("Courier", 9), wrap="word")
        text_hist.pack(side="left", fill="both", expand=True)
        scrollbar_hist.config(command=text_hist.yview)
        
        # Afficher les transactions
        text_hist.insert("end", f"\n{'='*70}\n")
        text_hist.insert("end", f"Compte: {compte.numero_compte} - {compte.titulaire}\n")
        text_hist.insert("end", f"{'='*70}\n\n")
        
        for i, trans in enumerate(compte.transactions, 1):
            text_hist.insert("end", f"{i}. {trans}\n")
        
        text_hist.insert("end", f"\n{'='*70}\n")
        text_hist.insert("end", f"Solde actuel: {compte.solde} FCFA\n")
        text_hist.insert("end", f"{'='*70}\n")
        
        text_hist.config(state="disabled")
        
        btn_fermer_hist = tk.Button(fenetre_hist, text="Fermer", font=("Arial", 10),
                                    bg="gray", fg="white", width=15, command=fenetre_hist.destroy)
        btn_fermer_hist.pack(pady=10)
    
    btn_historique = tk.Button(fenetre_op, text="📜 Voir l'historique", font=("Arial", 11),
                              bg="purple", fg="white", width=25, command=voir_historique_compte)
    btn_historique.pack(pady=5)
    
    # Bouton fermer
    btn_fermer = tk.Button(fenetre_op, text="❌ Fermer", font=("Arial", 11),
                          bg="gray", fg="white", width=25, command=fenetre_op.destroy)
    btn_fermer.pack(pady=15)


#