# Guia de Implementação - VMware Enhanced Module

## Resumo

Este guia detalha como implementar as melhorias no módulo VMware do cmdbsybcer para coletar as mesmas informações que o script `getallvmscols.py`.

## Passo a Passo da Implementação

### 1. **Backup dos Arquivos Atuais**

```bash
# Fazer backup dos arquivos que serão modificados
cp application/modules/vmware/custom_attributes.py application/modules/vmware/custom_attributes.py.backup
cp application/plugins/vmware.py application/plugins/vmware.py.backup
```

### 2. **Atualizar o Arquivo custom_attributes.py**

Substituir o conteúdo de `application/modules/vmware/custom_attributes.py` pelo código aprimorado fornecido no artefato "Código Aprimorado - VMware Custom Attributes Plugin".

**Principais mudanças:**
- Método `get_custom_setting()` para acessar configurações do banco de dados
- Método `get_vm_tags()` para coletar tags VMware
- Método `get_vm_folder_hierarchy()` para hierarquia de folders
- Método `get_vm_attributes()` expandido com todos os campos
- Método `print_getallvmscols_format()` para compatibilidade
- Filtro de templates no `get_current_attributes()`

### 3. **Atualizar o Arquivo vmware.py (CLI)**

Substituir o conteúdo de `application/plugins/vmware.py` pelo código dos comandos CLI aprimorados.

**Novos comandos adicionados:**
- `list_vms_enhanced` - Listar VMs com informações completas
- `compare_getallvmscols` - Comparar com formato original
- `test_connection` - Testar conexão e capacidades

### 4. **Configurar a Conta VMware via Interface GUI**

**Em vez de arquivos de configuração, use a interface web:**

1. Acesse a interface do cmdbsybcer
2. Vá em **Accounts** → **Accounts** → **Create**
3. Configure conforme o guia "Configuração VMware via Interface GUI"

#### **Configuração Básica da Conta:**
| Campo | Valor |
|-------|-------|
| **Name** | `diamante-vmware` |
| **Type** | `Vmware vCenter` |
| **Address** | `SEU_VCENTER.EXEMPLO.COM` |
| **Username** | `DOMINIO\USUARIO` |
| **Password** | `SUA_SENHA_AQUI` |
| **Enabled** | ✅ |

#### **Custom Fields (Configurações Avançadas):**
| Name | Value |
|------|-------|
| `collect_tags` | `true` |
| `include_templates` | `false` |
| `collect_folder_hierarchy` | `true` |
| `max_folder_depth` | `9` |
| `debug_vm_collection` | `false` |

### 5. **Adicionar Dependências**

Verificar se as dependências estão instaladas:

```bash
# Verificar se requests está disponível para API REST
pip install requests

# Verificar se pyVmomi está atualizado
pip install --upgrade pyvmomi
```

### 6. **Testes Iniciais**

#### 6.1 Testar Conexão
```bash
./cmdbsyncer vmware test_connection diamante-vmware --debug
```

#### 6.2 Comparar com getallvmscols.py
```bash
./cmdbsyncer vmware compare_getallvmscols diamante-vmware --debug
```

#### 6.3 Listar VMs em formato compatível
```bash
# Formato igual ao getallvmscols.py
./cmdbsyncer vmware list_vms_enhanced diamante-vmware --format getallvmscols

# Formato JSON para análise
./cmdbsyncer vmware list_vms_enhanced diamante-vmware --format json

# Formato CSV
./cmdbsyncer vmware list_vms_enhanced diamante-vmware --format csv
```

### 7. **Validação dos Dados**

#### 7.1 Executar getallvmscols.py original
```bash
sudo /root/.local/bin/pipenv run /opt/pentaho/data-integration/seges/glpi-dc/vmware-inv/getallvmscols.py \
  -nossl -s SEU_VCENTER_AQUI \
  -u 'DOMINIO\USUARIO' -p 'SUA_SENHA' > original_output.txt
```

#### 7.2 Executar novo módulo
```bash
./cmdbsyncer vmware list_vms_enhanced diamante-vmware --format getallvmscols > enhanced_output.txt
```

#### 7.3 Comparar resultados
```bash
# Comparar quantidades
wc -l original_output.txt enhanced_output.txt

# Comparar campos (assumindo que têm mesma ordem)
diff original_output.txt enhanced_output.txt
```

### 8. **Configurações Avançadas via Interface GUI**

Para ajustar configurações, edite a conta `diamante-vmware` na interface:

#### 8.1 Habilitar Coleta de Tags
- Edite a conta → Custom Fields
- Adicione/modifique: `collect_tags` = `true`

#### 8.2 Incluir Templates
- Custom Fields: `include_templates` = `true`

#### 8.3 Configurar Timeouts
- Custom Fields: `connection_timeout` = `60`

### 9. **Integração com Processo Existente**

#### 9.1 Testar Inventorização
```bash
./cmdbsyncer vmware inventorize_custom_attributes diamante-vmware --debug
```

#### 9.2 Testar Export de Attributes
```bash
./cmdbsyncer vmware export_custom_attributes diamante-vmware --debug
```

### 10. **Monitoramento e Logs**

#### 10.1 Configurar Logging Detalhado
```yaml
# Em config/logging.yaml
logging:
  vmware_plugin:
    level: "DEBUG"
    log_file: "/var/log/cmdbsyncer/vmware_enhanced.log"
```

#### 10.2 Monitorar Performance
```bash
# Verificar logs
tail -f /var/log/cmdbsyncer/vmware_enhanced.log

# Verificar tempo de execução
time ./cmdbsyncer vmware inventorize_custom_attributes diamante
```

## Verificação de Sucesso

### Checklist de Validação

- [ ] **Conexão**: Módulo conecta com sucesso ao vCenter
- [ ] **Quantidade**: Mesmo número de VMs que getallvmscols.py
- [ ] **Campos básicos**: Nome, IP, hostname coletados corretamente
- [ ] **Folders**: Hierarquia de folders coletada
- [ ] **Templates**: Identificação de templates funciona
- [ ] **Host ESXi**: Nome do host coletado
- [ ] **UUIDs**: Instance e BIOS UUID coletados
- [ ] **Tags**: Tags VMware coletadas (se habilitado)
- [ ] **Performance**: Tempo de execução aceitável

### Campos que Devem Estar Presentes

| Campo Original | Campo Enhanced | Status |
|----------------|----------------|--------|
| name | name | ✅ |
| folders | folder_hierarchy | ✅ |
| tags | tags | ✅ |
| template | is_template | ✅ |
| vmPathName | vm_path_name | ✅ |
| host.name | esxi_host_name | ✅ |
| hostName | hostname | ✅ |
| guestFullName | guest_os | ✅ |
| instanceUuid | instance_uuid | ✅ |
| uuid | uuid | ✅ |
| powerState | power_state | ✅ |
| toolsStatus | tools_status | ✅ |
| ipAddress | ip_address | ✅ |

## Solução de Problemas

### Problemas Comuns

#### 1. **Erro de Autenticação**
```bash
# Verificar credenciais
./cmdbsyncer vmware test_connection diamante --debug
```

#### 2. **Erro de SSL**
```python
# Verificar configuração SSL no código
if app.config.get('DISABLE_SSL_ERRORS'):
    context = ssl._create_unverified_context()
```

#### 3. **Tags não coletadas**
```yaml
# Verificar se API REST está habilitada
settings:
  collect_tags: true
```

#### 4. **Performance lenta**
```yaml
# Ajustar configurações de performance
performance:
  batch_size: 50
  vm_timeout: 5
```

### Logs para Debug

#### Habilitar Debug Detalhado
```bash
./cmdbsyncer vmware list_vms_enhanced diamante --debug
```

#### Verificar Logs do Sistema
```bash
grep -i vmware /var/log/cmdbsyncer/*.log
grep -i error /var/log/cmdbsyncer/vmware_enhanced.log
```

## Rollback (se necessário)

```bash
# Restaurar arquivos originais
cp application/modules/vmware/custom_attributes.py.backup application/modules/vmware/custom_attributes.py
cp application/plugins/vmware.py.backup application/plugins/vmware.py

# Reiniciar serviços
systemctl restart cmdbsyncer
```

## Próximos Passos

1. **Documentar** as novas funcionalidades
2. **Treinar** usuários nos novos comandos
3. **Monitorar** performance em produção
4. **Ajustar** configurações conforme necessário
5. **Implementar** alertas para falhas de coleta

## Comandos de Referência Rápida

```bash
# Teste completo
./cmdbsyncer vmware test_connection diamante --debug

# Comparação com original
./cmdbsyncer vmware compare_getallvmscols diamante

# Inventorização completa
./cmdbsyncer vmware inventorize_custom_attributes diamante

# Export de attributes
./cmdbsyncer vmware export_custom_attributes diamante

# Listagem em formato original
./cmdbsyncer vmware list_vms_enhanced diamante --format getallvmscols
```
