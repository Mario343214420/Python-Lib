from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts import options as opts
# bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
# bar.render()

citys = ['丰县', '沛县', '铜山区', '贾汪区', '鼓楼区', '泉山区', '云龙区', '邳州市', '新沂市', '睢宁县']
values = [120, 160, 180, 200, 180, 190, 130, 160, 140, 170]
geo = Geo()
geo.add_schema(maptype="徐州")
geo.add_coordinate("某地", 117.3, 34.3)
print([list(z) for z in zip(citys, values)])
geo.add(
    "test",
    [list(z) for z in zip(citys, values)],
    type_= ChartType.EFFECT_SCATTER
)
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(
    visualmap_opts=opts.VisualMapOpts(),
    title_opts=opts.TitleOpts(title="Geo地图示例")
)
geo.render("测试.html")