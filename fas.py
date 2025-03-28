#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import ssl
from datetime import datetime

class FerramentaAuditoria:
    def __init__(self, alvo):
        self.alvo = alvo
        self.portas_abertas = []

    def verificar_porta(self, porta):
        """Verifica se uma porta específica está aberta"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            resultado = sock.connect_ex((self.alvo, porta))
            sock.close()
            return resultado == 0
        except socket.gaierror:
            print("[!] Hostname não pôde ser resolvido")
            sys.exit()
        except socket.error:
            print("[!] Não foi possível conectar ao servidor")
            sys.exit()

    def varredura_portas(self, inicio=1, fim=100):
        """Realiza varredura de portas no alvo"""
        print(f"\n[*] Iniciando varredura de portas em {self.alvo}")
        print(f"[*] Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for porta in range(inicio, fim + 1):
            sys.stdout.write(f"\r[*] Verificando porta {porta}")
            sys.stdout.flush()
            if self.verificar_porta(porta):
                self.portas_abertas.append(porta)
                print(f"\n[+] Porta {porta} está aberta")

        print(f"\n[*] Varredura concluída!")
        if self.portas_abertas:
            print(f"[+] Portas abertas encontradas: {', '.join(map(str, self.portas_abertas))}")
        else:
            print("[!] Nenhuma porta aberta encontrada")

    def analise_ssl(self):
        """Analisa configuração SSL/TLS"""
        for porta in [443, 8443]:
            try:
                context = ssl.create_default_context()
                with socket.create_connection((self.alvo, porta), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.alvo) as ssock:
                        cert = ssock.getpeercert()
                        print(f"\n[*] Informações SSL/TLS (porta {porta}):")
                        print(f"[+] Versão: {ssock.version()}")
                        print(f"[+] Cifra: {ssock.cipher()[0]}")
                        print(f"[+] Certificado expira em: {cert['notAfter']}")
            except Exception as e:
                print(f"\n[!] Erro na análise SSL porta {porta}: {e}")

def main():
    """Função principal"""
    if len(sys.argv) != 2:
        print("Uso: python fas.py <alvo>")
        print("Exemplo: python fas.py exemplo.com.br")
        sys.exit(1)

    alvo = sys.argv[1]
    print(f"[*] Iniciando auditoria de segurança em {alvo}")
    
    ferramenta = FerramentaAuditoria(alvo)
    
    try:
        ferramenta.varredura_portas()
        ferramenta.analise_ssl()
        print("\n[*] Auditoria concluída!")
        
    except KeyboardInterrupt:
        print("\n[!] Auditoria interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Erro durante a auditoria: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
