import gi
import subprocess
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk

CONFIG_PATH = os.path.expanduser('~/.config/rpm-install.config')

class MyApp(Adw.Application):

    def __init__(self, rpm_files):
        super().__init__(application_id='com.example.MyApp',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.rpm_files = rpm_files
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        win = MyAppWindow(application=app, rpm_files=self.rpm_files)
        win.present()

class MyAppWindow(Adw.ApplicationWindow):

    def __init__(self, rpm_files, **kwargs):
        super().__init__(**kwargs)
        self.rpm_files = rpm_files
        self.set_title("RPM Package Installer")
        self.set_default_size(400, 300)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_content(main_box)

        header_bar = Adw.HeaderBar()
        header_bar.set_title_widget(Gtk.Label(label="Install RPM Package"))
        main_box.append(header_bar)

        backend_info = self.get_backend_info()

        if len(rpm_files) == 1:
            package_info = self.get_package_info(rpm_files[0])
            info_label = Gtk.Label(label=package_info)
            info_label.set_margin_top(20)
            info_label.set_margin_bottom(10)
            info_label.set_halign(Gtk.Align.CENTER)
            info_label.set_valign(Gtk.Align.CENTER)
            info_label.set_wrap(True)
            info_label.set_max_width_chars(60)
            main_box.append(info_label)
        else:
            package_list = "\n".join([f"{i + 1}. {os.path.basename(rpm_file)}" for i, rpm_file in enumerate(rpm_files)])
            list_label = Gtk.Label(label=f"Packages to be installed:\n\n{package_list}")
            list_label.set_margin_top(20)
            list_label.set_margin_bottom(10)
            list_label.set_halign(Gtk.Align.CENTER)
            list_label.set_valign(Gtk.Align.CENTER)
            list_label.set_wrap(True)
            list_label.set_max_width_chars(60)
            main_box.append(list_label)

        backend_label = Gtk.Label(label=f"Using backend: {backend_info}")
        backend_label.set_margin_top(10)
        backend_label.set_margin_bottom(10)
        backend_label.set_halign(Gtk.Align.CENTER)
        backend_label.set_valign(Gtk.Align.CENTER)
        backend_label.set_wrap(True)
        backend_label.set_max_width_chars(60)
        main_box.append(backend_label)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.CENTER)
        main_box.append(button_box)

        yes_button = Gtk.Button(label="Yes")
        yes_button.connect("clicked", self.on_yes_button_clicked)
        button_box.append(yes_button)

        no_button = Gtk.Button(label="No")
        no_button.connect("clicked", self.on_no_button_clicked)
        button_box.append(no_button)

    def get_package_info(self, rpm_file):
        try:
            result = subprocess.run(["rpm", "-qpi", rpm_file], capture_output=True, text=True, check=True)
            package_info_full = result.stdout.strip()
            package_info_lines = package_info_full.split('\n')

            # Extract relevant information
            package_info = {}
            keys = ["Name", "Version", "Release", "Architecture", "Install Date", "Size", "Summary"]
            for line in package_info_lines:
                for key in keys:
                    if line.startswith(key):
                        package_info[key] = line.split(":", 1)[1].strip()

            # Format the extracted information
            formatted_info = "\n".join([f"{key}: {package_info[key]}" for key in keys if key in package_info])
        except subprocess.CalledProcessError as e:
            formatted_info = f"Error occurred: {e}"
        return formatted_info

    def get_backend_info(self):
        backend = self.read_config_backend()
        return backend

    def on_yes_button_clicked(self, button):
        backend = self.read_config_backend()
        try:
            if backend == 'dnf':
                subprocess.run(["pkexec", "dnf", "install", "-y"] + self.rpm_files, check=True)
            elif backend == 'zypper':
                subprocess.run(["pkexec", "zypper", "install", "-y"] + self.rpm_files, check=True)
            elif backend == 'rpm':
                subprocess.run(["pkexec", "rpm", "-i"] + self.rpm_files, check=True)
            print(f"Packages installed successfully using {backend}.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        self.close()

    def on_no_button_clicked(self, button):
        self.close()

    def read_config_backend(self):
        default_backend = 'dnf'
        if os.path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as config_file:
                backend = config_file.read().strip()
                if backend in ['dnf', 'zypper', 'rpm']:
                    return backend
        return default_backend

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 installer.py <path_to_rpm_file1> <path_to_rpm_file2> ...")
        sys.exit(1)

    rpm_files = sys.argv[1:]
    for rpm_file in rpm_files:
        if not os.path.isfile(rpm_file) or not rpm_file.endswith('.rpm'):
            print(f"Invalid RPM file: {rpm_file}")
            sys.exit(1)

    app = MyApp(rpm_files)
    app.run(None)
