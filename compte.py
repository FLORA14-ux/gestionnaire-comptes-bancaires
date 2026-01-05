from datetime import datetime

class Transaction:
    """Représente une transaction (dépôt ou retrait)"""
    
    def __init__(self, type_operation, montant, solde_apres):
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.type_operation = type_operation
        self.montant = montant
        self.solde_apres = solde_apres
    
    def __str__(self):
        """Affiche la transaction de manière lisible"""
        return f"{self.date} - {self.type_operation} : {self.montant} FCFA (Solde: {self.solde_apres} FCFA)"


class Compte:
    """Représente un compte bancaire"""
    
    _compteur = 1
    
    def __init__(self, titulaire, type_compte="Courant", solde_initial=0):
        """Crée un nouveau compte"""
        self.numero_compte = f"CPT{Compte._compteur:05d}"
        Compte._compteur += 1
        
        self.titulaire = titulaire
        self.type_compte = type_compte
        self.solde = solde_initial
        self.date_creation = datetime.now().strftime("%d/%m/%Y")
        self.transactions = []
        
        if solde_initial > 0:
            trans = Transaction("Dépôt initial", solde_initial, self.solde)
            self.transactions.append(trans)
    
    def deposer(self, montant):
        """Effectue un dépôt"""
        if montant <= 0:
            return False, "Le montant doit être positif !"
        
        self.solde += montant
        trans = Transaction("Dépôt", montant, self.solde)
        self.transactions.append(trans)
        return True, f"Dépôt de {montant} FCFA effectué. Nouveau solde : {self.solde} FCFA"
    
    def retirer(self, montant):
        """Effectue un retrait"""
        if montant <= 0:
            return False, "Le montant doit être positif !"
        
        if montant > self.solde:
            return False, f"Solde insuffisant ! Solde actuel : {self.solde} FCFA"
        
        self.solde -= montant
        trans = Transaction("Retrait", montant, self.solde)
        self.transactions.append(trans)
        return True, f"Retrait de {montant} FCFA effectué. Nouveau solde : {self.solde} FCFA"
    
    def obtenir_solde(self):
        """Retourne le solde actuel"""
        return self.solde
    
    def obtenir_historique(self):
        """Retourne la liste des transactions"""
        return self.transactions
    
    def __str__(self):
        """Affiche les infos du compte"""
        return f"Compte {self.numero_compte} - {self.titulaire} ({self.type_compte}) - Solde: {self.solde} FCFA"


if __name__ == "__main__":
    print("=== TEST DE LA CLASSE COMPTE ===\n")
    
    compte1 = Compte("Jean Dupont", "Courant", 1000)
    print(compte1)
    print()
    
    succes, message = compte1.deposer(500)
    print(message)
    print()
    
    succes, message = compte1.retirer(200)
    print(message)
    print()
    
    print("=== HISTORIQUE ===")
    for trans in compte1.obtenir_historique():
        print(trans)