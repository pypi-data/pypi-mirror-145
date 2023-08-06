import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
__author__ = 'jundurraga'


def plot_time_frequency_responses(dataframe: pd.DataFrame = None,
                                  rows_by: str = None,
                                  cols_by: str = None,
                                  sub_average_time_buffer_size: int = None,
                                  time_xlim: [float, float] = None,
                                  time_ylim: [float, float] = None,
                                  freq_xlim: [float, float] = None,
                                  freq_ylim: [float, float] = None,
                                  time_vmarkers: np.array = None,
                                  freq_vmarkers: np.array = None,
                                  title_by: str = 'row',
                                  title_v_offset: float = 0.0
                                  ) -> plt.figure:
    """
    This function will plot the waveforms contained in a pandas dataframe read using the sqlite_waveforms_to_pandas
    function of pEEGy.
    The rows and columns of the output plot are specified by the factors of the dataframe.
    The output will show the data for each of those factors (both individual and average data).
    :param dataframe: a pandas dataframe returned by sqlite_waveforms_to_pandas function of pEEGy.
    :param rows_by: name of the factor in the dataframe for which the rows in the plot will be split.
    :param cols_by: name of the factor in the dataframe for which the columns in the plot will be split.
    :param sub_average_time_buffer_size: This is a parameter used to sub_average time_domain data. For example, if each
    of your data have 10000 points, and you want to show the average having a length of 1000 samples, you could specify
    sub_average_time_buffer_size = 1000. This will averaged the 10000 points by splitting the data into blocks of 1000
    sampels.
    :param time_xlim: x axis limis for the time-domain panels
    :param time_ylim: y axis limis for the time-domain panels
    :param freq_xlim: x axis limis for the frequency-domain panels
    :param freq_ylim: y axis limis for the frequency-domain panels
    :param time_vmarkers: array with x values to add a vertical marker in the time-domain panels
    :param freq_vmarkers: array with x values to add a vertical marker in the frequency-domain panels
    :param title_by: string specifying from which factor you want to show the titles in each panel. This can be: "row",
    "col", or "both"
    :param title_v_offset: float specifying the vertical offset of the title
    :return:
    """
    _rows_and_cols = []
    n_rows = 1
    n_cols = 1
    row_conditions = np.array([1])
    col_conditions = np.array([1])
    if rows_by is not None:
        _rows_and_cols.append(rows_by)
        _, idx = np.unique(dataframe[rows_by], return_index=True)
        row_conditions = dataframe[rows_by].iloc[np.sort(idx)].values
        n_rows = row_conditions.size
    idx_rows = np.arange(row_conditions.size)

    if cols_by is not None:
        _rows_and_cols.append(cols_by)
        _, idx = np.unique(dataframe[cols_by], return_index=True)
        col_conditions = dataframe[cols_by].iloc[np.sort(idx)].values
        n_cols = col_conditions.size
    idx_cols = np.arange(col_conditions.size)
    if len(_rows_and_cols):
        groups = dataframe.groupby(_rows_and_cols)
    else:
        groups = [((row_conditions[0], col_conditions[0]), dataframe)]
    fig_out, ax = plt.subplots(n_rows, n_cols)
    gs = gridspec.GridSpec(n_rows, n_cols)
    for _id, ((_current_row_group, _current_col_group), _group) in enumerate(groups):
        _idx_row = idx_rows[_current_row_group == row_conditions].squeeze()
        _idx_col = idx_cols[_current_col_group == col_conditions].squeeze()
        for _i, (_, _row) in enumerate(_group.iterrows()):
            y = _row['y']
            x = _row['x']
            fs = _row['x_fs']
            _domain = _row['domain']
            if y.ndim == 1:
                y = y.reshape([-1, 1])
            y_single_responses = y

            if _domain == 'time' and sub_average_time_buffer_size is not None:
                fs = 1 / np.mean(np.diff(x))
                used_samples = int(np.floor(y.shape[0] // sub_average_time_buffer_size) * sub_average_time_buffer_size)
                y_f = y[0: used_samples, :]
                y_f = np.transpose(np.reshape(y_f, (sub_average_time_buffer_size, -1, y_f.shape[1]), order='F'),
                                   [0, 2, 1])
                y_f = np.mean(y_f, axis=2)
                x = np.arange(0, sub_average_time_buffer_size) / fs
                y_single_responses = y_f

            ax = plt.subplot(gs[_idx_row, _idx_col])
            if title_by == 'row':
                title = '{:}'.format(_current_row_group)
            if title_by == 'col':
                title = '{:}'.format(_current_col_group)

            if title_by == 'both':
                title = '{:} / {:}'.format(_current_row_group, _current_col_group)

            ax.set_title(title, y=1 + title_v_offset, size=6)
            if _domain == 'time':
                y_mean = np.mean(y_single_responses, axis=1)
                ax.plot(x, y_single_responses,  linewidth=1.0, alpha=0.2, color='gray')
            if _domain == 'frequency':
                y_mean = np.mean(np.abs(y_single_responses), axis=1)
                ax.plot(x, np.abs(y_single_responses), linewidth=1.0, alpha=0.1, color='gray')

            ax.plot(x, y_mean, color='m', linewidth=1.5)
            if _idx_row == row_conditions.size // 2 and _idx_col == 0:
                ax.set_ylabel('Amplitude [{:}]'.format(_row['y_unit']))
            if _domain == 'time':
                ax.set_xlabel('Time [{:}]'.format(_row['x_unit']))
                if time_xlim is not None:
                    ax.set_xlim(time_xlim)
                if time_ylim is not None:
                    ax.set_ylim(time_ylim)
                if time_vmarkers is not None:
                    [ax.axvline(_t, color='k', linestyle=':', linewidth=0.5) for _t in time_vmarkers]
            if _domain == 'frequency':
                if freq_xlim is not None:
                    ax.set_xlim(freq_xlim)
                if freq_ylim is not None:
                    ax.set_ylim(freq_ylim)
                ax.set_xlabel('Frequency [{:}]'.format(_row['x_unit']))
                if freq_vmarkers is not None:
                    [ax.axvline(_f, color='k', linestyle=':', linewidth=0.5) for _f in freq_vmarkers]

    all_axes = fig_out.get_axes()
    for ax in all_axes:
        ax.spines['top'].set_visible(False)
        if not ax.is_last_row():
            ax.set_xticklabels([])
            ax.set_xlabel('')
        ax.spines['left'].set_visible(True)
        ax.spines['right'].set_visible(False)
    inch = 2.54
    fig_out.set_size_inches(12.0/inch, 2.25 * len(row_conditions)/inch)
    fig_out.subplots_adjust(top=0.98, bottom=0.08, hspace=0.0, left=0.15, right=0.95)
    return fig_out
