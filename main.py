from pl.console_ui import ConsoleUI

def main():
    try:
        app = ConsoleUI()
        app.run()
    except Exception as e:
        print(f"Сталася критична помилка: {str(e)}")
        input("Натисніть Enter для виходу...")

if __name__ == "__main__":
    main()