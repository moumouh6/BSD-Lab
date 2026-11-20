#!/usr/bin/env python3
"""
CryptoBox - Brique 1
Implémente : César, Substitution, Transposition par colonnes
"""

# ─── César ────────────────────────────────────────────────────────────────────

def cesar_chiffrer(msg, k):
    return ''.join(chr((ord(c) - ord('A') + k) % 26 + ord('A')) for c in msg)

def cesar_dechiffrer(msg, k):
    return cesar_chiffrer(msg, -k)

def cesar_brute_force(msg):
    results = []
    for k in range(1, 26):
        results.append((k, cesar_dechiffrer(msg, k)))
    return results

# ─── Substitution ─────────────────────────────────────────────────────────────

def subst_chiffrer(msg, cle):
    # cle[i] remplace la lettre i (A=0, B=1, …)
    return ''.join(cle[ord(c) - ord('A')] for c in msg)

def subst_dechiffrer(msg, cle):
    # table inverse
    inv = [''] * 26
    for i, lettre in enumerate(cle):
        inv[ord(lettre) - ord('A')] = chr(ord('A') + i)
    return ''.join(inv[ord(c) - ord('A')] for c in msg)

# ─── Transposition par colonnes ───────────────────────────────────────────────

def _ordre_colonnes(mot_cle):
    """Retourne l'ordre de lecture des colonnes (indices triés par lettre du mot-clé)."""
    return sorted(range(len(mot_cle)), key=lambda i: mot_cle[i])

def transpo_chiffrer(msg, mot_cle):
    n = len(mot_cle)
    # Compléter avec X
    while len(msg) % n != 0:
        msg += 'X'
    nb_lignes = len(msg) // n
    # Grille
    grille = [list(msg[i*n:(i+1)*n]) for i in range(nb_lignes)]
    ordre = _ordre_colonnes(mot_cle)
    # Lire chaque colonne dans l'ordre
    return ''.join(grille[ligne][col] for col in ordre for ligne in range(nb_lignes))

def transpo_dechiffrer(msg, mot_cle):
    n = len(mot_cle)
    nb_lignes = len(msg) // n
    ordre = _ordre_colonnes(mot_cle)
    # Reconstruire la grille colonne par colonne
    grille = [['' ] * n for _ in range(nb_lignes)]
    pos = 0
    for col in ordre:
        for ligne in range(nb_lignes):
            grille[ligne][col] = msg[pos]
            pos += 1
    return ''.join(grille[ligne][col] for ligne in range(nb_lignes) for col in range(n))

# ─── Tests de validation ──────────────────────────────────────────────────────

def tests():
    print("=== Tests de validation ===")
    # César
    r = cesar_chiffrer("BONJOUR", 3)
    print(f"César chiffrer BONJOUR k=3 : {r}  {'OK' if r == 'ERQMRXU' else 'ERREUR'}")
    r = cesar_dechiffrer("ERQMRXU", 3)
    print(f"César déchiffrer ERQMRXU k=3 : {r}  {'OK' if r == 'BONJOUR' else 'ERREUR'}")
    # Substitution
    cle_s = "QWERTYUIOPASDFGHJKLZXCVBNM"
    r = subst_chiffrer("ATTAQUE", cle_s)
    print(f"Subst chiffrer ATTAQUE : {r}  {'OK' if r == 'QZZQJXT' else 'ERREUR'}")
    r = subst_dechiffrer("QZZQJXT", cle_s)
    print(f"Subst déchiffrer QZZQJXT : {r}  {'OK' if r == 'ATTAQUE' else 'ERREUR'}")
    # Transposition
    r = transpo_chiffrer("RENDEZVOUSAMIDI", "PORTE")
    print(f"Transpo chiffrer RENDEZVOUSAMIDI : {r}  {'OK' if r == 'ESIEVMRZANOIDUD' else 'ERREUR'}")
    r = transpo_dechiffrer("ESIEVMRZANOIDUD", "PORTE")
    print(f"Transpo déchiffrer ESIEVMRZANOIDUD : {r}  {'OK' if r == 'RENDEZVOUSAMIDI' else 'ERREUR'}")
    print()

# ─── Challenge binôme 05 ──────────────────────────────────────────────────────

def challenge():
    print("=== Challenge binôme 05 ===")
    msg = "VQUCHCAKFT"
    cle_subst = "WQINTALMVYHJORKBUXPDSGZCFE"
    mot_cle_transpo = "NUAGE"

    print(f"Message chiffré : {msg}")
    print()

    # Couche 3 → retirer Substitution
    apres_subst = subst_dechiffrer(msg, cle_subst)
    print(f"Après déchiffrement Substitution : {apres_subst}")

    # Couche 2 → retirer Transposition
    apres_transpo = transpo_dechiffrer(apres_subst, mot_cle_transpo)
    print(f"Après déchiffrement Transposition : {apres_transpo}")

    # Couche 1 → force brute César
    print("\nForce brute César :")
    for k, texte in cesar_brute_force(apres_transpo):
        print(f"  k={k:2d} : {texte}")

    print()

if __name__ == "__main__":
    tests()
    challenge()
