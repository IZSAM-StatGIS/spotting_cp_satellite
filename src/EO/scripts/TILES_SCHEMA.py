def selectImages(regione):
    # Tiles per region
    if regione == 'Abruzzo':
        return ['R122_T33TUG', 'R122_T33TUH', 'R079_T33TVG', 'R122_T33TVH']
    elif regione == 'Sardegna':
        return ['R022_T32SMJ', 'R022_T32SNJ', 'R022_T32TMK', 'R065_T32TML',	'R022_T32TNK', 'R022_T32TNL']
    elif regione == 'Puglia':
        return ['R079_T33TWF', 'R079_T33TWG', 'R036_T33TXE', 'R036_T33TXF', 'R036_T33TYE', 'R036_T33TYF']
    elif regione == 'Bolzano':
        return ['R022_T32TPS', 'R065_T32TPT', 'R022_T32TQT']
    elif regione == 'Calabria':
        return ['R036_T33SWC', 'R079_T33SWD', 'R036_T33SXC', 'R036_T33SXD']
    elif regione == 'Campania':
        return ['R079_T33TVE', 'R079_T33TVF', 'R079_T33TWE']
    elif regione == 'Emilia_Romagna':
        return ['R065_T32TNQ', 'R022_T32TPQ', 'R022_T32TQP', 'R022_T32TQQ']
    elif regione == 'Friuli':
        return  ['R022_T33TUM', 'R122_T33TVL']
    elif regione == 'Lazio':
        return ['R022_T32TPM', 'R122_T33TTF', 'R122_T33TTG', 'R122_T33TUF']
    elif regione == 'Lombardia':
        return ['R065_T32TMR', 'R065_T32TMS', 'R065_T32TNR', 'R065_T32TNS']
    elif regione == 'Umbria_Marche':
        return ['R122_T33TUJ', 'R122_T32TQN']
    elif regione == 'Piemonte':
        return ['R108_T32TLP', 'R108_T32TLQ', 'R108_T32TLR', 'R108_T32TLS', 'R065_T32TMP', 'R065_T32TMQ']
    elif regione == 'Sicilia':
        return ['R122_T33STV',	'R122_T33STA', 'R122_T33STB', 'R122_T33STC', 'R079_T33SUB', 'R079_T33SUC', 'R079_T33SUV', 'R079_T33SVA', 'R079_T33SVB',	'R079_T33SVC', 'R036_T33SWA', 'R036_T33SWB']
    elif regione == 'Toscana':
        return ['R022_T32TNM',	'R022_T32TNN', 'R065_T32TNP', 'R022_T32TPN', 'R022_T32TPP']
    elif regione == 'Veneto':
        return ['R022_T32TPR', 'R022_T32TQR', 'R022_T32TQS', 'R122_T33TUK', 'R122_T33TUL']