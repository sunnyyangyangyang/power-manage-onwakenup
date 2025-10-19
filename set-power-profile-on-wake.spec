Name:           set-power-profile-on-wake
Version:        1.0
Release:        1%{?dist}
Summary:        Set power profile to balanced after system wake

License:        MIT
URL:            https://example.com

BuildArch:      noarch
Requires:       systemd
Requires:       systemd-rpm-macros
Requires:       power-profiles-daemon

%description
A systemd service that sets the power profile to balanced after the system
wakes from suspend, hibernate, or hybrid-sleep.

%prep
# No prep needed

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_unitdir}

cat > %{buildroot}%{_unitdir}/set-power-profile-on-wake.service << 'EOF'
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
%systemd_post set-power-profile-on-wake.service

%preun
%systemd_preun set-power-profile-on-wake.service

%postun
%systemd_postun_with_restart set-power-profile-on-wake.service

%files
%{_unitdir}/set-power-profile-on-wake.service

%changelog
* Sun Oct 19 2025 Your Name <your.email@example.com> - 1.0-1
- Initial package
