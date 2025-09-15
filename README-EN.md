# CMDBSyncer Plugins

Collection of custom plugins for CMDBSyncer - A modular rule-based system to synchronize hosts between Checkmk, Netbox and other systems.

## 📁 Available Plugins

### VMware REST API Plugin
Plugin for integration with VMware vCenter using native REST API, allowing import and inventorization of virtual machines.

**Location:** `vmware-rest/`

**Features:**
- ✅ Native vCenter REST API connection
- ✅ VM import as CMDBSyncer hosts
- ✅ Detailed inventorization with guest OS data
- ✅ Self-signed certificate support
- ✅ Cron job system integration
- ✅ Structured labels and inventory

## 🚀 Quick Start

1. Clone this repository
2. Navigate to the desired plugin
3. Follow the specific installation instructions
4. Configure through CMDBSyncer web interface

## 📋 Requirements

- CMDBSyncer 3.10.2 or higher
- Python 3.11+
- Administrative access to CMDBSyncer server

## 🔧 General Installation

```bash
# Clone the repository
git clone https://github.com/felipesoaresti/cmdbsyncer-plugins.git

# Navigate to specific plugin
cd cmdbsyncer-plugins/vmware-rest/

# Follow plugin README instructions
```

## 📚 Documentation

Each plugin has detailed documentation in its specific folder:

- **Installation**: Step-by-step installation guide
- **Configuration**: Configuration via web interface
- **Usage**: Usage examples and commands
- **Troubleshooting**: Common problem resolution

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is under the MIT license. See the `LICENSE` file for more details.

## 🔗 Useful Links

- [CMDBSyncer Homepage](https://cmdbsyncer.de)
- [Official Documentation](https://docs.cmdbsyncer.de)
- [Issues and Support](https://github.com/felipesoaresti/cmdbsyncer-plugins/issues)

## 🏷️ Tags

`cmdbsyncer` `vmware` `vcenter` `automation` `itil` `cmdb` `monitoring` `infrastructure`