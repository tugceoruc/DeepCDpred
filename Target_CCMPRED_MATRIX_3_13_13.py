
class Target(object):
    def __init__(self):
        self.aacomposition=[]
        self.profile=[]
        self.entropy=[]
        self.entropymean=0;
        self.potential=0
        self.mi=0
        self.minormal=0
        self.psicov=0
        self.evfold=0
        self.ccmpred=0
        
        self.ss_c=[]
        self.ss_h=[]
        self.ss_e=[]
        self.solvent=[]
        self.phi=[]
        self.psi=[]
        
        self.ss_cmean=0
        self.ss_hmean=0
        self.ss_emean=0
        self.solventmean=0
        
        self.seqlen=0
        self.nseq=0
        self.effnseq=0
        
        self.IPERGRP=6
        self.WINL=-6
        self.WINR=6
        self.CWINL=-2
        self.CWINR=2
        
        self.NUM_IN=2*(self.WINR-self.WINL+1)*self.IPERGRP+(self.CWINR-self.CWINL+1)*self.IPERGRP+547



        
           
        
