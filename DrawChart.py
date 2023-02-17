from datetime import datetime
import pandas as pd
import numpy as np
import db
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DrawChart:
    '''
    https://www.kaggle.com/code/yash161101/financial-charts-using-plotly-cheat-sheet
    https://jtr13.github.io/cc19/technical-analysis-for-stocks-using-plotly.html
    https://pythonnangcao.com/khoa-hoc/bai-tap-phan-tich-du-lieu-chung-khoan/
    https://vohoanghac.com/analysis/phannganhkmeans_cp68.html
    '''
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.df = db.GetStockData(symbol=self.symbol)

    def drawPrice(self):
        prices = self.df['Close']        
        fig = px.histogram(self.df,x="Close")
        fig.show()

        
    def draw(self):
        x_values = self.df['Date']
        y_values = self.df['Close']
        fig = px.bar(x=x_values, y=y_values)
        fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='crimson', size=10))
        fig.show()
    
    def draw2(self):
        x_values = self.df['Date']
        y_values = self.df['Close']
        fig = px.line(x=x_values, y=y_values)
        fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='crimson', size=10))
        fig.show()

    def draw_buy_signals(self):
        x_values = self.df['Date'].values
        y_values = self.df['Close'].values
        fig = px.line(x=x_values, y=y_values)

        window = 10
        prices = self.df['Close']
        volumes = self.df['Volume']
        dates = self.df['Date']
        signals = []
        
        for i in range(len(self.df)):
            vol = volumes[i]
            if vol == np.min(volumes[0:window]):
                signals.append([dates[i],prices[i],'min'])
            if vol == np.max(volumes[0:window]):
                signals.append([dates[i],prices[i],'max'])

        for signal in signals:
            x_value = signal[0]
            y_value = signal[1]
            note = signal[2]
            fig.add_annotation(x=x_value, y=y_value, text=note, showarrow=True, arrowhead=1)
        
        
        fig.update_layout(showlegend=False)
        fig.show()

    def draw_candle(self):
        length = 5*42
        window = 20
        df = self.df[0:length]

        # Create subplots and mention plot grid size
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03, subplot_titles=(self.symbol, 'Volume'), 
               row_width=[0.2, 0.7])
        # Plot OHLC on 1st row
        fig.add_trace(go.Candlestick(x=df["Date"], open=df["Open"], high=df["High"],
                        low=df["Low"], close=df["Close"], name=self.symbol), 
                        row=1, col=1)

        green_volume_df = df[df['Close'] > df['Open']]
        # Same for Close < Open, these are red candles/bars
        red_volume_df = df[df['Close'] < df['Open']]
        #yellow
        yellow_volume_df = df[df['Close'] == df['Open']]


        # Plot the red bars and green bars in the second subplot
        fig.add_trace(go.Bar(x=red_volume_df.Date, y=red_volume_df.Volume, showlegend=False, marker_color='#ef5350'), row=2,
                        col=1)
        fig.add_trace(go.Bar(x=green_volume_df.Date, y=green_volume_df.Volume, showlegend=False, marker_color='#26a69a'),
                        row=2, col=1)
        fig.add_trace(go.Bar(x=yellow_volume_df.Date, y=yellow_volume_df.Volume, showlegend=False, marker_color='yellow'),
                        row=2, col=1)
      
        prices = self.df['Close']
        volumes = self.df['Volume']
        dates = self.df['Date']
        signals = []

        for i in range(0, length):
            vol = volumes[i]
            if vol == np.min(volumes[i:i+window]):
                if df['Close'][i] < df['Open'][i]:
                    signals.append([dates[i],prices[i],'min'])
            if vol == np.max(volumes[i:i+window]):
                if df['Close'][i] > df['Open'][i]:
                    signals.append([dates[i],prices[i],'max'])

        for signal in signals:
            x_value = signal[0]
            y_value = signal[1]
            note = signal[2]
            fig.add_annotation(x=x_value, y=y_value, text=note, showarrow=True, arrowhead=1)
        

        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.write_image(f"data/images/{self.symbol}.png")
        fig.show()



class GroupStockChart:
    
    def __init__(self,symbols) -> None:
        self.symbols = symbols
        self.length = 5*42
        self.window = 20
        self.title = '; '.join(symbols)
        # Create subplots and mention plot grid size
        self.fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03, subplot_titles=(self.title, 'Volume'), 
               row_width=[0.2, 0.7])
        


    def draw_candle(self, symbol):
        df = db.GetStockData(symbol=symbol)
        df = df[0:self.length]

        # Plot OHLC on 1st row
        self.fig.add_trace(go.Candlestick(x=df["Date"], open=df["Open"], high=df["High"],
                        low=df["Low"], close=df["Close"], name=self.title), 
                        row=1, col=1)

        green_volume_df = df[df['Close'] > df['Open']]
        # Same for Close < Open, these are red candles/bars
        red_volume_df = df[df['Close'] < df['Open']]
        #yellow
        yellow_volume_df = df[df['Close'] == df['Open']]


        # Plot the red bars and green bars in the second subplot
        self.fig.add_trace(go.Bar(x=red_volume_df.Date, y=red_volume_df.Volume, showlegend=False, marker_color='#ef5350'), row=2,
                        col=1)
        self.fig.add_trace(go.Bar(x=green_volume_df.Date, y=green_volume_df.Volume, showlegend=False, marker_color='#26a69a'),
                        row=2, col=1)
        self.fig.add_trace(go.Bar(x=yellow_volume_df.Date, y=yellow_volume_df.Volume, showlegend=False, marker_color='yellow'),
                        row=2, col=1)
      
        prices = df['Close']
        volumes = df['Volume']
        dates = df['Date']
        signals = []

        for i in range(0, self.length):
            vol = volumes[i]
            if vol == np.min(volumes[i:i+self.window]):
                if df['Close'][i] < df['Open'][i]:
                    signals.append([dates[i],prices[i],'min'])
            if vol == np.max(volumes[i:i+self.window]):
                if df['Close'][i] > df['Open'][i]:
                    signals.append([dates[i],prices[i],'max'])

        for signal in signals:
            x_value = signal[0]
            y_value = signal[1]
            note = signal[2]
            self.fig.add_annotation(x=x_value, y=y_value, text=note, showarrow=True, arrowhead=1)
        

        self.fig.update(layout_xaxis_rangeslider_visible=False)
        #self.fig.write_image(f"data/images/{self.symbol}.png")
        #self.fig.show()

    def draw(self):
        for symbol in self.symbols:
            self.draw_candle(symbol=symbol)

        self.fig.show()


# symbols = ['VND','SCR','HBC','HAX']

# gc = GroupStockChart(symbols=symbols)
# gc.draw()
# for symbol in symbols:
#     d = DrawChart(symbol=symbol)
#     d.draw_candle()

d = DrawChart(symbol='nvl')
d.drawPrice()
