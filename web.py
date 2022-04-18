import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit_echarts
from pyecharts.charts import Funnel
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']# 设置微软雅黑字体
plt.rcParams['axes.unicode_minus'] = False # 避免坐标轴不能正常的显示负号
from pyecharts.charts import Map, Bar, Grid
from pyecharts import options as opts
import matplotlib.image as mpimg

data=pd.read_excel('data异常.xlsx')
data['ITEM_PRICE']=data['ITEM_PRICE'].apply(lambda x: x)
def tranAge(x):
   if 0<=x<100:
      x = 1
   elif 100<=x<1000:
      x = 2
   elif 1000<=x<10000:
      x = 3
   else :
      x =0
   return x
data['ITEM_PRICE'] = data['ITEM_PRICE'].apply(tranAge)
price = data.ITEM_PRICE.value_counts()
price=pd.DataFrame(price)
price.index=['0-100','100-1000','1000-10000' ,'大于10000']
price["number"]=price["ITEM_PRICE"]
price=price.drop(columns=['ITEM_PRICE'])
miss = data.miss.value_counts()
miss=pd.DataFrame(miss)
miss=miss.reset_index()
data['ITEM_SALES_VOLUME']=data['ITEM_SALES_VOLUME'].apply(lambda x: x)
def tranAge(x):
   if 0<=x<100:
      x = 1
   elif 100<=x<1000:
      x = 2
   elif 1000<=x<10000:
      x = 3
   else :
      x =0
   return x
data['ITEM_SALES_VOLUME'] = data['ITEM_SALES_VOLUME'].apply(tranAge)
volume=data.ITEM_SALES_VOLUME.value_counts()
volume=pd.DataFrame(volume)
volume["volume"]=["0-100","100-1000","1000-10000","大于10000"]
def tranAge(x):
   if 0<=x<100:
      x = 1
   elif 100<=x<1000:
      x = 2
   elif 1000<=x<10000:
      x = 3
   elif 10000<=x<100000:
      x = 4
   elif 10000<=x<100000:
      x=5
   else:
      x=0
   return x
data['ITEM_SALES_AMOUNT'] = data['ITEM_SALES_AMOUNT'].apply(tranAge)
AMOUNT= data.ITEM_SALES_AMOUNT.value_counts()
AMOUNT=pd.DataFrame(AMOUNT)
AMOUNT=AMOUNT.reset_index()
data.CATE_NAME_LV1= data.CATE_NAME_LV1.replace({np.nan:'missing'})
cate= data.CATE_NAME_LV1.value_counts()
cate=pd.DataFrame(cate)
cate=cate.reset_index()
y1 = np.array(cate['CATE_NAME_LV1'])
y1 =y1.tolist()
x = np.array(cate['index'])
x =x.tolist()
data.ITEM_DELIVERY_PLACE= data.ITEM_DELIVERY_PLACE.replace({np.nan:'missing'})
PLACE= data.ITEM_DELIVERY_PLACE.value_counts()
PLACE=pd.DataFrame(PLACE)
PLACE=PLACE.reset_index()
PLACE=PLACE.drop([0])
province_list = PLACE['index'].tolist()#将省份数据提取成列表
d_data = PLACE['ITEM_DELIVERY_PLACE'].values.tolist()#将确证的人数提取成列表
d=[]
for p in province_list:#构建循环
    n=d_data[province_list.index(p)]#根据列表中的省份名提取对应的确诊人数。
    p = p.replace('省', '').replace('市', '').replace('自治区', '').replace('壮族', '').replace('维吾尔', '').replace('回族', '')#将省份名改成适用于map的省份名。
    d.append([p, n])#将
def tranAge(x):
   if 0<=x<100:
      x = 1
   elif 100<=x<1000:
      x = 2
   elif 1000<=x<10000:
      x = 3
   elif x>10000:
      x =4
   return x
data['ITEM_FAV_NUM'] = data['ITEM_FAV_NUM'].apply(tranAge)
data.ITEM_FAV_NUM= data.ITEM_FAV_NUM.replace({np.nan:'missing'})
ITEM_FAV_NUM=data.ITEM_FAV_NUM.value_counts()
ITEM_FAV_NUM=pd.DataFrame(ITEM_FAV_NUM)
ITEM_FAV_NUM=ITEM_FAV_NUM.reset_index()
def tranAge(x):
   if 0<=x<100:
      x = 1
   elif 100<=x<1000:
      x = 2
   elif 1000<=x<10000:
      x = 3
   elif x>10000:
      x =4
   return x
data['TOTAL_EVAL_NUM'] = data['TOTAL_EVAL_NUM'].apply(tranAge)
data.TOTAL_EVAL_NUM= data.TOTAL_EVAL_NUM.replace({np.nan:'missing'})
TOTAL_EVAL_NUM=data.TOTAL_EVAL_NUM.value_counts()
TOTAL_EVAL_NUM=pd.DataFrame(TOTAL_EVAL_NUM)
TOTAL_EVAL_NUM=TOTAL_EVAL_NUM.reset_index()
ITEM_FAV_NUM_y1 = np.array(ITEM_FAV_NUM['ITEM_FAV_NUM'])#将男性转换成numpy类型的数据
ITEM_FAV_NUM_y1 =ITEM_FAV_NUM_y1.tolist()#
TOTAL_EVAL_NUM_y2 = np.array(TOTAL_EVAL_NUM['TOTAL_EVAL_NUM'])#将男性转换成numpy类型的数据
TOTAL_EVAL_NUM_y2 =TOTAL_EVAL_NUM_y2.tolist()#
FAV_EVAL_x=["missing","0-100","100-1000","1000-10000","大于10000"]





def volume_number():
    funnel1= (Funnel()
              .add("用户数", [list(z) for z in zip(volume['volume'], volume['ITEM_SALES_VOLUME'])],
                   # 生成[年龄结构,数据]的列表 ，并放进图标
                   sort_='ascending',  # 选择排序方式
                   label_opts=opts.LabelOpts(position="inside"))
              .set_global_opts(title_opts=opts.TitleOpts(title="销量"))
              )
    streamlit_echarts.st_pyecharts(funnel1,height=600)


def amount():
    list = ['100-1000', '0-100', '1000-10000', '10000-100000', "大于100000"]
    fig, ax = plt.subplots(figsize=(16,10), facecolor='white', dpi= 80)
    ax.vlines(x=AMOUNT.index, ymin=0, ymax=AMOUNT.ITEM_SALES_AMOUNT, color='blue', alpha=0.7, linewidth=40)  # 画好辅助线
    for i, AMOUNT_NUMBER in enumerate(AMOUNT.ITEM_SALES_AMOUNT):
        ax.text(i, AMOUNT_NUMBER + 0.5, round(AMOUNT_NUMBER, 1), horizontalalignment='center')  # 给柱状图添加好文本
    ax.set_title('销售额', fontdict={'size': 22})  # 设置标题
    ax.set(ylabel='数量', ylim=(0, 100000))  # 设置y轴的标签，和y轴的范围。
    ax.set(xlabel='价格区间')  # 设置y轴的标签，和y轴的范围
    plt.xticks(AMOUNT.index, list, rotation=60, horizontalalignment='right', fontsize=12)  # 设置x轴的文本显示，并旋转一定的角度。

    # Plot the data
    st.pyplot(fig)


def delivery():
    # with open("D:/Program Files/Python39/Lib/site-packages/echarts_countries_pypkg/resources/echarts-countries-js\china.js", "r") as f:
    #     map = streamlit_echarts.st_pyecharts("china", json.loads(f.read()), )
    # c = (
    #     Map()  # 定义一个map图标
    #         .add("商品发货地", d, "china")  # 定义图为中国地图，
    #         .set_global_opts(
    #         title_opts=opts.TitleOpts(title="发货地"),  # 设置地图的标题
    #         visualmap_opts=opts.VisualMapOpts(
    #             is_piecewise=True,  # 表示分段的颜色深度
    #             pieces=[{'min': 0, 'max': 60, 'label': "0-600", 'color': 'powderblue'},
    #                     {'min': 60, 'max': 120, 'label': "600-1200", 'color': 'skyblue'},
    #                     {'min': 120, 'max': 180, 'label': "1200-1800", 'color': 'dodgerblue'},
    #                     {'min': 180, 'max': 240, 'label': "1800-2400", 'color': 'royalblue'},
    #                     {'min': 240, 'max': 500, 'label': "50000-7000", 'color': 'blue'},
    #                     ]
    #         )  # 自定义颜色和颜色所代表的区间
    #     )
    #         .set_series_opts(
    #         label_opts=opts.LabelOpts(is_show=True))  # 展示地图的label值
    # )
    # streamlit_echarts.st_pyecharts(c,map=map,height=500)

    imag = mpimg.imread("C:/Users/cyashuai/Desktop/1.png")
    st.image(imag)


def cate():
    bar = (Bar()  # 定义一个条形图
           .add_xaxis(x)  # 加上我们的年份数据
           .add_yaxis('数量', y1)
           .set_global_opts(title_opts=opts.TitleOpts(title="异常数据各种种类数量", subtitle="种类"))
           .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
           .reversal_axis()
           )


    streamlit_echarts.st_pyecharts(bar,height=500)


def miss_number():
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='white', dpi=80)
    ax.bar([i + 1 for i in range(14)], miss["miss"], width=0.5)
    ax.set_xlabel("缺失数量")  # 设置x轴标签
    ax.set_ylabel("个数")  # 设置y轴标签
    ax.set_title("缺失值")  # 设置标题
    for i, AMOUNT_NUMBER in enumerate(miss.miss):
        ax.text(i+1, AMOUNT_NUMBER + 0.5, round(AMOUNT_NUMBER, 1), horizontalalignment='center')
        # 添加x坐标对应的label
    plt.xticks([i + 1 for i in range(14)], miss["index"], rotation=90)

    st.pyplot(fig)


def price_number():
    fig = px.pie(price ,values='number', names=['0-100', '100-1000', '1000-10000', '大于10000'],
                 color_discrete_map={
                     '0-100': 'lightcyan',
                     '100-1000': 'cyan',
                     '1000-10000': 'royalblue',
                     '大于10000': 'darkblue'},title="价格区间")


    st.plotly_chart(fig)


def FAV_EVA():
    bar = (Bar()  # 定义一个条形图
           .add_xaxis(FAV_EVAL_x)  # 加上我们的年份数据
           .add_yaxis('收藏', ITEM_FAV_NUM_y1, itemstyle_opts=opts.ItemStyleOpts(color="orange"))  # 加上男性人口的数据
           .add_yaxis('评论', TOTAL_EVAL_NUM_y2, itemstyle_opts=opts.ItemStyleOpts(color="purple"))  # 加上女性人口数据
           .set_global_opts(title_opts=opts.TitleOpts(title="评论和收藏数量"))  # 设置标题
           .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
           )

    streamlit_echarts.st_pyecharts(bar,height=500)




def Double_coordinates():

    st.markdown('#### 数据表展示')
    data[0:1000]
    data['ITEM_FAV_NUM'] = data['ITEM_FAV_NUM'].astype("str")
    data['TOTAL_EVAL_NUM'] = data['TOTAL_EVAL_NUM'].astype("str")
    data['ITEM_STOCK'] = data['ITEM_STOCK'].astype("str")
    st.table(data)
    #
    # st.markdown('#### 双坐标图')
    # x = df["年月"]
    # y1_1 = df['流失客户']
    # y1_2 = df['新客户']
    #
    # y2 = df["余额"]
    #
    # trace0_1 = go.Bar(x=x, y=y1_1,
    #                   marker=dict(color="red"),
    #                   opacity=0.5,
    #                   name="流失客户")
    #
    # trace0_2 = go.Bar(x=x, y=y1_2,
    #                   marker=dict(color="blue"),
    #                   opacity=0.5,
    #                   name="新客户")
    #
    # trace1 = go.Scatter(x=x, y=y2,
    #                     mode="lines",
    #                     name="余额",
    #                     # 【步骤一】：使用这个参数yaxis="y2"，就是绘制双y轴图
    #                     yaxis="y2")
    #
    # data = [trace0_1, trace0_2, trace1]
    #
    # layout = go.Layout(title="客户发展趋势",
    #                    xaxis=dict(title="年月"),
    #                    yaxis=dict(title="客户数量"),
    #                    # 【步骤二】：给第二个y轴，添加标题，指定第二个y轴，在右侧。
    #                    yaxis2=dict(title="金额", overlaying="y", side="right"),
    #                    legend=dict(x=0.78, y=0.98, font=dict(size=12, color="black")))
    #
    # fig = go.Figure(data=data, layout=layout)


def Layouts_plotly():
    st.sidebar.write('异常商品')
    add_selectbox = st.sidebar.radio(
        "具体特征",
        ("缺失值","价格", "销量", "销售额", "商品种类", "评论收藏", "发货地")
    )
    if add_selectbox == "缺失值":
        miss_number()
    elif add_selectbox == "价格":
        price_number()
    elif add_selectbox == "销量":
        volume_number()
    elif add_selectbox == "销售额":
        amount()
    elif add_selectbox == "商品种类":
        cate()
    elif add_selectbox == "评论收藏":
        FAV_EVA()
    elif add_selectbox == "发货地":
        delivery()
    # 补充表单
    st.sidebar.button('基本数据表', on_click=Double_coordinates)


def main():
    Layouts_plotly()


if __name__ == "__main__":
    main()



