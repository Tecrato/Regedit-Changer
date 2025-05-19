import os
import re
import json
import pygame as pag
import Utilidades as uti
import Utilidades_pygame as uti_pag
from typing import override, Callable
from pathlib import Path

from Utilidades_pygame.base_app_class import Base_class

from sound import Set_sounds
from funcs.folder_shortcut import create_folder_shortcut

class RegeditChanger(Base_class):
    @override
    def otras_variables(self) -> None:
        self.moving_tooltip = False
        self.configs = {}
        self.sonidos = Set_sounds()

        self.lista_opciones_registro: list[dict[str, str|Callable]] = [
            {"option_text": "Main", "func":lambda: self.goto('main'), "tooltip":"El inicio de la aplicacion"},
            {"option_text":"Barra lateral", "func":lambda: self.goto('op1'), "tooltip":"Crear Acceso directo a la carpeta deseada en la barra lateral del explorador de windows.\n\nAdemas de un acceso directo imborrable en escritorio(Opcional)"},
            {"option_text":"Menu contextual", "func":lambda: self.goto('op2'), "tooltip":"Crear opciones nuevas en el menu contextual al hacer click derecho en el explorador de archivos de windows"},
            {"option_text":"Aplicacion de inicio", "func":lambda: self.goto('op3'), "tooltip":"Ejecuta el programa o archivo seleccionado al iniciar windows"},
        ]


        # Variables para la opcion 1
        self.icono_carpeta: str|Path = r"C:\Users\Edouard\Documents\curso de programacion\Python\API's\Acelerador-de-descargas\Assets\img\descargas.ico"
        self.acceso_directo_imborrable = False
        self.carpeta_para_acceso_directo = ""
        
    @override
    def load_resources(self):
        try:
            configs = json.load(open(self.config.save_dir.joinpath('./configs.json')))
        except FileNotFoundError:
            with open(self.config.save_dir.joinpath('./configs.json'), 'w') as f:
                json.dump({}, f)
            uti.debug_print(f"No se pudo cargar las configuraciones", priority=2)
            configs = {}
        except Exception as err:
            uti.debug_print(f"No se pudo cargar las configuraciones", priority=2)
            configs = {}

        self.idioma = configs.get('idioma','español')


    def save_conf_manualy(self, key, value):
        try:
            config = json.load(open(self.config.save_dir.joinpath('./configs.json')))
            config[key] = value
            json.dump(config, open(self.config.save_dir.joinpath('./configs.json'), 'w'))
        except Exception as err:
            uti.debug_print(err, priority=2)
            self.Mini_GUI_manager.clear_group('config')
            self.Mini_GUI_manager.add(
                uti_pag.mini_GUI.more_objs.aviso1((50000, 50000), 'bottomright', f'error actualizando {key}',self.config.fonts["mononoki"]),
                group='config'
            )

    @override
    def post_init(self):
        self.acceso_directo_imborrable = True
        self.toggle_acceso_directo_imborrable()


    @override
    def generate_objs(self) -> None:
        # Titulo
        self.text_app_title = uti_pag.Text("Regedit Changer", 24, self.config.fonts["mononoki"], (self.config.resolution[0]//2, 20))


        # Main
        self.text_main_title = uti_pag.Text("Main", 16, self.config.fonts["mononoki"], (self.config.resolution[0]//2,80))
        
        self.text_main_description = uti_pag.Text(
            "Bienvenido a Regedit Changer, un programa para cambiar valores en el registro de windows.\n\nLa mayoria de cambios son reversibles o inofensivos, de cualquier forma se recomienda proceder con precaucion",
            16, self.config.fonts["mononoki"], (self.config.resolution[0]//4, 100), 'topleft', 
            max_width=self.config.resolution[0]//2, text_align='left'
        )

        # Opcion 1 (Barra lateral)
        self.text_op1_title = uti_pag.Text(self.lista_opciones_registro[1]["option_text"], 16, self.config.fonts["mononoki"], (self.config.resolution[0]//2,80))

        self.input_op1_nombre_carpeta = uti_pag.Input((self.config.resolution[0]//4 +10, 100), 12, self.config.fonts["mononoki"], "Nombre Del Acceso Directo", max_letter=50, width=300, height=30, padding=(10,10))

        self.btn_op1_select_icon = uti_pag.Button("Seleccionar Icono", 12, self.config.fonts["mononoki"], (self.config.resolution[0]//4 +10,self.input_op1_nombre_carpeta.rect.bottom+30), padding=(10,5), dire='left', func=self.seleccionar_icono)
        self.img_op1_icono_carpeta = uti_pag.Image(self.icono_carpeta, (self.btn_op1_select_icon.right+10, self.btn_op1_select_icon.centery), dire='left', size=(24,24))

        self.btn_op1_seleccionar_carpeta = uti_pag.Button("Seleccionar carpeta", 12, self.config.fonts["mononoki"], (self.config.resolution[0]//4 +10,self.btn_op1_select_icon.bottom+30), padding=(10,5), dire='left', func=self.seleccionar_carpeta)
        self.text_op1_carpeta_seleccionada = uti_pag.Text("C://...", 12, self.config.fonts["mononoki"], (self.config.resolution[0]//4 +10,self.btn_op1_seleccionar_carpeta.rect.bottom+10), padding=(10,5), dire='left', max_width=300)

        self.btn_op1_acceco_directo_imborrable = uti_pag.Button("Acceso directo imborrable?", 12, self.config.fonts["mononoki"], (self.config.resolution[0]//4 +10,self.text_op1_carpeta_seleccionada.rect.bottom +30), padding=(10,5), dire='left', func=self.toggle_acceso_directo_imborrable)

        self.btn_op1_crear = uti_pag.Button("Crear", 24, self.config.fonts["mononoki"], (300,350), padding=30, border_radius=-1, func=self.crear)


        self.img_op1_ejemplo = uti_pag.Image("./Data/images/barra_ejemplo_edit.png", (self.config.resolution[0] - 30, 60), dire='topright')

        #Opcion 2 (Menu contextual)
        self.text_op2_title = uti_pag.Text(self.lista_opciones_registro[2]["option_text"], 16, self.config.fonts["mononoki"], (self.config.resolution[0]//2,80))

        self.img_op2_ejemplo = uti_pag.Image("./Data/images/menu_ejemplo_edit.png", (self.config.resolution[0] - 30, 60), dire='topright', size=(320//1.5,562//1.5))


        #Opcion 3 (Aplicacion de inicio)
        self.text_op3_title = uti_pag.Text(self.lista_opciones_registro[3]["option_text"], 16, self.config.fonts["mononoki"], (self.config.resolution[0]//2,80))
    
        # Tooltip
        self.text_tooltip = uti_pag.Text(
            "Tooltip", 12, self.config.fonts["mononoki"], (self.config.resolution[0]//4,-500), border_radius=30, max_width=240,
            border_width=2, border_color = 'black', padding=20, color_rect=(20,20,20,20), with_rect=True,
            max_lines=-0
            )
        self.text_tooltip.smothmove(.8,.8,.9)

        # Barra Lateral
        self.bloque_main_opciones = uti_pag.Bloque(
            (0,50),
            (self.config.resolution[0]//4, self.config.resolution[1]-50),
            dire='topleft',
            border_color=(255,255,255,255),
        )
        self.bloque_main_opciones.add(
            uti_pag.Text(
                "Opciones", 16, self.config.fonts["mononoki"], (self.config.resolution[0]//8,50),
                min_width=self.bloque_main_opciones.width-1,
            ),
            f'(self.rect.w/2,15)',
        )
        for i,x in enumerate(self.lista_opciones_registro):
            if i <= 0:
                top = 20*2
            else:
                top = self.bloque_main_opciones.list_objs[-2]["GUI"].rect.bottom
            self.bloque_main_opciones.add(
                uti_pag.Button(
                    text=x["option_text"],
                    size=12, 
                    font=self.config.fonts["mononoki"], 
                    pos=(0,top), 
                    padding=5, 
                    dire='topleft', 
                    color='black', 
                    border_width=-1,
                    border_radius=0, 
                    min_width=self.bloque_main_opciones.width,
                    max_width=self.bloque_main_opciones.width,
                    min_height=30,
                    with_rect=True, 
                    wrap=True,
                    color_rect_active='lightgreen',
                    cursor= pag.SYSTEM_CURSOR_ARROW,
                    func= x["func"],
                    # func_to_hover=lambda top=top,txt=x["tooltip"]:self.spawn_tooltip(txt, (self.config.resolution[0]//4 +1,top+50), 'left'),
                    # func_out_hover=lambda txt=x["tooltip"]: self.despawn_tooltip(txt),
                )
            , f'(0,{top})', clicking=True)
            self.bloque_main_opciones.add(
                uti_pag.Button(
                    text='?',
                    size=12,
                    font=self.config.fonts["mononoki"],
                    min_width=15,
                    min_height=15,
                    padding=2,
                    border_radius=-1,
                    dire='center',
                    text_align='center',
                    border_width=-1,
                    color_rect=(130,130,130),
                    color_rect_active=(200,200,200),
                    # cursor= pag.SYSTEM_CURSOR_HAND,
                    func_to_hover=lambda top=top,txt=x["tooltip"]:self.spawn_tooltip(txt, (self.config.resolution[0]//4 +1,top+50), 'left'),
                    func_out_hover=lambda txt=x["tooltip"]: self.despawn_tooltip(txt),
                ),
                f'({self.bloque_main_opciones.width-15},{top+15})',clicking=True
            )



        # GUI
        self.gui_informacion = uti_pag.GUI.Info(self.ventana_rect.center, 'Regedit Changer', '', (550,275),font=None)
        self.gui_desicion = uti_pag.GUI.Desicion(self.ventana_rect.center, 'Regedit Changer', '', (550,275),font=None)
        

        #Listas de objetos
        self.lists_screens['main']["draw"] = [
            self.text_main_title,self.text_main_description
        ]
        self.lists_screens['main']["update"] = self.lists_screens['main']["draw"]
        self.lists_screens['main']["click"] = [
        ]

        # Opcion 1 (Barra lateral)
        self.registrar_pantalla('op1')
        self.lists_screens['op1']["draw"] = [
            self.text_op1_title, self.btn_op1_seleccionar_carpeta, self.text_op1_carpeta_seleccionada,
            self.input_op1_nombre_carpeta, self.btn_op1_select_icon, self.img_op1_icono_carpeta,
            self.btn_op1_crear,self.img_op1_ejemplo,
            self.btn_op1_acceco_directo_imborrable,
        ]
        self.lists_screens['op1']["update"] = self.lists_screens['main']["draw"]
        self.lists_screens['op1']["click"] = [
            self.btn_op1_seleccionar_carpeta,self.input_op1_nombre_carpeta, self.btn_op1_select_icon,
            self.btn_op1_crear,self.btn_op1_acceco_directo_imborrable
        ]
        self.lists_screens['op1']["inputs"] = [
            self.input_op1_nombre_carpeta
        ]
        # Opcion 2 (Menu contextual)
        self.registrar_pantalla('op2')
        self.lists_screens['op2']["draw"] = [
            self.text_op2_title,self.img_op2_ejemplo
        ]
        self.lists_screens['op2']["update"] = self.lists_screens['main']["draw"]
        self.lists_screens['op2']["click"] = [
        ]
        # Opcion 3 (Aplicacion de inicio)
        self.registrar_pantalla('op3')
        self.lists_screens['op3']["draw"] = [
            self.text_op3_title,
        ]
        self.lists_screens['op3']["update"] = self.lists_screens['main']["draw"]
        self.lists_screens['op3']["click"] = [
        ]

        self.overlay = [
            self.text_app_title, self.bloque_main_opciones,
            self.text_tooltip,

            self.gui_informacion, self.gui_desicion
        ]

    @override
    def otro_evento(self, actual_screen, evento):
        if evento.type == pag.KEYDOWN and evento.key == pag.K_ESCAPE:
            self.exit()
        elif evento.type == pag.MOUSEMOTION:
            if self.moving_tooltip:
                self.moving_tooltip = False

    def spawn_tooltip(self, tooltip: str, pos: tuple[int,int], dire: str = 'left') -> None:
        self.text_tooltip.text = tooltip
        self.text_tooltip.pos = pos
        self.text_tooltip.dire = dire
        self.moving_tooltip = True

    def despawn_tooltip(self, tooltip: str, **kwargs) -> None:
        if self.moving_tooltip:
            return
        self.text_tooltip.pos = (self.config.resolution[0]//4,-100)


    def open_GUI_dialog(self, texto, title='Acelerador de descargas', func=None,tipo=1, options=None):
        p = {
            1:self.gui_desicion,
            2:self.gui_informacion
        }[tipo]
        
        if options:
            p.options = options
        p.title.text = title
        p.body.text = texto
        p.func = func
        p.active = True
        p.redraw += 1

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funciones del programa
    def seleccionar_carpeta(self):
        carpeta = uti.win32_tools.askFolder(self.hwnd)
        if not carpeta:
            return
        if not Path(carpeta).exists() and not Path(carpeta).is_dir():
            self.open_GUI_dialog(f"La carpeta seleccionada no existe o no es una carpeta válida", 'Error', tipo=2)
            return
        print(carpeta)
        self.text_op1_carpeta_seleccionada.text = carpeta
        self.carpeta_para_acceso_directo = carpeta

    def seleccionar_icono(self):
        icono = uti.win32_tools.askFile("Seleccione un icono", filter="Iconos(*.ico)|*.ico")
        if not icono:
            return
        self.icono_carpeta = icono
        self.img_op1_icono_carpeta.path = icono

    def crear(self):
        if not self.input_op1_nombre_carpeta.get_text() or not re.match(r'^[a-zA-Z0-9\s\-]+$', self.input_op1_nombre_carpeta.get_text()):
            text = f"El nombre del acceso direct debe contener solo caracteres alfanumericos, espacios y guiones '-'\n"\
            "\n"\
            "No puede contener caracteres especiales como:\n"\
            "< > ? * : | \" / \\\n"\
            "\n" \
            "O como una carpeta ya existente"
            self.open_GUI_dialog(text, 'Error', tipo=2)
            return
        if not self.self.carpeta_para_acceso_directo:
            return
        if not self.icono_carpeta:
            return
        cslid = create_folder_shortcut(self.input_op1_nombre_carpeta.get_text(), self.text_op1_carpeta_seleccionada.text, self.icono_carpeta)
        print(cslid)
        with open(self.config.save_dir.joinpath('./clsid_list.txt'), 'a') as f:
            f.write(f"{self.input_op1_nombre_carpeta.get_text()}|{cslid}\n")

    def toggle_acceso_directo_imborrable(self):
        self.acceso_directo_imborrable = not self.acceso_directo_imborrable
        if self.acceso_directo_imborrable:
            self.btn_op1_acceco_directo_imborrable.text = "Acceso directo imborrable: SI"
            self.btn_op1_acceco_directo_imborrable.change_color_rect_ad('green','lightgreen')
        else:
            self.btn_op1_acceco_directo_imborrable.text = "Acceso directo imborrable: NO"
            self.btn_op1_acceco_directo_imborrable.change_color_rect_ad('red','mediumvioletred')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config = uti_pag.Config(
        title="Regedit Changer",
        author="Edouard Sandoval",
        my_company="Edouard Sandoval",
        copyright="2025 Edouard Sandoval",
        version="1.0",
        description="Un programa para cambiar valores en el registro de windows",
        fonts={"mononoki":r".\Data\fonts\mononoki Bold Nerd Font Complete Mono.ttf", "simbolos":r".\Data\fonts\Symbols.ttf"},
        icon="./Data/images/Registry_pre.png"
    )
    RegeditChanger(config=config)