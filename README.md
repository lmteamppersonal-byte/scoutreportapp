# ⚽ Scout Report - Aplicação de Scouting de Futebol

## 📋 Sobre o Projeto

Aplicação web profissional para criação de relatórios de scouting de futebol, com avaliação detalhada de jogadores baseada em 4 pilares fundamentais:

- **Físicas** - Atributos físicos e condicionamento
- **Técnicas** - Habilidades técnicas e fundamentos
- **Táticas** - Inteligência tática e posicionamento
- **Cognitivas** - Aspectos mentais e tomada de decisão

## ✨ Funcionalidades

- 📊 **Gráfico Radar Interativo** - Visualização completa do perfil do jogador
- 📥 **Exportação JPEG** - Download do gráfico em alta qualidade com fundo branco
- 📄 **Relatório PDF** - Geração de relatório profissional completo
- 🌐 **Relatório HTML** - Versão web do relatório para compartilhamento
- 💾 **Salvar/Carregar Sessão** - exporte os dados para JSON e reabra depois sem perder nada
- 🎨 **Personalização Visual** - Cores customizáveis para identidade visual
- 📸 **Fotos e Mapas de Calor** - Integração de imagens no relatório
- 📈 **Estatísticas da Temporada** - Tabela editável de performance

## 🚀 Como Usar

### Acesso Online
[Link será disponibilizado após deploy]

### Execução Local

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd football_scout_app
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

   > **❗ Nota:** A geração de imagens via Plotly/Kaleido exige o navegador Chrome e algumas bibliotecas do sistema. O app agora tenta instalar Chrome automaticamente se detectar o erro ao gerar o PDF, mas você pode executar manualmente:
   > ```bash
   > plotly_get_chrome          # baixa uma cópia de Chrome usada por Kaleido
   > sudo apt-get install -y libnss3 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libxpango-1.0-0 libcairo2 libasound2
   > ```

3. Execute a aplicação:
```bash
streamlit run scout_app.py
```

4. Acesse no navegador: `http://localhost:8501`

5. **Salvar / Carregar** – use o painel lateral para exportar sua sessão como JSON antes de fechar ou em caso de erro. Carregue o arquivo mais tarde para restaurar todos os campos e notas.

## 📦 Dependências

- streamlit - Framework web
- plotly - Gráficos interativos
- pandas - Manipulação de dados
- reportlab - Geração de PDFs
- kaleido - Exportação de imagens
- beautifulsoup4 & selenium - Web scraping (futuro)

## 🎯 Posições Suportadas

- Goleiro
- Laterais
- Zagueiros
- Volantes
- Médios
- Meias-atacantes
- Extremos
- Centroavantes

Cada posição tem critérios específicos de avaliação adaptados às demandas táticas e técnicas.

## 📝 Licença

Projeto desenvolvido para fins de scouting profissional de futebol.

## 🆕 Últimas Atualizações

- ✅ **Download de Gráfico JPEG** - Exportação com fundo branco em alta qualidade
- ✅ **Relatórios Profissionais** - Templates melhorados em PDF e HTML
- ✅ **Customização Visual** - Sistema de cores flexível

---

Desenvolvido com ❤️ para profissionais de scouting
