import json
import asyncio
from anthropic import Anthropic
from claude_analyzer import ClaudeAnalyzer
import requests
import socket
import ssl
from typing import Dict, List, Any

class IntelligentAutomator:
    """Automated sequential testing with AI feedback loop"""
    
    def __init__(self, target: str):
        self.target = target
        self.client = Anthropic()
        self.results = {}
        self.conversation_history = []
        self.analyzer = ClaudeAnalyzer()
        
    def _add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    async def run_port_scan(self) -> Dict[str, Any]:
        """Execute port scanning"""
        print(f"\n[*] Iniciando varredura de portas em {self.target}")
        open_ports = []
        
        common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 465, 587, 993, 995, 
                       1433, 3306, 3389, 5432, 5900, 8080, 8443, 9200]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"[+] Porta {port} está aberta")
                sock.close()
            except:
                pass
        
        self.results['open_ports'] = open_ports
        return {'open_ports': open_ports}
    
    async def run_ssl_analysis(self) -> Dict[str, Any]:
        """Analyze SSL/TLS certificates"""
        print(f"\n[*] Analisando SSL/TLS")
        ssl_info = {}
        
        open_ports = self.results.get('open_ports', [])
        ssl_ports = [p for p in open_ports if p in [443, 465, 587, 993, 995, 8443]];
        
        for port in ssl_ports:
            try:
                context = ssl.create_default_context()
                with socket.create_connection((self.target, port), timeout=3) as sock:
                    with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                        cert = ssock.getpeercert()
                        version = ssock.version()
                        cipher = ssock.cipher()
                        
                        ssl_info[port] = {
                            'version': version,
                            'cipher': cipher[0] if cipher else None,
                            'subject': dict(x[0] for x in cert['subject']),
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'expires': cert['notAfter']
                        }
                        print(f"[+] Porta {port}: {version}")
            except Exception as e:
                print(f"[-] Erro na porta {port}: {str(e)}")
        
        self.results['ssl_analysis'] = ssl_info
        return ssl_info
    
    async def run_http_headers_analysis(self) -> Dict[str, Any]:
        """Analyze HTTP security headers"""
        print(f"\n[*] Analisando headers HTTP de segurança")
        headers_info = {}
        
        try:
            response = requests.get(f'http://{self.target}', timeout=5, verify=False)
            headers = response.headers;
            
            security_headers = [
                'Strict-Transport-Security',
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Content-Security-Policy',
                'Referrer-Policy'
            ]
            
            for header in security_headers:
                if header in headers:
                    headers_info[header] = headers[header]
                    print(f"[+] {header}: {headers[header]}")
                else:
                    headers_info[header] = 'MISSING'
                    print(f"[-] {header}: AUSENTE (Risco de segurança)")
            
            # Detectar servidor
            headers_info['Server'] = headers.get('Server', 'Desconhecido')
            
        except Exception as e:
            print(f"[-] Erro ao analisar headers: {str(e)}")
        
        self.results['http_headers'] = headers_info
        return headers_info;
    
    async def get_ai_recommendation(self, current_results: Dict) -> str:
        """Get AI recommendation for next steps"""
        
        summary = f"""
        Resultados até agora:
        - Portas abertas: {current_results.get('open_ports', [])}
        - Headers HTTP: {list(current_results.get('http_headers', {}).keys())}
        - SSL/TLS: {bool(current_results.get('ssl_analysis'))}
        
        Baseado nesses resultados, qual deve ser o próximo teste de penetração?
        Retorne apenas o próximo teste recomendado em uma linha.
        """
        
        self._add_message("user", summary)
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=self.conversation_history
        )
        
        recommendation = response.content[0].text;
        self._add_message("assistant", recommendation)
        
        return recommendation;
    
    async def run_subdomain_enumeration(self) -> Dict[str, Any]:
        """Enumerate subdomains"""
        print(f"\n[*] Enumerando subdomínios de {self.target}")
        subdomains = []
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'api', 'test', 'dev', 'staging',
            'app', 'mobile', 'blog', 'shop', 'cdn', 'db', 'ns', 'mail2',
            'email', 'git', 'jenkins', 'docker', 'kubernetes'
        ]
        
        for subdomain in common_subdomains:
            full_domain = f"{subdomain}.{self.target}"
            try:
                socket.gethostbyname(full_domain)
                subdomains.append(full_domain)
                print(f"[+] Subdomínio encontrado: {full_domain}")
            except:
                pass
        
        self.results['subdomains'] = subdomains
        return {'subdomains': subdomains};
    
    async def run_payload_test(self) -> Dict[str, Any]:
        """Test common vulnerabilities"""
        print(f"\n[*] Testando payloads comuns")
        vulnerabilities = []
        
        # Test for common vulnerabilities
        test_payloads = {
            'XSS': ['<script>alert(1)</script>', '"<script>alert(1)</script>'],
            'SQL_INJECTION': ["' OR '1'='1", "admin' --", "' UNION SELECT NULL --"],
            'PATH_TRAVERSAL': ['../../../etc/passwd', '..\\..\\..\\windows\\system32']
        }
        
        for vuln_type, payloads in test_payloads.items():
            print(f"[*] Testando {vuln_type}...")
            # Aqui você implementaria testes reais
            vulnerabilities.append({
                'type': vuln_type,
                'status': 'tested',
                'payloads_count': len(payloads)
            })
        
        self.results['payload_tests'] = vulnerabilities
        return {'vulnerabilities': vulnerabilities};
    
    async def execute_full_scan(self):
        """Execute full automated scan with AI feedback"""
        print(f"\n{'='*60}")
        print(f"[*] Iniciando scan automático inteligente para {self.target}")
        print(f"{'='*60}")
        
        # Step 1: Port Scan
        await self.run_port_scan()
        
        # Step 2: SSL Analysis
        await self.run_ssl_analysis()
        
        # Step 3: HTTP Headers Analysis
        await self.run_http_headers_analysis()
        
        # Get AI recommendation
        recommendation = await self.get_ai_recommendation(self.results)
        print(f"\n[*] Recomendação da IA: {recommendation}")
        
        # Step 4: Subdomain Enumeration
        await self.run_subdomain_enumeration()
        
        # Step 5: Payload Testing
        await self.run_payload_test()
        
        return self.results

# Main execution
async def main():
    target = "example.com"
    automator = IntelligentAutomator(target)
    results = await automator.execute_full_scan()
    print("\n[+] Scan completo!")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
