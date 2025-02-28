import datetime
import json
import os
from typing import List, Dict
from abc import ABC, abstractmethod

class InterfejsUzytkownika(ABC):
    """Abstrakcyjna klasa bazowa dla interfejsu użytkownika"""
    
    @abstractmethod
    def wyswietl_menu(self) -> None:
        """Wyświetla główne menu aplikacji"""
        pass
    
    @abstractmethod
    def pobierz_wybor(self) -> str:
        """Pobiera wybór użytkownika"""
        pass
    
    @abstractmethod
    def wyswietl_zadania(self, zadania: List[Dict]) -> None:
        """Wyświetla listę zadań"""
        pass
    
    @abstractmethod
    def wyswietl_notatki(self, notatki: List[Dict]) -> None:
        """Wyświetla listę notatek"""
        pass
    
    @abstractmethod
    def pobierz_dane_zadania(self) -> tuple:
        """Pobiera dane nowego zadania od użytkownika"""
        pass
    
    @abstractmethod
    def pobierz_dane_notatki(self) -> tuple:
        """Pobiera dane nowej notatki od użytkownika"""
        pass

class InterfejsKonsolowy(InterfejsUzytkownika):
    """Konkretna implementacja interfejsu konsolowego"""
    
    def wyswietl_menu(self) -> None:
        print("\n=== ASYSTENT OSOBISTY ===")
        print("1. Dodaj zadanie")
        print("2. Pokaż zadania")
        print("3. Dodaj notatkę")
        print("4. Pokaż notatki")
        print("5. Wyjście")
    
    def pobierz_wybor(self) -> str:
        return input("\nWybierz opcję (1-5): ")
    
    def wyswietl_zadania(self, zadania: List[Dict]) -> None:
        if not zadania:
            print("Brak zadań do wyświetlenia.")
            return
        
        print("\nLista zadań:")
        for i, zadanie in enumerate(zadania, 1):
            print(f"\n{i}. Tytuł: {zadanie['tytul']}")
            print(f"   Opis: {zadanie['opis']}")
            print(f"   Status: {zadanie['status']}")
            if zadanie['termin']:
                print(f"   Termin: {zadanie['termin']}")
    
    def wyswietl_notatki(self, notatki: List[Dict]) -> None:
        if not notatki:
            print("Brak notatek do wyświetlenia.")
            return
        
        print("\nLista notatek:")
        for i, notatka in enumerate(notatki, 1):
            print(f"\n{i}. Tytuł: {notatka['tytul']}")
            print(f"   Treść: {notatka['tresc']}")
            print(f"   Data utworzenia: {notatka['data_utworzenia']}")
    
    def pobierz_dane_zadania(self) -> tuple:
        tytul = input("Podaj tytuł zadania: ")
        opis = input("Podaj opis zadania: ")
        termin = input("Podaj termin (opcjonalnie, wciśnij Enter aby pominąć): ").strip()
        return tytul, opis, termin if termin else None
    
    def pobierz_dane_notatki(self) -> tuple:
        tytul = input("Podaj tytuł notatki: ")
        tresc = input("Podaj treść notatki: ")
        return tytul, tresc

class AsystentOsobisty:
    def __init__(self, interfejs: InterfejsUzytkownika):
        self.interfejs = interfejs
        self.zadania: List[Dict] = []
        self.notatki: List[Dict] = []
        self.plik_zadania = "zadania.json"
        self.plik_notatki = "notatki.json"
        self.wczytaj_dane()

    def wczytaj_dane(self):
        """Wczytuje zapisane dane z plików JSON."""
        if os.path.exists(self.plik_zadania):
            with open(self.plik_zadania, 'r', encoding='utf-8') as f:
                self.zadania = json.load(f)
        if os.path.exists(self.plik_notatki):
            with open(self.plik_notatki, 'r', encoding='utf-8') as f:
                self.notatki = json.load(f)

    def zapisz_dane(self):
        """Zapisuje dane do plików JSON."""
        with open(self.plik_zadania, 'w', encoding='utf-8') as f:
            json.dump(self.zadania, f, ensure_ascii=False, indent=2)
        with open(self.plik_notatki, 'w', encoding='utf-8') as f:
            json.dump(self.notatki, f, ensure_ascii=False, indent=2)

    def dodaj_zadanie(self, tytul: str, opis: str, termin: str = None):
        """Dodaje nowe zadanie do listy."""
        zadanie = {
            "tytul": tytul,
            "opis": opis,
            "termin": termin,
            "status": "do zrobienia",
            "data_utworzenia": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.zadania.append(zadanie)
        self.zapisz_dane()
        print("Zadanie zostało dodane!")

    def dodaj_notatke(self, tytul: str, tresc: str):
        """Dodaje nową notatkę."""
        notatka = {
            "tytul": tytul,
            "tresc": tresc,
            "data_utworzenia": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.notatki.append(notatka)
        self.zapisz_dane()
        print("Notatka została dodana!")

    def uruchom(self):
        """Główna pętla aplikacji"""
        while True:
            self.interfejs.wyswietl_menu()
            wybor = self.interfejs.pobierz_wybor()
            
            if wybor == "1":
                tytul, opis, termin = self.interfejs.pobierz_dane_zadania()
                self.dodaj_zadanie(tytul, opis, termin)
            
            elif wybor == "2":
                self.interfejs.wyswietl_zadania(self.zadania)
            
            elif wybor == "3":
                tytul, tresc = self.interfejs.pobierz_dane_notatki()
                self.dodaj_notatke(tytul, tresc)
            
            elif wybor == "4":
                self.interfejs.wyswietl_notatki(self.notatki)
            
            elif wybor == "5":
                print("Do widzenia!")
                break
            
            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")

def main():
    interfejs = InterfejsKonsolowy()
    asystent = AsystentOsobisty(interfejs)
    asystent.uruchom()

if __name__ == "__main__":
    main()
