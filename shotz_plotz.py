'''
    ***** shotz_plotz.py *****

Plot data in DE1+ shot files (stored in de1plus/history folder).

Usage: python shotz_plotz.py file1.shot file2.shot ...      (wildcards OK)

Note: requires Python matplotlib.pyplot (pip install matplotlib)

Author: John M. Weiss, Ph.D.
Written 181009.

Modifications:
191111 - Modify shot_plot.py to plot multiple extractions on the same graph.
         Currently plots only pressure, flow, weight.
191120 - Minor cleanups for posting on Decent Diaspora.
'''

import sys, math, glob
import matplotlib.pyplot as plt

def process_data( lines ):
    ''' process_data( lines ): extract shot data and store in matrix '''

    # process shot file lines, one at a time
    headers = [ 'espresso_elapsed', 'espresso_pressure', 'espresso_weight', 'espresso_flow', 'espresso_flow_weight', 'espresso_temperature_basket', 'espresso_temperature_mix' ]
    data = []
    for line in lines:
        # eliminate non-data lines
        if '{' not in line: continue
        line = line.replace( '{', '' )
        line = line.replace( '}', '' )
        line = line.split()
        if len( line ) == 0: continue
        if line[0] not in headers: continue

        # store data lines in matrix
        data.append( line )

    # extract labels, convert strings to floats
    labels = [row[0] for row in data]
    values = []
    for r in data:
        values.append( [float(c) for c in r[1:]] )
    return labels, values

def get_shot_data( filename ):
    ''' get_shot_data( filename ): read DE1 shot data from file'''

    # open input file and read extraction data
    try:
        fin = open( filename )
        lines = fin.readlines()
        fin.close()
    except IOError:
        print( "Unable to open file:", filename )
        # sys.exit( -2 )
        return None, None

    # store shot data in matrix
    return process_data( lines )

def data_plot( labels, values ):
    ''' data_plot( labels, values ): generate scatter plot using matplotlib.pyplot '''

    # divide temperatures (C) by 10, so similar range as pressure
    for c in range( len( values[-1] ) ): values[-1][c] /= 10
    for c in range( len( values[-2] ) ): values[-2][c] /= 10

    # divide espresso_weight by 10, so similar range as pressure
    for c in range( len( values[2] ) ): values[2][c] /= 10

    # double flow rate? prolly not a good idea
    # for c in range( len( values[3] ) ): values[3][c] *= 2
    # for c in range( len( values[4] ) ): values[4][c] *= 2

    # plot temp, pressure, flow rate, flow weight, shot weight
    legend = ( 'time', 'pressure (bar)', 'shot weight (g)', 'flow rate (ml/s)', 'flow weight (g/s)', 'basket temp (C)', 'mix temp (C)' )
    colors = ( 'k', '#00B040', 'tab:orange', '#4060FF', 'tab:brown', '#DF0000', 'y' )
    vmax, tlen = 0, len( values[0] )
    for i in ( 1, 3, 4 ):
        vlen = min( tlen, len( values[i] ) )    # check for extra time steps
        plt.plot( values[0][0:vlen], values[i][0:vlen], color = colors[i] )
        # plt.plot( values[0][0:vlen], values[i][0:vlen], color = colors[i], label = legend[i] )
        vmax = max( vmax, max( values[i][0:vlen] ) ) # max y value
    plt.ylim( 0, math.ceil( vmax ) )

def main( argv ):
    ''' main( argv ): fake a main() function '''

    # process command-line arguments
    if len( sys.argv ) < 2:
        print( "Usage: python shotz_plotz.py file1.shot file2.shot ..." )
        sys.exit( -1 )

    # for each file
    for arg in sys.argv[1:]:
        for fname in glob.glob( arg ):
            # get shot data
            print( 'Processing file', fname )
            labels, values = get_shot_data( fname )
            if labels == None or values == None: continue

            # plot data
            data_plot( labels, values )

    # add plot decorations
    plt.grid()
    plt.title("DE1 Shot Plot")
    plt.legend()
    plt.xlabel('elapsed time (sec)')
    plt.ylabel('pressure, flow')

    # display plot
    plt.show()

# fake a main function call
main( sys.argv )
