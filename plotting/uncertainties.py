from ROOT import *
from math import sqrt
from array import array
from tdrStyle import *
from os import getenv
import plotConfig

setTDRStyle()

def plot_ratio(process,suffix = ''):

        highest = {}
        lowest = {}

        baseDir = getenv('CMSSW_BASE')+'/src/MonoXFit_CSV/'
        f = TFile(baseDir + 'combined_model.root','READ')

        if 'electron' in process:
            extralabel = 'Electrons'
        elif 'muon' in process:
            extralabel = 'Muons'
        elif 'photon' in process:
            extralabel = 'Photons'
        else:
            extralabel = ''

        if (process=='wz'):
                dirname = 'Z_constraints_category_monotop'+suffix
                base        = 'w_weights_monotop'+suffix
                label     = 'Z#rightarrow#nu#nu/W#rightarrow(l)#nu'
                addsys = []

        if (process=='dimuon'):
                dirname = "Z_constraints_category_monotop"+suffix
                base        = "zmm_weights_monotop"+suffix
                label     = 'Z#rightarrow#nu#nu/Z#rightarrow#mu#mu'
                addsys    = []

        if (process=='dielectron'):
                dirname = "Z_constraints_category_monotop"+suffix
                base        = "zee_weights_monotop"+suffix
                label     = 'Z#rightarrow#nu#nu/Z#rightarrowee'
                addsys    = sqrt(0.04*0.04)

        if (process=='photon'):
                dirname = "Z_constraints_category_monotop"+suffix
                base        = "photon_weights_monotop"+suffix
                label     = 'Z#rightarrow#nu#nu/#gamma'
                addsys    = 0

        if (process=='singleelectronw'):
                dirname = "W_constraints_category_monotop"+suffix
                base        = "wen_weights_monotop"+suffix
                label     = 'W#rightarrow(l)#nu/W#rightarrowe#nu'
                addsys    = sqrt(0.02*0.02)

        if (process=='singlemuonw'):
                dirname = "W_constraints_category_monotop"+suffix
                base        = "wmn_weights_monotop"+suffix
                label     = 'W#rightarrow(l)#nu/W#rightarrow#mu#nu'
                addsys    = sqrt(0.01*0.01)

        if (process=='singleelectrontop'):
                dirname = "Top_constraints_category_monotop"+suffix
                base        = "topen_weights_monotop"+suffix
                label     = 't#rightarrowb(l)#nu/t#rightarrowbe#nu'
                addsys    = sqrt(0.02*0.02)

        if (process=='singlemuontop'):
                dirname = "Top_constraints_category_monotop"+suffix
                base        = "topmn_weights_monotop"+suffix
                label     = 't#rightarrowb(l)#nu/t#rightarrowb#mu#nu'
                addsys    = sqrt(0.01*0.01)

        if (process=='singleelectronwtop'):
                dirname = "Top_constraints_category_monotop"+suffix
                base        = "topwen_weights_monotop"+suffix
                label     = 't#rightarrowb(l)#nu/t#rightarrow(b)e#nu'
                addsys    = sqrt(0.02*0.02)

        if (process=='singlemuonwtop'):
                dirname = "Top_constraints_category_monotop"+suffix
                base        = "topwmn_weights_monotop"+suffix
                label     = 't#rightarrowb(l)#nu/t#rightarrow(b)#mu#nu'
                addsys    = sqrt(0.01*0.01)

        ratio = f.Get(dirname+"/"+base)

        variations = {} # unc : { up : hup, down : hdown}

        f.cd(dirname)
        for key in gDirectory.GetListOfKeys():
                if ('TH1' in key.GetClassName()):
                        if (process in key.GetName()) or (base in key.GetName()):
                                uncname = '_'.join(key.GetName().replace(base,'').split('_')[1:-1])
                                if 'stat' in uncname:
                                    continue
                                if ('Up' in key.GetName()):
                                    if uncname not in variations:
                                        variations[uncname] = {}
                                    variations[uncname]['up'] = f.Get(dirname+"/"+key.GetName())
                                elif ('Down' in key.GetName()):
                                    if uncname not in variations:
                                        variations[uncname] = {}
                                    variations[uncname]['down'] = f.Get(dirname+"/"+key.GetName())

        maxvar = 0
        for v in variations.values():
            for vv in v.values():
                vv.Divide(ratio)
                maxvar = max(maxvar,vv.GetMaximum())
        one = ratio.Clone('one')
        one.Divide(ratio)
        maxvar = (maxvar-1)

        gStyle.SetOptStat(0)

        c = TCanvas("c","c",600,600)    
        c.SetTopMargin(0.06)
        c.cd()
        c.SetRightMargin(0.04)
        c.SetTopMargin(0.07)
        c.SetLeftMargin(0.15)

        one.SetMaximum(1+(maxvar*2.5))
        one.SetMinimum(1-(maxvar*1.5))
        one.GetYaxis().SetTitle('Uncertainty (%s)'%label)
        one.GetYaxis().CenterTitle()
        one.GetYaxis().SetTitleSize(0.4*c.GetLeftMargin())
        one.GetXaxis().SetTitle("U [GeV]")
        one.GetXaxis().SetTitleSize(0.4*c.GetBottomMargin())
        one.GetYaxis().SetTitleOffset(1.15)
        one.SetLineStyle(2)
        one.SetLineColor(kGray)
        one.SetLineWidth(2)
        one.Draw("hist")        

        legend = TLegend(.60,.65,.92,.9)

        legend.SetShadowColor(0);
        legend.SetFillColor(0);
        legend.SetFillStyle(0)
        legend.SetLineColor(0);

        extra_colors = [kBlue-7, kRed-7, kMagenta-7, kOrange+7, kTeal+9, kAzure+7, kViolet-7, kCyan+2, kGreen+2]
        extra_style = 2
        colors = {'btag':kRed, 'mistag':kBlue, 'sjbtag':kOrange, 'sjmistag':kAzure+1, 'mettrig':kBlack}
        ic = 0
        already_done = []
        for k in sorted(colors) + sorted(variations):
            if k in already_done or k not in variations:
                continue
            if 'di' in process or 'pho' in process:
                if k=='btag' or k=='mistag':
                    continue
            already_done.append(k)
            v = variations[k]
            if k in colors:
                color = colors[k]
                linestyle = 1
            else:
                color = extra_colors[ic]
                linestyle = extra_style
                ic += 1 
                if ic==len(extra_colors):
                    extra_style += 1
            for s in ['up','down']:
                h = v[s]
                h.SetLineColor(color)
                h.SetLineStyle(linestyle)
                h.SetLineWidth(3)
                h.Draw('hist same')
            legend.AddEntry(v['up'],k,'l')


        legend.SetNColumns(len(variations)/12+1)
        legend.Draw("same")

        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.035)
        latex2.SetTextAlign(11) # align left
        latex2.DrawLatex(0.15, 0.95, extralabel);
        latex2.SetTextAlign(31) # align right
        latex2.DrawLatex(0.87, 0.95, "%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi));
#        latex2.DrawLatex(0.87, 0.95, "2.1 pb^{-1} (13 TeV)");

        #latex3 = TLatex()
        #latex3.SetNDC()
        #latex3.SetTextSize(0.75*c.GetTopMargin())
        latex2.SetTextSize(0.7*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.19, 0.85, "CMS")
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.29, 0.85, "Preliminary")                    
        
        gPad.RedrawAxis()


        plotDir = plotConfig.plotDir

        c.SaveAs(plotDir+"variations_"+process+suffix+".pdf")
        c.SaveAs(plotDir+"variations_"+process+suffix+".png")


        del c

for suffix in ['','_loose']:
    plot_ratio('dimuon',suffix)
    plot_ratio('dielectron',suffix)
    plot_ratio('photon',suffix)
    plot_ratio('singlemuonw',suffix)
    plot_ratio('singleelectronw',suffix)
    plot_ratio('singlemuontop',suffix)
    plot_ratio('singleelectrontop',suffix)
    plot_ratio('singlemuonwtop',suffix)
    plot_ratio('singleelectronwtop',suffix)
    plot_ratio('wz',suffix)
