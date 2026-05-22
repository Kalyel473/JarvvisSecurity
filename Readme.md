# 🧠 J.A.R.V.I.S

### *Apenas Um Sistema de Segurança Muito Inteligente*

### **Ultra Pro Max Plus — Build 9.9.9**


 ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
 ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
 ██║███████║██████╔╝██║   ██║██║███████╗
 ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
 ██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
```

> **"J.A.R.V.I.S., execute um reconhecimento completo no alvo."**
> *— Todo hacker ético algum dia*

---

# 🚀 O que é o JARVIS?

O JARVIS é um **framework de segurança ofensiva de última geração**, criado para reunir diversas ferramentas e técnicas utilizadas em:

* 🔍 **Reconhecimento e OSINT** (DNS, WHOIS, transparência de certificados, Google Dorks, Shodan)
* 🌐 **Escaneamento de Rede** (ping sweep, scan multi-thread, fingerprint de SO, UDP scan)
* 🕸️ **Testes em Aplicações Web** (SQLi, XSS, LFI, SSRF, CORS, detecção de CMS, brute-force de diretórios)
* 🔐 **Ataques de Credenciais** (SSH/FTP/HTTP brute-force, cracking de hashes, password spraying)
* ⚔️ **Geração de Payloads** (reverse shells em mais de 10 linguagens, web shells, helper MSFvenom, ofuscação)
* 📈 **Pós-Exploração** (privilege escalation Linux/Windows, movimentação lateral, persistência, exfiltração)
* 📊 **Relatórios Automatizados** (HTML, JSON e Markdown com tema cyberpunk)
* 🤖 **Análise com IA** usando Claude (Opus 4.5) para sugestões inteligentes de exploração, análise e auxílio em CTFs

Tudo isso integrado em uma **interface CLI cyberpunk**, com gerenciamento de sessões, variáveis globais e automação via macros.

---

# 🎬 Demonstração

```bash
$ python3 jarvis.py --target vulnlab.com

JARVIS Ultra Pro Max Plus — LOUCURA TOTAL — v9.9.9

┌─[JARVIS]─[vulnlab.com]─[F:0]─[C:0]
└─$ recon vulnlab.com

[*] PIPELINE FULL RECON: vulnlab.com
[1/7] DNS Lookup...
[+] A: 192.168.1.10  |  MX: mail.vulnlab.com

[2/7] Transparência de Certificados...
[+] 23 subdomínios encontrados via crt.sh

[3/7] Enumeração de Subdomínios...
[+] admin.vulnlab.com → 192.168.1.10
[+] dev.vulnlab.com → 192.168.1.15

[4/7] WHOIS...

[5/7] Detecção de Tecnologias...
[+] WordPress, PHP, Apache

[6/7] Cabeçalhos HTTP...
[!] X-Frame-Options: AUSENTE
[+] [FINDING: MÉDIO] Cabeçalho de segurança ausente: X-Frame-Options

[7/7] Port Scan no IP 192.168.1.10...
[+] 22/tcp SSH, 80/tcp HTTP, 3306/tcp MySQL
```

---

# 🧩 Funcionalidades

## 🔥 Módulos Principais

| Módulo                     | Descrição                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| **Motor de IA**            | Integração com Claude Opus 4.5 para análise em tempo real, criação de payloads e ajuda em CTF |
| **Reconhecimento & OSINT** | DNS, WHOIS, transparência de certificados, enumeração de subdomínios, Google Dorks e Shodan   |
| **Scanner de Rede**        | Ping sweep, TCP/UDP scanning, fingerprint de sistema operacional e banner grabbing            |
| **Segurança Web**          | Auditoria completa web (CMS, headers, SQLi, XSS, LFI, SSRF, Open Redirect, CORS)              |
| **Brute Force**            | SSH, FTP, HTTP brute-force, cracking de hashes e password spraying                            |
| **Gerador de Payloads**    | Reverse shells, web shells, integração MSFvenom e ofuscação de comandos                       |
| **Pós-Exploração**         | Técnicas de privilege escalation, persistência, movimentação lateral e exfiltração            |
| **Sistema de Relatórios**  | Relatórios HTML cyberpunk, JSON e Markdown                                                    |
| **Automação**              | Macros, pipelines automáticos e gerenciamento de sessões                                      |

---

## ✨ Extras Legais

* 💾 Sistema completo de sessões (save/load)
* 🧠 Sistema de variáveis (`$TARGET`, `$LHOST`, etc.)
* ⌨️ Histórico de comandos com autocomplete
* 🌈 Interface ANSI cyberpunk
* 📚 Banco interno de vulnerabilidades (Log4Shell, EternalBlue, PrintNightmare...)
* 🎭 Toolkit de engenharia social
* 🎧 Listener TCP integrado para capturar shells reversas

---

# 📦 Instalação

## Requisitos

* **Python 3.8+**
* Chave de API da Anthropic (para funcionalidades de IA)
* Ferramentas recomendadas:

  * `nmap`
  * `hydra`
  * `medusa`
  * `nikto`
  * `sqlmap`
  * `crackmapexec`
  * `gobuster`
  * `chisel`

---

## Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/your-repo/jarvis.git

# Entre na pasta
cd jarvis

# Instale ferramentas opcionais (Debian/Ubuntu)
sudo apt install nmap hydra medusa nikto sqlmap crackmapexec gobuster chisel -y
```

---

## Dependências Python

```bash
python3 jarvis.py --cmd "install_deps"
```

Isso instalará automaticamente:

* anthropic
* requests
* paramiko

---

# ⚙️ Configuração

O JARVIS salva suas configurações em:

```bash
~/.jarvis_config.ini
```

Você pode editar manualmente ou usar os comandos internos.

---

## Configuração mínima da IA

```bash
set ai_key sk-ant-sua-chave-aqui
```

---

## Configurações disponíveis

* 🤖 IA → modelo, temperatura, max_tokens
* 🌐 Rede → timeout, threads, retries
* 🕵️ Stealth → user-agent, delays, headers aleatórios
* 📂 Workspace → caminhos, autosave, formato de relatórios

---

## Visualizar configuração atual

```bash
config
```

## Alterar valores

```bash
set threads 300
set timeout 2
set api_key sk-ant-...
```

---

# 🕹️ Utilização

## Modo Interativo

```bash
python3 jarvis.py -t vulnlab.com
```

---

## Executar comando único

```bash
python3 jarvis.py -t example.com -c "full_recon"
```

---

## Carregar sessão anterior

```bash
python3 jarvis.py --load SESSION_ID
```

---

# 💻 Shell Interativa

O prompt mostra:

* Sessão atual
* Alvo ativo
* Quantidade de findings
* Credenciais encontradas

---

## Fluxo básico

```bash
# Definir alvo
target vulnlab.com

# Reconhecimento completo
full_recon

# Auditoria web
web_audit http://vulnlab.com/app/

# Análise com IA
analyze

# Gerar relatório
report "Pentest Final"
```

---

# 📚 Categorias de Comandos

| Categoria          | Exemplos                                                |
| ------------------ | ------------------------------------------------------- |
| **Sistema**        | `status`, `save`, `load`, `notes add`                   |
| **IA**             | `ai Explique Log4Shell`, `analyze`, `ctf XOR challenge` |
| **Recon**          | `dns`, `whois`, `subdomain`, `dorks`                    |
| **Rede**           | `ping_sweep`, `portscan`, `nmap`, `osfingerprint`       |
| **Web**            | `web_audit`, `sqli`, `xss`, `lfi`                       |
| **Brute Force**    | `ssh_brute`, `http_brute`, `hash_crack`                 |
| **Payloads**       | `revshell`, `webshell`, `msfvenom`, `obfuscate`         |
| **Pós-Exploração** | `linprivesc`, `persist`, `lateral`, `exfil`             |
| **Relatórios**     | `report`, `report_json`, `report_md`                    |
| **Utilitários**    | `encode`, `hash`, `listen`, `cidr`                      |

---

## 💡 Dicas

```bash
help <comando>
```

Mostra ajuda detalhada sobre um módulo.

---

### Executar comandos do sistema

```bash
!ls -la
```

Qualquer comando prefixado com `!` será executado diretamente no shell do sistema.

---

# 🧠 Integração com IA

O JARVIS utiliza o **Claude Opus 4.5** da Anthropic.

A IA pode:

* 🔍 Analisar resultados de scans
* ⚔️ Sugerir vetores de exploração
* 🧪 Gerar payloads personalizados
* 📖 Explicar vulnerabilidades
* 🧠 Auxiliar em desafios CTF
* 🌐 Ajudar em movimentação lateral e pivoting

---

## Ativação

```bash
set ai_key sk-ant-...
```

## Exemplos

```bash
ai Como explorar Apache 2.4.49?
analyze
exploit_suggest Log4Shell
ctf desafio xor reversível
```

---



# 🛡️ Segurança & Legalidade

> ⚠️ **AVISO IMPORTANTE:**
> O JARVIS é uma ferramenta de **segurança ofensiva** destinada exclusivamente para:
>
> * Testes autorizados
> * Ambientes de laboratório
> * CTFs
> * Pesquisa educacional
>
> O uso contra sistemas sem autorização explícita é ilegal e antiético.

---

# 🤝 Contribuições

Contribuições são bem-vindas!

Você pode:

* 🐛 Reportar bugs
* 💡 Sugerir módulos
* 🔧 Criar Pull Requests
* 🎨 Melhorar a interface cyberpunk

---

# 📜 Licença

Distribuído sob a **Licença de Uso Educacional**.

Uso comercial sem autorização é proibido.

---

# 💬 Créditos

* **JARVIS Framework Team**
* **Anthropic**
* Comunidade Red Team & CTF
