# Configuração VMware via Interface GUI

## Como Configurar a Conta VMware no cmdbsybcer

### 1. **Acessar a Interface de Administração**

1. Acesse a interface web do cmdbsybcer
2. Faça login com suas credenciais
3. Vá até **Accounts** → **Accounts**

### 2. **Criar Nova Conta VMware**

1. Clique em **Create**
2. Preencha os campos básicos:

#### **Configuração Básica:**
| Campo | Valor |
|-------|-------|
| **Name** | `diamante-vmware` |
| **Type** | `Vmware vCenter` |
| **Address** | `SEU_VCENTER.EXEMPLO.COM` |
| **Username** | `DOMINIO\USUARIO` |
| **Password** | `SUA_SENHA_AQUI` |
| **Enabled** | ✅ Marcado |

#### **Account Settings:**
| Campo | Valor |
|-------|-------|
| **Is Master** | ✅ Marcado |

#### **Object Settings:**
| Campo | Valor |
|-------|-------|
| **Is Object** | ❌ Desmarcado |
| **Object Type** | `Autodetect by Plugin` |

### 3. **Configurações Avançadas (Custom Fields)**

Na seção **Additional configuration** → **Custom Fields**, adicione as seguintes configurações:

| Name | Value | Descrição |
|------|-------|-----------|
| `collect_tags` | `true` | Habilita coleta de tags VMware |
| `include_templates` | `false` | Inclui templates na coleta |
| `collect_folder_hierarchy` | `true` | Coleta hierarquia de folders |
| `max_folder_depth` | `9` | Profundidade máxima de folders |
| `debug_vm_collection` | `false` | Debug detalhado da coleta |
| `connection_timeout` | `30` | Timeout de conexão em segundos |

### 4. **Configurações de Plugin Settings (Opcional)**

Se necessário, na seção **Plugin Settings**, você pode configurar filtros por tipo de objeto:
- **Plugin**: `vmware`
- **Object Filter**: `host` (ou outros tipos conforme necessário)

### 5. **Salvar a Configuração**

1. Clique em **Save**
2. Verifique se a conta aparece na lista de contas ativas

## Como o Código Acessa as Configurações

O código Python acessa essas configurações através do sistema de Plugin do cmdbsybcer:

```python
# Exemplo de como o código acessa as configurações
vm = VMwareCustomAttributesPlugin('diamante-vmware')

# Configurações básicas ficam em:
vm.config['address']    # SEU_VCENTER.EXEMPLO.COM
vm.config['username']   # DOMINIO\USUARIO
vm.config['password']   # SUA_SENHA_AQUI

# Configurações customizadas ficam em:
vm.config['custom_fields']['collect_tags']           # 'true'
vm.config['custom_fields']['include_templates']      # 'false'
vm.config['custom_fields']['collect_folder_hierarchy'] # 'true'
```

## Atualização Necessária no Código

O código precisa ser ajustado para ler as configurações do campo `custom_fields`. Vou mostrar como:

```python
def get_custom_setting(self, setting_name, default_value=None):
    """
    Obter configuração customizada da conta
    """
    custom_fields = self.config.get('custom_fields', {})

    # Procurar pela configuração nos custom_fields
    for field in custom_fields:
        if field.get('name') == setting_name:
            value = field.get('value', default_value)
            # Converter string para boolean se necessário
            if value in ('true', 'True', '1'):
                return True
            elif value in ('false', 'False', '0'):
                return False
            return value

    return default_value

# Uso no código:
collect_tags = self.get_custom_setting('collect_tags', False)
include_templates = self.get_custom_setting('include_templates', False)
max_depth = int(self.get_custom_setting('max_folder_depth', '9'))
```

## Comandos CLI para Testar

Após configurar a conta, use estes comandos:

```bash
# Testar conexão
./cmdbsyncer vmware test_connection diamante-vmware --debug

# Listar VMs no formato original
./cmdbsyncer vmware list_vms_enhanced diamante-vmware --format getallvmscols

# Comparar com getallvmscols.py
./cmdbsyncer vmware compare_getallvmscols diamante-vmware --debug

# Inventorizar attributes
./cmdbsyncer vmware inventorize_custom_attributes diamante-vmware --debug
```

## Exemplo Visual da Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                        Create Account                           │
├─────────────────────────────────────────────────────────────────┤
│ Basics                                                          │
│ ┌─────────────────┬─────────────────────────────────────────┐   │
│ │ Name            │ diamante-vmware                         │   │
│ │ Type            │ Vmware vCenter                          │   │
│ └─────────────────┴─────────────────────────────────────────┘   │
│                                                                 │
│ Account Settings                                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ☑ Is Master                                                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Access Config                                                   │
│ ┌─────────────────┬─────────────────────────────────────────┐   │
│ │ Address         │ SEU_VCENTER.EXEMPLO.COM                 │   │
│ │ Username        │ DOMINIO\USUARIO                         │   │
│ │ Password        │ ••••••••••                              │   │
│ └─────────────────┴─────────────────────────────────────────┘   │
│                                                                 │
│ Additional Configuration                                        │
│ Custom Fields:                                                  │
│ ┌─────────────────┬─────────────────────────────────────────┐   │
│ │ collect_tags    │ true                                    │   │
│ │ include_templates│ false                                  │   │
│ │ max_folder_depth│ 9                                       │   │
│ └─────────────────┴─────────────────────────────────────────┘   │
│                                                                 │
│            [Save]              [Save and Continue]             │
└─────────────────────────────────────────────────────────────────┘
```

## Verificação da Configuração

Após salvar, você pode verificar a configuração:

1. **Via Interface**: A conta deve aparecer na lista com status ativo
2. **Via CLI**: Execute `./cmdbsyncer vmware test_connection diamante-vmware`
3. **Via Logs**: Verifique os logs em `/var/log/cmdbsyncer/`

## Solução de Problemas Comuns

### 1. **Conta não encontrada**
```bash
# Erro: Account 'diamante-vmware' not found
# Solução: Verificar se o nome está correto e a conta está habilitada
```

### 2. **Erro de conexão SSL**
- Adicionar custom field: `disable_ssl_verify` = `true`

### 3. **Credenciais incorretas**
- Verificar username (incluir domínio: `DOMINIO\USUARIO`)
- Verificar se a senha está correta

### 4. **Timeout de conexão**
- Aumentar custom field: `connection_timeout` = `60`

Esta é a forma correta de configurar o VMware no cmdbsybcer - via interface GUI, não via arquivos de configuração!
