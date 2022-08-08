import folium
import webbrowser
import pandas as pd
import gspread
from folium.plugins import MarkerCluster
import branca

gc = gspread.oauth()
sheet = gc.open('colorado_springs').get_worksheet(0)

df = pd.DataFrame(sheet.get_all_records())
df = df.astype(str)

location = df[['Latitude', 'Longitude']]
location_list = location.values.tolist()


class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start

    def propertyColors(df):
        if df['Status'] == 'Loaded':
            return 'green'

        elif df['Status'] == 'Waiting to hear back':
            return 'orange'

        elif df['Status'] == 'Not an option':
            return 'red'

        else:
            return 'darkblue'

    df['color'] = df.apply(propertyColors, axis=1)

    def showMap(self):
        # Create the map
        my_map = folium.Map(
            location=self.center, zoom_start=self.zoom_start, location_list=location_list)

        marker_cluster = MarkerCluster().add_to(my_map)

        for marker in range(0, len(location_list)):
            property_name = df['Property Name'].iloc[marker]
            year_built = df['Year Built'].iloc[marker]
            parking_ratio = df['Parking Ratio'].iloc[marker]
            bldg_size = df['RBA'].iloc[marker]
            available_space = df['Total Available Space (SF)'].iloc[marker]
            broker_co = df['Leasing Company Name'].iloc[marker]
            broker_name = df['Leasing Company Contact'].iloc[marker]
            broker_phone = df['Leasing Company Phone'].iloc[marker]
            notes = df['Notes'].iloc[marker]

            left_col_color = "#19a7bd"
            right_col_color = "#f2f0d3"

            html = '''<head>
				<h4 style="margin-bottom:10"; width="200px">{}</h4>'''.format(property_name) + '''
				</head>
				<table style="height: 126px; width: 375px;">
				<tbody>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Year Built</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(year_built) + '''
				</tr>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Parking Ratio</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(parking_ratio) + '''
				</tr>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Total Building Size (SF)</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(bldg_size) + '''
				</tr>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Total Available Space (SF)</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(available_space) + '''
				</tr>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Brokerage Company</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(broker_co) + '''
				</tr>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Broker Name</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(broker_name) + '''
				</tr>
				<tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Broker Phone</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(broker_phone) + '''
				</tr>
				<td style="background-color: ''' + left_col_color + ''';"><span style="color: #ffffff;">Notes</span></td>
				<td style="width: 200px;background-color: ''' + right_col_color + ''';">{}</td>'''.format(notes) + '''
				</tbody>
				</table>
				</html>
				'''

            iframe = folium.IFrame(html, width=510, height=280)
            popup = folium.Popup(iframe, max_width=500)

            folium.Marker(location_list[marker],
                          popup=popup,
                          icon=folium.Icon(color=df['color'][marker], icon_color='white', icon='info-sign', angle=0, prefix='fa')).add_to(marker_cluster)

        # Display the map
        my_map.save("map.html")
        webbrowser.open("map.html")


coords = [38.8339, -104.8214]
map = Map(center=coords, zoom_start=12)
map.showMap()
