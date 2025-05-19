import pythoncom
import winreg
import subprocess

def create_folder_shortcut(nombre, carpeta_destino, icono, escritorio=False):
    clsid = pythoncom.CreateGuid()
    clsid_str = str(clsid).upper()

    print(f"CLSID generado: {clsid_str}")
    # with open("clsid.txt", "a") as f:
    #     f.write(clsid_str + "\n")

    # Registrar CLSID en HKEY_CLASSES_ROOT y HKCU
    clsid_path = f"CLSID\\{clsid_str}"

    
    # HKEY_CLASSES_ROOT
    key_hkcr = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, clsid_path)
    crear_variables(key_hkcr, nombre, carpeta_destino, icono)
    
    # HKEY_CURRENT_USER\Software\Classes
    key_hkcu = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"SOFTWARE\\Classes\\{clsid_path}")
    crear_variables(key_hkcu, nombre, carpeta_destino, icono)

    # Vincular a "Este equipo"
    # if escritorio:
    try:
        namespace_path = f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Desktop\\NameSpace\\{clsid_str}"
        # namespace_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, namespace_path)
        namespace_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, namespace_path)
        winreg.SetValue(namespace_key, "", winreg.REG_SZ, nombre)
        winreg.CloseKey(namespace_key)
    except PermissionError:
        print("Error: Necesitas permisos de administrador para HKEY_LOCAL_MACHINE")

    if not escritorio:
        subprocess.run(
            f"reg add \"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel\" /v {clsid_str} /t REG_DWORD /d 1 /f",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"[✓] Creada en el panel de inicio: {clsid_str}")
        # key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel")
        # winreg.SetValueEx(key, clsid_str, 0, winreg.REG_SZ, nombre)
        # winreg.CloseKey(key)

    return clsid_str

def crear_variables(clsid_key, nombre, carpeta_destino, icono):
    # Configuración básica
    winreg.SetValue(clsid_key, "", winreg.REG_SZ, nombre)
    winreg.SetValueEx(clsid_key, "System.IsPinnedToNameSpaceTree", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(clsid_key, "SortOrderIndex", 0, winreg.REG_DWORD, 66)

    # Ícono
    icon_key = winreg.CreateKey(clsid_key, "DefaultIcon")
    winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, icono)
    winreg.CloseKey(icon_key)

    # InProcServer32
    inprocserver_key = winreg.CreateKey(clsid_key, "InProcServer32")
    winreg.SetValueEx(inprocserver_key, "", 0, winreg.REG_SZ, r"C:\Windows\System32\shell32.dll")
    winreg.CloseKey(inprocserver_key)

    # Instance y TargetFolder
    instance_key = winreg.CreateKey(clsid_key, "Instance")
    winreg.SetValueEx(instance_key, "CLSID", 0, winreg.REG_SZ, "{0E5AAE11-A475-4c5b-AB00-C66DE400274E}")
    
    init_property_key = winreg.CreateKey(instance_key, "InitPropertyBag")
    winreg.SetValueEx(init_property_key, "Attributes", 0, winreg.REG_DWORD, 16)
    winreg.SetValueEx(init_property_key, "TargetFolderPath", 0, winreg.REG_EXPAND_SZ, carpeta_destino)
    winreg.CloseKey(init_property_key)
    winreg.CloseKey(instance_key)

    # ShellFolder
    shell_folder_key = winreg.CreateKey(clsid_key, "ShellFolder")
    winreg.SetValueEx(shell_folder_key, "Attributes", 0, winreg.REG_DWORD, 4034920525)
    winreg.SetValueEx(shell_folder_key, "FolderValueFlags", 0, winreg.REG_DWORD, 40)
    winreg.CloseKey(shell_folder_key)


def eliminar_clsid(clsid: str):
    # Asegurar formato correcto del CLSID
    clsid = clsid.strip("{}").upper()
    clsid_formateado = "{" + clsid + "}"

    # Lista de todas las rutas del registro a eliminar
    rutas = [
        # HKEY_CLASSES_ROOT
        f"HKCR\\CLSID\\{clsid_formateado}",
        # HKEY_CURRENT_USER
        f"HKCU\\Software\\Classes\\CLSID\\{clsid_formateado}",
        # HKEY_LOCAL_MACHINE (MyComputer)
        f"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{clsid_formateado}",
        # HKEY_CURRENT_USER (MyComputer)
        f"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{clsid_formateado}",
        # Namespace en Desktop (opcional)
        f"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Desktop\\NameSpace\\{clsid_formateado}",
        f"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Desktop\\NameSpace\\{clsid_formateado}",
        # Namespace en el panel de inicio (opcional)
        f"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel\\{clsid_formateado}",
        f"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel\\{clsid_formateado}"
    ]

    # Eliminar cada ruta con reg delete
    for ruta in rutas:
        try:
            subprocess.run(
                f"reg delete {ruta} /f",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"[✓] Eliminada: {ruta}")
        except subprocess.CalledProcessError as e:
            if "el sistema no puede encontrar el archivo especificado" in e.stderr.decode().lower():
                print(f"[ ] No existe: {ruta}")
            else:
                print(f"[!] Error en {ruta}: {e.stderr.decode().strip()}")


if __name__ == "__main__":
    eliminar_clsid("{D8AFB4A4-F9ED-40B8-86CA-09632B9D6629}")