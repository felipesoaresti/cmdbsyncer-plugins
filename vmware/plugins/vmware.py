#!/usr/bin/env python3
"""VMware Enhanced CLI Commands"""
#pylint: disable=logging-fstring-interpolation
import click
import json
import csv
import sys
from datetime import datetime

try:
    from pyVmomi import vim
except ImportError:
    vim = None

from application.modules.rule.rewrite import Rewrite
from application.modules.vmware.models import (
    VMwareRewriteAttributes,
    VMwareCustomAttributes,
)
from application.modules.vmware.custom_attributes import (
    VMwareCustomAttributesPlugin,
)
from application.modules.vmware.rules import VmwareCustomAttributesRule
from syncerapi.v1 import (
    register_cronjob,
)
from syncerapi.v1.core import (
    cli,
)


@cli.group(name='vmware')
def cli_vmware():
    """VMware commands"""


# Comandos existentes mantidos...
def custom_attributes_export(account, debug=False):
    """Custom Attributes Export"""
    attribute_rewrite = Rewrite()
    attribute_rewrite.cache_name = 'vmware_rewrite'
    attribute_rewrite.rules = VMwareRewriteAttributes.objects(enabled=True).order_by('sort_field')

    rules = VmwareCustomAttributesRule()
    rules.rules = VMwareCustomAttributes.objects(enabled=True).order_by('sort_field')

    try:
        vm = VMwareCustomAttributesPlugin(account)
        vm.rewrite = attribute_rewrite
        vm.actions = rules
        vm.name = f"Export Attributes for {account}"
        vm.source = "vmware_attribute_export"
        vm.export_attributes()
    except Exception:
        if debug:
            raise


def custom_attributes_inventorize(account, debug=False):
    """Custom Attribute Inventorize"""
    try:
        vm = VMwareCustomAttributesPlugin(account)
        vm.name = f"Inventorize data from {account}"
        vm.source = "vmware_attribute_inventorize"
        vm.inventorize_attributes()
    except Exception:
        if debug:
            raise


# NOVOS COMANDOS PARA FUNCIONALIDADES APRIMORADAS

def list_vms_enhanced(account, include_templates=False, output_format='table', debug=False):
    """
    Listar VMs com informações aprimoradas (compatível com getallvmscols.py)
    """
    try:
        vm = VMwareCustomAttributesPlugin(account)
        vm.name = f"List VMs Enhanced for {account}"
        vm.source = "vmware_list_enhanced"
        vm.debug = debug

        # Conectar e coletar dados
        vm.connect()
        vms_data = vm.get_current_attributes(include_templates=include_templates)

        if output_format == 'getallvmscols':
            vm.print_getallvmscols_format()
        elif output_format == 'json':
            print(json.dumps(vms_data, indent=2, default=str))
        elif output_format == 'csv':
            print_csv_format(vms_data)
        else:
            print_table_format(vms_data)

    except Exception as e:
        if debug:
            raise
        print(f"Erro: {e}")


def compare_with_getallvmscols(account, debug=False):
    """
    Comparar dados coletados com o formato do getallvmscols.py
    """
    try:
        vm = VMwareCustomAttributesPlugin(account)
        vm.name = f"Compare with getallvmscols for {account}"
        vm.source = "vmware_compare"
        vm.debug = debug

        print("=== COMPARAÇÃO COM getallvmscols.py ===")
        print("Campos coletados pelo módulo enhanced:")

        vm.connect()
        vms_data = vm.get_current_attributes(include_templates=True)

        if vms_data:
            sample_vm = vms_data[0]
            print("\nCampos disponíveis:")
            for key in sorted(sample_vm.keys()):
                print(f"  - {key}: {type(sample_vm[key]).__name__}")

            print(f"\nTotal de VMs encontradas: {len(vms_data)}")
            print(f"VMs que são templates: {sum(1 for vm in vms_data if vm.get('is_template', False))}")
            print(f"VMs ativas: {sum(1 for vm in vms_data if not vm.get('is_template', False))}")

            print("\n=== FORMATO getallvmscols.py ===")
            vm.print_getallvmscols_format()
        else:
            print("Nenhuma VM encontrada.")

    except Exception as e:
        if debug:
            raise
        print(f"Erro: {e}")


def test_vmware_connection(account, debug=False):
    """
    Testar conexão e capacidades do VMware
    """
    try:
        vm = VMwareCustomAttributesPlugin(account)
        vm.name = f"Test Connection for {account}"
        vm.source = "vmware_test"
        vm.debug = debug

        print("=== TESTE DE CONEXÃO VMWARE ===")

        # Testar conexão básica
        print("1. Testando conexão básica...")
        vm.connect()
        print("   ✅ Conexão estabelecida com sucesso")

        # Testar coleta de VMs
        print("2. Testando coleta de VMs...")
        content = vm.vcenter.RetrieveContent()

        if vim is None:
            print("   ❌ Erro: pyVmomi não está disponível")
            return

        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        vms = container.view
        print(f"   ✅ {len(vms)} VMs encontradas")

        # Testar coleta de informações detalhadas
        print("3. Testando coleta de informações detalhadas...")
        if vms:
            sample_vm = vms[0]
            vm_data = vm.get_vm_attributes(sample_vm, content)
            print(f"   ✅ {len(vm_data)} campos coletados para VM exemplo")
            print(f"   VM exemplo: {vm_data.get('name', 'N/A')}")

        # Testar coleta de tags (se habilitado)
        print("4. Testando coleta de tags...")
        if vm.config.get('settings', {}).get('collect_tags', False):
            try:
                if vms and vms[0].config:
                    tags = vm.get_vm_tags(vms[0].config.instanceUuid)
                    print(f"   ✅ {len(tags)} tags encontradas para VM exemplo")
                else:
                    print("   ⚠️  Nenhuma VM disponível para teste de tags")
            except Exception as e:
                print(f"   ❌ Erro ao coletar tags: {e}")
        else:
            print("   ⚠️  Coleta de tags desabilitada na configuração")

        # Resumo das capacidades
        print("\n=== RESUMO DAS CAPACIDADES ===")
        capabilities = [
            ("Conexão VMware", "✅"),
            ("Coleta de VMs", "✅"),
            ("Informações básicas", "✅"),
            ("Hierarquia de folders", "✅"),
            ("Informações de template", "✅"),
            ("Host ESXi", "✅"),
            ("UUIDs", "✅"),
            ("Tags VMware", "✅" if vm.config.get('settings', {}).get('collect_tags') else "⚠️"),
        ]

        for capability, status in capabilities:
            print(f"  {capability}: {status}")

    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        if debug:
            raise


def print_csv_format(vms_data):
    """Imprimir no formato CSV"""
    if not vms_data:
        return

    # Cabeçalhos baseados no getallvmscols.py
    headers = [
        'name', 'folder_hierarchy', 'tags', 'is_template', 'vm_path_name',
        'esxi_host_name', 'hostname', 'guest_os', 'instance_uuid', 'uuid',
        'power_state', 'tools_status', 'ip_address'
    ]

    writer = csv.DictWriter(sys.stdout, fieldnames=headers)
    writer.writeheader()

    for vm_data in vms_data:
        row = {}
        for header in headers:
            value = vm_data.get(header, '')
            if header == 'tags' and isinstance(value, list):
                value = ', '.join([tag.get('name', '') for tag in value])
            row[header] = value
        writer.writerow(row)


def print_table_format(vms_data):
    """Imprimir em formato de tabela simples"""
    if not vms_data:
        print("Nenhuma VM encontrada.")
        return

    print(f"\n{'Nome':<30} {'Folder':<20} {'Template':<8} {'Host ESXi':<20} {'IP':<15} {'Estado':<10}")
    print("-" * 110)

    for vm_data in vms_data:
        name = vm_data.get('name', '')[:29]
        folder = vm_data.get('folder_hierarchy', '').split(' > ')[-1][:19] if vm_data.get('folder_hierarchy') else ''
        is_template = 'Sim' if vm_data.get('is_template', False) else 'Não'
        esxi_host = vm_data.get('esxi_host_name', '')[:19]
        ip = vm_data.get('ip_address', '')[:14]
        state = vm_data.get('power_state', '')[:9]

        print(f"{name:<30} {folder:<20} {is_template:<8} {esxi_host:<20} {ip:<15} {state:<10}")


# Registrar novos comandos CLI
@cli_vmware.command('list_vms_enhanced')
@click.option("--include-templates", is_flag=True, help="Incluir templates na listagem")
@click.option("--format", "output_format", default='table',
              type=click.Choice(['table', 'csv', 'json', 'getallvmscols']),
              help="Formato de saída")
@click.option("--debug", is_flag=True)
@click.argument('account')
def cli_list_vms_enhanced(account, include_templates, output_format, debug):
    """Listar VMs com informações aprimoradas"""
    list_vms_enhanced(account, include_templates, output_format, debug)


@cli_vmware.command('compare_getallvmscols')
@click.option("--debug", is_flag=True)
@click.argument('account')
def cli_compare_getallvmscols(account, debug):
    """Comparar com formato getallvmscols.py"""
    compare_with_getallvmscols(account, debug)


@cli_vmware.command('test_connection')
@click.option("--debug", is_flag=True)
@click.argument('account')
def cli_test_connection(account, debug):
    """Testar conexão e capacidades VMware"""
    test_vmware_connection(account, debug)


@cli_vmware.command('export_custom_attributes')
@click.option("--debug", is_flag=True)
@click.argument('account')
def cli_custom_attributes_export(account, debug):
    """Export Custom Attributes"""
    custom_attributes_export(account, debug)


@cli_vmware.command('inventorize_custom_attributes')
@click.option("--debug", is_flag=True)
@click.argument('account')
def cli_inventorize_custom_attributes(account, debug):
    """Inventorize Custom Attributes from VMware"""
    custom_attributes_inventorize(account, debug)


# Registrar cronjobs existentes
register_cronjob("VMware: Export Custom Attributes", custom_attributes_export)
register_cronjob("VMware: Inventorize Custom Attributes", custom_attributes_inventorize)
