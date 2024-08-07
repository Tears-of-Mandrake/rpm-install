# rpm-install (temp name)

Simple GUI which allows you to graphically install .rpm packages

# Features

1. Application supporting single .rpm file installation and also multiple file installation.
* In single file, application print few standard information about package
* In multi file, application print only package names, version and all what comes from file name.

2. Application allow to use few backend:
* dnf (default one)
* zypper
* rpm

You can switch beetwen by editin config file located in /home/user-name/.config/rpm-install.config (if this file not exist, create it)

# Dependency
Require runtime dependency as: gtk4.0 lib64adwaita1_0 lib64adwaita-gir1 python-gobject3

# Usage

Add application as default action to run when .rpm file is double clicked

Alternatively for testing, run python shell and invoke applications with the package being installed as:

python rpm-installer.py  '/path-to-installed-package/your-package.rpm' 



# Screenshots

(from early 0.0.0.5 release)

single file installation

![Zrzut ekranu z 2024-08-07 20-41-41](https://github.com/user-attachments/assets/1e979205-411e-444f-995b-0b736338161b)

multiple file installation

![Zrzut ekranu z 2024-08-07 20-41-58](https://github.com/user-attachments/assets/0c648a38-8d57-4d4c-a7b8-a961d831d195)

theme/style support (tested gnome 46 only)

White

![Zrzut ekranu z 2024-08-07 20-45-27](https://github.com/user-attachments/assets/a1adc20c-f797-4362-9ba2-7ad1a3b88187)
