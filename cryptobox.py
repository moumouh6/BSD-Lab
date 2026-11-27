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

# ─── Vigenère ─────────────────────────────────────────────────────────────────

def vigenere_chiffrer(msg, cle):
    cle = cle.upper()
    res = []
    ki = 0
    for c in msg:
        if c.isalpha():
            k = ord(cle[ki % len(cle)]) - ord('A')
            res.append(chr((ord(c.upper()) - ord('A') + k) % 26 + ord('A')))
            ki += 1
        else:
            res.append(c)
    return ''.join(res)

def vigenere_dechiffrer(msg, cle):
    cle = cle.upper()
    res = []
    ki = 0
    for c in msg:
        if c.isalpha():
            k = ord(cle[ki % len(cle)]) - ord('A')
            res.append(chr((ord(c.upper()) - ord('A') - k) % 26 + ord('A')))
            ki += 1
        else:
            res.append(c)
    return ''.join(res)

def vigenere_casser(texte_chiffre, longueur_cle):
    """Retrouve la clé par analyse de fréquence (E = lettre la plus fréquente)."""
    lettres = [c for c in texte_chiffre.upper() if c.isalpha()]
    cle = []
    for col in range(longueur_cle):
        colonne = lettres[col::longueur_cle]
        freq = [0] * 26
        for c in colonne:
            freq[ord(c) - ord('A')] += 1
        lettre_max = freq.index(max(freq))
        decalage = (lettre_max - (ord('E') - ord('A'))) % 26
        cle.append(chr(ord('A') + decalage))
    return ''.join(cle)

# ─── Tests de validation ──────────────────────────────────────────────────────

def tests_vigenere():
    print("=== Tests Vigenère ===")
    r = vigenere_chiffrer("ATTAQUE A L'AUBE", "CLE")
    attendu1 = "CEXCBYG A L'CFFG"
    print(f"Vigenère chiffrer : {r}  {'OK' if r == attendu1 else 'ERREUR attendu ' + attendu1}")
    r = vigenere_chiffrer("LA CLE, 14H", "TP")
    print(f"Vigenère chiffrer : {r}  {'OK' if r == 'EP VAX, 14W' else 'ERREUR (attendu EP VAX, 14W)'}")
    r = vigenere_dechiffrer("CEXCBYG A L'CFFG", "CLE")
    attendu3 = "ATTAQUE A L'AUBE"
    print(f"Vigenère déchiffrer : {r}  {'OK' if r == attendu3 else 'ERREUR'}")
    print()

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

def challenge_tp2():
    print("=== Challenge TP2 · Groupe 5 ===\n")

    # --- Challenge 1 : Flag Vigenère (clé : OLYJUZCZY) ---
    msg1 = "PLJZTQLZ"
    cle1 = "OLYJUZCZY"
    flag1 = vigenere_dechiffrer(msg1, cle1)
    print(f"Challenge 1 — Vigenère déchiffré (clé {cle1}) : {flag1}\n")

    # --- Challenge 2 : Flag casseur (longueur clé = 7) ---
    texte2 = """EJQNCCM SJV CKTVAJV, VGH TGRHOU DGI HRXHXX AJXBU DKSWHC C SXH
RHCUPZTWV. VG GBHVXO GITXY WYWYHJWV VG BXBJ : VS NT FTXVKITK
TYDSV RTEYXBG, A'XCSHWK ABHFLD VDNI. QHC ITGTWDEZ DGI IRXE
PIEWLC C RTRMHB NT LTSV NG AXJWV WGHLPLHC. CJ WTGXD, QC LT
HRXVTGIFLD FT WTHDVGG ETX OOVIKTX GO N'PEEMDLGI, VDRPO NT
YPNVKKI CJQHC ETLPW. FOVIX BJWRQSX HZIPKHTXY FYPIKT ZQ
KFKXGXDSTT JJN QO UPOPNW ZCH EXWH, WCXL TQOO FTOTSDSV UKPLLVG
SXH VXO N'TGCJPS EDFEYDSV AXH QHDVGXH. QHC UPOPSWC CGTQJV NW
CXJALOOT LXJFVG POPNHXV SXYF UOOPKFZH AWT VWFTEG ATCLXO WIBANVO
ETKIFLXGH ETYWBGH UXJQ ZNJL HTXFGCM FZH VGH TJYUOU. POTH FOVIX
HNPZNT HQXHBXPMXTQ, SNH IDZYKKTGI HDCUTK AF SVWETGY GOU
RAXKIBGBXCYV NG AXJW HZQFNT. NO K HPEAZ DDVTGSWH VC GXCFLCUPGRJ
SYWG JJJ GOU RAXKIBGBXCYV ZNJL HTOSFTL PUSKTPBHXHXV TG TZUYRT.
NC GRX ODM SJ SKUHX STLD GIKT QRXI, XFEWHFKHBQQH OV SBUKHBGCM
ETXB EWTFZH CGGOXHH. VG EKDGOOOT XHY TEG AT BJPYKGX WZPKKCX
EWHPGGX AJV WQIL HNPZNTL, AJV NCIXH IH XCXLHFQMG TM AJV ZTTGDRV.
VGH TIYDAWPGIX OO UPOTSW DTTL QNHX. NDKHVX'SNH KTHXZGGXCY XXG
QTHJ GO FDGCJHC XDETJ, LVU RHBRHXETGI UDB GHLPDHB NTL BTWC FT
IPXVO NTL EQXC EDNGFQDU, ENXX OOU KTGNDXVTL PAHM FTL RMLPHGXH F
OK HXG. JSH QTPGSJ SKTIBT IHC EDFEYHC VDFQJ HX SJXAVXOU BBCZWOU.
EHJW VO RGHIJJOT, DG EJXD WIBANVOT JG VJVDKDGCFLBG SX BTWC FT
IPXVO, SJB GJWSGCM ETXB PDNH IHC UJBIJV NG RTGFFDGGXH
FOOCIHXWHC. KA LJKISV PEDWV NG GXIJQST JG HJXV ODM SJ SKUHX
EWLXEXIPQ, WBGH EDSJ, OV S'TRYLFGG EP AHBKUBRFWSQC XC IHEZ
TMPUHC RPKITXD QJ XAQH OUI IGTSYUTX. AJV MNTL SJ FRKUYGJPOPI
KTXVOOQETSW KWM VAJV N'WCX BFLCQC. NCJ SYTIX QQLXFTX CJ SBQIXVJ
USGC LX QD MNT KTXWO UDNH QH ZCXEAFVCQC. XC NQPQGFPYLAWT,
E'TWUOWG EP UOEU UKTVXOPIX RTQCKHMT F HMTXKT ZQO EAX SNUOEIXBJQD
FPGH QH MQSX SZ SBQVKPRPO. NT VDIH OUI XCXXSVT IPWWKIT TKJF NGH
VDQOOIJXH, HRZKT LJW XX UTKKJXB QJ IJGOSG ETG JUBGJK HZU
SPIXGSHD. FTL GTEYVH IPWFYWGXCY HX RTKBFQOPRX AJV NGEHIX SEDABRX
D VC GXRMHBEWX SJ FOU RETX REDABTJV OV AXH ZWSNXLTSW OP FNTQTEGH
FXSXDGH. ETX EYPCXH UUKVXJJJV CQCM ETXBVPGI HRXPJXH : LDBFTK AJV
MNTL SFQC FTL UNFRKTKH XHZCGXH TX NCCL JS FYHUKT-KRBV CNBJUSSJX,
ANPSVTK AJV ZGGLDSQOU FNX D RXV PVRJV OV RAPSJOT XFBJGSCIXBJQD
WCX RQH NGH JJJ O'YP HHJUFYPCX FZ'HVNT T EZ HDTT XMURCGT. EP
GLLNXHIMHAWT WT Q'XXKKXGXLDG DNKWH CGH IDWWOU P AJNW RGJKTX. GOU
AXH UUOOXXGJV WKCNIJV, VGH XIZGSCCMH XH ZTTVXULDGCM KJUC NTL
BJLVNTNGJV ZNPVTX, FONAXH VXS UDGI UUYEWXH IHC RGBHJV
ONTVIWLAWTL TY OYKC WT Q'HXVGXT. TQ I GCMTSG CWGMDZW VG QKJNW
NGH IPLHC SJX A'TQ DQJKCJ HD ETEJN GOU REPALOTH. ITSGKPI EP
UHBKDWT IHC GMTBJQC, KA WTALOPI WXKISEXET IH DTDNKJU EPT VWFLCG
ABQWH KRGXH ILH JTNGJV. MGGMPNQC GINSNDXVH IGJIOTTGI YUKXPBAQHB
GC ZGTXZG STCX OOU HTAQHC FJ WTZASGBX TYDQG, DN A'TQ ZGJM EFUVGG
T KTLH DPLHJ. G'KWIKTX UOUIXCY VOWAL, PAHM NTNGX HMQJMTZUC, GI
GT QHFGCM EFV VC IXIJ SOPSTCY GOU WXJWHC. NT LDNU, VG EXGXRXPTE
UFLD NT MDZU NGH MPGOOU EHJW UKREXAJU AWT EP KHBOTMJWH KREKDHKO
GI JJJ OOU ABKWHC FDBKJQD GIKT WHXFJL."""
    cle2 = vigenere_casser(texte2, 7)
    print(f"Challenge 2 — Clé trouvée (L=7) : {cle2}")
    dechiffre2 = vigenere_dechiffrer(texte2, cle2)
    print(f"Début du texte déchiffré : {dechiffre2[:120]}\n")

    # --- Bonus : longueur inconnue ---
    texte3 = """HY GVI PECJEY UV PLWHCOI JRIQJ J'BVLEB GP QYCFA IG PCGGJ. YB
OWRCE, VYIG AQN JFHSGJR WRCZB GP NLVJDRG PPUEJCXTALNV GEBU ZS
LZMNDG. HCM GVPEGQPM IVAQTALN RL CLTP YPVT YBWNQ WRZFPGO BY
JREAKJCM VK IBPZCHK CRRT LMCJJBK FEPYTKRJGJR MLI YB SQYC.
C'RCOGO-KCUZ, YB XALN JV YBXA CN CVF SCCSYJ URSKALHVEG MNQQ
ZFIGBU. HCM WRZFNHCM J'ZAPVWJFVEG PWN JU GCNDG, HCM VESXPPQ
WFEFQTQGMVEG AGO ABRKRXWT BY JROIG AR FVJ CIWO AILINDGQV MV
SNFIJCHK DNIINC F'VRH CTWGWYV. YB UKGL, CV FLNAGF UVFZGJB
FVEGBOALN UVEOKAPY CVF OQYFYIJ RQ NA ACVC QBXECHK FEXPCC, JLZF
SKKJYK. CRP EWDYJ UH YQNB XV DRO UA PYDGYFUOCHK, FA ZQIKUEUR RP
PFY R CN JGJRBV VG LP NCARIQB NAQ FLDVBTAQ XVJ OXVAYOO HHF
RWPNVEG MQQP FR EHFV. HC ZFFGYCHJ ITTHMG QLY GCNZG EKGVEFB FWLM
CR IFG ZS KLREQKAP. WYRDRG OMCI, URP SQC FR TUXNASL UZZFPQC, FVJ
WBWJCM JV EBVNMOMVAQ UQP FV KROTWGH MRTRG ZCLIZROG H'CWFCR. LP
PPUTV YBU XSNJ RIBE ZCOO GVBTNCM, FE SLTIC FVJ RNWENYJ VA
NWAJKLVF PGYMHUVF BV HY JRIGFG YMGDVAZG. HCM GCHP CCCM AFHBPP
JYJ REYKPPYJ VG ZQIKYEKRKV YFUHLR XEPGIE RIBE LYMJZBK. NAQ DFLEP
FA ELREQ JCPAB, CVF OWAQ MV MVAGJR. NFLG IG IMHUV FB TASHZK
QBXWLN CVF BENYHJ URP EWDYJ FH ZJAX OE MBFUEL KLZ CLUOCXV LAB
INYHUV GBNATCJZBK. CLPYJ LAB XEANFZEB, NAQ ECRKLPO PYJFAKGJR
DLJDRG PYLU UNKU HY HLZG. XRNCM LER AGBYCKV, BK TADUZK YB OWRWY
GRKFWLN UVF EGQPYJ, VA ZJAPWYRAQ NA HILVHO TAQJFEFXDHC YK VA
FOWECERAQ EA OOZ RHOCER JL JR MCOQYI. CR QTWGH UV ARKP OOZKGB NW
EUIV HK RAS UMRAQ XELAK-URRZ DCOIVF. IGO TIPRTBWNQ M'ZEFQCHJYEK
QXPO JYJ TBJRWPNZDRKVO, PUEXRKV HCOIJ IXNEQYJ VG PQNRYEK HK
NETLV FH AG MSIZ DNKIAP. JVEQXPP JYJ GEBOECLVJ UBWNCM, FE
QFUYSNV RIBE OCM MFVPKJQ, IE IRDCNBY CVF IWIGYIVF AGO TCCCRP SQG
XVWVIGJR XVIEFGNC FR WRKGPPY. GLVP NA AUCDR P'KJQNRCYB. QJ
L'YEKRKF LJOJ HHB NA ZLLZG OGCSFZVE AGO PILVF PWN JYJ INFNO. YO
GVGFV IYNZE, YB RWWMRXR X EDYHXV : YBU LJUZERP QJR FRZFPG HY
JCRPB CQV WFCYFPAQ, YK C'NFT OCGSCR MNQQ ZIRVP. NAQ JRJFXIAPM JV
EBXAGFCVAQ NALNVDRKV, AABRETBPP SH JFHOKNC ZRKVDWA CN JV
COGLYLVEG MQQP F'RIEFXAC. VVRHZQQN JIVSBTALN TV ILAWEY CVAQ C
H'YPZFA, MCNAY HL'VI FKLHV MEXKICHK CR PGJRCDVAQ FA NUIKVO NKGH.
CV QBUAPN E'VFQ RWQ PZUR, ZQJRLRZEBOALN R TR NWA NYEJRKV YCOO
HHF PA J'IEK WXOWGM KINSGNQY. CR ARKP, JU KVZMGNYNLIR ZJQRY
SIHQCHCGVEG BV HC WZVY PG YMOMIR A'GPMCCVF NWA J'IE ER SQER
DRDNFU AL PZCYB. NAQ XLERP EDYHXVAQ FA DIIDR XXAA FV MRKV, OG
VZVA NWA JY GRLPCCC H'VJG GCIYCJ KBRV W DUZK YB OAKY U'LAB
UAKUZER X N'WSNIV. YBU WLWZVAP UWTUZVAQ UA EOZURO INYWV RHU
GPMCCVF BV W JU UZEBEPGIE UH PCXJY. ZCF ZQJLUZJFXKALN TYNNWA
NOZKF, ZJWOOV FNPKO CN TYNNWA NUJJNDG ALNIV YBU IMHKRTKGO BY
GZROTA. YOAFHOF'DSC VEPLTA, JYJ MBVCCCOIJ COWZCHKJ CXTPCHK RIBE
XCULTBRR Z'CUL, GEBXECHEVAQ SQCFHL'HK FA JYLI VQKJCLRZEB GP
CPZKRKV ZC LFLYBT LCHURAQ NAQ BVLEBU HCM GCHP EDYOUVF AG HY
DFLEKGA."""

    print("Bonus — Recherche longueur de clé (L=2 à 10) :")
    for L in range(2, 11):
        cle_b = vigenere_casser(texte3, L)
        debut = vigenere_dechiffrer(texte3, cle_b)[:80]
        print(f"  L={L} clé={cle_b} → {debut}")

if __name__ == "__main__":
    tests_vigenere()
    tests()
    challenge()
    challenge_tp2()
