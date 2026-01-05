from datetime import datetime
import json
import os


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


def sauvegarder_comptes(liste_comptes, fichier='data/comptes.json'):
    """Sauvegarde la liste des comptes dans un fichier JSON"""
    
    # Créer le dossier data s'il n'existe pas
    dossier = os.path.dirname(fichier)
    if dossier and not os.path.exists(dossier):
        os.makedirs(dossier)
    
    # Convertir les comptes en dictionnaires
    donnees = {
        'comptes': []
    }
    
    for compte in liste_comptes:
        compte_dict = {
            'numero_compte': compte.numero_compte,
            'titulaire': compte.titulaire,
            'type_compte': compte.type_compte,
            'solde': compte.solde,
            'date_creation': compte.date_creation,
            'transactions': []
        }
        
        # Ajouter les transactions
        for trans in compte.transactions:
            trans_dict = {
                'date': trans.date,
                'type_operation': trans.type_operation,
                'montant': trans.montant,
                'solde_apres': trans.solde_apres
            }
            compte_dict['transactions'].append(trans_dict)
        
        donnees['comptes'].append(compte_dict)
    
    # Sauvegarder dans le fichier
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(liste_comptes)} compte(s) sauvegardé(s)")


def charger_comptes(fichier='data/comptes.json'):
    """Charge la liste des comptes depuis un fichier JSON"""
    
    # Si le fichier n'existe pas, retourner une liste vide
    if not os.path.exists(fichier):
        print("ℹ️ Aucun fichier de sauvegarde trouvé")
        return []
    
    # Charger le fichier
    with open(fichier, 'r', encoding='utf-8') as f:
        donnees = json.load(f)
    
    liste_comptes = []
    
    for compte_data in donnees.get('comptes', []):
        # Créer le compte
        compte = Compte(
            titulaire=compte_data['titulaire'],
            type_compte=compte_data['type_compte'],
            solde_initial=0
        )
        
        # Restaurer les données
        compte.numero_compte = compte_data['numero_compte']
        compte.solde = compte_data['solde']
        compte.date_creation = compte_data['date_creation']
        compte.transactions = []
        
        # Restaurer les transactions
        for trans_data in compte_data['transactions']:
            trans = Transaction(
                trans_data['type_operation'],
                trans_data['montant'],
                trans_data['solde_apres']
            )
            trans.date = trans_data['date']
            compte.transactions.append(trans)
        
        liste_comptes.append(compte)
    
    print(f"✅ {len(liste_comptes)} compte(s) chargé(s)")
    return liste_comptes

if __name__ == "__main__":
    print("=== TEST 1 : Créer et sauvegarder ===\n")
    
    # Créer des comptes
    compte1 = Compte("Jean Dupont", "Courant", 1000)
    compte1.deposer(500)
    compte1.retirer(200)
    
    compte2 = Compte("Marie Martin", "Épargne", 2000)
    compte2.deposer(300)
    
    # Sauvegarder
    liste = [compte1, compte2]
    sauvegarder_comptes(liste)
    
    print("\n=== TEST 2 : Charger les comptes ===\n")
    
    # Charger
    comptes_charges = charger_comptes()
    
    print("\nComptes chargés :")
    for c in comptes_charges:
        print(f"  - {c}")