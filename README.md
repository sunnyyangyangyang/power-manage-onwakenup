# Power Manage on Wake

A systemd service that automatically restores the power profile to "balanced" after your Fedora system wakes from suspend, hibernate, or hybrid-sleep. This fixes the common issue where the power mode incorrectly changes from "balanced" to "performance" after resume.

## Problem

On many Fedora systems, when waking from suspend or hibernation, the power management daemon may incorrectly set the power profile to "performance" instead of maintaining the user's preferred "balanced" setting. This can lead to:

- Increased power consumption
- Higher CPU temperatures
- Reduced battery life on laptops
- Unwanted fan noise

## Solution

This project provides a simple systemd service that:
1. Listens for system wake events (suspend, hibernate, hybrid-sleep)
2. Temporarily sets power profile to "power-saver"
3. Waits 1 second
4. Restores the power profile to "balanced"

## Installation

### Method 1: Build from Source (Recommended)

1. Install required dependencies:
   ```bash
   sudo dnf install rpm-build systemd power-profiles-daemon
   ```

2. Download this repository:
   ```bash
   git clone https://github.com/sunnyyangyangyang/power-manage-onwakenup.git
   cd power-manage-onwakenup
   ```

3. Build the RPM package:
   ```bash
   rpmbuild -bb set-power-profile-on-wake.spec
   ```

4. Install the package:
   ```bash
   sudo dnf install /path/to/rpms/set-power-profile-on-wake-1.0-1.fcXX.noarch.rpm
   ```
   (Replace `fcXX` with your Fedora version)

5. Enable and start the service:
   ```bash
   sudo systemctl enable set-power-profile-on-wake.service
   sudo systemctl start set-power-profile-on-wake.service
   ```

### Method 2: Manual Installation

1. Create the systemd service file as root:

   ```bash
   sudo tee /etc/systemd/system/set-power-profile-on-wake.service << 'EOF'
   [Unit]
   Description=Set power profile to balanced after wake
   After=suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target

   [Service]
   Type=oneshot
   ExecStart=/bin/sh -c "/usr/bin/powerprofilesctl set power-saver && sleep 1 && /usr/bin/powerprofilesctl set balanced"

   [Install]
   WantedBy=suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
   EOF
   ```

2. Enable the service:
   ```bash
   sudo systemctl enable set-power-profile-on-wake.service
   ```

## Verification

After installation, you can verify the service is working by:

1. Checking if it's enabled:
   ```bash
   systemctl list-unit-files | grep set-power-profile-on-wake
   ```

2. Testing manually (optional):
   ```bash
   sudo systemctl start set-power-profile-on-wake.service
   powerprofilesctl status
   ```

3. Monitoring the service logs:
   ```bash
   journalctl -u set-power-profile-on-wake.service -f
   ```

## Usage

The service runs automatically on every system wake event. No manual intervention is required after installation.

To check current power profile:
```bash
powerprofilesctl status
```

## Configuration

If you prefer a different target power profile (instead of "balanced"), modify the `ExecStart` line in the systemd service file:

- `power-saver` - Maximum battery life, lower performance
- `balanced` - Balanced performance and power consumption (default)
- `performance` - Maximum performance, higher power consumption

## Uninstallation

To remove the service:

```bash
sudo systemctl stop set-power-profile-on-wake.service
sudo systemctl disable set-power-profile-on-wake.service
sudo rm /etc/systemd/system/set-power-profile-on-wake.service
```

Or if installed via RPM:
```bash
sudo dnf remove set-power-profile-on-wake
```

## Requirements

- Fedora Linux with systemd
- power-profiles-daemon package (usually pre-installed)
- bash shell

## Compatibility

Tested on:
- Fedora 34+
- Systems with Intel and AMD processors
- Both desktop and laptop configurations

## License

MIT License - see LICENSE file for details.

## Contributing

Pull requests are welcome! Please ensure compatibility with different Fedora versions and power management configurations.

## Author

sunnyyangyangyang - Initial work and maintenance.

---

*This project was created to solve a common but annoying issue affecting Fedora users. If you find it helpful, consider starring the repository to support further development.*
