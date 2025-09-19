# VMware REST API Plugin for CMDBSyncer

Custom plugin for integration with VMware vCenter using native REST API, enabling import and synchronization of virtual machines in CMDBSyncer.

## Objective

This plugin was developed for organizations that need to synchronize VM information from VMware vCenter with CMDBSyncer, using exclusively the vCenter REST API (no pyVmomi dependencies).

## Features

### VM Import
- Connects to vCenter via REST API (`/api/session`)
- Fetches all VMs via `/api/vcenter/vm` endpoint
- Creates hosts in CMDBSyncer with basic information
- Self-signed certificate support

### Detailed Inventorization
- Collects detailed data from each VM
- Guest OS information (hostname, IP, operating system)
- VMware Tools status
- UUID and technical configurations

### Automation
- Cron job system integration
- Programmable automatic synchronization
- Detailed execution logs

## Requirements

- CMDBSyncer: 3.10.2 or higher
- Python: 3.11+
- Libraries: requests, urllib3 (already included in CMDBSyncer)
- Access: Account with read permissions on vCenter
- Network: HTTPS connectivity with vCenter (port 443)

## Architecture

```
vCenter API     <-->     Plugin Python     <-->     CMDBSyncer
(REST/HTTPS)             vmware_rest_api             Database
                              ^
                              |
                         Cron Jobs
                         Automation
```

## Quick Installation

1. Copy the plugin to CMDBSyncer server
2. Configure VMware account in web interface
3. Run initial import
4. Configure cron jobs for automatic synchronization

See detailed guide in [`docs/installation-EN.md`](docs/installation-EN.md)

## Project Structure

```
vmware-rest/
├── README-EN.md                # This file
├── plugin/
│   └── vmware_rest_api.py      # Main plugin
├── docs/
│   ├── installation-EN.md      # Installation guide
│   ├── configuration.md        # Account configuration
│   ├── usage.md                # Commands and usage
│   ├── web-interface.md        # Web interface
│   └── troubleshooting.md      # Problem resolution
└── examples/
    └── configurations.md       # Configuration examples
```

## Main Commands

```bash
# Import VMs (first run)
./cmdbsyncer vmware_rest import_vms account-name

# Inventorize detailed data
./cmdbsyncer vmware_rest inventorize_vms account-name

# Debug mode for troubleshooting
./cmdbsyncer vmware_rest import_vms account-name --debug
```

## Collected Data

### Labels (Basic import)
- vm_id: Internal VM identifier
- power_state: VM state (POWERED_ON/OFF)
- cpu_count: Number of virtual CPUs
- memory_size_gb: Memory in GB
- vmware_source: Data origin

### Inventory (Detailed data)
- guest_hostname: Operating system hostname
- guest_ip: Primary IP address
- guest_os: Detected operating system
- tools_status: VMware Tools status
- vm_uuid: Unique VM UUID

## Configuration

### VMware Account in CMDBSyncer

```yaml
Name: my-vcenter
Type: vmware_vcenter
Address: vcenter.example.com
Username: DOMAIN\USER
Password: YOUR_PASSWORD_HERE

Custom Fields:
  inventorize_key: vmware_vcenter
  hostname_field: name
```

## Monitoring

### Web Interface
- Hosts → Hosts: View imported VMs
- Jobs → Cron Stats: Synchronization status
- Dashboard: General statistics

### Command Line
```bash
# View imported hosts
./cmdbsyncer host list | grep vmware

# Detailed logs
tail -f /var/log/cmdbsyncer/cmdbsyncer.log
```

## Troubleshooting

### Common Issues
- SSL Error: Configure `DISABLE_SSL_ERRORS = True`
- Credentials: Verify username and password
- Connectivity: Test HTTPS access to vCenter

See complete guide in [`docs/troubleshooting.md`](docs/troubleshooting.md)

## Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Open a Pull Request

## License

This project is under the MIT license. See [`LICENSE`](../LICENSE) for details.

## Useful Links

- [CMDBSyncer Documentation](https://docs.cmdbsyncer.de)
- [VMware vCenter API Reference](https://developer.vmware.com/apis/vsphere-automation/latest/)
- [Project Issues](https://github.com/felipesoaresti/cmdbsyncer-plugins/issues)