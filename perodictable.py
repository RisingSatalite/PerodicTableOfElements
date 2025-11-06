from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle, Line
import csv

# Use virtual environments to build
# pyinstaller --noconsole --onefile --ico=icon.ico perodictable.py

global data_list# why does global stop an error?
settings = []

def return_dictionary_for_element(symbol):
    try:
        for i in data_list:
            if i['Symbol'] == str(symbol):
                #print("Located")
                #print(i)
                return i
        #print("Not found")
    except:
        #print("Data not read")
        pass

def return_dictionary_for_data(symbol, from_where):
    for i in from_where:
        if i['Symbol'] == str(symbol):
            #print(i)
            return i
    #print("Not found")

def return_dictionary_for_settings(type, from_where):
    #print("Ran")
    for i in from_where:
        if i['Group'] == str(type):
            #print(i)
            return i
    #print("Not found")

def get_contrasting_text_color(r, g, b):
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return (1, 1, 1, 1) if brightness < 0.6 else (0, 0, 0, 1)

# Custom button class for periodic table elements
class PeriodicButton(ButtonBehavior, BoxLayout):
    def __init__(self, number, weight, symbol, name, data, **kwargs):
        super(PeriodicButton, self).__init__(orientation='vertical', **kwargs)

        # The elements data as dictionary
        element_data = data

        # Set colours for element
        self.red = 0.3
        self.green = 0.3
        self.blue = 0.3
        self.bright = 1
        try:
            #print(element_data["Type"])
            where = return_dictionary_for_settings(element_data["Type"], settings)
            #print(where)
            self.red = float(where["Red"])
            self.green = float(where["Green"])
            self.blue = float(where["Blue"])
            self.bright = float(where["Brightness"])
        except ValueError as ve:
            #print(f"Caught an error: {ve}")
            #print("Error getting the element colours")
            #print(element_data["Type"])
            pass

        # Create labels with different font sizes
        number_label = Label(text=f" {number}", font_size='15sp', halign='left', valign='top', size_hint=(0.7, 1), color=get_contrasting_text_color(self.red, self.blue, self.green))
        number_label.bind(size=number_label.setter('text_size'))

        weight_label = Label(text=f"{weight} ", font_size='15sp', halign='right', valign='top', size_hint=(1, 1), color=get_contrasting_text_color(self.red, self.blue, self.green))
        weight_label.bind(size=weight_label.setter('text_size'))
        
        symbol_label = Label(text=symbol, font_size='22sp', valign='middle', size_hint=(1, 1), color=get_contrasting_text_color(self.red, self.blue, self.green))
        name_label = Label(text=name, font_size='15sp', valign='bottom', size_hint=(1, 1), color=get_contrasting_text_color(self.red, self.blue, self.green))
        
        # Add labels to the button
        # Create a layout for weight and number
        box = BoxLayout(size_hint=(1, 1))
        box.add_widget(number_label)
        box.add_widget(weight_label) 
        # Add widgets to self
        self.add_widget(box)
        self.add_widget(symbol_label)
        self.add_widget(name_label)
    
    def on_size(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)  # set the border color to white
            Line(width=2, rectangle=(self.x, self.y, *value))
            Color(self.red, self.green, self.blue, self.bright)  # set the background color to green
            Rectangle(size=value, pos=self.pos)

    def on_pos(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)  # set the border color to white
            Line(width=2, rectangle=(*value, self.width, self.height))
            Color(self.red, self.green, self.blue, self.bright)  # set the background color to green
            Rectangle(size=self.size, pos=value)

class MyApp(App):
    def build(self):
        def create_button(text, where):
            data = return_dictionary_for_data(text, data_list)
            try:
                number = data['AtomicNumber']
            except:
                number = "Error"
            try:
                weight = data['AtomicMass']
            except:
                weight = "Error"
            try:
                symbol = data['Symbol']
            except:
                symbol = "Error"
            try:
                name = data['Element']
            except:
                name = "Error"
            button = PeriodicButton(number, weight, symbol, name, data)
            button.bind(on_press=lambda instance: self.show_popup(instance, data))
            where.add_widget(button)

        # Read data
        def read_csv_to_list(file_path):
            data = []
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(row)
            return data

        file_path = 'Elements/perodicdata.csv'
        data_list = read_csv_to_list(file_path)
        file_path2 = 'Elements/settings.csv'
        global settings
        settings = read_csv_to_list(file_path2)
        #print("Here")
        #print(settings)
        #for i in settings:
            #print(i)
        #for i in data_list:
            #print(i)
        #return_dictionary_for_element(1)
        #for i in settings:
            #print(i['Group'])
            #print(i)

        # Create main BoxLayout
        layout = BoxLayout(orientation='vertical')

        # Layout for the first row
        layout2 = BoxLayout(orientation='horizontal')
        create_button("H", layout2)
        for i in range(16):
            layout2.add_widget(Label()) 
        create_button("He", layout2)
        layout.add_widget(layout2)

        # Layout for the second row
        layout3 = BoxLayout(orientation='horizontal')
        create_button("Li", layout3)
        create_button("Be", layout3)
        for i in range(10):
            layout3.add_widget(Label())
        create_button("B", layout3)
        create_button("C", layout3)
        create_button("N", layout3)
        create_button("O", layout3)
        create_button("F", layout3)
        create_button("Ne", layout3)
        layout.add_widget(layout3)

        # Layout for the third row
        layout4 = BoxLayout(orientation='horizontal')
        create_button("Na", layout4)
        create_button("Mg", layout4)
        for i in range(10):
            layout4.add_widget(Label())
        create_button("Al", layout4)
        create_button("Si", layout4)
        create_button("P", layout4)
        create_button("S", layout4)
        create_button("Cl", layout4)
        create_button("Ar", layout4)
        layout.add_widget(layout4)

        layout5 = BoxLayout(orientation='horizontal')
        create_button("K", layout5)
        create_button("Ca", layout5)
        create_button("Sc", layout5)
        create_button("Ti", layout5)
        create_button("V", layout5)
        create_button("Cr", layout5)
        create_button("Mn", layout5)
        create_button("Fe", layout5)
        create_button("Co", layout5)
        create_button("Ni", layout5)
        create_button("Cu", layout5)
        create_button("Zn", layout5)
        create_button("Ga", layout5)
        create_button("Ge", layout5)
        create_button("As", layout5)
        create_button("Se", layout5)
        create_button("Br", layout5)
        create_button("Kr", layout5)
        layout.add_widget(layout5)

        layout6 = BoxLayout(orientation='horizontal')
        elementList5 = ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"]
        for i in elementList5:
            create_button(i, layout6)
        layout.add_widget(layout6)

        layout7 = BoxLayout(orientation='horizontal')
        elementList6 = ['Cs','Ba','La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn']
        for i in elementList6:
            create_button(i, layout7)
        layout.add_widget(layout7)

        layout8 = BoxLayout(orientation='horizontal')
        elementList7 = ['Fr','Ra','Ac','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og']
        for i in elementList7:
            create_button(i, layout8)
        layout.add_widget(layout8)

        layout.add_widget(Label(size_hint_y=0.5))

        layout9 = BoxLayout(orientation='horizontal')
        for i in range(3):
            layout9.add_widget(Label())
        elementList8 = ['Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu']
        for i in elementList8:
            create_button(i, layout9)
        layout9.add_widget(Label())
        layout.add_widget(layout9)

        layout10 = BoxLayout(orientation='horizontal')
        for i in range(3):
            layout10.add_widget(Label())
        elementList9 = ['Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr']
        for i in elementList9:
            create_button(i, layout10)
        layout10.add_widget(Label())
        layout.add_widget(layout10)

        return layout

    def show_popup(self, instance, type):
        # Create content for the popup
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Element information"))

        for x in type:
            main = BoxLayout(orientation='horizontal')
            
            # Right-aligned label
            right_label = Label(text=f"{x} ", halign='right', valign='middle')
            right_label.bind(size=right_label.setter('text_size'))
            main.add_widget(right_label)
            
            # Left-aligned label
            left_label = Label(text=f" {type[x]}", halign='left', valign='middle')
            left_label.bind(size=left_label.setter('text_size'))
            main.add_widget(left_label)
            
            content.add_widget(main)

        close_button = Button(text="Close")
        content.add_widget(close_button)
        
        # Create the popup
        popup = Popup(title=f'{type["Element"]}',
                      content=content,
                      size_hint=(0.95, 0.95),
                      auto_dismiss=False)
        
        # Bind the close button to dismiss the popup
        close_button.bind(on_press=popup.dismiss)
        
        # Open the popup
        popup.open()

if __name__ == "__main__":
    MyApp().run()
#try not 1 file