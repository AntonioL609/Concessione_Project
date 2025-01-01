import pandas as pd
import concession_project2 as prj
import matplotlib.pyplot as plt
from datetime import datetime

def Aggiungi_moto(df):
    # Richiesta del numero di moto da aggiungere
    counter = 0
    risposta = int(input("Quante moto vuoi aggiungere?"))

    while counter < risposta: 
        # Chiedi all utente le informazioni da inserire 
        anno = int(input("Inserisci l'anno della moto: "))
        marca = input("Inserisci la marca della moto: ")
        modello = input("Inserisci il modello della moto: ")
        diponibile=input("Inersici se è disponibile da subito (si/no): ")
        prezzo=int(input("Inserisci il prezzo della moto: "))
        quantita=int(input("Inserisi quante moto sono state acquistate: "))

        # Creazione di un dizionario con i dati inseriti
        nuovo_dizionario = {"Anno": [anno], "Marca": [marca], "Modello": [modello], "Disponibile":[diponibile], "Prezzo":[prezzo], "Quantità":[quantita]}
    
        # Creazione di un DataFrame con i dati della nuova moto
        nuovo_df = pd.DataFrame(nuovo_dizionario)
    
        # Aggiungere il nuovo DataFrame a quello esistente
        df = pd.concat([df, nuovo_df], ignore_index=True)

        counter += 1

    # Salvare il DataFrame aggiornato nel file CSV, sovrascrivendo quello esistente
    df.to_csv("concessionario_moto.csv", index=False)

    print("moto aggiunte con successo")

def Elimina_moto(df):
    # Chiedi all'utente di specificare la moto da eliminare
    modello = input("Inserisci il modello della moto da eliminare: ").strip().lower()

    # Verifica se il modello esiste nel DataFrame
    if not df['Modello'].str.lower().str.contains(modello).any():
        print(f"Il modello {modello} non è stato trovato.")
        return df
    
    # Filtra il DataFrame per rimuovere la moto specificata
    df = df[~df["Modello"].str.lower().str.contains(modello)]
    
    # Salva il DataFrame aggiornato nel file CSV, sovrascrivendo quello esistente
    df.to_csv("concessionario_moto.csv", index=False)

    print(f"La moto {modello} è stata eliminata correttamente.")
    return df


def Acquista_moto(df):
    # Chiedi all'utente di inserire il modello della moto
    modello = input("Inserisci il modello della moto per verificare la disponibilità e procedere all'acquisto: ").lower()

    # Trova la moto nel DataFrame (convertendo anche il DataFrame in minuscolo)
    risultato = df[df["Modello"].str.lower() == modello]  

    # Verifica se la moto è presente
    if not risultato.empty:
        # Mostra i dettagli della moto
        print("Moto trovata nel database!")
        print(risultato[["Marca", "Modello", "Anno", "Prezzo", "Quantità"]])
        
        # Verifica la disponibilità e la quantità della moto
        disponibilita = risultato.iloc[0]['Disponibile']
        quantita_disponibile = risultato.iloc[0]['Quantità']
        
        if disponibilita.lower() == "si":
            print(f"La moto {modello} è disponibile per l'acquisto.")
            conferma = input(f"Quantità disponibile: {quantita_disponibile}. Vuoi procedere con l'acquisto? (si/no): ").lower()
            
            if conferma == 'si':
                # Aggiorna la quantità disponibile
                df.loc[df['Modello'].str.lower() == modello, 'Quantità'] -= 1

                # Salva la vendita in un file separato
                data_vendita = datetime.now().strftime("%Y-%m-%d")
                vendita = {
                    "Modello": [modello],
                    "Marca": risultato.iloc[0]['Marca'],
                    "Anno": risultato.iloc[0]['Anno'],
                    "Prezzo": risultato.iloc[0]['Prezzo'],
                    "DataVendita": [data_vendita]
                }
                vendita_df = pd.DataFrame(vendita)
                
                # Controlla se esiste già un file delle vendite
                try:
                    vendite_df = pd.read_csv("vendite_moto.csv")
                    vendite_df = pd.concat([vendite_df, vendita_df], ignore_index=True)
                except FileNotFoundError:
                    vendite_df = vendita_df
                
                vendite_df.to_csv("vendite_moto.csv", index=False)

                # Salva il DataFrame aggiornato delle moto
                df.to_csv("concessionario_moto.csv", index=False)
                
                print(f"Hai acquistato con successo la moto!")
            else:
                print("Acquisto annullato.")
        else:
            print(f"La moto {modello} non è disponibile per l'acquisto.")
    else:
        print("Moto non trovata.")


def Verifica_disponibilita(df):
   # Chiedi all'utente il modello da cercare
    modello = input("Inserisci il modello della moto per verificare la disponibilità: ")
    
    # Filtra il dataframe per il modello
    risultato = df[df["Modello"].str.lower() == modello]
    
    # Controlla se il modello è stato trovato
    if not risultato.empty: # Se non è vuoto
        # Controlla se la moto è disponibile
        if risultato["Disponibile"].iloc[0] == 'Si':
            quantita = risultato["Quantità"].iloc[0]
            if quantita >= 0:
                print(f"La moto è disponibile. Quantità disponibile: {quantita}.")
            else:
                print(f"La moto è disponibile ma non ci sono pezzi in magazzino.")
        else:
            print(f"La moto non è disponibile.")
    else:
        print(f"Il modello non è presente nel file.")


def Verifica_utente_e_menu(df):
    # Imposta variabili di controllo
    controllo=True
    controllo2=True
    controllo3=True
    # Imposta username e password predefiniti
    Username="admin"
    Password="1234"
    # Chiedi se è un visitatore o un amministratore
    visitatore=input("sei un visitatore o un amministratore? ")
    while controllo:
        if visitatore.lower() == "amministratore":
            # Chiede all amministratore username e password 
            username=input("inserisci username: ")
            password=input("inserisci password: ")
            # Confronta le varibili predefinite con quelle date dall utente
            if Username == username and Password == password:
                print("Benvenuto amministratore") 
                controllo=False
                while controllo2:
                    # Mostra all amministratore le scelte che può fare 
                    scelta=int(input(""" Menu di scelta 
                                        1. per visualizzare le moto presenti;
                                        2. per verificare la disponibilità di una moto; 
                                        3. per eliminare una moto;
                                        4. per aggiungere una moto;
                                        5. per modificare qualche parametro delle moto presenti;
                                        7. per uscire dal menu;
                          """))
                    if scelta == 1:
                        print(df)
                    elif scelta == 2:
                        Verifica_disponibilita(df)
                    elif scelta == 3:
                        Elimina_moto(df)  
                    elif scelta == 4:
                        Aggiungi_moto(df) 
                    elif scelta == 5:
                        prj.Modifica_moto(df)   
                    elif scelta == 7:
                        print("Arrivederci")
                        controllo2=False   
                    else:
                        print("Numero inesistente, riprova")            
            else:
                print("nome utente o password sbagliati, riprova")
        elif visitatore.lower() == "visitatore":
            # Mostra al visitatore le scelte che può fare 
            print("Benvenuto visitatore!")
            while controllo3:
                risposta=int(input("""Menu di scelta:
                           1. per visualizzare le moto presenti;
                           2. per verificare la disponibilità di una moto;
                           3. per acquistare una moto;
                           4. per uscire dal menu di scelta; """))
                if risposta == 1:
                    print(df)
                elif risposta == 2:
                    Verifica_disponibilita(df)        
                elif risposta == 3:
                    Acquista_moto(df)
                elif risposta == 4:
                    print("Arrivederci")
                    controllo3=False
                    controllo=False
                else:
                    print("numero non valido, riprova")     
        else:
            print("utente selezionato non valido, riprova")   
                                     

# Leggi il CSV        
df= pd.read_csv("concessionario_moto.csv")
Verifica_utente_e_menu(df)


















 












