from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template, request
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile
from nba_api.stats.static import players
import pandas


#tutorial on flask comes from https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html
def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    hover_html = """
      <div>
        <span class="hover-tooltip">Scored: @Stat</span>
      </div>
      <div>
        <span class="hover-tooltip">Opponent: @Opponent</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data['Game'])
    ydr = Range1d(start=0,end=max(data['Stat'])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x='Game', top='Stat', bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = y_name
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = x_name
    plot.xaxis.major_label_orientation = 1
    return plot


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chart", methods= ['POST', 'GET'])
def chart():
    if request.method == 'POST':
        result = request.form
        playerName = result['Name']
        seasonYear =  result['Season']
        statCategory = result['Stat']
        playerId = players.find_players_by_first_name(playerName)[0]['id']
        # print(playerId)


        player_info = commonplayerinfo.CommonPlayerInfo(player_id= playerId)
        playerInfo = player_info.common_player_info.get_data_frame()
        # print (avaliableSeasonDF.at[0, 'SEASON_ID'])
        # print (playerInfo)
        # team_id =


        seasonInfo = playerfantasyprofile.PlayerFantasyProfile(player_id = playerId, season=seasonYear)

        seasonInfoByGame= seasonInfo.opponent.get_data_frame()
        # print(seasonInfoByGame)
        statDF = seasonInfoByGame.loc[:,statCategory]
        oppDF = seasonInfoByGame.loc[:,'GROUP_VALUE']
        print(statDF)
        bars_count = 10
        if bars_count <= 0:
            bars_count = 1

        data = {"Game": [], "Stat": statDF.tolist(), "Opponent": oppDF.tolist()}
        for i in range(1, len(statDF.tolist()) + 1):
            data['Game'].append(i)


        hover = create_hover_tool()
        title = playerName + ' ' + seasonYear
        print(data)
        plot = create_bar_chart(data, title, "Game",
                                statCategory, hover)
        script, div = components(plot)

        return render_template("chart.html", pn = playerName,sy = seasonYear,sc = statCategory,
                           the_div=div, the_script=script)

if __name__ == "__main__":
    app.run(debug=True)
