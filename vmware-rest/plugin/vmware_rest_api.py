#!/usr/bin/env python3
"""
VMware REST API Plugin for CMDBSyncer

This plugin provides integration with VMware vCenter using native REST API,
allowing import and inventorization of virtual machines into CMDBSyncer.

Author: Felipe Soares
License: MIT
Version: 1.0.0
"""

import click
import requests
import urllib3
import time
from application import logger, app
from syncerapi.v1 import (
    register_cronjob,
    Host,
)
from syncerapi.v1.core import (
    cli,
    Plugin,
)
from syncerapi.v1.inventory import run_inventory

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VMwareRestApiPlugin(Plugin):
    """
    VMware REST API Plugin

    Provides functionality to connect to VMware vCenter via REST API
    and synchronize virtual machine data with CMDBSyncer.
    """

    session_id = None
    base_url = None

    def __init__(self, account):
        """
        Initialize the plugin with account configuration.

        Args:
            account (str): Account name configured in CMDBSyncer
        """
        super().__init__(account)
        self.base_url = f"https://{self.config['address']}"

    def get_session_id(self):
        """
        Obtain session ID from vCenter REST API.

        Returns:
            bool: True if session obtained successfully, False otherwise
        """
        url = f"{self.base_url}/api/session"

        try:
            response = requests.post(
                url,
                auth=(self.config['username'], self.config['password']),
                verify=False,
                timeout=30
            )

            if response.ok:
                self.session_id = response.json()
                logger.info(f"Session ID obtained successfully")
                return True
            else:
                logger.error(f"Failed to obtain session ID: {response.status_code} {response.text}")
                return False

        except Exception as e:
            logger.error(f"Connection error to vCenter: {str(e)}")
            return False

    def get_vms(self):
        """
        Retrieve all virtual machines from vCenter.

        Returns:
            list: List of VM data dictionaries
        """
        if not self.session_id:
            if not self.get_session_id():
                return []

        url = f"{self.base_url}/api/vcenter/vm"
        headers = {"vmware-api-session-id": self.session_id}

        try:
            response = requests.get(url, headers=headers, verify=False, timeout=30)

            if response.ok:
                vms = response.json()
                logger.info(f"Found {len(vms)} VMs")
                return vms
            else:
                logger.error(f"Failed to retrieve VMs: {response.status_code} {response.text}")
                return []

        except Exception as e:
            logger.error(f"Error retrieving VMs: {str(e)}")
            return []

    def get_vm_details(self, vm_id):
        """
        Retrieve detailed information for a specific VM.

        Args:
            vm_id (str): VM identifier

        Returns:
            dict: VM details or None if error
        """
        if not self.session_id:
            if not self.get_session_id():
                return None

        url = f"{self.base_url}/api/vcenter/vm/{vm_id}"
        headers = {"vmware-api-session-id": self.session_id}

        try:
            response = requests.get(url, headers=headers, verify=False, timeout=30)

            if response.ok:
                return response.json()
            else:
                logger.warning(f"Failed to retrieve VM details for {vm_id}: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"Error retrieving VM details for {vm_id}: {str(e)}")
            return None

    def import_vms(self):
        """
        Import VMs as hosts in CMDBSyncer.

        This method retrieves all VMs from vCenter and creates corresponding
        hosts in CMDBSyncer with basic VM information as labels.
        """
        logger.info("Starting VM import from vCenter")

        vms = self.get_vms()
        if not vms:
            logger.warning("No VMs found")
            return

        created_count = 0
        updated_count = 0

        for vm_data in vms:
            hostname = vm_data.get('name', '').strip()
            if not hostname:
                logger.warning(f"VM without name ignored: {vm_data}")
                continue

            # Prepare VM labels
            labels = {
                'vm_id': vm_data.get('vm', ''),
                'power_state': vm_data.get('power_state', ''),
                'cpu_count': str(vm_data.get('cpu_count', 0)),
                'memory_size_gb': str(round(vm_data.get('memory_size_MiB', 0) / 1024, 2)),
                'memory_size_mib': str(vm_data.get('memory_size_MiB', 0)),
                'vmware_source': 'vcenter_rest_api',
                'vcenter_host': self.config['address'],
                'last_import': str(int(time.time())),
            }

            # Remove empty values
            labels = {k: v for k, v in labels.items() if v}

            logger.info(f"Processing VM: {hostname}")

            # Check if host already exists
            existing_host = Host.get_host(hostname, create=False)

            if existing_host:
                # Update existing host
                existing_host.update_host(labels)
                do_save = existing_host.set_account(account_dict=self.config)
                if do_save:
                    existing_host.save()
                    updated_count += 1
                    logger.info(f"Host {hostname} updated")
                else:
                    logger.info(f"Host {hostname} didn't need update")
            else:
                # Create new host
                host_obj = Host.get_host(hostname)
                host_obj.update_host(labels)
                do_save = host_obj.set_account(account_dict=self.config)
                if do_save:
                    host_obj.save()
                    created_count += 1
                    logger.info(f"Host {hostname} created")

        logger.info(f"Import completed: {created_count} created, {updated_count} updated")

    def inventorize_vms(self):
        """
        Inventorize existing VMs with detailed data.

        This method collects detailed information about VMs and stores
        it in the inventory section of existing hosts.
        """
        logger.info("Starting VM inventorization from vCenter")

        vms = self.get_vms()
        if not vms:
            logger.warning("No VMs found")
            return

        # Prepare data for inventorization
        processed_objects = []

        for vm_data in vms:
            hostname = vm_data.get('name', '').strip()
            if not hostname:
                continue

            # Prepare VM labels
            labels = {
                'vm_id': vm_data.get('vm', ''),
                'power_state': vm_data.get('power_state', ''),
                'cpu_count': str(vm_data.get('cpu_count', 0)),
                'memory_size_gb': str(round(vm_data.get('memory_size_MiB', 0) / 1024, 2)),
                'memory_size_mib': str(vm_data.get('memory_size_MiB', 0)),
                'vmware_source': 'vcenter_rest_api',
                'vcenter_host': self.config['address'],
                'last_inventory': str(int(time.time())),
            }

            # Retrieve additional VM details if possible
            vm_details = self.get_vm_details(vm_data.get('vm'))
            if vm_details:
                guest_info = vm_details.get('guest', {})
                config_info = vm_details.get('config', {})

                if guest_info:
                    labels.update({
                        'guest_hostname': guest_info.get('hostname', ''),
                        'guest_ip': guest_info.get('ip_address', ''),
                        'guest_os': guest_info.get('full_name', ''),
                        'tools_status': guest_info.get('tools_status', ''),
                    })

                if config_info:
                    labels.update({
                        'vm_uuid': config_info.get('uuid', ''),
                        'guest_id': config_info.get('guest_id', ''),
                        'annotation': config_info.get('annotation', ''),
                    })

            # Remove empty values
            labels = {k: v for k, v in labels.items() if v}
            processed_objects.append((hostname, labels))

        if processed_objects:
            logger.info(f"Inventorizing {len(processed_objects)} VMs")
            # Use run_inventory for inventorization
            run_inventory(self.config, processed_objects)
        else:
            logger.warning("No valid VMs to inventorize")


@cli.group(name='vmware_rest')
def cli_vmware_rest():
    """VMware REST API commands"""


def vmware_rest_import(account, debug=False):
    """
    Import VMs from vCenter via REST API

    Args:
        account (str): Account name configured in CMDBSyncer
        debug (bool): Enable debug mode
    """
    try:
        plugin = VMwareRestApiPlugin(account)
        plugin.name = f"Import VMs from {account}"
        plugin.source = "vmware_rest_import"
        plugin.import_vms()
    except Exception as e:
        logger.error(f"Import error: {str(e)}")
        if debug:
            raise


def vmware_rest_inventorize(account, debug=False):
    """
    Inventorize existing VMs

    Args:
        account (str): Account name configured in CMDBSyncer
        debug (bool): Enable debug mode
    """
    try:
        plugin = VMwareRestApiPlugin(account)
        plugin.name = f"Inventorize VMs from {account}"
        plugin.source = "vmware_rest_inventorize"
        plugin.inventorize_vms()
    except Exception as e:
        logger.error(f"Inventorization error: {str(e)}")
        if debug:
            raise


@cli_vmware_rest.command('import_vms')
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.argument('account')
def cli_vmware_rest_import(account, debug):
    """Import VMs from vCenter via REST API"""
    vmware_rest_import(account, debug)


@cli_vmware_rest.command('inventorize_vms')
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.argument('account')
def cli_vmware_rest_inventorize(account, debug):
    """Inventorize existing VMs with detailed data"""
    vmware_rest_inventorize(account, debug)


# Register cron jobs
register_cronjob("VMware REST: Import VMs", vmware_rest_import)
register_cronjob("VMware REST: Inventorize VMs", vmware_rest_inventorize)
