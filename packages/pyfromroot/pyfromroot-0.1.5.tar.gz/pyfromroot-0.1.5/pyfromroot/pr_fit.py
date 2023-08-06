#!/usr/bin/env python3

import ROOT
import numpy as np
from array import array
import random
import os
import pandas as pd


from fire import Fire
import importlib # dynamic import

import sys # to unload

from pyfromroot import prun   # this seems like mutual import, but it is not really

# ------------------------- MINUIT PART ----------------
#  pip3 install iminout  numba_stats numpy
from iminuit import cost, Minuit
import iminuit
from numba_stats import norm, uniform # faster replacements for scipy.stats functions


import glob

def main( *args ):
    if len(args)<1:
        print("X... no object name given  (and no model given too)")
        return
    if len(args)<2:
        print("X... no model given, I try to look for them")
        files = glob.glob("pr_model*.py")
        if len(files)==0:
            print("X... NO python fit models available now")
            return
        else:
            files = [x for x in files if x.find("pr_model_")>=0]
            files = [x.split("_")[2].split(".")[0] for x in files]
            print(f"i... available  FIT models: \n{files}")
            return


    fname = args[0]
    g_orig = ROOT.gDirectory.FindObject(f"{fname}")



    # - check the object. If None => try to load something
    #        AUTOMATIC LOAD
    #
    if g_orig==None:
        print(f"X... {fname} object doesnot exist in gDirectory")
        # - do we try to load it? If it is an actual file
        if os.path.exists(fname):
            print(f"i... BUT file /{fname} exists")
            print(f" ...       trying to unload and load /pr_load/")
            try:
                sys.modules.pop( "pr_load" )
            except:
                pass
            module_load = importlib.import_module( "pr_load" )
            ok = False
            try:
                if len(args)>1: # accept y,x as 2nd parameter
                    module_load.main( fname , args[2] )
                else:
                    module_load.main( fname  )
                ok = True
            except:
                ok = False
            if not ok:
                return
            fname = os.path.splitext(fname)[0]
            print( fname )
            g_orig = ROOT.gDirectory.FindObject( fname )


    # MODULE========================================== I call again prun;

    shape = args[1]
    polorder = None

    # print (len(shape))
    # print( shape.find("pol") )
    # print(  shape[-1] )
    # print( [ str(i) for i in range(0,10) ] )

    # POL0-9
    if (len(shape)==4) and (shape.find("pol")==0) and ( shape[-1] in [ str(i) for i in range(0,10) ] ):
        print("i... POLi model shape  detected")
        polorder = int(shape[-1])
        shape = "polall"

    # POC0-9 - chebyshev
    if (len(shape)==4) and (shape.find("poc")==0) and ( shape[-1] in [ str(i) for i in range(0,10) ] ):
        print("i... POLi model shape  detected")
        polorder = int(shape[-1])
        shape = "pocall"

    model_name = f"model_{shape}"
    module = prun.import_module( model_name )




    if module is None:
        print(f"X... module {model_name} not found...")
        return
    #if not(os.path.exists(f"{model}.py")):
    #    print(f"X... required model file  {model}.py does not exist")
    #    return

    #------------------------------ MODEL SHOULD BE LOADED HERE ------

    # # UNimport module first - case there was an error there previously
    # try:
    #     # -------- I must unload to be able to edit the source whil being in CLING
    #     print(f" ...       trying to unload model  {model}  at first")
    #     sys.modules.pop( model)
    # except:
    #     print(f" ...       model  {model} was not imported previously")
    # module = importlib.import_module( model )
    #------------------------------------------------------






    print(f"i... extracting /{g_orig.GetName()}/ of type /{g_orig.ClassName()}/")

    # -------------------------------   get Arrays -> import to numpy  .asarray
    ishisto = False

    if g_orig.ClassName()=="TGraph":
        x=np.asarray( g_orig.GetX() )
        y=np.asarray( g_orig.GetY() )
        dx = np.zeros_like(x)
        dy = np.zeros_like(y)+1
        print("!... UNIT ERROR SET ON Y-AXIS !!")

    if g_orig.ClassName()=="TGraphErrors":
        x=np.asarray( g_orig.GetX() )
        y=np.asarray( g_orig.GetY() )
        dx=np.asarray( g_orig.GetEX() )
        dy=np.asarray( g_orig.GetEY() )

    if g_orig.ClassName()=="TH1F":
        ishisto = True
        #
        # i need to convert to np; be sure it is np.float64!
        # maybe - kill all zero points??? or set error 1??
        # ZOOM with GetFirst GetLast
        #
        #   x chan -0.5 to compensate midbin!
        #
        #  NASTY TRICK - x=x-zx1 -> and back...... I cannot converge at 7000chan
        #
        #
        zx1,zx2 = g_orig.GetXaxis().GetFirst(),g_orig.GetXaxis().GetLast()

        x  = np.asarray( np.arange( zx1,  zx2+1 ) ,  np.float64 )
        #
        # i have proble with large distances
        #
        #x  = np.asarray( np.arange( zx1-zx1,  zx2+1-zx1 ) ,  np.float64 )
        #x = x + 0.5 # bin center
        y  = np.zeros_like(x)
        dy = np.zeros_like(y)+1


        for i in range(zx1,zx2+1): # zx1,zx2+1 all range
            # i checked that I must -0.5 as bin[0] is underflow
            x[i-zx1] = float(x[i-zx1] - 0.5)
            y[i-zx1] = g_orig.GetBinContent( i)
            if y[i-zx1]>0:
                dy[i-zx1]=np.sqrt(y[i-zx1])
                #dy[i-zx1]=10

        dx = np.zeros_like(x)


        x = np.array(  x  ,  np.float64)
        y = np.array(  y  ,  np.float64)
        dx = np.array(  dx  ,  np.float64)
        dy = np.array(  dy  ,  np.float64)
        #dx=np.asarray( g_orig.GetEX() )
        #dy=np.asarray( g_orig.GetEY() )

    #---------------------------------------- DONE with importing TGraphs or histos ----------






    #-*********************************now the MINUIT PART
    #-*********************************now the MINUIT PART
    yf = module.main( x,y,dy , polorder )




    # --- I can output the results.  I do it for : gpol1
    #print(type(yf))

    if type(yf) is np.ndarray:
        print("")

    elif type(yf) is tuple: # ------------ i wanted to get 3 functions (fit,low,high)
        yf,yf_l,yf_h=yf[0],yf[1],yf[2]

    elif  type(yf) is dict:
        print("i... full dict of data return")
        data_dict = yf
        yf_l = data_dict['yf_l']
        yf_h = data_dict['yf_h']
        yf   = data_dict['yf']

    else:
        print("X... I am watching the output of the fit module. Unknown. Stop") # just yf values to plot
        return
        #-*********************************now the MINUIT PART
    #-*********************************now the MINUIT PART

    #x = x + zx1 # trick to converge




    # ///////////////////////////////////////////////////// plotting results
    cmain = ROOT.gROOT.GetListOfCanvases().FindObject("fitresult")
    if ROOT.addressof(cmain)==0:
        print("i... creating a new /fitresult/ canvas")
        cmain = ROOT.TCanvas("fitresult","fitresult",600,800)
        print("i... creating a new /fitresult/ canvas draw")
        cmain.Draw()
        print("i... creating a new /fitresult/ canvas drawn")
        #cmain = ROOT.gPad.GetCanvas()  # reset all canvas

    cmain.SetFillColor(19)
    cmain.Clear()
    print("i... div a new /fitresult/ canvas")
    cmain.Divide(1,2) # div canvas
    cmain.cd(1)

    ####g_xy = ROOT.TGraph( len(x) , x.flatten("C"), yf.flatten("C") )
    g_orig.SetMarkerStyle(7) # small circle , no lines...

    # if low number of points-plit triagles
    if len(x)<15: g_orig.SetMarkerStyle(22)
    g_orig.Draw() # for histo NOT PAWL;  it works with NO PAWL TGraph too
    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    #x = x[:5]
    #yf= yf[:5]
    #y = y[:5]
    #print(type(x),  len(x)  , x)
    #print(type(yf), len(yf) , yf)


    # --------------------- result plotted ---------------
    gf = ROOT.TGraph( len(x) , x.flatten("C"), yf.flatten("C") )
    gf.SetLineColor(6) # 5 yellow
    gf.SetLineWidth(2)
    #gf.SetFillStyle(3004)
    #gf.SetFillColor(6)
    #gf.SetFillColorAlpha( 6, 0.05)
    #gf.Draw("sameLF") # i liked to fill gaus F
    gf.Draw("sameL")


    # if not ("yf_l" in locals()):
    #     yf_l = yf
    # # --------------------- result plotted ---------------
    # gf_l = ROOT.TGraph( len(x) , x.flatten("C"), yf_l.flatten("C") )
    # gf_l.SetLineColor(6) # 5 yellow
    # gf_l.SetLineWidth(1)
    # gf_l.SetLineStyle(4)
    # gf_l.Draw("sameL")

    # if not ("yf_h" in locals()):
    #     yf_h = yf
    # # --------------------- result plotted ---------------
    # gf_h = ROOT.TGraph( len(x) , x.flatten("C"), yf_h.flatten("C") )
    # gf_h.SetLineColor(6) # 5 yellow
    # gf_h.SetLineWidth(1)
    # gf_h.SetLineStyle(3)
    # gf_h.Draw("sameL")

    ROOT.gPad.SetGrid()
    if ishisto:  ROOT.gPad.SetLogy()
    ROOT.gPad.Modified()
    ROOT.gPad.Update()






    cmain.cd(2) # --------second pad --------------------------
    # ------ differences ------------------
    #gfy=np.asarray( gf.GetY() )
    gfy = yf
    diffy = y-gfy
    gf_diff= ROOT.TGraphErrors( len(x) , x.flatten("C"),
                                diffy.flatten("C"),
                                dx.flatten("C"),
                                dy.flatten("C")    )


    # keep the axes' labels from original graph

    newtitle =  f"exp-fit:{g_orig.GetTitle()};{g_orig.GetXaxis().GetTitle()};{g_orig.GetYaxis().GetTitle()}-fit"
    #print(f"NEWTITLE={newtitle}")
    gf_diff.SetTitle( newtitle)
    gf_diff.SetMarkerStyle(7) # small circle , no lines...
    gf_diff.SetLineColor(4)
    gf_diff.Draw("PAW")


    # plotting the red line of perfect fit

    zeroy = y-y
    gf_zero= ROOT.TGraph( len(x) , x.flatten("C"), zeroy.flatten("C")  )
    gf_zero.SetLineColor(2)
    gf_zero.Draw("same")
    ROOT.gPad.SetGrid()
    ROOT.gPad.SetLogy( False)
    ROOT.gPad.Modified()
    ROOT.gPad.Update()



    #-------------------------- I NEED to REGISTER all to be able to display on gPad


    prun.register(cmain, "fitresult")

    prun.register(gf, "fit")
    #prun.register(gf_l, "fit_low")
    #prun.register(gf_h, "fit_high")
    prun.register(gf_diff, "fitdiff")
    prun.register(gf_zero, "linezero")

    if "data_dict" in locals():
        return data_dict
    else:
        return


if __name__=="__main__":
    Fire(main)
    # update canvas
    #ROOT.gPad.Modified()
    #ROOT.gPad.Update()
    input('press ENTER to end...')
