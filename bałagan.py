import os
import shutil
from threading import Thread, Lock
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time

class FileOrganizer:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.extensions = {}
        self.lock = Lock()
        self.queue = Queue()
        
    def scan_directory(self, directory):
        """Skanuje katalog w poszukiwaniu plików i dodaje je do kolejki."""
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    self.queue.put(entry.path)
                elif entry.is_dir():
                    self.scan_directory(entry.path)
        except PermissionError:
            print(f"Brak dostępu do katalogu: {directory}")
            
    def process_file(self, file_path):
        """Przetwarza pojedynczy plik."""
        try:
            _, extension = os.path.splitext(file_path)
            extension = extension.lower()
            if extension:
                with self.lock:
                    if extension not in self.extensions:
                        self.extensions[extension] = []
                    self.extensions[extension].append(os.path.basename(file_path))
        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {file_path}: {e}")

    def worker(self):
        """Funkcja wykonywana przez wątek - przetwarza pliki z kolejki."""
        while True:
            try:
                file_path = self.queue.get_nowait()
                self.process_file(file_path)
                self.queue.task_done()
            except:
                break

    def organize(self, num_threads=None):
        """Główna metoda organizująca pliki z wykorzystaniem wielu wątków."""
        if num_threads is None:
            num_threads = os.cpu_count() * 2  # Domyślnie 2 wątki na rdzeń
            
        print(f"Rozpoczynam skanowanie katalogu: {self.source_dir}")
        start_time = time.time()
        
        # Skanowanie katalogu i dodanie plików do kolejki
        self.scan_directory(self.source_dir)
        total_files = self.queue.qsize()
        print(f"Znaleziono {total_files} plików do przetworzenia")
        
        # Utworzenie i uruchomienie wątków
        threads = []
        for _ in range(num_threads):
            thread = Thread(target=self.worker)
            thread.start()
            threads.append(thread)
            
        # Oczekiwanie na zakończenie wszystkich wątków
        for thread in threads:
            thread.join()
            
        end_time = time.time()
        print(f"\nCzas wykonania: {end_time - start_time:.2f} sekund")
        
        # Wyświetlenie podsumowania
        print("\nPodsumowanie znalezionych plików według rozszerzeń:")
        for ext, files in sorted(self.extensions.items()):
            print(f"{ext}: {len(files)} plików")
            
    def create_extension_lists(self, output_dir):
        """Tworzy pliki tekstowe z listami plików dla każdego rozszerzenia."""
        os.makedirs(output_dir, exist_ok=True)
        
        for ext, files in self.extensions.items():
            ext = ext[1:] if ext.startswith('.') else ext
            output_file = os.path.join(output_dir, f"files_{ext}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                for file in sorted(files):
                    f.write(f"{file}\n")
        
        print(f"\nUtworzone listy plików zostały zapisane w katalogu: {output_dir}")

if __name__ == "__main__":
    # Przykład użycia:
    source_directory = "Balagan"  # Ścieżka do folderu "Balagan"
    output_directory = "ListyPlikow"  # Katalog na listy plików
    
    organizer = FileOrganizer(source_directory)
    organizer.organize()
    organizer.create_extension_lists(output_directory)
