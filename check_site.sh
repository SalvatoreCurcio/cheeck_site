#!/bin/bash

SITE="https://phica.eu/forums/"

while true; do
    echo "--- Avvio del monitoraggio ---"
    
    # Risoluzione del DNS e acquisizione dell'indirizzo IP
    IP_ADDRESS=$(nslookup phica.net | grep -A1 'Name:' | tail -n1 | awk '{print $2}')
    
    echo "Nome di dominio: phica.net"
    echo "Indirizzo IP: $IP_ADDRESS"

    # Controllo se l'IP è stato risolto
    if [[ -z "$IP_ADDRESS" ]]; then
        echo "STATO: DOWN (Impossibile risolvere il DNS)"
        echo "Attendendo 30 secondi per il prossimo controllo..."
        sleep 30
        continue
    fi
    
    # Eseguo il controllo HTTP
    STATUS=$(curl -Is --max-time 10 "$SITE" | head -n 1 | awk '{print $2}')
    echo "Stato HTTP: $STATUS"

    case $STATUS in
        200)
            echo "STATO: UP"
            ;;
        403|429|503)
            echo "STATO: UP"
            ;;
        502)
            echo "STATO: BAD_GATEWAY"
            ;;
        ""|000)
            echo "STATO: DOWN (Errore HTTP)"
            ;;
        *)
            echo "STATO: DOWN (Codice di stato sconosciuto: $STATUS)"
            ;;
    esac

    echo "Attendendo 30 secondi per il prossimo controllo..."
    sleep 30
done
