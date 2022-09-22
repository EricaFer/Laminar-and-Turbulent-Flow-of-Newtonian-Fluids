import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy.optimize import fsolve,minimize_scalar
import numpy as np

relativeRugosity = [0.00001,0.0001,0.0004,
                    0.0008,0.002,0.006,0.01,
                    0.02,0.03,0.04,0.05]

def f_laminar(reynolds):
    return 64/reynolds

def f_turbulent(f,rugosity,reynolds):

    firstTerm = rugosity/3.7
    secondTerm = 2.51/(reynolds*np.sqrt(f))

    # Solving Colebrook's equation (non linear)
    return -2.0*np.log10(firstTerm+secondTerm)-1/np.sqrt(f)


def plotPoints():

    X = []
    Y = []

    laminarX = [x for x in range(700,2300,50)]
    laminarY = []

    print('\nCalculating Laminar Flow\n')

    for reynolds in range(700,2300,50):
        
        laminarY.append(f_laminar(reynolds))

    X.append(laminarX)
    Y.append(laminarY)

    print('Laminar Flow was just calculated!\n')


    print('Calculating Turbulent Flow\n')

    turbulentX = [x for x in range(2300,10**8,10**7)]

    for rugosity in relativeRugosity:
        
        turbulentY = []

        for reynolds in range(2300,10**8,10**7):

            f0 = fsolve(f_turbulent,x0= 0.0003,args = (rugosity,reynolds))

            f = np.around(f0,decimals=3)

            turbulentY.extend(f)

        X.append(turbulentX)
        Y.append(turbulentY)

    print('Turbulent Flow was just calculated\n')

    return X,Y

def plotImage(X,Y):

    print('Plotting Image\n')

    fig,ax = plt.subplots(figsize = (12,7))

    pal = sns.color_palette("hls", len(relativeRugosity)+1)

    color_list = pal.as_hex()

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

    for i in range(0,len(X)):

        plt.plot(X[i],Y[i],color = color_list[i])

    for i, rugosity in enumerate(relativeRugosity):

        ax.text(2.5*10**7, Y[i+1][-1] + 0.001, r'$\epsilon/d={}$'.format(rugosity),
                verticalalignment='bottom', horizontalalignment='left')

    plt.xscale('log')
    plt.yscale('log')

    plt.axvspan(2300, 4000, facecolor='gainsboro', alpha=0.5) 

    plt.grid(which='major', linestyle='--', linewidth='1.0', color='k') 
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='k') 

    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.ScalarFormatter())  

    plt.autoscale(enable=True, axis='both')
    plt.minorticks_on

    plt.title(
        'Moody Diagram',
        fontsize=22,
        y = 1.01)

    plt.xlabel(
        r'Reynolds Number, $Re = \frac{V d \rho}{\mu}$',
        fontsize= 18)

    plt.ylabel('Friction Factor, f',fontsize= 16)

    ax2 = ax.twinx()

    ax2.set_ylabel(r'$\frac{\epsilon}{d}$ = Relative Rugosity',
                    fontsize=16,
                    x = 1.3)

    ax2.set_yticks([])

    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(which = 'minor',axis='y', labelsize=13)
    ax.tick_params(which = 'major',axis='y', labelsize=16)

    plt.annotate('Laminar Flow\nf = 64/Re', (7.2*10**2,0.46),fontsize=13) 

    plt.annotate('Transition Zone\n 2,300 <  Re < 4,000', (1.18* 10 ** 3, 0.33),fontsize=13)

    ax.set_xlim(6*10**2,10**8)
    #ax.set_ylim(0,0.1)

    plt.show()

    fig.savefig(f'./images/moody_diagram.png',bbox_inches='tight');