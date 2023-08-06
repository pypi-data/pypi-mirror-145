#!/usr/bin/env python3

import scipy.integrate as integrate


################################
# i need interpolation now.... #
#https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np


import urllib3
from bs4 import BeautifulSoup

from fire import Fire

import re


# ----------- z correspond the name
elements=['n','H','He','Li','Be','B','C','N','O','F','Ne',
                        'Na','Mg','Al','Si','P','S','Cl','Ar',
                        'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',  'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
                        'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
                        'Cs', 'Ba',
                        'La','Ce','Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu','Hf',
                        'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
                        'Po', 'At', 'Rn', 'Fr','Ra', 'Ac',  'Th', 'Pa', 'U',
                        'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                        'Fm', 'Md', 'No', 'Lr','Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
                        'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']; #110-118

# --------- name corresponds the list of stables
# stable_isotopes[ elements[6] ]  # will also give 14C etc...
stable_isotopes={ "H":[1,2,3],
"He":[3,4],
"Li":[6,7],
"Be":[9],
"B":[10,11],
"C":[12,13,14],
"N":[14,15],
"O":[16,17,18],
"F":[19],
"Ne":[20,21,22],
"Na":[23,22],
"Mg":[24,25,26],
"Al":[27],
"Si":[28,29,30],
"P":[31],
"S":[32,33,34,36],
"Cl":[35,37,36],
"Ar":[36,38,40,39],
"K":[39,40,41],
"Ca":[40,42,43,44,46,48,41],
"Sc":[45],
"Ti":[46,47,48,49,50],
"V":[50,51],
"Cr":[50,52,53,54],
"Mn":[55,53],
"Fe":[54,56,57,58],
"Co":[59,60],
"Ni":[58,60,61,62,64],
"Cu":[63,65],
"Zn":[64,66,67,68,70],
"Ga":[69,71],
"Ge":[70,72,73,74,76],
"As":[75],
"Se":[74,76,77,78,80,82,79],
"Br":[79,81],
"Kr":[78,80,82,83,84,86,85],
"Rb":[85,87],
"Sr":[84,86,87,88],
"Y":[89],
"Zr":[90,91,92,94,96],
"Nb":[93],
"Mo":[92,94,95,96,97,98,100],
"Tc":[98,97,99],
"Ru":[96,98,99,100,101,102,104],
"Rh":[103],
"Pd":[102,104,105,106,108,110],
"Ag":[107,109],
"Cd":[106,108,110,111,112,113,114,116],
"In":[113,115],
"Sn":[112,114,115,116,117,118,119,120,122,124],
"Sb":[121,123,125],
"Te":[120,122,123,124,125,126,128,130],
"I":[127,129],
"Xe":[124,126,128,129,130,131,132,134,136],
"Cs":[133,134,135,137],
"Ba":[130,132,134,135,136,137,138,133],
"La":[138,139,137],
"Ce":[136,138,140,142],
"Pr":[141],
"Nd":[142,143,144,145,146,148,150],
"Pm":[145,146,147],
"Sm":[144,147,148,149,150,152,154,151],
"Eu":[151,153,152,154,155],
"Gd":[152,154,155,156,157,158,160],
"Tb":[159,157,160],
"Dy":[156,158,160,161,162,163,164],
"Ho":[165],
"Er":[162,164,166,167,168,170],
"Tm":[169,171],
"Yb":[168,170,171,172,173,174,176],
"Lu":[175,176,173,174],
"Hf":[174,176,177,178,179,180],
"Ta":[180,181],
"W":[180,182,183,184,186],
"Re":[185,187],
"Os":[184,186,187,188,189,190,192],
"Ir":[191,193],
"Pt":[190,192,194,195,196,198],
"Au":[197],
"Hg":[196,198,199,200,201,202,204],
"Tl":[203,205,204],
"Pb":[204,206,207,208],
"Bi":[209,207],
"Po":[208,209,210],
"At":[210,211],
"Rn":[210,211,222],
"Fr":[212,222,223],
"Ra":[226,228],
"Ac":[225,227],
"Th":[230,232,229],
"Pa":[231,233],
"U":[233,234,235,238,236],
"Np":[236,237],
"Pu":[238,239,240,241,242,244],
"Am":[241,243],
"Cm":[243,244,245,246,247,248],
"Bk":[247,249],
"Cf":[249,250,251,252],
"Es":[252,254],
"Fm":[253,257],
"Md":[258,260],
"No":[255,259],
"Lr":[261,262],
"Rf":[265,267],
"Db":[268,270],
"Sg":[269,271],
"Bh":[270,274],
"Hs":[269,270],
"Mt":[276,278],
"Ds":[280,281],
"Rg":[281,282],
"Cn":[283,285],
"Nh":[285,286],
"Fl":[287,288,289],
"Mc":[288,289,290],
"Lv":[291,292,293],
"Ts":[293,294],
"Og":[294] }


def plot_spline( ax, tckslist , Emax=40, label="label" ,  clear=False):
    """
    plots the list of data: [x,y] label
    """
    mymin=1
    for tcks2 in tckslist:
        tcks=tcks2[0]
        label=tcks2[1]
        if tcks is None:
            continue
        mymin = min( mymin, tcks[1].min() ) # minimum for yaxis
        #print( tcks )
        #print( type(tcks) )

        if label[-1]=="m":
            ax.plot( tcks[0], tcks[1],'-.',label=label)
        else:
            ax.plot( tcks[0], tcks[1],'-',label=label)

        # Emin=min(tcks.x) # MeV
        # # Emax=max(tcks.x) # MeV

        # unew = np.arange( Emin, Emax, 0.0001)
        # out=tcks(unew)

        # #out = interpolate.splev(unew, tcks, der=0)
        # #xnew = np.linspace(x[0], x[-1], num=10000 , endpoint=True )
        # #ynew = interpolate.splev(xnew, tcks, der=0)
        # #plt.plot( x,y , '.', xnew, ynew ,'-' )
        # plt.plot(  unew, out ,'-' , label=label)

        ax.legend( fontsize=8)

    plt.yscale("log")
    plt.ylim( max( [1e-2, mymin ]) )
    plt.xlim( [0, Emax] )
    plt.grid()
    #plt.show()



def get_tendl( proj, targ, product,  plot=False , kind="linear" , xsset="tot" , Emax = 40 ):
    url="https://tendl.web.psi.ch/tendl_2017/proton_html/Mg/ProtonMg26residual.html"

    if proj=="h1": p1="proton"
    if proj=="h2": p1="deuteron"
    if proj=="h3": p1="triton"
    if proj=="he3": p1="he3"
    if proj=="he4": p1="alpha"


    LABEL = "TENDL19_"+targ+"("+proj+",x)"+product

    t=targ.capitalize()
    r=product.capitalize()
    t2,t3,r2,r3="","","",""


    # extension="tot"
    extension=xsset # normally total

    # ============================= Groundstate or Isomer ==== GET EXTENSION
    if r[-1]=='g':
        extension = "L00"
        r = r[:-1]

    # ------ ISOMER ----------- someimes L01, L10, L03
    if r[-1] == 'm':
        extension = "isomer"
        r=r[:-1]

    #=====target create zeroes mg26 -> Mg026  ---> tzero
    for i in range(len(t)):
        if not t[i].isdigit():
            t2=t2+ t[i]
        else:
            t3=t3+ t[i]
        #print( i,t[i], t[i].isdigit() )
    tzero="{}{}".format( t2,t3.zfill(3) ) #zerofill
    #print(t, t2, t3)


    #=== product/residual ========= -> r
    for i in range(len(r)):
        if not r[i].isdigit():
            r2=r2+ r[i]
        else:
            r3=r3+ r[i]
        #print( i,r[i], r[i].isdigit() )
    r="{}{}".format( r2,r3.zfill(3) ) #zerofill
    #print(r, r2, r3)


    #================= Find Z Of Element  -> rZ
    if t2 in elements:
        tZ=elements.index(t2)
    else:
        print("X... no such element",t2)
        quit()
    if r2 in elements:
        rZ=elements.index(r2)
    else:
        print("X... no such element",r2)
        quit()

    # ============================= Groundstate or Isomer ==== GET EXTENSION
    if extension == "isomer":

        rname = "rp{}{}.L".format(  str(rZ).zfill(3), r3.zfill(3)  )

        # https://tendl.web.psi.ch/tendl_2019/proton_html/Fe/ProtonFe54residual.html

        # url="https://tendl.web.psi.ch/tendl_2019/{}_file/{}/{}/tables/residual/{}".format( p1 , t2, t , rname )
        url="https://tendl.web.psi.ch/tendl_2019/{}_html/{}/{}{}residual.html".format( p1 , t2, p1.capitalize(), t.capitalize() )
        #print(url)
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data.decode('utf-8'), "lxml")
        links = [item['href'] if item.get('href') is not None else item['src'] for item in soup.select('[href^="http"], [src^="http"]') ]
        #print(links)
        possible_extensions = []
        for l in links:
            if (l.find(rname)>=0) and (l[-4:]!=".ave") and (l[-4:]!=".L00"):
                extension = l[-3:]
                #print("i... ",l, extension)
                possible_extensions.append(extension)
        if len(possible_extensions)>1:
            print("X... there are more isomers - I QUIT")
            quit()
        #for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        #    print( link.get('href') )
        #tab= soup.get_text().strip().split("\n")
        #print(tab)

        #if "".join(tab).find("404 Not Found")>=0:
        #    print("X...  {} NOT FOUND  ".format( url ) )

        # quit()

    # https://tendl.web.psi.ch/tendl_2019/proton_file/Fe/Fe054/tables/residual/rp026052.L05

    rname = "rp{}{}.{}".format(  str(rZ).zfill(3), r3.zfill(3) , extension )
    url="https://tendl.web.psi.ch/tendl_2019/{}_file/{}/{}/tables/residual/{}".format( p1 , t2, tzero , rname )

    # url="https://tendl.web.psi.ch/tendl_2017/{}_file/{}/{}/tables/residual/rp{}{}.{}".format( p1 , t2, t , str(rZ).zfill(3), r3.zfill(3) , extension )
    # url="https://tendl.web.psi.ch/tendl_2017/proton_file/Mg/Mg026/tables/residual/rp008016.tot"
    #print("i... WWW: ",url)

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), "lxml")
    tab= soup.get_text().strip().split("\n")
    #print(tab)
    if "".join(tab).find("404 Not Found")>=0:
        print("X... {} TENDL: reaction {} NOT FOUND in  TENDL ; ".format( LABEL, rname) )
        return None, LABEL
        quit()



    Ethrs = [ i for i in tab if i.find("E-threshold")>0 ][0].split("=")[1].strip()
    Ethrs = float( '%.2f'%(float(Ethrs)) )
    if Ethrs >= Emax:
        print("X... {} treshold too high = {}".format(LABEL, Ethrs) )
        return None, LABEL

    tab=[x for x in tab if x.find("#")<0]
    #print(tab)
    #r=[x.extract() for x in soup.findAll('p')]
    #print(r[0])
    excit={}
    Elowest = 200
    for t in tab:
        # ------ I kill all bellow some XS
        if float(t.split()[1])>1e-7:
            excit[ float(t.split()[0]) ] = float(t.split()[1])
            if Elowest > float(t.split()[0]):
                Elowest = float(t.split()[0])
    if Elowest >= Emax:
        print("X... {} Elowest too high = {}".format( LABEL, Elowest) )
        return None, LABEL

    x= np.asarray( list(excit.keys()) ,   dtype=np.float32)
    y= np.asarray( list(excit.values()) , dtype=np.float32)



    # INTERP1D : gives the object with .x  .y and info howto manage
    #tcks = interpolate.interp1d( x, y ,kind="linear" )  #  FUNCTION
    #tcks = interpolate.interp1d( x, y ,kind="cubic" )  #  FUNCTION

    tcks = interpolate.interp1d( x, y ,kind=kind )  #  FUNCTION
    tcks = [x,y]
    #
    #  SPLREP - it creates   TUPLE OF ARRAYS and needs SPLEV to DRAW
    # SPLREP find hte BSPLINE,  SPLEV evaluates from knots and repres.
    #tcks2 = interpolate.splrep( x, y, s=0 )  # SPLINE FUNCTION
        #print(tcks2)
    #
    if plot:
        plot_spline( [tcks] , label="Exc.Fun." )

    print("D... reaction: {} ... threshold/lowest: {}/{} MeV    data length: {}".format(LABEL, Ethrs, Elowest, len(tcks[0])  ) )
    return [tcks, LABEL ]  # interpolated function





def plot_a_z( proj='h1', targ='fe56', prod_a=[49,59], prod_z=[22,28], exclude_stable = False):
    curves=[]

    fe={54:5.8, 56:91.7, 57:2.12, 58:0.28 }

    plt.switch_backend('Agg')
    plt.ioff()

    Emax = 35
    for a in range( *prod_a ):
        print("_"*50, "Z=",a)

        fig,ax = plt.subplots()
        curves = []

        for z in range( *prod_z ):
            final_or = elements[z]+str(a) # this is for TENDL


            if exclude_stable:
                # exclude stable isotopes:
                radio = True
                for i in stable_isotopes[ elements[z] ]:  # will also give 14C etc...
                    if i == a:
                        radio = False # IS STABLE

                if not radio:
                    print("X  {} .... STABLE .... ".format(final_or) )
                    continue

            final=final_or
            curves.append( get_tendl( proj,targ, final  , Emax = Emax, kind="cubic" ) )

            final=final_or+"g"
            curves.append( get_tendl( proj,targ, final  , Emax = Emax, kind="cubic" ) )

            final=final_or+"m"
            curves.append( get_tendl( proj,targ, final  , Emax = Emax, kind="cubic" ) )

            #ifun1=get_tendl( "h1", "fe56", "fe53"  , kind="cubic" )
            #curves.append( ifun1 )

        LABEL2 = "exc_TENDL19_"+targ+"("+proj+",x)X"+str(a)
        print("_"*50, " plotting - clearing ", LABEL2)
        plot_spline( ax, curves , Emax = Emax, clear = True)

        plt.savefig(LABEL2+".png")
        plt.cla()
        plt.clf()
        plt.close(fig)



if __name__ == "__main__":
    print("D... only az works now..... if you tune")
    Fire( {"az":plot_a_z,
           "ps":plot_spline} )
    #ifun1=get_tendl( "h1", "mg26", "al26"  , kind="cubic" )
    #ifun2=get_tendl( "h1", "mg26", "al26g"  ,kind="cubic")
    #ifun3=get_tendl( "h1", "mg26", "al26m"  ,kind="cubic")
