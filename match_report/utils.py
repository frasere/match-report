import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def statsbomb_pitch_plot(w,h,opacity=0.7):
    """
    Plot football pitch using 120x80 Statsbomb dimensions
    https://github.com/statsbomb/statsbombpy
    y coordinates in data must be negated (0,0 is top left of pitch)
    
    Args
    w : width of plot (inches)
    h : height of plot (inches)
    
    Return
    fig,ax
    """
    
    
    fig,ax = plt.subplots(figsize=(w,h))
    #Pitch Outline & Centre Line
    _=ax.plot([0,0],[0,80], color="black",alpha=opacity) # left touchline
    _=ax.plot([0,120],[0,0], color="black",alpha=opacity) # top touchline
    _=ax.plot([120,120],[0,80], color="black",alpha=opacity) # right touchline
    _=ax.plot([0,120],[80,80], color="black",alpha=opacity) # bottom touchline
    _=ax.plot([60,60],[0,80], color="black",alpha=opacity) # centre line

    #Left Penalty Area
    _=ax.plot([0,18],[18,18],color="black",alpha=opacity) # top
    _=ax.plot([0,18],[62,62],color="black",alpha=opacity) #  bottom
    _=ax.plot([18,18],[18,62],color="black",alpha=opacity)

    #Right Penalty Area
    _=ax.plot([102,120],[18,18],color="black",alpha=opacity)
    _=ax.plot([102,102],[18,62],color="black",alpha=opacity)
    _=ax.plot([102,120],[62,62],color="black",alpha=opacity)

    #Left 6-yard Box
    _=ax.plot([0,6],[30,30],color="black",alpha=opacity)
    _=ax.plot([6,6],[30,50],color="black",alpha=opacity)
    _=ax.plot([0,6],[50,50],color="black",alpha=opacity)

    #Right 6-yard Box
    _=ax.plot([114,120],[30,30],color="black",alpha=opacity)
    _=ax.plot([114,114],[30,50],color="black",alpha=opacity)
    _=ax.plot([114,120],[50,50],color="black",alpha=opacity)

    #Prepare Circles
    centreCircle = plt.Circle((60,40),12,color="black",fill=False,alpha=opacity)
    centreSpot = plt.Circle((60,40),0.5,color="black",alpha=opacity)
    leftPenSpot = plt.Circle((12,40),0.5,color="black",alpha=opacity) # penspot
    rightPenSpot = plt.Circle((108,40),0.5,color="black",alpha=opacity) # penspot

    #Draw Circles
    _=ax.add_patch(centreCircle)
    _=ax.add_patch(centreSpot)
    _=ax.add_patch(leftPenSpot)
    _=ax.add_patch(rightPenSpot)

    _=ax.set_axis_off()
    
    return fig,ax


def cumulative_event_line(events,hist_bins,figsize,colour):
    """
    plot cumulative event line across pitch dimensions
    
    Arg
    --------
    events : pandas df
    hist_bins : tuple (int,int)
    figsize : tuple (int,int) #in inches
    colour : string (matplot.cmap args)
    
    Return
    ---------
    fig
    
    """
    
    #  press count frequency
    press_counts = np.sum(np.histogram2d(events["location_x"],
                                         events["location_y"],
                                         bins=hist_bins)[0],
                          axis=1)
    
    total_press_counts = np.hstack((0,press_counts)) # add in zero at start
    
    
    # bin edges (locations on the pitch)
    press_zones = np.histogram2d(events["location_x"],
                                 events["location_y"],
                                 bins=hist_bins)[1]

    # df of locations and frequency
    presses = pd.DataFrame([total_press_counts,press_zones])
    
    # plot
    fig,ax = plt.subplots(figsize=figsize)
    _=ax.plot(presses.iloc[1,:],presses.iloc[0,:],c=colour)
    _=ax.set(xlim=[0,120])
    _=ax.plot([60,60],[0,np.amax(total_press_counts)],ls='--',c='k')
    _=plt.annotate('Halfway',(61,4),rotation=90)
    _=sns.despine()
    
    return


def event_2dhist(events,hist_bins,colour):
    """
    plot 2d histogram across pitch dimensions
    
    Arg
    --------
    events : pandas df
    hist_bins : tuple (int,int)
    colour : string (matplot.cmap args)
    
    Return
    ---------
    fig
    
    """
    
    _=plt.hist2d(events["location_x"],
             events["location_y"],
             bins=hist_bins,
            cmin = 1,  #sets below 0 to white 
            cmap=colour) 
    _=plt.ylim([0,80])
    _=plt.xlim([0,120])
    _=plt.colorbar()
    
    return


def radar_plot(data,player1,player2):
    
    # ------- PART 1: Create background
    # number of variable
    categories=list(data)
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    #_=plt.yticks(np.percentile(data,[20,40,60,80,100]),['20%','40%','60%','80%','100%'],color="k",size=7) 

    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values=data.loc[player1,:].values.tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=player1)
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values=data.loc[player2,:].values.tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=player2)
    ax.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    _=plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1)) #
    
    return ax



def pass_network(df):
    """
    return pass network data points
    uses average touches for player locations
    completed passes for pass links
    input df for a team and half (not sure would make sense for whole game)
    
    Arg
    -----------
    df : df of events for a team
    
    """
    
    # team name and plyrs
    team_name = list(df['possession_team_name'].unique())
    lineup = list(df['player_name'].unique())
    
    # ave location of plyrs (based on touches)
    touch_events = ['Pass','Ball Receipt*','Carries','Shot','Ball Recovery','Clearance','Block',
               'Goal Keeper','Miscontrol','Dribble','Interception']
    touches = df[df['event_type_name'].isin(touch_events)]
    player_locs = touches.groupby('player_name')[['location_x','location_y']].mean()
    
     # completed passes
    team_pass = df[(df['event_type_name']=='Pass')&
                   (df['outcome_name'].isnull())]
    # for given players
    player_pass = team_pass[team_pass['player_name'].isin(lineup)]
    
    # x and y average locations of complete passes made
    x_ave = (
        player_pass.groupby(['player_name'])['location_x'].sum()
        /player_pass.groupby(['player_name'])['location_x'].count()
    )

    y_ave = (
        player_pass.groupby(['player_name'])['location_y'].sum()
        /player_pass.groupby(['player_name'])['location_y'].count()
    )
    
    # create the df of passes made and counts
    players = []
    for i in lineup:
        players.append(player_pass[player_pass['player_name']==i]
                       .groupby(['player_name','pass_recipient_name'])['pass_recipient_name'].count())
        
    list_dfs = []
    for i in range(len(players)):
        list_dfs.append(pd.DataFrame(players[i]))
        list_dfs[i].columns = ['passes']
        list_dfs[i] = list_dfs[i].reset_index()

    passes_df = pd.concat(list_dfs)
    
    # add locations into pass df
    for i in x_ave.index:
        passes_df.loc[(passes_df['player_name']==i),'x start (ave)']= x_ave[i]
        passes_df.loc[(passes_df['player_name']==i),'y start (ave)']= y_ave[i]
        passes_df.loc[(passes_df['pass_recipient_name']==i),'x end (ave)']= x_ave[i]
        passes_df.loc[(passes_df['pass_recipient_name']==i),'y end (ave)']= y_ave[i]
        passes_df.loc[(passes_df['player_name']==i),'x loc (ave)']= player_locs.loc[i]['location_x']
        passes_df.loc[(passes_df['player_name']==i),'y loc (ave)']= player_locs.loc[i]['location_y']
    
    
    
    return passes_df.reset_index(drop=True)







