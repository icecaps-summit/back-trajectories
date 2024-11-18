# %%
import xarray as xr
import hvplot.xarray
import hvplot.pandas
import datetime as dt
import cartopy.crs as ccrs
import panel as pn
pn.extension('tabulator', sizing_mode='stretch_width')

# %%
fn = "https://icecaps-o.s3-ext.jc.rl.ac.uk/back-trajectories"

@pn.cache()
def get_data(filename):
    return xr.open_zarr(filename)
dye2_back_trajectories = get_data(fn)

# %% widgets
variables = [variable for variable in dye2_back_trajectories.variables]

time      = pn.widgets.DatetimePicker(name='Date of Trajectories', value=dt.datetime(2024, 5, 15), start=dt.datetime(2024, 5, 15), end = dt.datetime.today() - dt.timedelta(days=1))
level     = pn.widgets.IntSlider(name='Vertical Level of Trajectory (m)', start=100, end=9100, value=100, step=500, bar_color='green')
variable  = pn.widgets.Select(name='Trajectory Variable', options=variables)
kind      = pn.widgets.Select(name='Plot Type', options=['scatter', 'hist'])

# %%
def get_dataframe(time, level):
    df = dye2_back_trajectories.sel(time=time.strftime('%Y-%m-%d %H'), vertical_level=level, method='nearest').to_dataframe()
    return df

ref_time = dye2_back_trajectories['ref_time_along_trajectories'].values
df = pn.rx(get_dataframe)(time=time, level=level)

# %% Indicators
indicators = pn.FlexBox(
    pn.indicators.Number(
        value=df[variable].min(),  name="Min ", format="{value:,.0f}", font_size='24pt', title_size='8pt',
    ),
    pn.indicators.Number(
        value=df[variable].mean(), name="Mean ", format="{value:,.0f}", font_size='24pt', title_size='8pt',
    ),
    pn.indicators.Number(
        value=df[variable].max(),  name="Max ", format="{value:,.0f}", font_size='24pt', title_size='8pt',
    ), 
    justify_content='flex-end',
)

# %% Figure definition
trj = pn.pane.HoloViews(df.hvplot.points('longitude',
                                        'latitude',
                                        geo=True,
                                        color=variable,
                                        cmap='viridis',
                                        xlim=[-90, 0],
                                        ylim=[50, 84],
                                        coastline=True,
                                        projection=ccrs.NearsidePerspective(central_longitude=-46.3, central_latitude=66.5), 
    )
)

#fig = df[variable].hvplot(kind=kind, grid=True, c=ref_time, cmap='RdYlBu', legend=False)
fig = df[variable].hvplot(kind=kind, grid=True, c=variable, cmap='viridis', legend=False)

# %%
tseries  = pn.pane.HoloViews(fig, name='Plot', sizing_mode='stretch_width')
table = pn.widgets.Tabulator(df,  name='Table', pagination='remote', page_size=8)
thetaT = pn.pane.HoloViews(df.hvplot.scatter(x='air_potential_temperature', y='air_temperature', c=variable, cmap='viridis', grid=True))

tabs = pn.Tabs(tseries, table)

# %% Serve the template
pn.template.FastListTemplate(
    title="DYE-2 back trajectory dashboard",
    main=[pn.WidgetBox(pn.Row(*[time, level, variable, kind])), indicators,
          pn.FlexBox(pn.Row(trj, tabs), height=350),
          thetaT],
).servable()

# %%
