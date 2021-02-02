import pandas as pd

def event_selector(raw_csv,event_type=None):
    """
    select specified event from raw csv. drop duplicate data
    
    Arg
    ------
    event_type : str
    
    Out
    -------
    events : pandas df
    
    """
    
    if event_type != None:
        events =raw_csv[raw_csv['event_type_name']==event_type].reset_index()

        # drop duplicates
        events.drop_duplicates(subset=['timestamp','player_name',
                                       'event_type_name','location_x', 'location_y'],
                               inplace=True)
    elif event_type == None:
        events = raw_csv.drop_duplicates(subset=['timestamp',
                                                 'player_name','event_type_name',
                                                 'location_x', 'location_y'])
    else:
        raise KeyError('Enter properly')
    
    return events