from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from collections import defaultdict
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout

class HomeScreen(Screen):
    pass

class ChooseDate(Screen):
    pass

class HavePlane(Screen):
    pass

class EnterText(Screen):
    pass

class SpiltMoney(Screen):
    pass

class TextBill(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class MainApp(MDApp):
    choosed_date = defaultdict(int)
    editing_card = None
    people_bill = defaultdict(int)
    
    def build(self):
        Window.size = (360, 640)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file('main.kv')

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def show_edit_dialog(self, label_id, title, kv_id):
        if kv_id == "choose_date":
            label = self.root.ids.choose_date.ids[label_id]
        else:
            label = self.root.ids.spilt_money.ids[label_id]

        self.dialog = MDDialog(
            title = title,
            type="custom",
            content_cls=MDTextField(
                hint_text="Enter new text",
                text=""
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.update_label_text(label)
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
    
    def update_label_text(self, label):
        new_text = self.dialog.content_cls.text
        label.text = new_text
        self.dialog.dismiss()

    def on_save(self, instance, value, date_range):
        date_str = str(value)
        self.choosed_date[date_str] += 1
        self.rank()
    
    def rank(self):
        sorted_dates = sorted(self.choosed_date.items(), key=lambda item: item[1], reverse=True)
        top_four = sorted_dates[:4]
        rank_text = "\n\n".join([f"{i + 1}. {date}: {count}" for i, (date, count) in enumerate(top_four)])
        self.root.ids.screen_manager.get_screen('choose_date').ids.rank_label.text = rank_text

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def clean_date_picker(self, label_id):
        self.choosed_date.clear()
        self.root.ids.screen_manager.get_screen('choose_date').ids.rank_label.text = ""
        label = self.root.ids.choose_date.ids[label_id]
        label.text = "Topic of Vote"

    def add_card(self):
        screen = self.root.ids.screen_manager.get_screen('enter_text')
        text = screen.ids.text_input.text 
        if text: 
            if self.editing_card:
                self.editing_card.children[1].text = text
                self.editing_card = None
            else:
                card = MDCard(size_hint=(1, None), height=dp(200), style="filled")
                card_label = MDLabel(text=text, theme_text_color="Secondary", halign='left', padding=(dp(10), dp(10)))
                card.add_widget(card_label)

                button_layout = RelativeLayout(size_hint=(0.2, 1))
                delete_button = MDIconButton(icon="delete", pos_hint={"center_x": 0.7, "center_y": 0.1})
                edit_button = MDIconButton(icon="pencil", pos_hint={"center_x": 0.7, "center_y": 0.3})
                delete_button.bind(on_release=lambda x: self.delete_card(card, "have_plane"))
                edit_button.bind(on_release=lambda x: self.edit_card(card, "enter_text"))
                button_layout.add_widget(delete_button)
                button_layout.add_widget(edit_button)
                card.add_widget(button_layout)

                self.root.ids.screen_manager.get_screen('have_plane').ids.content_grid.add_widget(card)
            screen.ids.text_input.text = ""
        self.change_screen('have_plane')

    def edit_card(self, card, card_id):
        screen = self.root.ids.screen_manager.get_screen(card_id)
        self.editing_card = card 
        if card_id == "enter_text":      
            text = card.children[1].text
            screen.ids.text_input.text = text
        else:
            text_money = card.children[1].children[2].text.replace("Money:","")
            screen.ids.money_text.text = text_money
            text_people = card.children[1].children[1].text.replace("People:","")
            screen.ids.people_text.text = text_people
            text_details = card.children[1].children[0].text.replace("Details:","")
            screen.ids.details_text.text = text_details

        self.change_screen(card_id)

    def cancel_edit(self, screen_id):
        self.editing_card = None
        self.change_screen(screen_id)

    def delete_card(self, card, screen_id):
        if screen_id == "have_plane":
            self.root.ids.screen_manager.get_screen(screen_id).ids.content_grid.remove_widget(card)
        else:
            self.root.ids.screen_manager.get_screen(screen_id).ids.bill_grid.remove_widget(card)
            text_money = card.children[1].children[2].text.replace("Money:","") 
            text_people = card.children[1].children[1].text.replace("People:","").split()
            for people in text_people:
                self.people_bill[people] -= float(text_money) / len(text_people)

    def delete_all_card(self, screen_id):
        if screen_id == "have_plane":
            content_grid = self.root.ids.screen_manager.get_screen(screen_id).ids.content_grid
            content_grid.clear_widgets()
        else:
            content_grid = self.root.ids.screen_manager.get_screen(screen_id).ids.bill_grid
            content_grid.clear_widgets()
            self.close_dialog(None)
            self.people_bill.clear()

    def add_bill(self):
        screen = self.root.ids.screen_manager.get_screen('text_bill')
        text_money = screen.ids.money_text.text 
        text_people = screen.ids.people_text.text 
        text_details = screen.ids.details_text.text

        if text_money and text_people:
            if self.editing_card:
                text_people_original = self.editing_card.children[1].children[1].text.replace("People:","").split()
                set_people_original = set(text_people_original)
                set_people = set(text_people.split())
                edited_pepole = set_people_original - set_people
                text_money_original = self.editing_card.children[1].children[2].text.replace("Money:","")
                for people in text_people_original:
                    self.people_bill[people] -= float(text_money_original) / len(text_people_original)
                for people in edited_pepole:
                    del self.people_bill[people]

                for people in set_people:
                    self.people_bill[people] += float(text_money) / len(set_people)

                self.editing_card.children[1].children[2].text = "Money:" + text_money
                self.editing_card.children[1].children[1].text = "People:" + text_people
                self.editing_card.children[1].children[0].text = "Details:" + text_details
                self.editing_card = None
            else:
                card = MDCard(size_hint=(1, None), height=dp(200), style="filled")
                label_layout = RelativeLayout(size_hint=(0.6, 1))
                card_label_money = MDLabel(text="Money:" + text_money, theme_text_color="Secondary", pos_hint={"center_x": 0.6, "center_y": 0.8} )
                card_label_people = MDLabel(text="People:" + text_people, theme_text_color="Secondary", pos_hint={"center_x": 0.6, "center_y": 0.6})
                card_label_details = MDLabel(text="Details:" + text_details, theme_text_color="Secondary", pos_hint={"center_x": 0.6, "center_y": 0.4})

                people_list = text_people.split()
                for people in people_list:
                    self.people_bill[people] += float(text_money) / len(people_list)

                label_layout.add_widget(card_label_money)
                label_layout.add_widget(card_label_people)
                label_layout.add_widget(card_label_details)
                card.add_widget(label_layout)

                button_layout = RelativeLayout(size_hint=(0.2, 1))
                delete_button = MDIconButton(icon="delete", pos_hint={"center_x": 0.7, "center_y": 0.1})
                edit_button = MDIconButton(icon="pencil", pos_hint={"center_x": 0.7, "center_y": 0.3})
                delete_button.bind(on_release=lambda x: self.delete_card(card, "spilt_money"))
                edit_button.bind(on_release=lambda x: self.edit_card(card, "text_bill"))
                button_layout.add_widget(delete_button)
                button_layout.add_widget(edit_button)
                card.add_widget(button_layout)

                self.root.ids.screen_manager.get_screen('spilt_money').ids.bill_grid.add_widget(card)
            screen.ids.money_text.text = ""
            screen.ids.people_text.text = ""
            screen.ids.details_text.text = ""
        self.change_screen('spilt_money')
    
    def show_splited_bill(self):
        text = ""
        for key, value in self.people_bill.items():
            text += f"{key} needs to pay {value}\n"
        self.dialog = MDDialog(
            title = "Splited Bill",
            text = text,
            type="custom",
            buttons=[
                MDFlatButton(
                    text="Delete All",
                    on_release=lambda x: self.delete_all_card("spilt_money")
                    
                ),
                MDFlatButton(
                    text="Keep",
                    on_release=self.close_dialog
                ),
            ]
        )
        self.dialog.open()
 
if __name__ == '__main__':
    MainApp().run()
