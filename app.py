# %%
import xarray as xr
import hvplot.xarray
import panel as pn

pn.extension(design='material', sizing_mode='stretch_width')

# %%
sfcmet = xr.open_zarr("https://icecaps-o.s3-ext.jc.rl.ac.uk/sfcmet/", consolidated=True)

# %%
pn1 = pn.Row(sfcmet['temperature at 2 meters'].hvplot(), sizing_mode='stretch_both')

# %%
pn.template.MaterialTemplate(
    site='Panel',
    title='Nifty Dashboard for Von',
    main=[pn1],
).servable()