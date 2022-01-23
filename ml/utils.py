def remove_unwanted_columns(df, ROI):
    '''
    Given a list of ROIs, the function will drop columns that are not desired.
    '''
    for column in df.columns:
        if column not in ROI:
            df = df.drop(columns=column)
    return df

def reorder_df(df, area):
    '''
    Reorders the columns in proper order
    '''
    cols = list(df.columns.values)
    cols.pop(cols.index(area))
    df = df[[area]+cols]
    return df

def combine_left_right_vol(df):
    '''
    Heuristic - Combine the Left and Right volumes into one column
    '''
    for column in df.columns:
        if "Left" in column:
            area = "-".join(column.split("-")[1:])
            left_area = f"Left-{area}"
            right_area = f"Right-{area}"
            df[area] = df[left_area] + df[right_area]
            df = df.drop(columns = [left_area, right_area])
            df = reorder_df(df, area)
    return df