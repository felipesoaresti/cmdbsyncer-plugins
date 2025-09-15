# Installation Guide - VMware REST API Plugin

This guide explains how to install and configure the VMware REST API plugin in CMDBSyncer.

## 📋 Prerequisites

### System
- **CMDBSyncer**: Version 3.10.2 or higher
- **Python**: 3.11 or higher
- **Operating System**: Linux (tested on Red Hat/CentOS)
- **Permissions**: Root or sudo access on CMDBSyncer server

### Network and Access
- **Connectivity**: HTTPS (port 443) to vCenter
- **Certificates**: Support for self-signed certificates
- **Credentials**: Service account on vCenter with read permissions

### Python Dependencies
The plugin uses libraries already included in CMDBSyncer:
- `requests` - For HTTP requests
- `urllib3` - For SSL connection management
- `click` - For command line interface

## 🛠️ Step-by-Step Installation

### 1. Locate CMDBSyncer Directory

```bash
# Default installation directory
cd /var/www/cmdbsyncer

# Activate virtual environment
source ENV/bin/activate

# Verify it's working
./cmdbsyncer --help
```

**Possible locations:**
- `/var/www/cmdbsyncer` (default installation)
- `/srv/cmdbsyncer` (some distributions)
- `/opt/cmdbsyncer` (custom installation)

### 2. Copy the Plugin

```bash
# Navigate to plugins directory
cd /var/www/cmdbsyncer/application/plugins/

# Download plugin from GitHub
wget https://raw.githubusercontent.com/felipesoaresti/cmdbsyncer-plugins/main/vmware-rest/plugin/vmware_rest_api.py

# Or copy manually
# cp /path/to/vmware_rest_api.py .

# Verify it was copied
ls -la vmware_rest_api.py
```

### 3. Verify Syntax

```bash
# Test Python syntax
python -m py_compile vmware_rest_api.py

# If no errors, it's correct
echo "Plugin syntax OK"
```

### 4. Configure SSL (If Needed)

If using self-signed certificates on vCenter:

```bash
# Edit configuration file
vim /var/www/cmdbsyncer/application/config.py

# Make sure this line exists:
DISABLE_SSL_ERRORS = True
```

### 5. Restart CMDBSyncer (Optional)

```bash
# If using systemd
sudo systemctl restart cmdbsyncer

# Or if using manual process
pkill -f cmdbsyncer
# Then restart according to your configuration
```

## ✅ Installation Verification

### 1. Test Commands

```bash
cd /var/www/cmdbsyncer
source ENV/bin/activate

# Verify commands are available
./cmdbsyncer vmware_rest --help

# Should show:
# Usage: cmdbsyncer vmware_rest [OPTIONS] COMMAND [ARGS]...
# VMware REST API commands
#
# Commands:
#   import_vms      Import VMs from vCenter via REST API
#   inventorize_vms Inventorize existing VMs with detailed data
```

### 2. Verify Registered Jobs

In CMDBSyncer web interface:

1. Access `http://your-server:5003`
2. Go to **Jobs** → **Cron Groups** → **Create**
3. In the **Command** field, you should see:
   - `VMware REST: Import VMs`
   - `VMware REST: Inventorize VMs`

## 🔧 Initial Configuration

### 1. Configure Global SSL

Edit `/var/www/cmdbsyncer/application/config.py`:

```python
# For self-signed certificates
DISABLE_SSL_ERRORS = True

# HTTP timeouts (optional)
HTTP_REQUEST_TIMEOUT = 30
HTTP_MAX_RETRIES = 3
```

### 2. Verify Permissions

```bash
# Files should have correct permissions
chown cmdbsyncer:cmdbsyncer /var/www/cmdbsyncer/application/plugins/vmware_rest_api.py
chmod 644 /var/www/cmdbsyncer/application/plugins/vmware_rest_api.py
```

## 🐳 Docker Installation

If using CMDBSyncer in Docker:

```bash
# Enter container
docker exec -it cmdb_syncer-api-1 sh

# Navigate to plugins
cd /srv/cmdbsyncer/application/plugins/

# Copy file
# (file should be mounted or copied to container)

# Test
./cmdbsyncer vmware_rest --help
```

## 🔍 Installation Troubleshooting

### Issue: Command not found

```bash
# Error: bash: ./cmdbsyncer: No such file or directory
# Solution: Verify you're in the correct directory
pwd
ls -la cmdbsyncer
```

### Issue: Module not found

```bash
# Error: ModuleNotFoundError: No module named 'application'
# Solution: Activate virtual environment
source ENV/bin/activate
```

### Issue: Syntax error

```bash
# Error: SyntaxError or IndentationError
# Solution: Verify file was copied correctly
python -m py_compile vmware_rest_api.py
```

### Issue: VMware commands don't appear

```bash
# Solution: Restart CMDBSyncer or force reload
sudo systemctl restart cmdbsyncer

# Or manually
pkill -f "python.*cmdbsyncer"
# Restart the process
```

### Issue: SSL Certificate Error

```bash
# Error: [SSL: CERTIFICATE_VERIFY_FAILED]
# Solution: Configure DISABLE_SSL_ERRORS = True
vim application/config.py
```

## 📝 Next Steps

After successful installation:

1. **Configure a VMware account**: See [`configuration.md`](configuration.md)
2. **Run first import**: See [`usage.md`](usage.md)
3. **Configure automation**: Set up cron jobs
4. **Monitor via web interface**: Track synchronization

## 📞 Support

If you encounter problems:

1. Check logs: `tail -f /var/log/cmdbsyncer/cmdbsyncer.log`
2. Run in debug mode: `./cmdbsyncer vmware_rest import_vms account --debug`
3. Consult [`troubleshooting.md`](troubleshooting.md)
4. Open GitHub issue: [Issues](https://github.com/felipesoaresti/cmdbsyncer-plugins/issues)

## 🔄 Updates

To update the plugin:

```bash
# Backup current file
cp vmware_rest_api.py vmware_rest_api.py.backup

# Download new version
wget -O vmware_rest_api.py https://raw.githubusercontent.com/felipesoaresti/cmdbsyncer-plugins/main/vmware-rest/plugin/vmware_rest_api.py

# Test new version
./cmdbsyncer vmware_rest --help

# If everything works, remove backup
rm vmware_rest_api.py.backup
```