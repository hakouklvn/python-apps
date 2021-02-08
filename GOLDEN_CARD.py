import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


class GOLDEN_CARD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Golden Card')
        self.root.resizable(False, False)
        self.create_widgets()
        style = ttk.Style()
        style.configure('TLabel', background='#e4e1dd')
        self.root.configure(background='#e4e1dd')

    def code(self):
        self.verify_code()

        """Test whether your golden card is true or not"""
        card_number = self.text.get()
        if len(card_number) != 16:
            value = 'Error:(golden card shoud have 16 number.)'
            self.scr.insert(tk.INSERT, value)
        else:
            list_num = []
            res_addition = 0
            # index takes every num from golden card
            for index in range(len(card_number)):
                if index % 2 != 0:                               # if index is even: then append it to list_num as it is
                    list_num.append(int(card_number[index]))
                elif index % 2 == 0:                             # if index is odd: then duplicate that number
                    duplicate_num = str(int(card_number[index]) * 2)
                    # if  len(duplication) is < 2 so (keep, append) it
                    if len(duplicate_num) < 2:
                        result = int(duplicate_num[0])
                        list_num.append(result)
                    else:                                        # if not calculate the two number and append it
                        result = int(
                            duplicate_num[0]) + int(duplicate_num[1])
                        list_num.append(result)
                # i takes every num from new list except the last one, then calculate them together
            for i in list_num[:(len(card_number) - 1)]:
                res_addition += i

                # if 10 - (result_of_calucation % 10) = last num of list so true
            c = res_addition % 10
            d = 10 - c

            if d == int(list_num[-1]):
                self.scr.insert(
                    tk.INSERT, '*********Card verified*********' + '\n')

            else:
                self.scr.insert(
                    tk.INSERT, '*********False card*********' + '\n')

    def _delete(self):
        self.entry_text.delete(0, tk.END)
        self.scr.delete(1.0, tk.END)

    def verify_code(self):
        self.scr = scrolledtext.ScrolledText(
            self.root, width=33, height=9, font=('Arial', 14))
        self.scr.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    def create_widgets(self):
        # first label
        ttk.Label(self.root, text='Card: ', font=('Arial', 14)).grid(
            row=0, column=0, padx=10, pady=10)
        self.cards = tk.StringVar()
        self.chosen_card = ttk.Combobox(
            self.root, width=32, textvariable=self.cards, state='readonly', font=('Arial', 14))
        self.chosen_card.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        self.chosen_card['value'] = ('master card', 'golden card')
        self.chosen_card.current(1)
        # second label
        ttk.Label(self.root, text='number: ', font=('Arial', 14)).grid(
            row=1, column=0, padx=10, pady=10)
        self.text = tk.StringVar()
        self.entry_text = ttk.Entry(
            self.root, textvariable=self.text, width=33, font=('Arial', 14))
        self.entry_text.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
        self.entry_text.focus()
        # first button
        verify = ttk.Button(self.root, text='Verify', command=self.code)
        verify.grid(row=2, column=2, padx=10, pady=10)
        # second button
        delete = ttk.Button(self.root, text='Delete', command=self._delete)
        delete.grid(row=2, column=1, padx=10, pady=10)

        # some configuration
        for child in self.root.winfo_children():
            child.grid_configure(sticky=tk.W)


def main():
    gold_card = GOLDEN_CARD()
    gold_card.root.mainloop()


if __name__ == "__main__":
    main()
