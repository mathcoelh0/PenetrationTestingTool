# Ferramenta de Auditoria de Segurança (FAS)

Uma ferramenta de auditoria de segurança e teste de penetração desenvolvida em Python. Esta ferramenta ajuda profissionais de segurança e administradores de sistemas a realizar avaliações de segurança básicas em sistemas e redes.

## O que esse projeto faz

- **Varredura de Portas**
  - Verifica portas abertas (1-100)
  - Identificação rápida de serviços ativos
  - Timeout configurável para respostas

- **Análise SSL/TLS**
  - Verificação de certificados SSL
  - Identificação de versões do protocolo
  - Análise de cifras utilizadas
  - Verificação de data de expiração de certificados

## Você tem que ter pra usar 

- Python 3.8 ou superior
- Sistema Operacional: Windows, Linux ou macOS
- Conexão com internet (para análises remotas)

##  Instalação

1. Clone o repositório:
```bash
git clone https://github.com/mathcoelh0/PenetrationTestingTool.git
cd PenetrationTestingTool
```

2. (Opcional, faz se quiser você não é obrigado a nada) Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## 🚀 Uso

Para iniciar uma varredura básica:
```bash
python fas.py alvo
```

Exemplo:
```bash
python fas.py exemplo.com.br
```

## 🔍 Exemplos de Saída

```
[*] Iniciando auditoria de segurança em exemplo.com.br

[*] Iniciando varredura de portas em exemplo.com.br
[*] Iniciado em: 2025-03-28 12:32:20
[*] Verificando porta 80
[+] Porta 80 está aberta
[*] Verificando porta 443
[+] Porta 443 está aberta

[*] Informações SSL/TLS (porta 443):
[+] Versão: TLSv1.3
[+] Cifra: TLS_AES_256_GCM_SHA384
[+] Certificado expira em: 2025-06-02
```

## ⚠️ Aviso Legal

Esta ferramenta deve ser usada apenas para testes de segurança autorizados. O usuário é responsável por cumprir todas as leis e regulamentos aplicáveis. O uso indevido desta ferramenta pode constituir crime.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Enviar pull requests

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
