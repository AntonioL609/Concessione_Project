def Modifica_moto(df):
    
   # Chiedi all'utente il modello da modificare
    modello = input("Inserisci il modello della moto da modificare: ")
    
    # Filtra il DataFrame per il modello scelto
    risultato = df[df["Modello"] == modello]
    
    if not risultato.empty:
        print(f"Dati attuali per il modello {modello}:")
        print(risultato)
        
        # Chiedi all'utente quale colonna vuole modificare
        colonna = input("Quale colonna vuoi modificare? (Marca, Anno, Modello, Disponibile, Prezzo, Quantità): ")
        
        if colonna in df.columns:
            # Chiedi il nuovo valore
            nuovo_valore = input(f"Inserisci il nuovo valore per {colonna}: ")
            
            # Verifica il tipo di dato e aggiorna il DataFrame
            if colonna == "Prezzo" or colonna == "Quantità" or colonna == "Anno":
                # Converti a intero o float se necessario
                nuovo_valore = int(nuovo_valore)
            
            # Modifica il valore nel DataFrame
            df.loc[df["Modello"] == modello, colonna] = nuovo_valore
            
            # Riscrivi il file CSV con i dati aggiornati
            df.to_csv("concessionario_moto.csv", index=False)
            print(f"Il modello è stato aggiornato correttamente.")
        else:
            print("Colonna non valida. Riprova.")
    else:
        print(f"Il modello non è presente nel file.")

        

def Moto_vendute(df):
    # Variabile per memorizzare i risultati totali
    totale_moto_vendute = 0

    while True:
        # Mostra i modelli disponibili per la vendita
        print("Modelli disponibili:")
        print(df[df["Disponibile"] == "Si"][["Modello", "Quantità"]])
    
        # Inserisci il modello venduto o termina
        modello_venduto = input("Inserisci il modello venduto o scrivi 'fine' per terminare: ")
        if modello_venduto.lower() == "fine":
            break
    
        # Filtra il DataFrame per trovare il modello
        risultato = df[df["Modello"] == modello_venduto]
    
        if not risultato.empty:
            # Verifica se la moto è disponibile
            if risultato["Disponibile"].iloc[0] == "Si":
                quantita_disponibile = risultato["Quantità"].iloc[0]
            
                # Chiedi la quantità venduta
                quantita_venduta = int(input("Quante moto sono state vendute? "))
            
                # Controlla se c'è abbastanza disponibilità
                if quantita_venduta <= quantita_disponibile:
                    # Aggiorna la quantità nel DataFrame
                    df.loc[df["Modello"] == modello_venduto, "Quantità"] -= quantita_venduta
                
                    # Aggiorna il totale delle vendite
                    totale_moto_vendute += quantita_venduta
                
                    print(f"Vendute {quantita_venduta} moto del modello {modello_venduto}.")
                else:
                    print(f"Quantità insufficiente per la vendita. Disponibili solo {quantita_disponibile} moto.")
            else:
                print("La moto non è disponibile per la vendita.")
        else:
            print("Moto inesistente!")
    # Salva il DataFrame aggiornato in un file CSV
    df.to_csv("concessionario_moto.csv", index=False)   


    

 



    
    




        

