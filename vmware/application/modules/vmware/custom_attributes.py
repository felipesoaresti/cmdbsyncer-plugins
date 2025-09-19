#!/usr/bin/env python3
"""Sync VMware Vsphere Custom Attributes - VERSÃO APRIMORADA"""
#pylint: disable=logging-fstring-interpolation

import requests
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, MofNCompleteColumn

try:
    from pyVmomi import vim
except ImportError:
    pass

from syncerapi.v1 import (
    Host,
)

from syncerapi.v1.inventory import (
    run_inventory,
)

from application import logger
from application import app
from application.modules.vmware.vmware import VMWareVcenterPlugin


class VMwareCustomAttributesPlugin(VMWareVcenterPlugin):
    """
    VMware Custom Attributes - VERSÃO APRIMORADA
    Inclui todas as informações coletadas pelo getallvmscols.py
    """
    console = None
    container_view = None

    def get_vm_tags(self, vm_id):
        """
        Coletar tags VMware usando REST API
        """
        try:
            base_url = f'https://{self.config["address"]}'
            cis_url = f'{base_url}/rest/com/vmware/cis'

            with requests.Session() as session:
                session.auth = (self.config['username'], self.config['password'])
                session.verify = False

                # Autenticar na API REST
                token_response = session.post(f'{cis_url}/session')
                if token_response.status_code == 200:
                    # Coletar todas as tags
                    tags_response = session.get(f'{cis_url}/tagging/tag')
                    if tags_response.status_code == 200:
                        tags_data = tags_response.json()
                        vm_tags = []

                        for tag_id in tags_data.get('value', []):
                            # Verificar se a tag está associada à VM
                            associations_response = session.post(
                                f'{cis_url}/tagging/tag-association/id:{tag_id}?~action=list-attached-objects'
                            )
                            if associations_response.status_code == 200:
                                associations = associations_response.json().get('value', [])
                                for association in associations:
                                    if association.get('id') == vm_id:
                                        # Obter detalhes da tag
                                        tag_details = session.get(f'{cis_url}/tagging/tag/id:{tag_id}')
                                        if tag_details.status_code == 200:
                                            tag_info = tag_details.json().get('value', {})
                                            vm_tags.append({
                                                'name': tag_info.get('name', ''),
                                                'description': tag_info.get('description', '')
                                            })
                        return vm_tags
        except Exception as e:
            logger.debug(f"Erro ao coletar tags para VM {vm_id}: {e}")
        return []

    def get_vm_folder_hierarchy(self, vm, max_depth=9):
        """
        Coletar hierarquia completa de folders da VM
        """
        vm_folders = []
        try:
            parent_obj = vm
            for count in range(1, max_depth + 1):
                try:
                    # Navegar para o parent
                    parent_obj = parent_obj.parent
                    if parent_obj and hasattr(parent_obj, 'name'):
                        # Inserir no início para manter ordem hierárquica
                        vm_folders.insert(0, parent_obj.name)
                    else:
                        break
                except (AttributeError, TypeError):
                    break

            return ' > '.join(vm_folders) if vm_folders else ''
        except Exception as e:
            logger.debug(f"Erro ao coletar hierarquia de folders: {e}")
            return ''

    def get_vm_attributes(self, vm, content):
        """
        Prepare Attributes - VERSÃO EXPANDIDA
        Coleta todas as informações disponíveis no getallvmscols.py
        """
        # Coletar hierarquia de folders
        folder_hierarchy = self.get_vm_folder_hierarchy(vm)

        # Coletar tags (se habilitado na configuração)
        vm_tags = []
        collect_tags = self.config.get('settings', {}).get('collect_tags', False)
        if collect_tags and vm.config:
            vm_tags = self.get_vm_tags(vm.config.instanceUuid)

        # Atributos básicos
        attributes = {
            "name": vm.name,
            "folder_hierarchy": folder_hierarchy,
            "tags": vm_tags,
        }

        # Informações do Guest
        if vm.guest:
            attributes.update({
                "ip_address": vm.guest.ipAddress or "",
                "hostname": vm.guest.hostName or "",
                "full_name": vm.guest.guestFullName or "",
                "tools_status": str(vm.guest.toolsStatus) if vm.guest.toolsStatus else "",
            })

        # Informações de Configuração
        if vm.config:
            attributes.update({
                "cpu_count": vm.config.hardware.numCPU,
                "memory_mb": vm.config.hardware.memoryMB,
                "guest_os": vm.config.guestFullName or "",
                "uuid": vm.config.uuid or "",
                "guest_id": vm.config.guestId or "",
                "annotation": vm.config.annotation or "",
                "is_template": vm.config.template,
                "vm_path_name": vm.config.vmPathName or "",
                "instance_uuid": vm.config.instanceUuid or "",
            })

        # Informações de Runtime
        if vm.runtime:
            # Obter nome do host ESXi
            esxi_host_name = ""
            try:
                if vm.runtime.host:
                    esxi_host_name = vm.runtime.host.name
            except Exception as e:
                logger.debug(f"Erro ao obter nome do host ESXi: {e}")

            attributes.update({
                "power_state": str(vm.runtime.powerState) if vm.runtime.powerState else "",
                "runtime_host": vm.runtime.host,
                "boot_time": vm.runtime.bootTime,
                "esxi_host_name": esxi_host_name,
            })

        # Informações de Rede
        if vm.network:
            networks = []
            for network in vm.network:
                networks.append({'name': network.name})
            attributes['networks'] = networks

        # Informações de Datastore
        if vm.datastore:
            datastores = []
            for datastore in vm.datastore:
                datastores.append({'name': datastore.info.name})
            attributes['datastores'] = datastores

        # Custom Fields existentes
        if vm.customValue:
            for custom_field in vm.customValue:
                field_key = custom_field.key
                field_name = next(
                    (f.name for f in content.customFieldsManager.field if f.key == field_key),
                    f"custom_{field_key}"
                )
                attributes[field_name] = custom_field.value

        # Formatar valores para string/lista quando necessário
        return_dict = {}
        for key, value in attributes.items():
            if value is None:
                value = ""
            elif not isinstance(value, (str, list, dict, bool, int, float)):
                value = str(value)
            return_dict[key] = value

        return return_dict

    def get_current_attributes(self, include_templates=None):
        """
        Return list of all Objects and their Attributes
        VERSÃO APRIMORADA com filtro de templates
        """
        # Verificar configuração para incluir templates
        if include_templates is None:
            include_templates = self.config.get('settings', {}).get('include_templates', False)

        content = self.vcenter.RetrieveContent()
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        self.container_view = container.view

        data = []
        for vm in self.container_view:
            # Filtrar templates se necessário
            try:
                if not include_templates and vm.config and vm.config.template:
                    logger.debug(f"Pulando template: {vm.name}")
                    continue
            except Exception as e:
                logger.debug(f"Erro ao verificar se é template: {e}")

            try:
                vm_data = self.get_vm_attributes(vm, content)
                data.append(vm_data)
            except Exception as e:
                logger.error(f"Erro ao processar VM {vm.name}: {e}")
                if self.debug:
                    raise

        return data

    def print_getallvmscols_format(self):
        """
        Imprimir no formato compatível com getallvmscols.py
        Para fins de comparação e debug
        """
        self.connect()
        vms_data = self.get_current_attributes()

        print("=== FORMATO COMPATÍVEL COM getallvmscols.py ===")
        for vm_data in vms_data:
            # Formatar similar ao getallvmscols.py
            name = vm_data.get('name', '')
            folders = vm_data.get('folder_hierarchy', '')
            tags = ', '.join([tag.get('name', '') for tag in vm_data.get('tags', [])])
            is_template = vm_data.get('is_template', False)
            vm_path = vm_data.get('vm_path_name', '')
            esxi_host = vm_data.get('esxi_host_name', '')
            hostname = vm_data.get('hostname', '')
            guest_os = vm_data.get('guest_os', '')
            instance_uuid = vm_data.get('instance_uuid', '')
            bios_uuid = vm_data.get('uuid', '')
            power_state = vm_data.get('power_state', '')
            tools_status = vm_data.get('tools_status', '')
            ip_address = vm_data.get('ip_address', '')

            print(f"'{name}';'{folders}';'{tags}';'{is_template}';'{vm_path}';'{esxi_host}';'{hostname}';'{guest_os}';'{instance_uuid}';'{bios_uuid}';'{power_state}';'{tools_status}';'{ip_address}'")

    def export_attributes(self):
        """
        Export Custom Attributes - VERSÃO MANTIDA
        """
        self.connect()
        current_attributes = {x['name']:x for x in self.get_current_attributes()}

        current_vms = {x.name:x for x in self.container_view}

        object_filter = self.config['settings'].get(self.name, {}).get('filter')
        db_objects = Host.objects_by_filter(object_filter)
        total = db_objects.count()
        with Progress(SpinnerColumn(),
                      MofNCompleteColumn(),
                      *Progress.get_default_columns(),
                      TimeElapsedColumn()) as progress:
            self.console = progress.console.print
            task1 = progress.add_task("Updating Attributes", total=total)
            hostname = None
            for db_host in db_objects:
                try:
                    hostname = db_host.hostname
                    all_attributes = self.get_attributes(db_host, 'vmware_vcenter')
                    if not all_attributes:
                        progress.advance(task1)
                        continue
                    custom_rules = self.get_host_data(db_host, all_attributes['all'])
                    if not custom_rules:
                        progress.advance(task1)
                        continue

                    self.console(f" * Working on {hostname}")
                    logger.debug(f"{hostname}: {custom_rules}")
                    changes = []
                    if vm_host_data := current_attributes.get(hostname):
                        for new_attr_name, new_attr_value in custom_rules['attributes'].items():
                            old_value = False
                            if old_attr := vm_host_data.get(new_attr_name):
                                old_value = old_attr
                            if old_value != new_attr_value:
                                changes.append(f"{new_attr_name}: {old_attr} to {new_attr_value}")
                                current_vms[hostname].SetCustomValue(key=new_attr_name,
                                                                     value=new_attr_value)
                        logger.debug(f" Updated: {changes}")
                    else:
                        logger.debug(f" Not found in VMware Data")
                        progress.advance(task1)
                        continue

                except Exception as error:
                    if self.debug:
                        raise
                    self.log_details.append((f'export_error {hostname}', str(error)))
                    self.console(f" Error in process: {error}")
                progress.advance(task1)

    def inventorize_attributes(self):
        """
        Inventorize Custom Attributes - VERSÃO MANTIDA
        """
        self.connect()
        run_inventory(self.config, [(x['name'], x) for x in self.get_current_attributes()])
