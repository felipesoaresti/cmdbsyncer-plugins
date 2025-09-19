# Guia de Instalação - VMware REST API Plugin

Este guia explica como instalar e configurar o plugin VMware REST API no CMDBSyncer.

## Pré-requisitos

### Sistema
- CMDBSyncer: Versão 3.10.2 ou superior
- Python: 3.11 ou superior
- Sistema Operacional: Linux (testado em Red Hat/CentOS)
- Permissões: Acesso root ou sudo no servidor CMDBSyncer

### Rede e Acesso
- Conectividade: HTTPS (porta 443) para o vCenter
- Certificados: Suporte a certificados auto-assinados
- Credenciais: Conta de serviço no vCenter com permissões de leitura

### Dependências Python
O plugin utiliza bibliotecas já incluídas no CMDBSyncer:
- `requests` - Para requisições HTTP
- `urllib3` - Para gerenciamento de conexões SSL
- `click` - Para interface de linha de comando

## Instalação Passo a Passo

### 1. Localize o Diretório do CMDBSyncer

```bash
# Diretório padrão de instalação
cd /var/www/cmdbsyncer

# Ative o ambiente virtual
source ENV/bin/activate

# Verifique se está funcionando
./cmdbsyncer --help
```

Possíveis localizações:
- `/var/www/cmdbsyncer` (instalação padrão)
- `/srv/cmdbsyncer` (algumas distribuições)
- `/opt/cmdbsyncer` (instalação customizada)

### 2. Copie o Plugin

```bash
# Navegue até o diretório de plugins
cd /var/www/cmdbsyncer/application/plugins/

# Baixe o plugin do GitHub
wget https://raw.githubusercontent.com/felipesoaresti/cmdbsyncer-plugins/main/vmware-rest/plugin/vmware_rest_api.py

# Ou copie manualmente o arquivo
# cp /caminho/para/vmware_rest_api.py .

# Verifique se foi copiado
ls -la vmware_rest_api.py
```

### 3. Verifique a Sintaxe

```bash
# Teste a sintaxe do Python
python -m py_compile vmware_rest_api.py

# Se não houver erros, está correto
echo "Plugin sintaxe OK"
```

### 4. Configure SSL (Se Necessário)

Se usar certificados auto-assinados no vCenter:

```bash
# Edite o arquivo de configuração
vim /var/www/cmdbsyncer/application/config.py

# Certifique-se que esta linha existe:
DISABLE_SSL_ERRORS = True
```

### 5. Reinicie o CMDBSyncer (Opcional)

```bash
# Se usando systemd
sudo systemctl restart cmdbsyncer

# Ou se usando processo manual
pkill -f cmdbsyncer
# Depois reinicie conforme sua configuração
```

## Verificação da Instalação

### 1. Teste os Comandos

```bash
cd /var/www/cmdbsyncer
source ENV/bin/activate

# Verifique se os comandos estão disponíveis
./cmdbsyncer vmware_rest --help

# Deve mostrar:
# Usage: cmdbsyncer vmware_rest [OPTIONS] COMMAND [ARGS]...
# VMware REST API commands
#
# Commands:
#   import_vms      Import VMs from vCenter via REST API
#   inventorize_vms Inventorize existing VMs with detailed data
```

### 2. Verifique os Jobs Registrados

Na interface web do CMDBSyncer:

1. Acesse `http://seu-servidor:5003`
2. Vá para **Jobs** → **Cron Groups** → **Create**
3. No campo **Command**, você deve ver:
   - `VMware REST: Import VMs`
   - `VMware REST: Inventorize VMs`

## Configuração Inicial

### 1. Configurar SSL Global

Edite `/var/www/cmdbsyncer/application/config.py`:

```python
# Para certificados auto-assinados
DISABLE_SSL_ERRORS = True

# Timeouts HTTP (opcional)
HTTP_REQUEST_TIMEOUT = 30
HTTP_MAX_RETRIES = 3
```

### 2. Verificar Permissões

```bash
# Arquivos devem ter permissões corretas
chown cmdbsyncer:cmdbsyncer /var/www/cmdbsyncer/application/plugins/vmware_rest_api.py
chmod 644 /var/www/cmdbsyncer/application/plugins/vmware_rest_api.py
```

## Instalação em Docker

Se usar CMDBSyncer em Docker:

```bash
# Entre no container
docker exec -it cmdb_syncer-api-1 sh

# Navegue para plugins
cd /srv/cmdbsyncer/application/plugins/

# Copie o arquivo
# (arquivo deve estar montado ou copiado para o container)

# Teste
./cmdbsyncer vmware_rest --help
```

## Troubleshooting da Instalação

### Problema: Comando não encontrado

```bash
# Erro: bash: ./cmdbsyncer: No such file or directory
# Solução: Verifique se está no diretório correto
pwd
ls -la cmdbsyncer
```

### Problema: Módulo não encontrado

```bash
# Erro: ModuleNotFoundError: No module named 'application'
# Solução: Ative o ambiente virtual
source ENV/bin/activate
```

### Problema: Erro de sintaxe

```bash
# Erro: SyntaxError ou IndentationError
# Solução: Verifique se o arquivo foi copiado corretamente
python -m py_compile vmware_rest_api.py
```

### Problema: Comandos VMware não aparecem

```bash
# Solução: Reinicie o CMDBSyncer ou force reload
sudo systemctl restart cmdbsyncer

# Ou manualmente
pkill -f "python.*cmdbsyncer"
# Reinicie o processo
```

### Problema: SSL Certificate Error

```bash
# Erro: [SSL: CERTIFICATE_VERIFY_FAILED]
# Solução: Configure DISABLE_SSL_ERRORS = True
vim application/config.py
```

## Próximos Passos

Após a instalação bem-sucedida:

1. Configure uma conta VMware: Veja [`configuration.md`](configuration.md)
2. Execute a primeira importação: Veja [`usage.md`](usage.md)
3. Configure automação: Defina cron jobs
4. Monitore via interface web: Acompanhe a sincronização

## Suporte

Se encontrar problemas:

1. Verifique os logs: `tail -f /var/log/cmdbsyncer/cmdbsyncer.log`
2. Execute em modo debug: `./cmdbsyncer vmware_rest import_vms conta --debug`
3. Consulte [`troubleshooting.md`](troubleshooting.md)
4. Abra uma issue no GitHub: [Issues](https://github.com/felipesoaresti/cmdbsyncer-plugins/issues)

## Atualizações

Para atualizar o plugin:

```bash
# Backup do arquivo atual
cp vmware_rest_api.py vmware_rest_api.py.backup

# Baixe a nova versão
wget -O vmware_rest_api.py https://raw.githubusercontent.com/felipesoaresti/cmdbsyncer-plugins/main/vmware-rest/plugin/vmware_rest_api.py

# Teste a nova versão
./cmdbsyncer vmware_rest --help

# Se tudo funcionar, remova o backup
rm vmware_rest_api.py.backup
```
