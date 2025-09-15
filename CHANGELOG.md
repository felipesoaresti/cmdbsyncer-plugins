# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.0.0] - 2025-09-15

### Adicionado
- Plugin VMware REST API inicial para CMDBSyncer
- Conexão nativa via API REST do vCenter (sem dependência do pyVmomi)
- Importação de VMs como hosts no CMDBSyncer
- Inventarização detalhada com dados do guest OS
- Suporte a certificados auto-assinados
- Integração com sistema de cron jobs do CMDBSyncer
- Documentação completa de instalação, configuração e uso
- Guia de troubleshooting abrangente
- Exemplos de configuração para diferentes cenários
- Guia da interface web para visualização de dados

### Funcionalidades Principais
- **Import VMs**: Comando para importar VMs como hosts
- **Inventorize VMs**: Comando para coletar dados detalhados
- **Automação**: Registros de cron jobs automáticos
- **Logs**: Sistema de logging integrado
- **Filtros**: Suporte a filtros personalizados (via customização)

### Dados Coletados
#### Import Básico
- ID da VM, estado, CPUs, memória
- Origem dos dados e timestamps
- Integração com conta do CMDBSyncer

#### Inventorização Detalhada
- Hostname e IP do guest OS
- Sistema operacional detectado
- Status do VMware Tools
- UUID e configurações técnicas
- Anotações e metadados

### Documentação
- **README.md**: Visão geral e início rápido
- **installation.md**: Guia passo a passo de instalação
- **configuration.md**: Configuração de contas e SSL
- **usage.md**: Comandos e exemplos de uso
- **web-interface.md**: Como usar a interface web
- **troubleshooting.md**: Resolução de problemas
- **configurations.md**: Exemplos para diferentes cenários

### Compatibilidade
- CMDBSyncer 3.10.2+
- Python 3.11+
- VMware vCenter 6.7+
- Certificados auto-assinados e válidos

### Segurança
- Criptografia automática de senhas
- Suporte a contas de domínio
- Configuração de SSL flexível
- Logs de auditoria

## Roadmap Futuro

### [1.1.0] - Planejado
- [ ] Filtros configuráveis via interface web
- [ ] Suporte a múltiplas threads para alto volume
- [ ] Métricas de performance integradas
- [ ] Exportação de relatórios

### [1.2.0] - Planejado
- [ ] Integração com alertas do CMDBSyncer
- [ ] Dashboard específico para VMware
- [ ] Suporte a clusters e resource pools
- [ ] Histórico de mudanças de VMs

### Contribuições
Contribuições são bem-vindas! Veja o arquivo README.md para instruções.

### Suporte
Para reportar bugs ou solicitar funcionalidades, abra uma issue no GitHub.
