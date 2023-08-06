import datetime
import matplotlib.pyplot as plt

import geospacelab.visualization.mpl.dashboards as dashboards


def test():
    dt_fr = datetime.datetime(2016, 3, 14, 0)
    dt_to = datetime.datetime(2016, 3, 15, 23,)
    dashboard = dashboards.TSDashboard(dt_fr=dt_fr, dt_to=dt_to)
    ds1 = dashboard.dock(
        datasource_contents=['madrigal', 'isr', 'millstonehill', 'vi'])

    ds2 = dashboard.dock(
        datasource_contents=['madrigal', 'isr', 'millstonehill', 'gridded'])
    v_i_N = dashboard.assign_variable('v_i_N', dataset=ds1)
    v_i_E = dashboard.assign_variable('v_i_E', dataset=ds1)
    v_i_Z = dashboard.assign_variable('v_i_Z', dataset=ds1)
    E_E = dashboard.assign_variable('E_E', dataset=ds1)
    E_N = dashboard.assign_variable('E_N', dataset=ds1)

    n_e = dashboard.assign_variable('n_e', dataset=ds2)

    # ds2 = dashboard.dock(
    #     datasource_contents=['madrigal', 'isr', 'millstonehill', 'gridded'])
    layout = [[n_e], [v_i_E], [v_i_N], [v_i_Z], [E_E], [E_N]]
    # layout = [[Bz, By], [v_sw], [n_p], [sym_h]]
    dashboard.set_layout(panel_layouts=layout, hspace=0.1)
    dashboard.draw()
    # dashboard.save_figure(file_name='example_omni_6', append_time=False)
    pass


if __name__ == "__main__":
    test()
    plt.show()
