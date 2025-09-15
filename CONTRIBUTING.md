# Contribuindo para CMDBSyncer Plugins

Obrigado pelo seu interesse em contribuir! Este documento fornece diretrizes para contribuir com o projeto.

## 🤝 Como Contribuir

### 1. Reportar Bugs

Antes de reportar um bug:
- Verifique se já não existe uma issue aberta
- Teste com a versão mais recente
- Reproduza o problema em ambiente isolado

**Template para Bug Report:**
```
**Descrição do Bug**
Descrição clara e concisa do problema.

**Para Reproduzir**
1. Configure a conta com...
2. Execute o comando...
3. Observe o erro...

**Comportamento Esperado**
O que deveria acontecer.

**Ambiente**
- CMDBSyncer: [versão]
- SO: [sistema operacional]
- Python: [versão]
- vCenter: [versão]

**Logs**
[Cole logs relevantes aqui]

**Screenshots**
Se aplicável, adicione screenshots.
```

### 2. Solicitar Funcionalidades

Para solicitar novas funcionalidades, abra uma issue explicando:
- Qual problema a funcionalidade resolveria
- Como você imagina que funcionaria
- Alternativas que considerou

### 3. Contribuir com Código

#### Preparação do Ambiente

```bash
# 1. Fork do repositório no GitHub

# 2. Clone seu fork
git clone https://github.com/seu-usuario/cmdbsyncer-plugins.git
cd cmdbsyncer-plugins

# 3. Adicione o repositório original como upstream
git remote add upstream https://github.com/felipesoaresti/cmdbsyncer-plugins.git

# 4. Crie branch para sua feature
git checkout -b feature/minha-nova-funcionalidade
```

#### Padrões de Código

**Python:**
- Siga PEP 8 para estilo de código
- Use docstrings para funções e classes
- Máximo 88 caracteres por linha
- Use type hints quando apropriado

#### Testes

```bash
# Execute testes básicos
cd /var/www/cmdbsyncer
source ENV/bin/activate

# Teste sintaxe
python -m py_compile application/plugins/vmware_rest_api.py

# Teste comandos
./cmdbsyncer vmware_rest --help

# Teste funcional (se tiver ambiente de teste)
./cmdbsyncer vmware_rest import_vms conta-teste --debug
```

#### Commit

**Formato de mensagens:**
```
tipo: descrição breve

Descrição mais detalhada se necessário.

- Lista de mudanças
- Cada item em linha separada

Fixes #123
```

**Tipos de commit:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Apenas documentação
- `style`: Formatação
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Manutenção

## 📋 Diretrizes Específicas

### Segurança
- **Nunca commite credenciais** reais
- Use exemplos genéricos na documentação
- Valide todas as entradas do usuário

### Performance
- Considere impacto em ambientes com muitas VMs
- Implemente timeouts apropriados
- Use logging eficiente

### Compatibilidade
- Mantenha compatibilidade com versões suportadas
- Documente breaking changes claramente

### Documentação
- Mantenha documentação em português brasileiro
- Use linguagem clara e acessível
- Inclua exemplos práticos

## 🎯 Áreas que Precisam de Ajuda

### Prioridade Alta
- Testes automatizados
- Suporte a mais versões do vCenter
- Otimização de performance
- Melhorias na documentação

### Prioridade Média
- Novos filtros e funcionalidades
- Integração com outros sistemas
- Dashboard específico
- Métricas de monitoramento

## 🎉 Reconhecimento

Todos os contribuidores serão:
- Listados no arquivo CONTRIBUTORS.md
- Mencionados nos release notes
- Reconhecidos na documentação

Obrigado por ajudar a melhorar este projeto!
