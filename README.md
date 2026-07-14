# Publiq — Gerador de Conteúdo para Redes Sociais
 
> Gerador automático de posts para Instagram, LinkedIn e Twitter/X com revisão humana
> antes de publicar. Desenvolvido para a Nexus Consultoria.
 
---
 
## Funcionalidades
 
- Gera posts adaptados para Instagram, LinkedIn e Twitter/X
- 4 tons de voz: profissional, descontraído, inspiracional, educativo
- Revisão humana no loop — aprovar, editar ou rejeitar cada post
- Validação de temas proibidos e proteção contra prompt injection
- Posts aprovados salvos em JSON para integração com agendadores
- Testes unitários com cobertura completa
 
---
 
## Como rodar
 
```bash
git clone https:/https://github.com/FernandaAndradedev-hash/publiq
cd publiq
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Preencha ANTHROPIC_API_KEY no .env
 
python src/cli.py          # gera posts interativamente
python src/cli.py --list   # lista posts salvos
```
 
---
 
## Testes
 
```bash
pytest tests/ -v
```
 
---
 
## Estrutura
 
````
publiq/
├── src/
│   ├── config.py        # Configurações
│   ├── validators.py    # Segurança e validação
│   ├── brand_voice.py   # Identidade da marca
│   ├── generator.py     # Geração por rede social
│   ├── reviewer.py      # Aprovação humana
│   ├── storage.py       # Persistência em JSON
│   └── cli.py           # Interface CLI
├── posts/               # Posts aprovados
└── tests/
````
 
---
 
## Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
