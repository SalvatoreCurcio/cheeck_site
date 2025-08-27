#!/bin/bash
# ==================================================
# BYPASS CLOUDFLARE ULTIMATE - Parrot OS / Kali Linux
# ==================================================
# Script ottimizzato per distro security con Firefox
# ==================================================

echo "╔══════════════════════════════════════════════════╗"
echo "║    CLOUDFLARE BYPASS TOOL - PARROT OS/KALI       ║"
echo "║                  https://phica.eu/forums/        ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "[+] Distro rilevata: $(lsb_release -d | cut -f2)"
echo "[+] Utente: $USER"
echo "[+] Data: $(date)"
echo ""

# Configurazione
TARGET_URL="https://phica.eu/forums/"
USER_AGENT_FILE="/tmp/user_agents.txt"
PROXY_FILE="/tmp/proxies.txt"
LOG_FILE="/var/log/phica_bypass.log"
SUCCESS_FILE="/tmp/successful_proxies.txt"

# Creazione file temporanei
create_temp_files() {
    echo "[+] Creazione file temporanei..."
    
    # User-Agent realistici
    cat > "$USER_AGENT_FILE" << 'EOF'
Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0
EOF

    # Lista proxy aggiornata (mix di HTTP/HTTPS/SOCKS)
    cat > "$PROXY_FILE" << 'EOF'
185.199.229.156:7492
185.199.228.220:7300
185.199.231.45:8382
142.93.130.169:8118
64.225.8.82:9981
157.245.27.74:3128
8.219.97.248:80
45.95.147.106:8080
47.253.105.175:3333
20.111.54.16:8123
198.199.86.11:8080
47.88.3.19:8080
154.236.189.28:1976
103.155.217.105:41367
45.131.5.245:4444
socks5://38.154.227.167:5868
socks4://184.168.121.153:4145
http://201.151.62.20:5678
https://158.69.225.110:3128
socks5://64.225.4.12:10001
EOF

    touch "$SUCCESS_FILE"
    sudo touch "$LOG_FILE"
    sudo chmod 644 "$LOG_FILE"
}

# Installazione dipendenze
install_dependencies() {
    echo "[+] Controllo dipendenze..."
    
    if ! command -v curl &> /dev/null; then
        echo "[+] Installando curl..."
        sudo apt update && sudo apt install -y curl
    fi

    if ! command -v tor &> /dev/null; then
        echo "[+] Installando Tor..."
        sudo apt install -y tor
    fi

    if ! command -v proxychains &> /dev/null; then
        echo "[+] Installando proxychains..."
        sudo apt install -y proxychains4
    fi

    if ! command -v wget &> /dev/null; then
        echo "[+] Installando wget..."
        sudo apt install -y wget
    fi

    if ! command -v nmap &> /dev/null; then
        echo "[+] Installando nmap..."
        sudo apt install -y nmap
    fi
}

# Controllo funzionalità Tor
check_tor() {
    echo "[+] Controllo servizio Tor..."
    if ! systemctl is-active --quiet tor; then
        echo "[+] Avvio servizio Tor..."
        sudo systemctl start tor
        sleep 3
    fi
    
    if curl --socks5 127.0.0.1:9050 -s https://check.torproject.org/ | grep -q "Congratulations"; then
        echo "[✓] Tor funzionante"
        return 0
    else
        echo "[×] Tor non funzionante"
        return 1
    fi
}

# Test proxy
test_proxy() {
    local proxy=$1
    echo "[?] Test proxy: $proxy"
    
    if timeout 10 curl -s -x "$proxy" https://httpbin.org/ip > /dev/null; then
        echo "[✓] Proxy funzionante: $proxy"
        echo "$proxy" >> "$SUCCESS_FILE"
        return 0
    else
        echo "[×] Proxy non funzionante: $proxy"
        return 1
    fi
}

# Rotazione avanzata User-Agent
get_random_ua() {
    local ua
    if [ -f "$USER_AGENT_FILE" ]; then
        ua=$(shuf -n 1 "$USER_AGENT_FILE")
        echo "$ua"
    else
        echo "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0"
    fi
}

# Tecnica 1: Curl avanzato con header personalizzati
curl_bypass() {
    local attempt=$1
    local proxy=$2
    local ua=$(get_random_ua)
    
    echo "[+] Tentativo $attempt - Curl avanzato"
    echo "[+] User-Agent: $ua"
    echo "[+] Proxy: ${proxy:-Nessuno}"
    
    local headers=(
        "-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'"
        "-H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3'"
        "-H 'Accept-Encoding: gzip, deflate, br'"
        "-H 'Connection: keep-alive'"
        "-H 'Upgrade-Insecure-Requests: 1'"
        "-H 'Sec-Fetch-Dest: document'"
        "-H 'Sec-Fetch-Mode: navigate'"
        "-H 'Sec-Fetch-Site: none'"
        "-H 'Sec-Fetch-User: ?1'"
        "-H 'Cache-Control: max-age=0'"
        "-H 'TE: trailers'"
    )
    
    local cmd="curl -s -o /dev/null -w '%{http_code}' --compressed --connect-timeout 15"
    cmd+=" -A '$ua'"
    
    if [ -n "$proxy" ]; then
        cmd+=" -x '$proxy'"
    fi
    
    for header in "${headers[@]}"; do
        cmd+=" $header"
    done
    
    cmd+=" '$TARGET_URL?bypass=$RANDOM&t=$(date +%s)'"
    
    local response=$(eval "$cmd" 2>/dev/null)
    echo "$response"
}

# Tecnica 2: Proxychains + curl
proxychains_bypass() {
    local attempt=$1
    local proxy=$2
    
    echo "[+] Tentativo $attempt - Proxychains"
    
    # Configurazione temporanea proxychains
    local temp_conf="/tmp/proxychains_temp.conf"
    echo "strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000" > "$temp_conf"
    
    if [ -n "$proxy" ]; then
        echo "$proxy" >> "$temp_conf"
    else
        # Usa proxy da file
        local random_proxy=$(shuf -n 1 "$PROXY_FILE")
        echo "$random_proxy" >> "$temp_conf"
    fi
    
    local response=$(timeout 20 proxychains4 -f "$temp_conf" curl -s -o /dev/null -w "%{http_code}" \
        -A "$(get_random_ua)" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
        -H "Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3" \
        "$TARGET_URL?pc=$RANDOM" 2>/dev/null)
    
    rm -f "$temp_conf"
    echo "$response"
}

# Tecnica 3: Tor + curl
tor_bypass() {
    local attempt=$1
    echo "[+] Tentativo $attempt - Rete Tor"
    
    local response=$(timeout 25 curl --socks5 127.0.0.1:9050 -s -o /dev/null -w "%{http_code}" \
        -A "$(get_random_ua)" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
        -H "Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3" \
        "$TARGET_URL?tor=$RANDOM" 2>/dev/null)
    
    echo "$response"
}

# Tecnica 4: Google Cache
google_cache_bypass() {
    local attempt=$1
    echo "[+] Tentativo $attempt - Google Cache"
    
    local response=$(timeout 15 curl -s -o /dev/null -w "%{http_code}" \
        -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
        "http://webcache.googleusercontent.com/search?q=cache:${TARGET_URL}" 2>/dev/null)
    
    echo "$response"
}

# Tecnica 5: Wayback Machine
wayback_bypass() {
    local attempt=$1
    echo "[+] Tentativo $attempt - Wayback Machine"
    
    local archive_date="2023$(printf "%02d" $((RANDOM % 12 + 1)))"
    local response=$(timeout 15 curl -s -o /dev/null -w "%{http_code}" \
        -A "$(get_random_ua)" \
        "http://web.archive.org/web/$archive_date/${TARGET_URL}" 2>/dev/null)
    
    echo "$response"
}

# Funzione di logging
log_result() {
    local attempt=$1
    local technique=$2
    local response=$3
    local proxy=$4
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="$timestamp - Attempt: $attempt - Technique: $technique - HTTP: $response - Proxy: ${proxy:-Direct}"
    
    echo "$log_entry" | sudo tee -a "$LOG_FILE" > /dev/null
}

# Main loop
main() {
    echo "[+] Inizializzazione bypass Cloudflare..."
    echo "[+] Target: $TARGET_URL"
    echo ""
    
    install_dependencies
    create_temp_files
    check_tor
    
    # Test proxy disponibili
    echo "[+] Test proxy disponibili..."
    while IFS= read -r proxy; do
        test_proxy "$proxy" &
    done < "$PROXY_FILE"
    wait
    
    local attempt=1
    local max_attempts=50
    local success_count=0
    
    echo "[+] Avvio sequenza bypass ($max_attempts tentativi)..."
    echo ""
    
    while [ $attempt -le $max_attempts ]; do
        echo "╔═══════════════════════════════════════════════╗"
        echo "║               TENTATIVO $attempt/$max_attempts               ║"
        echo "╚═══════════════════════════════════════════════╝"
        
        local technique=""
        local response=""
        local proxy_used=""
        
        # Selezione tecnica casuale
        case $((RANDOM % 6)) in
            0)
                technique="CURL_ADVANCED"
                proxy_used=$(shuf -n 1 "$SUCCESS_FILE" 2>/dev/null || echo "")
                response=$(curl_bypass "$attempt" "$proxy_used")
                ;;
            1)
                technique="PROXYCHAINS"
                response=$(proxychains_bypass "$attempt")
                ;;
            2)
                technique="TOR_NETWORK"
                response=$(tor_bypass "$attempt")
                ;;
            3)
                technique="GOOGLE_CACHE"
                response=$(google_cache_bypass "$attempt")
                ;;
            4)
                technique="WAYBACK_MACHINE"
                response=$(wayback_bypass "$attempt")
                ;;
            5)
                technique="DIRECT_CONNECTION"
                response=$(curl_bypass "$attempt" "")
                ;;
        esac
        
        # Analisi risposta
        echo "[+] Risposta HTTP: $response"
        
        case $response in
            "200")
                echo "[🎉] SUCCESSO! Sito raggiungibile!"
                success_count=$((success_count + 1))
                ;;
            "403"|"429")
                echo "[⛔] Bloccato da Cloudflare (WAF)"
                ;;
            "404")
                echo "[🔍] Pagina non trovata"
                ;;
            "000"|"")
                echo "[💥] Timeout/Errore di connessione"
                ;;
            "5"*)
                echo "[🔥] Errore server interno"
                ;;
            *)
                echo "[ℹ️] Codice HTTP: $response"
                ;;
        esac
        
        # Logging
        log_result "$attempt" "$technique" "$response" "$proxy_used"
        
        # Delay casuale tra tentativi
        local delay=$((RANDOM % 31 + 30))
        echo "[⏰] Prossimo tentativo in $delay secondi..."
        echo ""
        
        sleep $delay
        attempt=$((attempt + 1))
    done
    
    # Riepilogo finale
    echo "╔═══════════════════════════════════════════════╗"
    echo "║                 RIEPILOGO                     ║"
    echo "╚═══════════════════════════════════════════════╝"
    echo "[📊] Tentativi totali: $max_attempts"
    echo "[✅] Successi: $success_count"
    echo "[📁] Log completo: $LOG_FILE"
    echo "[💾] Proxy funzionanti: $SUCCESS_FILE"
    echo ""
    
    # Pulizia file temporanei
    rm -f "$USER_AGENT_FILE" "$PROXY_FILE" "$SUCCESS_FILE"
}

# Esecuzione principale
if [ "$EUID" -eq 0 ]; then
    echo "[!] Avviato come root, procedura sicura."
    main
else
    echo "[!] Avvio come utente normale..."
    main
fi
