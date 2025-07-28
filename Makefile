PROJECT = Altered Card Bot

# Cible pour créer un environnement virtuel
venv:
	@echo "🔧 Création de l'environnement virtuel..."
	@python3 -m venv venv

# Cible pour installer les dépendances
install:
	@echo "📦 Installation des dépendances..."
	@pip install flask requests

# Cible pour lancer l'application
run:
	@echo "🚀 Lancement du bot Altered..."
	@python backend/main.py

# Tout en une seule commande : venv + install + run
setup:
	@echo "🔍 Configuration complète et lancement..."
	@make venv && make install && make run