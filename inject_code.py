import sys
import time

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("Veuillez patienter, installation des dépendances en cours...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pyperclip"])
    import pyautogui
    import pyperclip

def main():
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print("Erreur:", e)
        sys.exit(1)

    print("==================================================")
    print(" INJECTION AUTOMATIQUE CONTRE LES CRASH SÉCURISÉE")
    print("==================================================")
    print("ATTENTION: VOUS AVEZ 8 SECONDES !!!")
    print("1. CLIQUEZ GAUCHE DIRECTEMENT DANS LE CADRE DU TERMINAL WOKWI.")
    print("2. ASSUREZ-VOUS QUE VOTRE SOURIS/CURSEUR CLIGNOTE À CÔTÉ DU '>>>'.")
    print("3. LACHEZ LA SOURIS ET ATTENDEZ.")
    
    for i in range(8, 0, -1):
        print(f"[{i} secondes...] Cliquez sur >>>")
        time.sleep(1)

    print("\n[!] INJECTION EN COURS... NE TOUCHEZ PLUS À RIEN !")

    # 1. Entrer en mode Paste (Ctrl+E) pour MicroPython
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(1)

    # 2. Découper le code par LIGNES entières et non par de simples caractères 
    # pour ne pas couper un mot en plein milieu.
    lines = code.split('\n')
    chunk_size = 8 # On envoie 8 lignes par 8 lignes (très safe)
    
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i+chunk_size]
        chunk_text = '\n'.join(chunk_lines) + '\n'
        
        pyperclip.copy(chunk_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.25) # Temps de digestion par MicroPython

    # 3. Quitter et exécuter (Ctrl+D)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'd')
    
    print("\n✅ Terminé avec succès ! Votre code est envoyé proprement.")

if __name__ == '__main__':
    main()
