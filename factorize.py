import time
from multiprocessing import Pool, cpu_count

def factorize_sync(number):
    """
    Znajduje wszystkie liczby, przez które podana liczba jest podzielna bez reszty.
    Wersja synchroniczna.
    """
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize(*numbers):
    """
    Znajduje wszystkie liczby, przez które podane liczby są podzielne bez reszty.
    """
    return [factorize_sync(num) for num in numbers]

def factorize_parallel(*numbers):
    """
    Znajduje wszystkie liczby, przez które podane liczby są podzielne bez reszty.
    Wersja równoległa wykorzystująca wiele rdzeni procesora.
    """
    with Pool(cpu_count()) as pool:
        return pool.map(factorize_sync, numbers)

if __name__ == '__main__':
    # Test wydajności
    numbers = (128, 255, 99999, 10651060)
    
    # Test wersji synchronicznej
    start_time = time.time()
    a, b, c, d = factorize(*numbers)
    end_time = time.time()
    sync_time = end_time - start_time
    print(f"Czas wykonania wersji synchronicznej: {sync_time:.2f} sekund")
    
    # Test wersji równoległej
    start_time = time.time()
    a, b, c, d = factorize_parallel(*numbers)
    end_time = time.time()
    parallel_time = end_time - start_time
    print(f"Czas wykonania wersji równoległej: {parallel_time:.2f} sekund")
    print(f"Przyspieszenie: {sync_time/parallel_time:.2f}x")
    
    # Testy poprawności
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("Wszystkie testy przeszły pomyślnie!")
