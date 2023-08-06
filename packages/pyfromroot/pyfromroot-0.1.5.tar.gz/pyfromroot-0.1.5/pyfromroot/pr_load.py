#!/usr/bin/env python3

import ROOT
import numpy as np
from array import array
import random
import os
import pandas as pd

from fire import Fire

#import prun # looks like mutual import, but it is not really
from  pyfromroot import prun

import ROOT
import time
#   the DAT file can contain TAGS:
#   #COLNAME: frame,x,y     ... column names (selfexplaining)
#   #LOAD_AS: x,dx,y,dy     ... order of columns  for x,y,dx,dy TGraph(Errors)
#


def create_histo(df, hpos):
    x = np.array(  df[ df.columns[hpos] ]  ,  np.float64)
    h = ROOT.TH1F( "h", "h", len(df), 0, len(df) )
    bn = 0
    for bc in x:
        bn+=1
        h.SetBinContent(  bn, bc )
    return h


def main( *args ):

    print(f"i... @load: args={args}")
    if len(args)==0:
        print("X... no file given")
        return

    fname = args[0]
    if not os.path.exists( fname ):
        print(f"X... data file {fname} not found")
        return


    # - argument has a priority above LOAD_AS .......................
    xynames = None
    if len(args)>1:
        print("d... argument for xy was sent...")
        # this must be the order:  xynames
        xynames = args[1]
        if type(xynames) is tuple: # in case of commandline operation
            #print("X... tuple")
            xynames = ",".join(xynames)
        xynames = xynames.split(",")
        print(f"i... order of columns is f{xynames}")

    else:
        print("D... ok, no argument that would take a priority")


    # - LOAD_AS x,y,dx,dy CODES for columns and COLNAMES inside the file ---
    #  and handle the priority of ARGS xydxdy ..............
    names = []
    if xynames is None: xynames = []
    columns = 0
    with open(fname) as f:
        print("i... looking the file for COLNAMES: and LOAD_AS:")
        i = 0
        for com in f:
            com = com.strip()
            print(com)
            i+=1
            if i>10: break
            com=com.strip()
            if com.find("#")!=0:
                columns = len(com.split())
            if com.find("#COLNAME:")==0:
                names2 = com.split(":")[1].strip().split(",")
                names = names2

            if com.find("#LOAD_AS:")==0:
                # overrides?
                names2 = com.split(":")[1].strip().split(",")
                if (len(names2)>1)and( 'x' in names2)and('y' in names2): # x,y at least
                    if len(xynames)==0:
                        xynames = names2



    # ------ I may have names(column names) and xynames(the load order)

    # here I do the correct number of columns - BUTBUT later I do the same....
    while len(xynames)<columns:
        xynames.append(f"c_{len(xynames)}")

    for i in range(len(xynames)):
        if xynames[i]=="_":xynames[i]=f"col_{i}"


    if len(names)==0: names=xynames
    if len(names)!=len(xynames): names=xynames



    #
    # HERE, all column names should be defined, if available
    # Order is defined by now
    #
    print("i... existing columns = ", columns)
    print("i... COLNAME:",names)
    print("i... LOAD_AS:" ,xynames)
    #print(names,xynames)


    # --- -if something is missing - quit
    histo = False
    if not( ('x' in xynames)and('y' in xynames) ):
        if not( ('h' in xynames) ):
            print("X... no <x> OR no <y> given; neither <h> for histogram" )
            print("X... try  x,y,dx,dy  or y,x ...." )
            return
        else:
            histo = True


    # count columns first to be sure it matches the names ;ADD fake colnames
    df = pd.read_csv(fname, delimiter="\s+", header=None, comment="#", nrows=2)
    i=1
    while len(names) <  df.shape[1]:
        names.append(f"col{i:d}")
        i+=1

    print("TRYING TO SUGGEST............")
    print(df)

    if len(names)!=df.shape[1]:
        print(f"X... column probl: names={len(names)} i={i} dfcols={df.shape}" )

    # read all data now; column names are from COLNAMES or xynames(if not def)
    df = pd.read_csv(fname, delimiter="\s+", header=None, comment="#", names = names )
    print(df)

    #
    # HERE THE DF SHOULD BE PERFECTLY LOADED with colnames, defined x,y, maybe++
    #

    # ------ graph name in CLING
    NAME1 = os.path.splitext(fname)[0]
    print(f"D... graph name = {NAME1}")



    #------------------------------ HISTO OR GRAPH --------------
    if histo:
        hpos = xynames.index('h')
        print(f"i... h position {hpos}")
        print(f"i... hname= {names[hpos]} ")
    else:
        xpos = xynames.index('x')
        ypos = xynames.index('y')
        print(f"i... x position {xpos}  y position {ypos}")
        print(f"i... xname= {names[xpos]}  yname= {names[ypos]}")


    if histo:
        g = create_histo(df, hpos)
        g.Draw()
        g.SetTitle(f"{NAME1};channel;{names[hpos]}")
        ROOT.gPad.SetLogy()
        g.Print()

    else:

        x = np.array(  df[ df.columns[xpos] ]  ,  np.float64)
        y = np.array(  df[ df.columns[ypos] ]  ,  np.float64)

        #
        # check if dx and/or dy  given
        #

        if ('dx' in names)and('dy' in names):
            dxpos = xynames.index('dx')
            dypos = xynames.index('dy')
            dx = np.array(  df[ df.columns[dxpos] ]  ,  np.float64)
            dy = np.array(  df[ df.columns[dypos] ]  ,  np.float64)
            g = ROOT.TGraphErrors( len(x) , x.flatten("C"), y.flatten("C"), dx.flatten("C"), dy.flatten("C") )
        elif ('dx' in names):
            dxpos = xynames.index('dx')
            dx = np.array(  df[ df.columns[dxpos] ]  ,  np.float64)
            dy = np.zeros_like(y)
            g = ROOT.TGraphErrors( len(x) , x.flatten("C"), y.flatten("C"), dx.flatten("C"), dy.flatten("C") )
        elif ('dy' in names):
            dypos = xynames.index('dy')
            dy = np.array(  df[ df.columns[dypos] ]  ,  np.float64)
            dx = np.zeros_like(x)
            g = ROOT.TGraphErrors( len(x) , x.flatten("C"), y.flatten("C"), dx.flatten("C"), dy.flatten("C") )
        else:
            g = ROOT.TGraph( len(x) , x.flatten("C"), y.flatten("C") )

        #
        # PLOT
        #  xpos and ypos are for axis labels
        #
        #g.Print()
        # plot nicely on (maybe new) TCanvas
        g.SetMarkerStyle(7) # small circle , no lines...
        g.SetMarkerStyle(1) # small circle , no lines...
        g.SetMarkerStyle(22) # small...
        g.SetTitle(f"{NAME1};{names[xpos]};{names[ypos]}")
        g.Draw("PAW") # no lines...

    # ------------------------------ END OF GRAPH / HISTO ---------------
    ROOT.gPad.SetGrid()
    prun.register(g,NAME1)
    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    return

if __name__=="__main__":
    Fire(main)
    print("H... close canvas to exit...")
    while ROOT.addressof(ROOT.gPad)!=0:
        time.sleep(0.2)
    #input('press ENTER to end...')
