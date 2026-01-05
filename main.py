# Lance l'application
"""
Fichier principal - Gestionnaire de Comptes Bancaires
Point d'entrée de l'application
"""

from interface import creer_interface_principale

if __name__ == "__main__":
    print("=" * 50)
    print("  GESTIONNAIRE DE COMPTES BANCAIRES")
    print("=" * 50)
    print("Lancement de l'application...\n")
    
    # Lancer l'interface graphique
    creer_interface_principale()
    
    print("\nApplication fermée. À bientôt ! 👋")