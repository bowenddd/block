import tkinter
from tkinter import messagebox, Toplevel, Frame, ttk
import pymongo
from price_predict import *

class Page(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("区块链价格预测系统")
        self.root.geometry('370x370')
        self.dataGet_button = tkinter.Button(self.root, command=self.dataGet, text='获取数据', width=25, height=10)
        self.dataAnalysis_button = tkinter.Button(self.root, command=self.dataAnalysis, text='分析数据', width=25, height=10)
        self.Retain1_button = tkinter.Button(self.root, command=self.Predict, text='保留', width=25, height=10)
        self.Retain2_button = tkinter.Button(self.root, command=self.Retain2, text='保留', width=25, height=10)
    def GuiArrang(self):
        self.dataGet_button.place(x=0, y=0)
        self.dataAnalysis_button.place(x=185, y=0)
        self.Retain1_button.place(x=0, y=185)
        self.Retain2_button.place(x=185, y=185)
    def dataGet(self):
        self.top = Toplevel()
        self.top.title = ('数据获取')
        self.top.geometry('800x700')
        tmp = None
        def arrang():
            currency1Chosen.place(x=60, y=20)
            currency1Chosen.current(0)
            currency2Chosen.place(x=280, y=20)
            currency2Chosen.current(0)
            label_to.place(x=220, y=20)
            Submit_button.place(x=500, y=20)
            Drawing_button.place(x=600, y=20)
            self.tree.column("a", width=200, anchor="center")
            self.tree.column("b", width=90, anchor="center")
            self.tree.column("c", width=110, anchor="center")
            self.tree.column("d", width=130, anchor="center")
            self.tree.column("e", width=180, anchor="center")
            self.tree.heading("a", text="订单时间")
            self.tree.heading("b", text="买卖类型")
            self.tree.heading("c", text="币种单价")
            self.tree.heading("d", text="成交币种数量")
            self.tree.heading("e", text="订单总额")
            self.tree.place(x=38, y=80)
            vbar.place(x=695, y=30, height=550)

        def dataCrawl():
            rootUrl = 'https://data.gateio.co/api2/1/tradeHistory/'
            currency1.get()
            url = rootUrl + currency1.get() + '_' +currency2.get()
            browsers = requests.get(url).json()
            items = None
            if (browsers["result"] == "true"):
                items = browsers["data"]
            else:
                messagebox.showinfo(title='error', message='Please Retry')
            for _ in map(self.tree.delete, self.tree.get_children("")):
                pass
            for item in items:
                self.tree.insert("", "end", values=(item["date"], item["type"], item["rate"], item["amount"], item["total"]))
            Drawing_button['state'] = 'active'
        def dataDrawing():
            messagebox.showinfo(title='Waiting~', message='I am drawing!')
        currency1 = tkinter.StringVar()
        currency2 = tkinter.StringVar()
        currency1Chosen = ttk.Combobox(self.top, width=12, textvariable=currency1)
        currency1Chosen['values'] = ('eth', 'btc')
        label_to = tkinter.Label(self.top, text='to')
        currency2Chosen = ttk.Combobox(self.top, width=12, textvariable=currency2)
        currency2Chosen['values'] = ('usdt', 'cnyx')
        Submit_button = tkinter.Button(self.top, command=dataCrawl, text='开始抓取')
        Drawing_button = tkinter.Button(self.top, command=dataDrawing, text='绘制图表', state='disabled')
        self.tree = ttk.Treeview(self.top, show="headings", height=28, columns=("a", "b", "c", "d", "e"))
        vbar = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        arrang()

    def dataAnalysis(self):
        pass
    def Predict(self):
        self.top = Toplevel()
        self.top.title = ('数据获取')
        self.top.geometry('800x700')
        ave_price_show = tkinter.StringVar()
        origin_price_data_show = tkinter.StringVar()
        predicted_price_show = tkinter.StringVar()
        def price_predict():
            url = 'https://data.gateio.co/api2/1/tradeHistory/btc_usdt'
            data = []
            load_btc_data(url, data)
            data_process(data)
            origin_price_data = copy.deepcopy(np.array(data).T[1])
            # 对数据归一化
            new_btc_data, max, min = data_nornalization(data)
            new_btc_data = np.array(new_btc_data).reshape((1, 80, 4))
            ave_price = origin_price_data.mean()
            # 预测价格
            result = predict(new_btc_data)
            predicted_price = result[0][0] * (max[1] - min[1]) + min[1]
            ave_price_show.set('最新80笔交易的平均价格:' + str(ave_price))
            origin_price_data_show.set('当前最新价格:' + str(origin_price_data[-1]))
            predicted_price_show.set('预测的下一次交易的价格:' + str(predicted_price))

            print('最新80笔交易的平均价格:{}'.format(ave_price))
            print('当前最新价格：{}'.format(origin_price_data[-1]))
            print('预测的下一次交易的价格:{}'.format(predicted_price))
            # 可视化
            l1 = range(1, len(origin_price_data) + 1)
            plt.plot(l1, origin_price_data, 'b-', color='blue')
            l2 = [80, 81]
            predict_data = [origin_price_data[-1], predicted_price]
            plt.plot(l2, predict_data, 'b-o', color='red')
            image_name = 'predicted_price.png'
            plt.savefig(image_name)
            image = Image.open(image_name)
            image = ImageTk.PhotoImage(image)
            imgLabel.config(image=image)
            imgLabel.image = image

        B = tkinter.Button(self.top, text='预测下一次交易的价格', command=price_predict)
        B.pack()
        l_ave_price = tkinter.Label(self.top, textvariable=ave_price_show)
        l_origin_price_data = tkinter.Label(self.top, textvariable=origin_price_data_show)
        l_predicted_price = tkinter.Label(self.top, textvariable=predicted_price_show)
        imgLabel = tkinter.Label(self.top)
        l_ave_price.pack()
        l_origin_price_data.pack()
        l_predicted_price.pack()
        imgLabel.pack()
    def Retain2(self):
        pass




def main():
    L = Page()
    L.GuiArrang()
    tkinter.mainloop()

if __name__ == '__main__':
    main()