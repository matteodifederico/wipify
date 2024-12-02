import os
import random
import shutil

def generate_random_data(size):
    """Genera dati casuali della dimensione specificata."""
    return os.urandom(size)

def wipe_file(file_path, passes=3):
    """Sovrascrive un file con dati casuali e poi lo elimina."""
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'wb') as file:
            for pass_num in range(passes):
                print(f"Passaggio {pass_num + 1}/{passes} per il file: {file_path}")
                file.write(generate_random_data(file_size))
                file.flush()
                os.fsync(file.fileno())  # Forza la scrittura su disco
        
        os.remove(file_path)
        print(f"File eliminato in modo sicuro: {file_path}")
    except Exception as e:
        print(f"Errore durante il wiping del file {file_path}: {e}")

def wipe_directory(directory_path, passes=3):
    """Sovrascrive tutti i file in una directory e poi elimina la directory."""
    try:
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                wipe_file(file_path, passes)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
        shutil.rmtree(directory_path)
        print(f"Directory eliminata in modo sicuro: {directory_path}")
    except Exception as e:
        print(f"Errore durante il wiping della directory {directory_path}: {e}")

def wizard():
    print(r"""
         __      __.__       .__  _____       
        /  \    /  \__|_____ |__|/ ____\__.__.
        \   \/\/   /  \____ \|  \   __<   |  |
         \        /|  |  |_> >  ||  |  \___  |
          \__/\  / |__|   __/|__||__|  / ____|
               \/     |__|             \/     
                
        """)
    print("Questo strumento permette di eliminare file o directory in modo sicuro e definitivo.")
    
    while True:
        mode = input("Vuoi cancellare un file o una directory? (file/directory): ").strip().lower()
        if mode in ['file', 'directory']:
            break
        print("Scelta non valida. Digita 'file' o 'directory'.")
    
    path = input(f"Inserisci il percorso del {mode} da eliminare: ").strip()
    if not os.path.exists(path):
        print(f"Errore: il percorso '{path}' non esiste.")
        return
    
    passes = input("Quanti passaggi di sovrascrittura vuoi effettuare? (default: 3)\n[3 Sicuro, 5 Molto Sicuro, 10 Estremeamente Sicuro]: ").strip()
    passes = int(passes) if passes.isdigit() and int(passes) > 0 else 3

    if mode == 'file':
        if os.path.isfile(path):
            wipe_file(path, passes)
        else:
            print(f"Errore: il percorso '{path}' non è un file.")
    elif mode == 'directory':
        if os.path.isdir(path):
            wipe_directory(path, passes)
        else:
            print(f"Errore: il percorso '{path}' non è una directory.")

if __name__ == "__main__":
    wizard()
