# VMware REST API Plugin para CMDBSyncer

Plugin personalizado para integração com VMware vCenter usando API REST nativa, permitindo importação e sincronização de máquinas virtuais no CMDBSyncer.

## 🎯 Objetivo

Este plugin foi desenvolvido para organizações que precisam sincronizar informações de VMs do VMware vCenter com o CMDBSyncer, usando exclusivamente a API REST do vCenter (sem dependências do pyVmomi).

## ✨ Funcionalidades

### 🔄 Importação de VMs
- Conecta no vCenter via API REST (`/api/session`)
- Busca todas as VMs via endpoint `/api/vcenter/vm`
- Cria hosts no CMDBSyncer com informações básicas
- Suporte a certificados auto-assinados

### 📊 Inventarização Detalhada
- Coleta dados detalhados de cada VM
- Informações do guest OS (hostname, IP, sistema operacional)
- Status do VMware Tools
- UUID e configurações técnicas

### 🕐 Automação
- Integração com sistema de cron jobs
- Sincronização automática programável
- Logs detalhados de execução

## 📋 Requisitos

- **CMDBSyncer**: 3.10.2 ou superior
- **Python**: 3.11+
- **Bibliotecas**: requests, urllib3 (já incluídas no CMDBSyncer)
- **Acesso**: Conta com permissões de leitura no vCenter
- **Rede**: Conectividade HTTPS com o vCenter (porta 443)

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   vCenter API   │◄──►│  Plugin Python  │◄──►│   CMDBSyncer    │
│  (REST/HTTPS)   │    │ vmware_rest_api │    │    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                ▲
                                │
                         ┌─────────────┐
                         │ Cron Jobs   │
                         │ Automation  │
                         └─────────────┘
```

## 🚀 Instalação Rápida

1. **Copie o plugin** para o servidor CMDBSyncer
2. **Configure a conta** VMware na interface web
3. **Execute a importação** inicial
4. **Configure cron jobs** para sincronização automática

Veja o guia detalhado em [`docs/installation.md`](docs/installation.md)

## 📁 Estrutura do Projeto

```
vmware-rest/
├── README.md                    # Este arquivo
├── plugin/
│   └── vmware_rest_api.py      # Plugin principal
├── docs/
│   ├── installation.md         # Guia de instalação
│   ├── configuration.md        # Configuração da conta
│   ├── usage.md                # Comandos e uso
│   ├── web-interface.md        # Interface web
│   └── troubleshooting.md      # Resolução de problemas
└── examples/
    └── configurations.md       # Exemplos de configuração
```

## 🎮 Comandos Principais

```bash
# Importar VMs (primeira execução)
./cmdbsyncer vmware_rest import_vms nome-da-conta

# Inventarizar dados detalhados
./cmdbsyncer vmware_rest inventorize_vms nome-da-conta

# Modo debug para troubleshooting
./cmdbsyncer vmware_rest import_vms nome-da-conta --debug
```

## 📊 Dados Coletados

### Labels (Import básico)
- **vm_id**: Identificador interno da VM
- **power_state**: Estado da VM (POWERED_ON/OFF)
- **cpu_count**: Número de CPUs virtuais
- **memory_size_gb**: Memória em GB
- **vmware_source**: Origem dos dados

### Inventory (Dados detalhados)
- **guest_hostname**: Hostname do sistema operacional
- **guest_ip**: Endereço IP principal
- **guest_os**: Sistema operacional detectado
- **tools_status**: Status do VMware Tools
- **vm_uuid**: UUID único da VM

## 🔧 Configuração

### Conta VMware no CMDBSyncer

```yaml
Name: meu-vcenter
Type: vmware_vcenter
Address: vcenter.exemplo.com
Username: usuario\serviceaccount
Password: suasenhaaqui

Custom Fields:
  inventorize_key: vmware_vcenter
  hostname_field: name
```

## 📈 Monitoramento

### Interface Web
- **Hosts → Hosts**: Ver VMs importadas
- **Jobs → Cron Stats**: Status da sincronização
- **Dashboard**: Estatísticas gerais

### Linha de Comando
```bash
# Ver hosts importados
./cmdbsyncer host list | grep vmware

# Logs detalhados
tail -f /var/log/cmdbsyncer/cmdbsyncer.log
```

## 🔍 Troubleshooting

### Problemas Comuns
- **Erro SSL**: Configure `DISABLE_SSL_ERRORS = True`
- **Credenciais**: Verifique usuário e senha
- **Conectividade**: Teste acesso HTTPS ao vCenter

Veja o guia completo em [`docs/troubleshooting.md`](docs/troubleshooting.md)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie sua feature branch
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja [`LICENSE`](../LICENSE) para detalhes.

## 🔗 Links Úteis

- [Documentação CMDBSyncer](https://docs.cmdbsyncer.de)
- [VMware vCenter API Reference](https://developer.vmware.com/apis/vsphere-automation/latest/)
- [Issues do Projeto](https://github.com/felipesoaresti/cmdbsyncer-plugins/issues)
