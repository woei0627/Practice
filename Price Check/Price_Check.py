from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import pandas as pd

class Price_Check:

    def __init__(self, master):

        master.title('Price Check')
        master.resizable(False, False)
        master.configure(background='#e1d8b9')

        self.item_index = {"orb of alternation": 1, 'orb of fusing': 2, 'orb of alchemy': 3, 'chaos orb':4, 'gemcutter':5, 'exalted orb':6}

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        self.logo = PhotoImage(file='logo.gif')

        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0)
        ttk.Label(self.frame_header, text='Price Check', style='Header.TLabel', foreground='red').grid(row=0, column=1, ipadx=5)

        ttk.Separator(orient='horizontal').pack(fill='x')

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text='Own:').grid(row=0, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Wnat:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Result:').grid(row=2, column=0, padx=5, sticky='sw')

        self.entry_own = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.entry_want = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.text_result = Text(self.frame_content, width=50, height=10, font=('Arial', 10))

        self.entry_own.grid(row=1, column=0, padx=5)
        self.entry_want.grid(row=1, column=1, padx=5)
        self.text_result.grid(row=3, column=0, columnspan=2, padx=5)

        ttk.Button(self.frame_content, text='Submit', command=self.submit).grid(row=4, column=0, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear', command=self.clear).grid(row=4, column=1, padx=5, pady=5, sticky='w')
    def get_price(self, c):
        y=["","","",""]
        q=0
        result=0
        s=True
        for i in c:
            y[q]=i
            q+=1
        for i in y[2]:
            if i == ".":
                s = False
            if i == "0" or i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9":
                if s is True:
                    result = result * 10 + int(i)
                else:
                    result = result + int(i) / 10
        return result
    def submit(self):

        html = urlopen("http://currency.poe.trade/search?league=Bestiary&online=x&want={}&have={}".format(self.item_index[self.entry_want.get()], self.item_index[self.entry_own.get()]))
        res = BeautifulSoup(html.read(), "html5lib")
        x = ["", "", "", ""]
        j, z, u = 0, 0, 0
        result=[0, 0, 0]
        seller_names=["", "", ""]
        abc=res.find('div', {'class':'displayoffer'})
        seller=res.findAll('div', {'class':'displayoffer'})
        for i in seller[0], seller[1], seller[2]:
            seller_names[u]=i['data-ign']
            u += 1
            #print(i['data-ign'])

        result[0]=self.get_price(res.findAll('small')[0])
        result[1] = self.get_price(res.findAll('small')[2])
        result[2] = self.get_price(res.findAll('small')[4])

        re_form=list(zip(seller_names, result))
        print(pd.DataFrame(data=re_form, columns=['Names', 'Price']))

        #print(seller_names)
        #print(result)
        #self.text_result.insert(END, str(abc['data-ign'])+'\n')
        #self.text_result.insert(END, str(result[0])+' {}\n'.format(self.entry_own.get()))
        #self.text_result.insert(END, pd.DataFrame(data=re_form, columns=['Names', 'Price']))
        for i in range(0, 3):
            self.text_result.insert(END, str(seller_names[i] + " "))
            self.text_result.insert(END, str(result[i]) + ' {}\n'.format(self.entry_own.get()))
        print("http://currency.poe.trade/search?league=Bestiary&online=x&want={}&have={}".format(self.item_index[self.entry_want.get()], self.item_index[self.entry_own.get()]))

    def clear(self):
        self.entry_own.delete(0, 'end')
        self.entry_want.delete(0, 'end')
        self.text_result.delete(1.0, 'end')



def main():

    root = Tk()
    price = Price_Check(root)
    mainloop()


if __name__ == '__main__': main()