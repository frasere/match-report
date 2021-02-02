import pandas as pd
import numpy as np




def fwds_kpis(cfs):
    """
    calulate kpis for forwards
    
    Arg
    ------
    cfs : pandas df of forward events
    
    Out
    -------
    df : pandas df of kpis
    
    """
    
    cfs_df = cfs[['xg','event_type_name','play_pattern_name','player_name',
       'player_position_name', 'location_x', 'location_y', 'end_location_x',
       'end_location_y','under_pressure', 'outcome_name','counterpress','aerial_won']]
    
    # xg,shots, box_touches, pressures, aerials
    xg = cfs_df.groupby(['player_name'])['xg'].sum()
    shots = cfs_df[cfs_df['event_type_name']=='Shot'].groupby(['player_name'])['event_type_name'].count()
    box_touches = cfs_df[(cfs_df['location_x']>=99.6)
      &(cfs_df['location_y']>=17.67)
      &(cfs_df['location_y']<=65.75)
      &(cfs_df['event_type_name']!='Pressure')].groupby(['player_name'])['player_name'].count()
    
    pressures = (cfs_df[(cfs_df['event_type_name']=='Pressure')].
                 groupby(['player_name'])['event_type_name'].count())
    
    aerials = cfs_df[(cfs_df['aerial_won']>0)].groupby(['player_name'])['aerial_won'].count()
    
    dribbles = (cfs_df[(cfs_df['event_type_name']=='Dribble')
                      &(cfs_df['outcome_name']=='Complete')]
                .groupby(['player_name'])['player_name'].count())
    
    df = pd.concat([xg,shots,box_touches,pressures,dribbles,aerials],axis=1)
    df.columns = ['xg','shots','box_touches','pressures','succ. dribbles','aerials_won']
    df['shot_touch%'] = (df['shots']/df['box_touches'])*100
    df['xg/shot'] = df['xg']/df['shots']
    df['goals'] = [0,1]
    
    df = df.fillna(0)
    df = df[['goals','xg','shots','xg/shot','shot_touch%','box_touches','pressures','succ. dribbles','aerials_won']]
    
    return round(df,2)

def wb_kpis(wbs):
    # calc kpis for wb
    
    cfs_df = wbs[['xg','event_type_name','type_name','play_pattern_name','player_name',
       'player_position_name', 'location_x', 'location_y', 'end_location_x','pass_cross',
       'end_location_y','under_pressure', 'outcome_name','counterpress','aerial_won']]
    
    # xg,shots, box_touches, pressures, aerials
    tackles = cfs_df[cfs_df['type_name']=='Tackle'].groupby(['player_name'])['type_name'].count()
    intercepts = (cfs_df[cfs_df['event_type_name']=='Interception']
                  .groupby(['player_name'])['event_type_name'].count())
    
    pressures = (cfs_df[(cfs_df['event_type_name']=='Pressure')].
             groupby(['player_name'])['event_type_name'].count())
    
    crosses = (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['pass_cross']==True)].
             groupby(['player_name'])['event_type_name'].count())
    
    # passes carries dribbles into final 3rd
    deep_prog = (cfs_df[(cfs_df['event_type_name']=='Pass')
                        |(cfs_df['event_type_name']=='Dribble')
                       |(cfs_df['event_type_name']=='Carries')
                       &(cfs_df['location_x']>=80)].
             groupby(['player_name'])['event_type_name'].count())
    
    pass_complete =  (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['outcome_name'].isnull())].
             groupby(['player_name'])['event_type_name'].count())
    
    pass_incomp = (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['outcome_name']=='Incomplete')].
             groupby(['player_name'])['event_type_name'].count())

    dribbles = (cfs_df[(cfs_df['event_type_name']=='Dribble')
                      &(cfs_df['outcome_name']=='Complete')]
                .groupby(['player_name'])['player_name'].count())
    
    aerials = cfs_df[(cfs_df['aerial_won']>0)].groupby(['player_name'])['aerial_won'].count()
    
    fouls = (cfs_df[(cfs_df['event_type_name']=='Foul Won')]
                .groupby(['player_name'])['player_name'].count())
    
    # create df    
    df = pd.concat([tackles,pressures,crosses,deep_prog,pass_complete
                    ,pass_incomp,dribbles,aerials,fouls],axis=1)
    df.columns = ['tack','pressures','crosses','deep_prog','pass_comp',
                  'pass_incomp','succ. dribbles','aerials_won','fouls_won']
    df['pass_%'] = (df['pass_comp']/(df['pass_incomp']+df['pass_comp']))*100
    df = df.fillna(0)
    
    df = df[['tack','pressures','crosses','deep_prog','pass_%','succ. dribbles','aerials_won','fouls_won']]
    
    return round(df,2)


def cm_kpis(cms):
    # calc kpis for wb
    
    cfs_df = cms[['xg','event_type_name','type_name','play_pattern_name','player_name',
       'player_position_name', 'location_x', 'location_y', 'end_location_x','pass_cross',
       'end_location_y','under_pressure', 'outcome_name','counterpress','aerial_won']]
    
    # xg,shots, box_touches, pressures, aerials
    pass_complete =  (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['outcome_name'].isnull())].
             groupby(['player_name'])['event_type_name'].count())
    
    pass_incomp = (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['outcome_name']=='Incomplete')].
             groupby(['player_name'])['event_type_name'].count())
    
    # passes carries dribbles into final 3rd
    deep_prog = (cfs_df[(cfs_df['event_type_name']=='Pass')
                        |(cfs_df['event_type_name']=='Dribble')
                       |(cfs_df['event_type_name']=='Carries')
                       &(cfs_df['location_x']>=80)].
             groupby(['player_name'])['event_type_name'].count())
    
    dribbles = (cfs_df[(cfs_df['event_type_name']=='Dribble')
                      &(cfs_df['outcome_name']=='Complete')]
                .groupby(['player_name'])['player_name'].count())
    
    fouls = (cfs_df[(cfs_df['event_type_name']=='Foul Won')]
            .groupby(['player_name'])['player_name'].count())

    pressures = (cfs_df[(cfs_df['event_type_name']=='Pressure')].
             groupby(['player_name'])['event_type_name'].count())
    
    
    tackles = cfs_df[cfs_df['type_name']=='Tackle'].groupby(['player_name'])['type_name'].count()
    intercepts = (cfs_df[cfs_df['event_type_name']=='Interception']
                  .groupby(['player_name'])['event_type_name'].count())
    
    
    # create df    
    df = pd.concat([pass_complete,pass_incomp,deep_prog,dribbles,fouls
                    ,pressures,tackles,intercepts],axis=1)
    df.columns = ['pass_comp','pass_incomp','deep prog.','succ. dribbles','fouls_won',
                 'pressures','tack','int']
    df['pass_%'] = (df['pass_comp']/(df['pass_incomp']+df['pass_comp']))*100
    
    df = df.fillna(0)
    df = df[['pass_%','deep prog.','succ. dribbles','fouls_won','pressures','tack']]
    
    return round(df,2)


def cb_kpis(cbs):
    # calc kpis for wb
    
    cfs_df = cbs[['xg','event_type_name','type_name','play_pattern_name','player_name',
       'player_position_name', 'location_x', 'location_y', 'end_location_x','pass_cross',
       'end_location_y','under_pressure', 'outcome_name','counterpress','aerial_won',
                 'pass_height_name','under_pressure']]
    
    # xg,shots, box_touches, pressures, aerials
    pass_complete =  (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['outcome_name'].isnull())].
             groupby(['player_name'])['event_type_name'].count())
    
    pass_incomp = (cfs_df[(cfs_df['event_type_name']=='Pass')&
                     (cfs_df['outcome_name']=='Incomplete')].
             groupby(['player_name'])['event_type_name'].count())
    
    pressures = (cfs_df[(cfs_df['event_type_name']=='Pressure')].
         groupby(['player_name'])['event_type_name'].count())
    
    fouls = (cfs_df[(cfs_df['event_type_name']=='Foul Won')]
        .groupby(['player_name'])['player_name'].count())
    
    tackles = cfs_df[cfs_df['type_name']=='Tackle'].groupby(['player_name'])['player_name'].count()
    intercepts = (cfs_df[cfs_df['event_type_name']=='Interception']
                  .groupby(['player_name'])['event_type_name'].count())
    
    aerials = cfs_df[(cfs_df['aerial_won']>0)].groupby(['player_name'])['aerial_won'].count()   
    
    clear = (cfs_df[(cfs_df['event_type_name']=='Clearance')]
        .groupby(['player_name'])['player_name'].count())
    
#     # create df    
    df = pd.concat([pass_complete,pass_incomp,pressures,fouls,
                    tackles,intercepts,aerials,clear],axis=1)
    df.columns = ['pass_comp','pass_incomp','pressures','fouls_won',
                 'tack','int','aerials_won','clearances']
    df['pass_%'] = (df['pass_comp']/(df['pass_incomp']+df['pass_comp']))*100
    
    df = df.fillna(0)
    
    df = df[['pass_%','pressures','fouls_won',
                 'tack','aerials_won','clearances']]
    
    return round(df,2)

def team_kpi(all_events):
    """
    calulate kpis for each team across the whol match
    
    Arg
    ------
    all_events : all_events df
    
    Out
    -------
    df : pandas df
    
    """
    
    teams_df = all_events[((all_events['team_name']=='Fleetwood Town')
                 |(all_events['team_name']=='Wycombe Wanderers'))]
    
    # calculate kpis
    pressures = (teams_df[(teams_df['event_type_name']=='Pressure')].
         groupby(['team_name'])['event_type_name'].count())

    crosses = (teams_df[(teams_df['event_type_name']=='Pass')&
                     (teams_df['pass_cross']==True)].
             groupby(['team_name'])['event_type_name'].count())

    # passes carries dribbles into final 3rd
    deep_prog = (teams_df[(teams_df['event_type_name']=='Pass')
                        |(teams_df['event_type_name']=='Dribble')
                       |(teams_df['event_type_name']=='Carries')
                       &(teams_df['location_x']>=80)].
             groupby(['team_name'])['event_type_name'].count())

    pass_complete =  (teams_df[(teams_df['event_type_name']=='Pass')&
                     (teams_df['outcome_name'].isnull())].
             groupby(['team_name'])['event_type_name'].count())

    pass_incomp = (teams_df[(teams_df['event_type_name']=='Pass')&
                     (teams_df['outcome_name']=='Incomplete')].
             groupby(['team_name'])['event_type_name'].count())

    xg = teams_df.groupby(['team_name'])['xg'].sum()

    shots = teams_df[teams_df['event_type_name']=='Shot'].groupby(['team_name'])['event_type_name'].count()

    box_touches = teams_df[(teams_df['location_x']>=99.6)
      &(teams_df['location_y']>=17.67)
      &(teams_df['location_y']<=65.75)
      &(teams_df['event_type_name']!='Pressure')].groupby(['team_name'])['team_name'].count()
    
    
    # combine kpis
    df = pd.concat([xg,shots,box_touches,pressures,deep_prog,crosses,pass_complete,pass_incomp],axis=1)
    df.columns = ['xg','shots','box_touches','pressures','deep prog','crosses','pass comp','pass incomp']

    df['shot_touch%'] = (df['shots']/df['box_touches'])*100
    df['xg/shot'] = df['xg']/df['shots']
    df['pass%'] = (df['pass comp']/(df['pass comp']+df['pass incomp']))*100
    
    df = round(df[['xg','shots','xg/shot','box_touches','shot_touch%','deep prog'
          ,'crosses','pressures','pass%']].transpose(),2)
    
    return df