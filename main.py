from config.db_manager import DatabaseManager
from views.main_view import MenuApp

if __name__ == "__main__":
    # 1. Inicializar la base de datos de la empresa
    db = DatabaseManager("empresa_ecotech.db")

    # 2. Iniciar la aplicación e interfaz interactiva
    app = MenuApp(db)
    app.mostrar_menu_principal()