import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe
import matplotlib.cm as cm
import matplotlib.colors as colors



def linear_color_scale(series,cmap,vmin,vmax):
    norm = colors.Normalize(vmin, vmax, clip=True)
    mapper = cm.ScalarMappable(norm,cmap)
    # convert to rgba
    c = []
    for i in series:
        c.append(mapper.to_rgba(i))
    return c



def player_ave_locations(df,color_scale):
    # locations based on average touches
    
    # team name and plyrs
    team_name = list(df['possession_team_name'].unique())
    lineup = list(df['player_name'].unique())
    
    # ave location of plyrs (based on touches)
    touch_events = ['Pass','Ball Receipt*','Carries','Shot','Ball Recovery','Clearance','Block',
               'Goal Keeper','Miscontrol','Dribble','Interception']
    touches = df[df['event_type_name'].isin(touch_events)]
    player_locs = touches.groupby('player_name')[['location_x','location_y']].mean()
    player_touches = touches.groupby('player_name')['player_name'].count()
    player_touches.name = 'touch_count'
    
    # xg 
    player_locs['xg'] = df.groupby(['player_name'])['xg'].sum()
    
    # linear color scale
    player_locs['xg_colors'] = linear_color_scale(player_locs['xg'],color_scale,
                                                  player_locs['xg'].min(),
                                                  player_locs['xg'].max())
    
    return player_locs.join(player_touches)


def combination_finder(df):
    # search all combinations of list
    
    lineup = list(df['formation_player_name'].unique())
    
    combs = []
    for c in itertools.combinations(lineup,2):
        combs.append(c)
    
    return combs


def pass_combination_counts(passes,lineup):
    
    combs = combination_finder(lineup)
    
    # pass counts
    pass_combs= []   
    for p1,p2 in combs:
        p = (passes[((passes['player_name']==p1)&
           (passes['pass_recipient_name']==p2))|
          ((passes['player_name']==p2)&
           (passes['pass_recipient_name']==p1))])[['player_name','pass_recipient_name','event_type_name']]
        df = pd.DataFrame({'player1':p1,
                  'player2':p2,
                  'pass_count':len(p)},
                 index=[0])
        pass_combs.append(df)
    
    passes_df = pd.concat(pass_combs).reset_index(drop=True)


    return passes_df


def pass_xgc(df):
    # xg contribution for pass combinations
    
    # shot possessions
    shot_possessions = df[df['event_type_name']=='Shot']['possession'].unique()
    
    # xg contribution per pass for each possession
    xgc = []
    for poss in shot_possessions:
        d = df[df['possession']==poss].copy()
        xg = d['xg'].sum()
        passes = d.groupby(['player_name','pass_recipient_name'])['pass_recipient_name'].count()
        xgc.append((xg/passes.sum())*passes)
    
    f = pd.concat(xgc).groupby(['player_name','pass_recipient_name']).sum()
    f.name = 'xgc'
    
    return pd.DataFrame(f).reset_index()



def pass_combination_xgc(events,lineup):
    
    df = pass_xgc(events)
    combs = combination_finder(lineup)
    # pass counts
    pass_combs= []   
    for p1,p2 in combs:
        p = (df[((df['player_name']==p1)&
           (df['pass_recipient_name']==p2))|
          ((df['player_name']==p2)&
           (df['pass_recipient_name']==p1))])
        d = pd.DataFrame({'player1':p1,
                  'player2':p2,
                  'xgc':p['xgc'].sum()},
                 index=[0])
        pass_combs.append(d)
    
    passes_df = pd.concat(pass_combs).reset_index(drop=True)
    
    
    return passes_df


def pass_network_combinations_df(passes,events,lineup,color_scale):
    # pass net counts, xgc and locations
    
    # pass counts
    passes = pass_combination_counts(passes,lineup)
    pass_df = passes[passes['pass_count']>0]
    # xg
    pass_xgc = pass_combination_xgc(events,lineup)
    xgc_df = pass_xgc[pass_xgc['xgc']>0]
    
    # join with xgc info
    joined_df = pass_df.merge(xgc_df,on=['player1','player2'],how='outer').fillna(0)
    
    # master df
    plyr_locs = player_ave_locations(events,color_scale)
    master_df = (
    joined_df.merge(plyr_locs[['location_x','location_y']].reset_index().rename(columns={'player_name':'player1',
                                                                             'location_x':'loc_x1',
                                                                             'location_y':'loc_y1'})
            ).merge(plyr_locs[['location_x','location_y']].reset_index().rename(columns={'player_name':'player2',
                                                                             'location_x':'loc_x2',
                                                                             'location_y':'loc_y2'}))
    )
    master_df['xgc_colors'] = linear_color_scale(master_df['xgc'],
                                                 color_scale,
                                                 master_df['xgc'].min(),
                                                 master_df['xgc'].max())
    
    return master_df