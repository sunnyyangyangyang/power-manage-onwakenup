Name:           set-power-profile-on-wake
Version:        1.0
Release:        0.8%{?dist}
Summary:        Set power profile to balanced after system wake

License:        MIT
URL:            https://example.com

BuildArch:      noarch
Requires:       systemd
Requires:       power-profiles-daemon

%description
A systemd service that sets the power profile to balanced after the system
wakes from suspend, hibernate, or hybrid-sleep.

%prep
# No prep needed

%build
# Nothing to build

%install
mkdir -p %{buildroot}/usr/lib/systemd/system

cat > %{buildroot}/usr/lib/systemd/system/set-power-profile-on-wake.service << 'EOF'
[Unit]
Description=Set power profile to balanced after wake
After=suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c "/usr/bin/powerprofilesctl set power-saver && sleep 1 && /usr/bin/powerprofilesctl set balanced"

[Install]
WantedBy=suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
EOF

%post
if [ $1 -eq 1 ]; then
    # 首次安装
    systemctl daemon-reload >/dev/null 2>&1 || :
    systemctl enable set-power-profile-on-wake.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
    # 完全卸载
    systemctl disable set-power-profile-on-wake.service >/dev/null 2>&1 || :
    systemctl stop set-power-profile-on-wake.service >/dev/null 2>&1 || :
fi

%postun
systemctl daemon-reload >/dev/null 2>&1 || :

%files
/usr/lib/systemd/system/set-power-profile-on-wake.service

%changelog
* Sun Oct 19 2025 Your Name <your.email@example.com> - 1.0-2
- Fixed scriptlet errors, now uses direct systemctl commands

* Sun Oct 19 2025 Your Name <your.email@example.com> - 1.0-1
- Initial package