
ceck_site è in bash

chmod +x check_site.sh
./check_site.sh

per cambiare dominio aprire sia il file .sh e cambiare il .net Ex: IP_ADDRESS=$(nslookup phica.net 

per clousflare_bypass.sh :

sudo su
chmod +x cloudflare_bypass.sh
sudo +x cloudflare_bypass.sh

ti consiglio di accendere la VPN in caso cloudflare ti bloccasse, io uso AnonSurf, alcune volte ti darà errore 403 o altri tipi di errori, farà 50 tentativi in tutto con un tot di secondi ognuna, quando vedi che un tentativo è andato a buon fine (di solito esce "[+] Risposta HTTP: [+] Tentativo 4 - Curl avanzato
[+] User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
[+] Proxy: 198.199.86.11:8080
000
[ℹ️] Codice HTTP: [+] Tentativo 4 - Curl avanzato
[+] User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
[+] Proxy: 198.199.86.11:8080
000
[⏰] Prossimo tentativo in 53 secondi...)

vuol dire che il sito è on, purtroppo no non ho messo quando è down o quando è in bad gateway, cosa che lo script in bash fa meglio e ti consiglio di usare quello piuttosto che questo in pythone. Ci lavorerò su in sti giorni per migliorarlo.
