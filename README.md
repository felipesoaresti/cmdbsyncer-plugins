# CMDBSyncer Plugins

Coleção de plugins personalizados para o CMDBSyncer - Sistema modular baseado em regras para sincronizar hosts entre Checkmk, Netbox e outros sistemas.

## 📁 Plugins Disponíveis

### VMware REST API Plugin
Plugin para integração com VMware vCenter usando API REST nativa, permitindo importação e inventarização de máquinas virtuais.

**Localização:** `vmware-rest/`

**Características:**
- ✅ Conexão via API REST nativa do vCenter
- ✅ Importação de VMs como hosts no CMDBSyncer
- ✅ Inventarização detalhada com dados do guest OS
- ✅ Suporte a certificados auto-assinados
- ✅ Integração com sistema de cron jobs
- ✅ Labels e inventário estruturados

## 🚀 Início Rápido

1. Clone este repositório
2. Navegue até o plugin desejado
3. Siga as instruções de instalação específicas
4. Configure através da interface web do CMDBSyncer

## 📋 Requisitos

- CMDBSyncer 3.10.2 ou superior
- Python 3.11+
- Acesso administrativo ao servidor CMDBSyncer

## 🔧 Instalação Geral

```bash
# Clone o repositório
git clone https://github.com/felipesoaresti/cmdbsyncer-plugins.git

# Navegue até o plugin específico
cd cmdbsyncer-plugins/vmware-rest/

# Siga as instruções do README do plugin
```

## 📚 Documentação

Cada plugin possui documentação detalhada em sua pasta específica:

- **Installation**: Guia de instalação passo a passo
- **Configuration**: Configuração via interface web
- **Usage**: Exemplos de uso e comandos
- **Troubleshooting**: Resolução de problemas comuns

## 🤝 Contribuindo

1. Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🔗 Links Úteis

- [CMDBSyncer Homepage](https://cmdbsyncer.de)
- [Documentação Oficial](https://docs.cmdbsyncer.de)
- [Issues e Suporte](https://github.com/felipesoaresti/cmdbsyncer-plugins/issues)

## 🏷️ Tags

`cmdbsyncer` `vmware` `vcenter` `automation` `itil` `cmdb` `monitoring` `infrastructure`
