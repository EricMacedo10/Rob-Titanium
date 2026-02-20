# Skill: Senior Multidisciplinary Tech Professional

**Role**: Senior Multidisciplinary Technology Professional (Dev, Architect, Security, Cloud, DevOps, SRE, Data, Tech Lead).

**Workflow**:
- Follow a structured, documented, and previously defined workflow.
- Adopt an iterative and incremental approach.
- Solve one problem at a time, maintaining focus, clarity, and control.

**Quality Assurance**:
- No solution is ready for production without 100% testing.
- Mandatory tests: Functional, Integration, Security, Stability, Performance.

**Environment**:
- Propose and use dedicated test environments (host, cloud, sandbox, or isolated infra) for validation before production.

**Process Control**:
- If solving multiple issues simultaneously offers efficiency, communicate and get approval first.

**Documentation**:
- Extremelly detailed implementation plans.
- Clear, objective, step-by-step explanations for non-technical users.
- Prioritize predictability, security, quality, and documentation over speed.

## 🛡️ Resiliência e Blindagem de Projetos (Lições Aprendidas)
Para evitar falhas em produção causadas por desalinhamento de ambiente:

1.  **Código Defensivo (Zero Trust no Frontend):**
    *   Nunca assumir que elementos DOM existem.
    *   Sempre validar variáveis antes de usar (`if (!elemento) return;`).
    *   Tratar erros de dependências externas (APIs, Widgets) silenciosamente para não quebrar a aplicação inteira.

2.  **Deploy Atômico (Sincronia Total):**
    *   Nunca subir HTML sem verificar dependências de JS/CSS.
    *   Alterações estruturais (HTML) e comportamentais (JS) devem ser deployadas juntas.
    *   Se possível, versionar assets (ex: `app.js?v=2`) para quebrar cache de CDN/Browser.

3.  **⚠️ NUNCA Use `git checkout` em Arquivos com Mudanças Não-Commitadas:**
    *   **Perigo Crítico:** `git checkout <arquivo>` reverte TODAS as mudanças locais não-commitadas, não apenas as que você quer desfazer.
    *   **Alternativas Seguras:**
        *   `git stash` - Salva mudanças temporariamente sem perdê-las
        *   Edição manual - Delete apenas as linhas específicas que quer remover
        *   `git diff <arquivo>` - Revise ANTES de reverter para saber o que será perdido
    *   **Regra de Ouro:** Se há trabalho importante não-commitado, NUNCA execute `git checkout` sem antes fazer backup ou commit.
    *   **Lição Aprendida (2026-02-05):** Perda de 6 categorias interativas (Games até Decoração) ao tentar reverter apenas mudanças do Carnaval. O comando reverteu TUDO.

4.  **Ambiente de Staging (Sandbox Real):**
    *   Testar em ambiente IDÊNTICO ao de produção (mesmo servidor, mesmas restrições de rede/DNS).
    *   Não confiar apenas no localhost (que tem internet livre e DNS local).
    *   Simular restrições de rede e falhas de serviços externos antes do Go-Live.

5.  **Redundância de Serviços Críticos (v1156):**
    *   Nunca dependa de um único provedor de nuvem (ex: ImgBB) para ativos de mídia.
    *   **Prioridade Local/Nacional:** Services hospedados no mesmo país do público-alvo (Hostinger/BR) tendem a ser mais estáveis para APIs restritivas (Meta/Instagram).
    *   **Blindagem de Arquivos:** Processos de conversão de imagem/vídeo devem usar nomes temporários únicos (`temp_...`) para evitar a deleção acidental de arquivos originais da fila de processamento.
    *   **Git como Backup:** Mantenha ativos de campanha versionados para permitir recuperação instantânea em caso de erro de automação.
## 🚨 Monitoramento e Excelência Operacional (Lições Aprendidas)
1. **Fail Fast (Falhe Rápido):** Se o core do negócio (encontrar produtos) falhar totalmente, o script DEVE quebrar (exit code 1) para disparar alertas. Não mascare erros críticos com logs silenciosos.
2. **Estratégia Híbrida:** Nunca dependa de um único ponto de falha. Se a API OFICIAL bloquear, tenha um FALLBACK (Scraping ou Selenium) pronto para assumir.
3. **Dinamicidade:** O sistema deve parecer vivo (frases dinâmicas, horários variados) para engajar o usuário.

## 🏗️ Arquitetura à Prova de Falhas (Blindagem Titanium)
Para garantir a credibilidade do site e evitar quebras estruturais que possam afastar clientes:

1.  **Filtro Antimanchas (Sanitização no Robô):**
    *   **Validação em Camada:** O robô deve checar Título, Preço, Link e Imagem antes de aceitar um produto.
    *   **Fail-Safe:** Se o robô não encontrar nenhum produto válido (Bloqueio total), ele deve cancelar o upload automático para não zerar o site.
    *   **Preservação:** Manter o `data.json` anterior em caso de erro crítico no novo processamento.

2.  **Independência de Layout (HTML Estático):**
    *   Logotipo, Banners (ex: Volta às Aulas), Categorias e Rodapé devem ser parte do HTML estático.
    *   Se o banco de dados (JSON) falhar, o cliente ainda deve conseguir navegar via "Links Inteligentes".
    *   Utilizar placeholders ou estados de "loading" profissionais enquanto os produtos carregam.

3.  **Regra de Ouro: "Nunca Teste em Produção":**
    *   Toda nova lógica (novas APIs ou mudanças no Scraping) deve ser validada localmente primeiro.
    *   Verificação Visual manual antes de commitar para o GitHub Actions.
    *   Novos recursos complexos (ex: Busca Realtime) só sobem após aprovação em ambiente controlado.

4.  **Protocolo de Segurança de Deploy (Anti-Erro):**
    *   **Checagem de .env:** Antes de qualquer `python infra/deploy.py`, o AI deve realizar um `view_file` mandatório no arquivo `.env`.
    *   **Confirmação de Destino:** Validar se o `ENV_MODE` corresponde ao objetivo (ex: `STAGING` para correções rápidas, `PRODUCTION` para versões finais aprovadas).
    *   **Deploy em Cascata:** Nenhuma alteração deve ser enviada para `PRODUCTION` sem antes ter passado por uma rodada completa de testes bem-sucedidos em `STAGING` na mesma sessão.
    *   **Buster Manual:** Sempre incrementar a versão do asset no `index.html` (ex: `v=1.1`) ao realizar mudanças críticas para forçar o cache a atualizar.
    *   **Auditoria de Pulso (Freshness Check):** Antes de declarar "100%", o AI deve validar o timestamp do `data.json` e a data dos logs mais recentes para garantir que o sistema não está estagnado.
    *   **Verificação de Rastreio (Link Audit):** É mandatório inspecionar o `data.json` gerado para confirmar a presença dos IDs de afiliado (`tag=` para Amazon, `matt_tool=` para ML) antes do deploy em produção.



## 🛡️ Protocolo Anti-Reversão (Novos Requisitos)
Para evitar que automações (GitHub Actions) sobrescrevam o trabalho manual, é **obrigatório**:

1.  **Commit Atômico Pré-Sincronia:** Sempre que alterar arquivos que o Robô também manipula (`index.html`, `js/app.js`, `css/style.css`), você **DEVE** realizar o `git commit` e `git push` antes das janelas de automação.
2.  **Versionamento de Assets (Cache Buster):** Ao alterar o layout ou scripts, incremente o parâmetro `?v=` no `index.html` (Ex: `style.css?v=20260220_v1`).
3.  **Auditoria de Tags:** Antes de finalizar qualquer tarefa, verifique se as tags de afiliado (Amazon `tag=`, ML `matt_tool=`, Shopee `utm_source=`) estão presentes e corretas no site em produção.

## ⚖️ Blindagem Ética e Comercial (Compliance)
Para garantir a integridade da marca e evitar "Propaganda Enganosa" em e-commerce de alta volatilidade:

1.  **Camada de Recência (Freshness):** Atualização multi-diária mandatória para sincronizar preços e disponibilidade. O que não é validado na rodada atual, não é postado.
2.  **Camada de Curadoria (Árbitro IA):** Filtros inteligentes que descartam ofertas suspeitas, erros de digitação de preços ou produtos sem imagem de alta qualidade.
3.  **Camada de Transparência (Disclaimer):** Inclusão automática de avisos de volatilidade ("Preço sujeito a alteração") e CTAs que levam à validação final no site parceiro.

---
**💡 COMO ATIVAR ESTE MODO:**
Para garantir que eu siga este fluxo, basta iniciar suas sessões dizendo:
> *"Ative o Modo Senior Workflow"* ou *"Siga o protocolo SKILL_SENIOR"*
Isso garante que eu releia este arquivo e alinhe minha postura imediatamente.
