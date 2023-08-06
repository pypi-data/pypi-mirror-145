# -*- coding: utf-8 -*-
"""
This module is based on the following paper:

Bacon, C. (1993). Numerical prediction of the propagation of elastic waves in 
longitudinally impacted rods : Applications to Hopkinson testing. 
*International Journal of Impact Engineering*, 13(4), 527‑539. 
https://doi.org/10.1016/0734-743X(93)90084-K

   Summary-- Simple expressions, based on one-dimensional elastic wave theory, are
   established which permit prediction of normal force and particle velocity at 
   cross-sections of a non-uniform linearly-elastic rod. The initial normal force
   and particle velocity at each cross-section of that rod must be known.


First define a bar, then give it to :class:`WP2` or :class:`Waveprop` along 
with an incident wave for propagation computation::

    bar = Barhete(E=[210, 78], rho=[7800, 2800], L=[1, 1.1], d=[0.030, 0.028])
    incw = np.ones(100)
    prop = WP2(bar, incw)

Be careful:

* :class:`WP2` works only with :class:`Barhete` bars; traction is not transmitted throught interfaces
* :class:`Waveprop` works with :class:`Barhete` and :class:`Barhomo` bars, but does not take interfaces between bars/segments into account (the bars are stuck, traction can cross interfaces)

Created on Fri Aug 22 11:13:37 2014

@author: dbrizard
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings

import figutils as fu


class WP2:
    """Second version of wave propagation, using :class:`Segment` for each bar
    of constant section.
    
    No traction crossing interfaces (=section changes).

    
    """
    
    def __init__(self, bar, incw=None, nstep=0, left='free', right='free', 
                 Vinit=0, contactLoss=1e-9):
        """Computte wave propagation
        
        /!\ Anechoic condition at impact end (left) until the end of the 
        prescribed incident wave *incw*
        
        :param obj bar: bar setup (:class:`Barhete` object)
        :param array incw: incident force wave (input left impact)
        :param int nstep: optional number of time step
        :param str left: left boundary condition, once incident wave is finished
        :param str right: right boundary condition ('free' or 'infinite')
        :param float Vinit: initial velocity of left bar
        :param float contactLoss: threshold for contact loss between segments. No loss if None
        """
        if nstep==0:
            n_trav = 2.5  # number of wave travels through the entire bar
            nstep = int(n_trav*np.sum(bar.nelt))
            print("Simulation time set to %i travels across all bars."%n_trav)
        
        nT = nstep  # len(incw)

        # Initial conditions: at rest (first line) + initialization of matrices
        for ii, ss in enumerate(bar.seg):
            if ii==0 and not Vinit==0:
                print("Setting initial velocity of first segment (Vo=%g)"%Vinit)
                ss.initCalc(nT, Vo=Vinit)
                incw = np.zeros(0)
            else:
                ss.initCalc(nT)
        
        contact = []
        for it in range(nT)[1:]:
            for ii, ss in enumerate(bar.seg):
                ss.compMiddle(it)  # middle state of each segment
                if ii==0: 
                    # first segment LEFT:
                    if it<=len(incw):
                        ss.compLeft(it, incw=incw[it-1])  # excited
                    else:
                        ss.compLeft(it, left=left)  # not excited any more
                    # first segment RIGHT:
                    if bar.nseg>1:
                        ss.compRight(it, rseg=bar.seg[ii+1])
                    else:
                        ss.compRight(it)  # only one segment
                    
                elif ii==bar.nseg-1:
                    # last segment:
                    ss.compLeft(it, lseg=bar.seg[ii-1])
                    ss.compRight(it, right=right) 
                    
                else:
                    # middle segments: interfaces
                    ss.compLeft(it, lseg=bar.seg[ii-1])
                    ss.compRight(it, rseg=bar.seg[ii+1])
                
                # now that Force and Velocity are computed for time index `it`,
                # post-process to get Displacement:
                ss.compDispl(it)
                
            # XXX this is where interfaces (.left and .right) of the concerned
            # segments must be updated
            if contactLoss is not None:
                for (Sleft, Sright) in zip(bar.seg[:-1], bar.seg[1:]):
                    if Sright.Displ[it,0] - Sleft.Displ[it,-1]>contactLoss:
                        Sleft.Right = 'free'
                        Sright.Left = 'free'
                        contact.append(0)
                    elif Sleft.Displ[it,-1] - Sright.Displ[it,0]>contactLoss:
                        warnings.warn("Bar indentation should not happen :(")
                        contact.append(-1)
                    else:
                        # do nothing, Segments are still in contact
                        contact.append(1)


        time = np.arange(nT)*bar.dt
        for ss in bar.seg:
            ss.setTime(time) #set :attr:`time` for each :class:`Segment`
            ss.computeStressStrain()
        
        self.time = time
        self.bar = bar
        self.gatherForce()
        self.contact = {'state':contact, 'threshold':contactLoss}


    def gatherForce(self):
        """Gather all the :attr:`Force` of each :class:`Segment` in :class:`Barhete`
        in one array.
        """
        # intervals for plotting
        xx = self.bar.x
        x2 = np.hstack((-xx[1]/2, (xx[1:] + xx[:-1])/2, xx[-1]+(xx[-1]-xx[-2])/2)) #
        self.xplot = x2
        
        #get x values
        Force = np.zeros((len(self.time), len(xx)))
        ind0 = 0
        for ii, ss in enumerate(self.bar.seg):
            ind1 = ind0 + ss.Force.shape[1]-1
            if ii==self.bar.nseg-1:
                Force[:, ind0:ind1+1] = ss.Force
            else:
                Force[:, ind0:ind1] = ss.Force[:, :-1]
            ind0 = ind1
        
        self.Force = Force

    def plot(self, figname=None, gatherForce=True, typ='FVD'):
        """Plot Force and Velocity lagrangian diagrams (time versus space)
        
        Wrapper of :meth:`WP2.subplot` method
        
        :param str figname: name for the figure
        :param bool gatherForce: do not use subplot for Force diagram
        :param str typ: choose variables to plot (F: force, V: velocity, D: displacement)
        """
        if 'F' in typ:
            # ---PLOT FORCE---
            if gatherForce:
                self.plotForce(figname=figname)
            else:
                self.subplot(figname, 'F')
        
        if 'V' in typ:
            # ---PLOT VELOCITY---
            self.subplot(figname, 'Veloc')
        
        if 'D' in typ:
            # ---PLOT DISPLACEMENT---
            self.subplot(figname, 'Displ')


    def plotForce(self, figname=None, vert=None, autovert=True):
        """Plot Force lagrangian diagram (time versus space)
        
        :param str figname: name for the figure
        :param list vert: vertical lines to trace
        :param bool autovert: automatically plot vertical lines at interfaces and bar ends
        """
        # ---HANDLE TIME SCALE---
        if self.time[-1]<1e-6:
            scale = 1e9
            tlab = 't [ns]'
        elif self.time[-1]<1e-3:
            scale = 1e6
            tlab = 't [µs]'
        elif self.time[-1]<1:
            scale = 1e3
            tlab = 't [ms]'
        else:
            scale = 1
            tlab = 't [s]'
        
        
        plt.figure(figname)
        plt.title('Force [N]')
        
        tt = scale*self.time
        xx = self.bar.x
        ampli = getMax(self.Force)
        QM = plt.pcolormesh(xx, tt, self.Force, cmap='PiYG', vmin=-ampli, vmax=ampli,
                            # edgecolor='w', lw=.1, alpha=0.6,
                            rasterized=True, shading='nearest')
        plt.colorbar()
        plt.xlabel('x [m]')
        plt.ylabel(tlab)
        plt.axvline(x=self.bar.x[-1], color='.5')
        xmin, xmax, ymin, ymax = getMinMaxQMCoordinates(QM)
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.box(False)
        
        if vert is not None:
            for v in vert:
                plt.axvline(x=v, color='.8')
        if autovert:
            try:
                verts = np.hstack((0, np.cumsum(self.bar.L)))
                for v in verts:
                    plt.axvline(x=v, color='.7')
            except AttributeError:
                print("This may not be a Barhete instance, no vertical lines to plot...")
        
        plt.xlim(xmin=self.xplot[0], xmax=self.xplot[-1]) # XXX get rid of xplot?
        plt.ylim(ymax=scale*self.time[-1])
    
    
    def subplot(self, figname=None, typ='Veloc'):
        """Plot Force or Velocity lagrangian diagram (time versus space) on a
        subplot for each segment
        
        :param str ForV: Force or Velocity ('F', 'V')
        """
        gs = plt.GridSpec(1, len(self.bar.seg), width_ratios=[ss.l for ss in self.bar.seg])
        
        shading = 'nearest'
        if typ.lower() in ('veloc', 'velocity', 'v'):
            ZVAL = [ss.Veloc for ss in self.bar.seg]
            title = 'Velocity [m/s]'
            cmap = plt.cm.PRGn
            prefix = '-V'
        elif typ.lower() in('force', 'f'):
            ZVAL = [ss.Force for ss in self.bar.seg]
            title = 'Force [N]'
            cmap = plt.cm.PiYG
            prefix = '-F'
        elif typ.lower() in ('displ', 'displacement'):
            ZVAL = [ss.Displ for ss in self.bar.seg]
            title = 'Displacement [m]'
            cmap = plt.cm.PiYG
            prefix = '-D'
        elif typ.lower() in ('stress', 'sig'):
            ZVAL = [ss.Stress/1e6 for ss in self.bar.seg]
            title = 'Stress [MPa]'
            cmap = plt.cm.PiYG
            prefix = '-sig'
            shading ='flat'
            print('NOT POSSIBLE YET')
        elif typ.lower() in ('strain', 'eps'):
            ZVAL = [ss.Strain/1e6 for ss in self.bar.seg]
            title = 'Strain [µdef]'
            cmap = plt.cm.PRGn
            prefix = '-eps'
            shading = 'flat'
            print('NOT POSSIBLE YET')


        
        # ---HANDLE FIGURE NAME---
        if figname is not None:
            figname += prefix
        
        # ---HANDLE TIME SCALE---
        if self.time[-1]<1e-6:
            scale = 1e9
            tlab = 't [ns]'
        elif self.time[-1]<1e-3:
            scale = 1e6
            tlab = 't [µs]'
        elif self.time[-1]<1:
            scale = 1e3
            tlab = 't [ms]'
        else:
            scale = 1
            tlab = 't [s]'
            
        AMPLI = [getMax(zz) for zz in ZVAL]
        ampli = np.max(AMPLI)
        axes = []
        
        plt.figure(figname)
        for ii, (sseg, Zval) in enumerate(zip(self.bar.seg, ZVAL)):
            if ii==0:
                ax = plt.subplot(gs[ii])
            else:
                ax = plt.subplot(gs[ii], sharey=axes[0])
            axes.append(ax)
            QM = plt.pcolormesh(sseg.x, self.time*scale, Zval, cmap=cmap,
                                vmin=-ampli, vmax=ampli, 
                                # edgecolor='w', lw=.1, #alpha=1,
                                rasterized=True, shading='nearest')
            plt.box(False) # TODO: is False the good choice ?
            # Distinction between first and following subplots
            if ii==0:
                plt.xlabel('x [m]')
                plt.ylabel(tlab)
                plt.title(title)
            else:
                plt.tick_params(axis='y', labelleft=False)
            # Ajustements
            xmin, xmax, ymin, ymax = getMinMaxQMCoordinates(QM)
            plt.xlim(xmin=sseg.x[0], xmax=sseg.x[-1])
            plt.ylim(ymin, ymax)
        plt.colorbar(ax=axes)  # space is stolen on all the axes


    def getState(self, t, plot=True):
        """Get state of the bars at given time.
        
        :param float t: time at which state is desired
        :param bool plot: enable graphical output or not        
        """
        indt = np.where(t>=self.time)[0][-1]
        
        if plot:
            plt.figure()
            
            for ss in self.bar.seg:
                plt.subplot(211)
                plt.plot(ss.x, ss.Force[indt, :], '.-')
                plt.subplot(212)
                plt.plot(ss.x, ss.Veloc[indt, :], '.-')
                
            plt.xlabel('x [m]')
            plt.subplot(211), plt.ylabel('Force [N]')
            plt.title('t = %g s'%self.time[indt])
            plt.subplot(212), plt.ylabel('Velocity [m/s]')
        
        return None #XXX il va bien falloir renvoyer qq chose si on veut récupérer les valeurs


    def getSignal(self, x, iseg=None, plot=True, Displ=True, time='ms',
                  figname=None, marker=None):
        """Get temporal signal at given position on the bar.
        
        :param float x: x position of sensor (local coordinates if **iseg** is given, otherwise global)
        :param int iseg: index of segment where the sensor is
        :param bool plot: enable graphical output or not
        :param bool Displ: also return (and plot) displacement
        :param str time: time scale ('s', 'ms', 'µs')
        :param str figname: name for the figure
        :param str marker: marker
        
        :var array F: Force
        :var array V: Velocity
        :var array xx: ??
        :var array indx: ??
        """
        if type(iseg)==int:
            if type(x)==float:
                # local coordinates = segment coordinate
                indx = np.where(x>=self.bar.seg[iseg].xloc)[0][-1]
            elif type(x)==int:
                # x is taken as an index
                indx = x
            xx = self.bar.seg[iseg].xloc[indx]
        elif iseg is None:
            # global coordinates. Have to determine iseg first
            xmins = np.array([ss.x[0] for ss in self.bar.seg])
            # array otherwise where won't work
            iseg = np.where(x>=xmins)[0][-1]
            indx = np.where(x>=self.bar.seg[iseg].x)[0][-1]
            xx = self.bar.seg[iseg].x[indx]

        F = self.bar.seg[iseg].Force[:, indx]
        V = self.bar.seg[iseg].Veloc[:, indx]
        nsbp = 2
        if Displ:
            D = self.bar.seg[iseg].Displ[:, indx]
            nsbp+=1
        
        stime, xlab = scaleTime(self.time, scale=time)
        
        if plot:
            plt.figure(figname)
            ax1 = plt.subplot(nsbp, 1, 1)
            plt.axhline(color='0.8')
            plt.plot(stime, F, 'm', marker=marker)
            plt.ylabel('Force [N]')
            plt.title('x = %g m'%xx)
            plt.box(False)

            plt.subplot(nsbp, 1, 2, sharex=ax1)
            plt.axhline(color='0.8')
            plt.plot(stime, V, 'c', marker=marker)
            plt.ylabel('Velocity [m/s]')
            plt.box(False)
            
            if Displ:
                plt.subplot(nsbp, 1, 3, sharex=ax1)
                plt.axhline(color='0.8')
                plt.plot(stime, D, 'g', marker=marker)
                plt.ylabel('Displacement [m]')
                plt.box(False)
            plt.xlabel(xlab)
        
        if Displ:
            return F, V, D, (xx, indx, iseg)
        else:
            return F, V, (xx, indx, iseg)


    def plotInterface(self, interf=0, figname=None, markers='.+'):
        """Plot Force, Velocity and Displacement at interface between Segments
        
        Basically a wrapper of :meth:`WP2.getSignal` which takes care of selecting
        the right indices to get data at the given interface.
                
        :param int interf: interface index
        :param str figname: name for the figure
        :param str markers: markers for left and right variables
        """
        iseg1 = interf
        iseg2 = interf+1
        nX1 = int(self.bar.seg[iseg1].nX)
        
        F1, V1, D1, _ = self.getSignal(nX1-1, iseg1, figname=figname, marker='.')
        F2, V2, D2, _ = self.getSignal(0, iseg2, figname=figname, marker='+')
    
    
    def plotDeSaintVenant(self, scale=100, figname=None, ms=5, lines='0.8'):
        """Plot x-t displacement diagram.
        
        :param float scale: scale factor to increase Displ and make it visible
        :param str figname: name for the figure
        :param float ms: give marker size to get points plotted (color=Force)
        :param color lines: give color to get lines plotted
        """
        if ms is not None:
            ZVAL = [ss.Force for ss in self.bar.seg]
            AMPLI = [getMax(zz) for zz in ZVAL]
            ampli = np.max(AMPLI)
        
        
        plt.figure(figname)
        for ii, ss in enumerate(self.bar.seg):
            if lines is not None:
                plt.plot(ss.time, ss.x+scale*ss.Displ, 
                         color=lines, ls='-', zorder=0)
                plt.xlabel('t [s]')
                plt.ylabel('x [m]')
            
            if ms is not None:
                time = np.tile(ss.time, (ss.Force.shape[1], 1))
                plt.scatter(time.T, ss.x+scale*ss.Displ, s=ms, c=ss.Force,
                            cmap='PiYG', vmin=-ampli, vmax=ampli)
        if ms is not None:
            plt.colorbar(label='Force [N]')
        
        plt.title('displacement scale factor %g'%scale)
        plt.xlabel('t [s]')
        plt.ylabel('x [m]')
        plt.box(on=False)

class Waveprop:
    '''One-dimensional wave propagation problem for a rod with a piecewise
    constant impedance.
    
    /!\ Impedance should not be null.
    
    Right side of the bar is a free end
    Left side of the bar is infinite bar (anechoic conditions)
    
    '''
    
    def __init__(self, bar, incw, nstep=0, left='free', right='free', Vinit=0, indV=None):
        '''Compute propagation of incident wave in the given bar.
        
        First version: traction can cross section changes (ie interfaces)
        
        :param obj bar:    instance of :class:`Barhomo` or :class:`Barhete`
        :param array incw: incident wave
        :param int nstep:  number of calculation steps (if 0, length of **incw**)
        :param str left:   left boundary condition ('free' or 'infinite') after the end of **incw**
        :param str right:  right boundary condition ('free' or 'infinite')
        :param float Vinit: initial bar velocity
        :param int indV: index of end of impact section! LEFT=impactor=speed, RIGHT=bars=static
        '''
        # Number of calculation steps
        if nstep==0:
            # si la durée n'est pas précisée, on se base sur la durée de l'excitation
            nstep = len(incw)
        else:
            # si le nbre de pas de calcul est précisé...
            n_trav = 10  # number of time the wave travels through the entire bar(s)
            if nstep > n_trav*np.sum(bar.nelt):
                # ...on vérifie quand même qu'on n'en demande pas trop
                print("/!\ computation may be long and heavy")
        
#        nX = len(bar.Z) # ca va pas du tout !!
        nX = len(bar.x)  # number of nodes
        nT = nstep  # len(incw)
        time = np.arange(nT)*bar.dt
        Z = bar.Z  # number of elements

        # Initial conditions: at rest (first line) + initialization of matrices
        Force = np.zeros((nT, nX))  # normal force
        Veloc = np.zeros((nT, nX))  # particule velocity
        # TODO: initial velocity not giving the proper results.
        if not Vinit==0 and indV==None:
            Veloc += Vinit
            # contrainte générée par le choc à la la vitesse Vinit à gauche de la barre
            Finit = .5*bar.Z[0]*Vinit # since Z=A*rho*co et F=A* 1/2*rho*co*Vinit
            incw = Finit * np.ones(len(incw))
            warnings.warn("Incident Wave 'incw' was overwritten")
        
        if indV:
            Veloc[0,:indV+1] = Vinit
#            Force[0,indV] = .5*bar.Z[0]*Vinit # since Z=A*rho*co et F=A* 1/2*rho*co*Vinit
            # NO initial Force, this is automatic !!
            incw = np.zeros(0)
            warnings.warn("Testing impact initial conditions!")
            
        # pour éviter de se mélanger dans les indices, cf. cahier #3 p20        
        
        nExc = len(incw) #end of the excitation vector
        # Time step progression
        for it in range(nT)[1:]:
            # LEFT boundary conditions
            if it <= nExc:
                Force[it, 0] = (2*Z[1]*incw[it-1] + Z[0]*(Force[it-1, 1] + Z[1]*Veloc[it-1, 1]))/(Z[0]+Z[1])
                Veloc[it, 0] = (Force[it-1, 1] + Z[1]*Veloc[it-1, 1] -2*incw[it-1])/(Z[0]+Z[1])
            else:
                if left=='free':
                    Force[it, 0] = 0
                    Veloc[it, 0] = Veloc[it-1, 1] + Force[it-1, 1]/Z[0]
                    #/!\ indices semblent bon. Reste les signes... à vérifier
                elif left=='infinite':
                    #XXX j'ai des doutes sur les Z0 et Z1...
                    Force[it, 0] = (Z[0]*(Force[it-1, 1] + Z[1]*Veloc[it-1, 1]))/(Z[0]+Z[1])
                    Veloc[it, 0] = (Force[it-1, 1] + Z[1]*Veloc[it-1, 1])/(Z[0]+Z[1])
                elif left in ('fixed', 'clamped'):
                    Force[it, 0] = Force[it-1, 1] - Z[0]*Veloc[it-1, 1]  # XXX TOCHECK!!
                    Veloc[it, 0] = 0
                
                    
            
            # RIGHT boundary conditions
            if right=='free':
                Force[it, -1] = 0
                Veloc[it, -1] = Veloc[it-1, -2] - Force[it-1, -2]/Z[-1]
            elif right=='infinite':
                Force[it, -1] = (Force[it-1, -2] - Z[-1]*Veloc[it-1, -2])/2
                Veloc[it, -1] = -Force[it-1, -2]/2/Z[-1] + Veloc[it-1, -2]/2
            elif right in ('fixed', 'clamped'):
                Force[it, -1] = Force[it-1, -2] - Z[-1]*Veloc[it-1, -2]  # XXX TOCHECK!!
                Veloc[it, -1] = 0
                   
            if 'damped' in right or False:
                C = 1e4  # [N.s/m]
                Force[it, -1] += -C*Veloc[it, -1]  # XXX Formula presumed wrong
            if 'spring' in right or False:
                K = 1e8  # [N/m]
                displ = np.sum(Veloc[:,-1]*bar.dt)
                print(displ)
                Force[it, -1] += -K*displ
            if 'friction' in right:
                Ff = 1e4  # [N]
                if Veloc[it, -1] is not 0:
                    if abs(Force[it, -1])>Ff:
                        Force[it, -1] -= Ff
                    else:
                        print('this is complex')


            # Middle of the bar
            Zi = Z[:-1]  # Z_i
            Zii = Z[1:]  # Z_i+1 # tiens donc, on retombe sur nos pieds ici...

            Fl = Force[it-1, :-2]  # Force left F(x-c_i*T, t-T)
            Fr = Force[it-1, 2:]  # Force right F(x+c_i*T, t-T)
            Vl = Veloc[it-1, :-2]  # Veloc left V(x-c_i*T, t-T)
            Vr = Veloc[it-1, 2:]  # Veloc right V(x+c_i*T, t-T)
            
            Force[it, 1:-1] = (Zii*Fl + Zi*Fr + Zi*Zii*(Vr-Vl))/(Zi+Zii)
            Veloc[it, 1:-1] = (Fr - Fl + Zi*Vl + Zii*Vr)/(Zi+Zii)
        
        # Store nodal variables
        self.Force = Force  # @nodes
        self.Veloc = Veloc  # @nodes
        self.Displ = np.cumsum(Veloc*bar.dt, axis=0)  # @nodes
        # Store element variables
        self.Strain = (self.Displ[:,1:]-self.Displ[:,:-1])/bar.dx  # @elements
        self._Stress = {}
        # This is not the correct way to compute stress, I believe,
        self._Stress['left'] = self.Force[:,:-1]/bar.A  # left stress, @elements
        self._Stress['right'] = self.Force[:,1:]/bar.A  # right stress, @elements
        # This should rather be the way
        self.Stress = self.Strain*bar.E
        
        # Traction-Compression state
        LR = Force*Veloc
        state = np.zeros(LR.shape)
        seuil = LR.ptp()*1e-6
        state[LR < -seuil] = -1
        state[LR > seuil] = 1
        
        # intervals for plotting
        xx = bar.x
        x2 = np.hstack((-xx[1]/2, (xx[1:] + xx[:-1])/2, xx[-1]+(xx[-1]-xx[-2])/2))
        # TODO: remove x2 ? see if shading option of pcolormesh works...

        # Filling attributes
        self.xplot = x2
        self.LR = LR #left (>0) or right (<0) propagation
        self.state = state
        self.time = time
        self.bar_discret = bar


    def compState(self, seuil, plot=True):
        '''Compute again state (left or right propagating waves) based on given *seuil*
        
        The threshold above which the wave is taken into account is computed 
        as LR.ptp()*seuil
        
        :attr:`seuil` means that this method was used.
        
        Mainly for development purpose...
        
        :param float seuil: threshold
        :param bool plot:  enable graphical output
        '''
        s = self.LR.ptp()*seuil
        state = np.zeros(self.LR.shape)
        state[self.LR < -s] = -1
        state[self.LR > s] = 1
        self.state = state
        self.seuil = seuil
        
        if plot:
            self.plotmatrix(state, 'TC state %g threshold'%seuil)
        
        
    def plotmatrix(self, Zvalues, title=None, cmap='PRGn', vert=None, autovert=True, time='ms'):
        '''Plot lagrange diagram of matrix *Zvalues*.
        
        Mainly used in :meth:`plot` or directly for development.
        
        :param array Zvalues: 
        :param str title: title for the figure
        :param cmap cmap: colormap
        :param list vert: list of position of vertical lines to plot (or None)
        :param bool autovert: automatic vertical lines at segment changes
        :param str time: time scale ('ms', 's', 'µs')
        '''
        # ---HANDLE TIME SCALE---
        time_, xlab = scaleTime(self.time, scale=time)
        
        x = self.bar_discret.x
        # Detect and handle nodal or elementary variable
        if Zvalues.shape[1]==len(x):
            # Nodal property : len(x) = number of nodes
            shading = 'nearest'
        elif Zvalues.shape[1]==len(x)-1:
            # Elementary property : len(x) = number of elements = number of nodes - 1
            shading = 'flat'
            dt = time_[1]-time_[0]
            time_ = np.concatenate((time_, [time_[-1]+dt]))
        
        ampli = getMax(Zvalues)
        plt.figure()
        plt.title(title)
        # *pcolormesh* est effectivement beaucoup plus rapide que *pcolor*
        QM = plt.pcolormesh(x, time_, Zvalues, cmap=cmap, vmin=-ampli, vmax=ampli,
                            rasterized=True, shading=shading) 
        plt.colorbar()
        plt.xlabel('x [m]')
        plt.ylabel(xlab)
        plt.axvline(x=self.bar_discret.x[-1], color='.5')
        # Adjust limits to QuadMesh limits
        xmin, xmax, ymin, ymax = getMinMaxQMCoordinates(QM)
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.box(False)
        
        
        # ---ADD VERTICAL LINES---
        if vert is not None:
            for v in vert:
                plt.axvline(x=v, color='.8')
        # XXX Following is useless, no Barhomo.L attribute. Why did I write it?
        # if autovert:
        #     try:
        #         verts = np.hstack((0, np.cumsum(self.bar_discret.L)))
        #         for v in verts:
        #             plt.axvline(x=v, color='.7')
        #     except AttributeError:
        #         if self.bar_discret.__class__.__name__=='Barhete':
        #             warnings.warn('There is a big BIG problem')
        #         else:
        #             print("this may not be a Barhete instance, no vertical lines to plot")
        
        
    
    def plot(self, typ='VF', vert=None, autovert=True):
        '''Plot lagrange diagram -time versus space- of wave propagation.
        
        Type of diagram can be:
        
        * 'V': Velocity;
        * 'F': Force;
        * 'dir': wave direction (left or right);
        * 'state': wave direction (Left (+1) or Right (-1));
        * 'sig': stress (sigma);
        * 'eps': strain (epsilon).
        
        :param str typ: the diagram(s) to plot       
        :param list vert: list of vertical lines to plot on the diagram.
        :param bool autovert: automatically plot vertical lines corresponding to bar lengthes.
        '''
        if 'F' in typ:
            self.plotmatrix(self.Force, 'Force [N]', plt.cm.PuOr,
                            vert=vert, autovert=autovert)  # PiYG
        if 'V' in typ:
            self.plotmatrix(self.Veloc, 'Particule velocity [m/s]', plt.cm.RdBu,
                            vert=vert, autovert=autovert)
        if 'dir' in typ:
            self.plotmatrix(self.LR, 'Wave direction (left or righ)', plt.cm.BrBG,
                            vert=vert, autovert=autovert)
        if 'state' in typ:
            self.plotmatrix(self.state, 'Left (+1) or Right (-1)', plt.cm.PuOr,
                            vert=vert, autovert=autovert)
        if 'D' in typ:
            self.plotmatrix(self.Displ, 'Displacement [m]',
                            vert=vert, autovert=autovert)
        if 'sig' in typ:
            self.plotmatrix(self.Stress/1e6, 'Stress [MPa]',
                            vert=vert, autovert=autovert)
        if 'eps' in typ:
            self.plotmatrix(self.Strain*1e6, 'Strain [µdef]',
                            vert=vert, autovert=autovert)
    
    def getcut(self, x=None, t=None, isind=False):
        """Get temporal evolution at given abscissa x,
        or state of the bar at given time t.
        
        :param float x: get temporal evolution at abscissa x.
        :param float t: get bar state at given time t.
        :param bool isind: boolean to specify index instead of abscissa/time value.

        :returns: time (for given x) or abscissa (for given t)
        :returns: force
        :returns: particule velocity
        """
        if x is not None:
            if isind:
                indx = x
            else:
                # get index of column to plot
                indx = np.where(self.bar_discret.x <= x)[0][-1]
            x = self.time
            force = self.Force[:,indx]
            veloc = self.Veloc[:,indx]
            displ = self.Displ[:,indx]
        elif t is not None:
            if isind:
                indt = t
            else:
                # get index of line to plot
                indt = np.where(self.time <= t)[0][-1]
            x = self.bar_discret.x
            force = self.Force[indt,:]
            veloc = self.Veloc[indt,:]
            displ = self.Displ[indt,:]
        
        return x, force, veloc, displ
    
    
    def plotcut(self, x=None, t=None, isind=False, tscale='ms'):
        '''Plot temporal evolution at given abscissa x,
        or state of the bar at given time t.
        
        /!\ one of x or t arguments MUST be None.
        
        :param float x: get temporal evolution at abscissa x.
        :param float t: get bar state at given time t.
        :param bool isind: give time/abscissa index instead of time/abscissa value
        
        See also :meth:`Waveprop.getcut`
        '''
        ab, force, veloc, displ = self.getcut(x, t, isind)

        plt.figure()
        ax1 = plt.subplot(311)        
        
        if x is not None:
            plt.title('x=%g m'%x)
            xlab = 't [s]'
        elif t is not None:
            plt.title('t=%g s'%t)
            xlab = 'x [m]'
        #---FORCE---        
        plt.axhline(y=0, color='0.8')
        plt.plot(ab, force, 'r.-', drawstyle='steps-post')
        plt.ylabel('Force')
        
        #---VELOCITY---
        plt.subplot(312, sharex=ax1)
        plt.axhline(y=0, color='0.8')
        plt.plot(ab, veloc, 'b.-', drawstyle='steps-post')
        plt.ylabel('Velocity')
        plt.xlabel(xlab)
    
        #---DISPLACEMENT---
        plt.subplot(313, sharex=ax1)
        plt.plot(ab, displ, 'g.-', drawstyle='steps-post')
        plt.ylabel('Displacement')
        plt.xlabel(xlab)
        
    
    def plotFV(self, x, figname=None):
        """Plot wave in Force-Velocity plane.
        
        :param float x: get temporal evolution at abscissa x.
       """
        _, F, V = self.getcut(x=x)
        
        plt.figure(figname)
        # plt.title('x=%g m'%x)
        plt.axhline(y=0, color='0.8', zorder=0)
        plt.axvline(x=0, color='0.8', zorder=0)
        plt.plot(V, F, '.-', label='x=%g m'%x)
        plt.xlabel('V [m/s]')
        plt.ylabel('F [N]')
        plt.legend()
        plt.box(False)
        
    
    def plotEvol(self, indf=None):
        """Plot evolution of state of the bar as time increases
        
        :param int indf: final index until which to plot data
        """
        x = self.bar_discret.x
        dx = np.hstack( (np.diff(x), np.diff(x)[-1]) )
        df = np.max(self.Force)
        dv = np.max(self.Veloc)
        
        plt.figure()
        try:
            nt = indf+1
        except TypeError:
            nt = len(self.Force)
        fu.degrade(ncoul=nt)
        
        for ii, (ff, vv) in enumerate(zip(self.Force, self.Veloc)):
#            plt.subplot(211)
            plt.plot(x+dx*ii/nt, ff+df*ii/nt, '.-', drawstyle='steps-post')
            
#            plt.subplot(212)
#            plt.plot(x+dx*ii/nt, vv, '.-', drawstyle='steps-post')

    
    def plotDeSaintVenant(self, scale=100, figname=None, ms=5, lines='0.8', XPplot=False):
        """Plot x-t displacement diagram.
        
        :param float scale: scale factor to increase Displ and make it visible
        :param str figname: name for the figure
        :param float ms: give marker size to get points plotted (color=Force)
        :param color lines: give color to get lines plotted
        :param bool XPplot: experimental plots with pcolor. Warning: grid is not correctly adjusted yet.
        """
        displacement = self.bar_discret.x+scale*self.Displ
        plt.figure(figname)
        if lines is not None:
            plt.plot(self.time, displacement, color=lines, ls='-', zorder=0)
            plt.xlabel('t [s]')
            plt.ylabel('x [m]')
        
        if ms is not None:
            time = np.tile(self.time, (self.Force.shape[1], 1))
            plt.scatter(time.T, displacement, s=ms, c=self.Force, cmap='PuOr')
            plt.colorbar(label='Force [N]')
        
        
        plt.title('displacement scale factor %g'%scale)
        plt.xlabel('t [s]')
        plt.ylabel('x [m]')
        plt.box(on=False)
        
        if XPplot:
            #---EXPERIMENTAL PLOT---
            plt.figure('force')
            offset = self.bar_discret.dt/2
            plt.pcolor(time.T-offset, displacement, self.Force, ec='k', shading='nearest')  # ça déforme un peu la grille...
            plt.plot(self.time, displacement, color='0.8', ls='-')
    
            plt.figure('strain')
            offset = self.bar_discret.dt/2
            plt.pcolor(time.T-offset, displacement, self.Strain, ec='k', shading='flat')
            plt.plot(self.time, displacement, color='0.8', ls='-')
        
def scaleTime(time, scale='s'):
    """Return scaled time or index
    
    :param array time: input time array, unit supposed to be in [s]
    :param str scale: desired output unit ('s', 'ms', 'µs'). Can also be 'ind'
    """
    if scale in ('s'):
        scaledtime = time
        lab = 't [s]'
    elif scale in ('ms'):
        scaledtime = time*1e3
        lab = 't [ms]'
    elif scale in ('µs'):
        scaledtime = time*1e6
        lab = 't [µs]'    
    elif scale in ('ind'):
        scaledtime = range(len(time))
        lab = 'index [-]'
    return scaledtime, lab


def getMinMaxQMCoordinates(QM):
    """Get min and max for x and y coordinates

    :param QuadMesh QM: :class:`matplotlib.collections.QuadMesh` object from :func:`plt.pcolormesh`
    """
    xmin = QM._coordinates[:,:,0].min()
    xmax = QM._coordinates[:,:,0].max()
    ymin = QM._coordinates[:,:,1].min()
    ymax = QM._coordinates[:,:,1].max()
    return xmin, xmax, ymin, ymax



def getMax(mat):
    '''Get the maximum absolute extremum.
    
    :param array mat: 2D array
    '''
    return np.max([np.abs(mat.min()), np.abs(mat.max())])


def trapezeWave(plateau=20, rise=5, fall=None, A=1):
    """Define trapezoidal incident wave
    
    :param int plateau: number of points on the plateau
    :param int rise: number of points for rising part
    :param int fall: number of points for falling part
    :param float A: amplitude of wave
    """
    if not fall:
        fall = rise
    Mrise = np.linspace(0, A, num=rise, endpoint=False)
    Mfall = np.linspace(0, A, num=fall, endpoint=False)
    Mplat = np.ones(plateau)*A
    
    trap = np.hstack((Mrise, Mplat, Mfall[::-1]))
    return trap
    

class Barhomo:
    """Homogeneous bar (ie continuous rod) with section changes.
    
    Mother class of :class:`Barhete`
    """
    def __init__(self, dx, d, E, rho):
        '''Barre homogème, avec uniquement des variations se section (d)
        
        Zero impedance should be avoided for calculation step coming next within
        :class:`Waveprop`.
        
        :param flaot dx: spatial discretization
        :param list d: diameters 
        :param float E: Young's modulus
        :param float rho: density
        '''
        A = np.pi*d**2/4
        co = np.sqrt(E/rho)
        Z = A*rho*co
        
        x = np.arange(len(d)+1)*dx
        dt = dx/co

        self.nelt = len(d)
        self.E = E
        self.rho = rho
        self.co = co
        self.dt = dt
        self.dx = dx
        self.x = x
        self.d = d   
        self.A = A
        self.Z = Z
        
    def plot(self, typ='DZ', ls='.-'):
        """Graphical representation of discretized bar: geometry and impedance.
        
        :param str typ: choose graphical output ('D':diameter, 'Z':impedance)
        """
        def plotRectangle(xo, dx, d):
            '''Plot rectangle at position xo, with width dx and height d (cf. #3 p.20).
            '''
            r = d/2
            xs = (xo, xo+dx, xo+dx, xo, xo)
            ys = (-r,    -r,     r,  r, -r)
            plt.plot(xs, ys, ls)
        
        if 'D' in typ.upper():
            plt.figure()
            #fu.degrade(len(self.d))
            for ii, dd in enumerate(self.d):
                plotRectangle(self.x[ii+1], -(self.x[ii+1]-self.x[ii]), dd)
            plt.xlabel('x [m]')
            plt.ylabel('r [m]')
            plt.ylim(ymin=-1.2*np.max(self.d)/2, ymax=1.2*np.max(self.d)/2)

        if 'Z' in typ.upper():
            plt.figure()
            plt.plot((self.x[:-1]+self.x[1:])/2, self.Z, '.')
            plt.xlabel('x [m]')
            plt.ylabel('Z [kg/s]')



class Barhete(Barhomo):
    """Heterogeneous bar with cross-section/modulus/density changes along the
    bar length.
    
    Sister class of :class:`Barhomo`
    
    :attr:`seg` is a list of :class:`Segment` objects, this is then used in :class:`WP2`.
    
    :class:`Waveprop` uses the other attributes.
    
    """
    def __init__(self, E, rho, L, d, dt=0, nmin=4, right='free'):
        '''Define and spatially discretize bar into :class:`Segment` s of constant properties
        
        :param list E: Young's moduli
        :param list rho: densities
        :param list L: bar segment lengthes
        :param list d: bar segment diameters
        :param float dt: time step (automatically determined if 0)
        :param int nmin: minimum number of 'elements' in a bar segment of constant properties
        '''
        bar = Bar(E, rho, L, d)
        
        if dt==0 and not nmin==0:
            dx_s = np.array(L)/nmin
            # corresponding dt
            dt_s = dx_s/bar.co
            dt = dt_s.min()
            # keeping smallest dt
            dx = bar.co*dt
            
            nelt = np.rint(np.array(L)/dx).astype(int)  # round to nearest integer
            Lentier = nelt*dx  # XXX
            
        elif not dt==0:
            dx_s = bar.co*dt  # co=dx/dt
            dx = dx_s.min()
        
        
        self.bar_continuous = bar  # Bar object
        # arrays of size the number of segments:
        self.L = Lentier
        self.dx = dx
        self.nelt = nelt
        
        ind = np.cumsum(np.hstack((0, nelt))).astype(int)
        
        def _fillHete(prop):
            '''index *ind* and property *prop*
            
            :param array ind: list of indices, last index gives total length of returned array
            :param array prop: corresponding list of property
            '''
            p = np.zeros(ind[-1])
            for ii in range(len(prop)):
                p[ind[ii]:ind[ii+1]] = prop[ii]
            return p
        

        # reste à constituer toutes les variables discrétisées
        self.ind = ind  # ind of section change
        self.E = _fillHete(E)
        self.dt = dt  # en principe il n'y en a qu'un !
        DX = _fillHete(dx)
        self.x = np.cumsum(np.hstack((0, DX)))
        self.d = _fillHete(d)
        self.Z = _fillHete(bar.Z)  # y'a que Z qui sert pour le calcul !!

        self.nseg = len(bar.co)
        # define segment list
        s = []
        for ii, (zz, ll, ddx, nn, EE) in enumerate(zip(bar.Z, Lentier, dx, nelt, E)):
            if ii==0:
                le = 'impact'
                xo = 0
            else:
                le = 'interf'
                xo = s[-1].x[-1]  # last segment's extremity
            if ii==self.nseg-1:
                ri = right
            else:
                ri = 'interf'
            s.append(Segment(nn, zz, EE, ll, ddx, dt, xo, le, ri))
        self.seg = s


    def changeSection(self, iseg=0, l=None, d=None):
        """Change the section of part of a Segment to model a bar with section 
        change.
        
        :param int iseg: index of segment
        :param float l: position of the section change
        :param float d: new section for the right portion
        """
        # z = rho*A*co
        z = np.pi*d**2/4*self.bar_continuous.rho[iseg]*self.bar_continuous.co[iseg]
        self.seg[iseg].resetImpedance(l, z)

    def plotProperties(self, figname=None):
        """Plot evolution of properties of the bar along the length
        
        :param str figname: name for the figure
        """
        for ii, seg in enumerate(self.seg):
            seg.plotProperties(figname, label='segment %i'%ii)
        if figname is not None:
            for ii, ll in enumerate(np.cumsum(self.L)):
                plt.axvline(ll, ls=':', color='C%i'%ii, label='interf %i'%ii) #color='0.8', 
            plt.xlabel('x [m]')
            plt.ylabel('Z [kg/s]')
            plt.legend()
    
    
    def __repr__(self):
        """Instance representation method
        
        """
        irm ='===========\n'
        
        for ss in self.seg:
            irm+= ss.__repr__()
            irm+='===========\n'

        return irm

class Segment(object):
    """Bar segment with constant properties
    
    For later use in :class:`WP2` through :class:`Barhete`
    """
    def __init__(self, nel, z, E, l, dx, dt, xo, left='infinite', right='infinite'):
        """
        
        :param int nel:  number of elements in segment
        :param float z:  segment impedance
        :param float E:  segment elastic modulus
        :param float l:  segment length
        :param float dx: length of elements in segment
        :param float dt: time step
        :param float xo: abscissa of left end of segment
        :param str left: 'infinite', 'free', 'impact' or 'interf'
        :param str right: idem
        
        The following attributes are added:
        
        :cvar int nX: number of points along x direction
        :cvar array xplot: x position of points in global coordinate system
        """
        self.nX = nel+1  # number of points along x space
        # UN = np.ones(self.nx) # point number = element number +1 !!
        #self.z = z  # 
        self.Z = np.ones(nel)*z
        self.E = E
        self.l = l
        self.dx = dx
        self.dt = dt
        self.xloc = np.arange(nel+1)*dx  # local coordinates
        self.x = xo + np.arange(nel+1)*dx  # global coordinates
        self.xplot = np.hstack((xo-dx/2, self.x+dx/2))
        self.left = left
        self.right = right
    
    def resetImpedance(self, l, z):
        """Reset impedance of elements after position l along the length
        
        Be careful, this new impedance MUST NOT change wave speed. Otherwise
        spatial discretization is obsolete. Only section change is permitted.
        
        :param float l: beginning position of new impedance
        :param float z: new impedance        
        """
        ind = np.where(l>self.xloc)[0][-1]
        self.Z[ind:] = z
    
    def initCalc(self, nT, Vo=0):
        """Initialize before wave propagation computation
        
        :param int nT: number of computation/time steps
        :param float Vo: initial velocity
        """
        self.nT = nT
        self.Force = np.zeros((self.nT, self.nX))
        self.Veloc = Vo * np.ones((self.nT, self.nX))
        self.Displ = np.zeros((self.nT, self.nX))
    
    def setTime(self, time):
        """Set :attr:`time` attribute.
        
        :param array time: time vector
        """
        self.time = time
    
    def compMiddle(self, it):
        """Compute state in the middle of the segment
        
        :param int it: time index
        """
        Fl = self.Force[it-1, :-2]  # Force left F(x-c_i*T, t-T)
        Fr = self.Force[it-1, 2:]  # Force right F(x+c_i*T, t-T)
        Vl = self.Veloc[it-1, :-2]  # Veloc left V(x-c_i*T, t-T)
        Vr = self.Veloc[it-1, 2:]  # Veloc right V(x+c_i*T, t-T)
        # Z = self.z
        Zi = self.Z[:-1]  # Z_i
        Zii = self.Z[1:]  # Z_i+1
        self.Force[it, 1:-1] = (Zii*Fl + Zi*Fr + Zi*Zii*(Vr-Vl)) / (Zi+Zii)
        self.Veloc[it, 1:-1] = (Fr - Fl + Zi*Vl + Zii*Vr) / (Zi+Zii)

    def compLeft(self, it, lseg=None, incw=None, left=None):
        """Compute state of left bar end.
        
        Bar end can be: free, infinite, interf (interface with another :class:`Segment`),
        impact (impacted end, in which case **incw** must be given).
        
        :param int it: time index
        :param obj lseg: left :class:`Segment`        
        :param float incw: input force (incident wave)
        :param str left: left boundary condition (supersedes :attr:`Segment.left`)
        """
        if not left:
            left = self.left
            
        if left=='free':
            self.Force[it, 0] = 0
            self.Veloc[it, 0] = self.Veloc[it-1, 1] + self.Force[it-1, 1]/self.Z[0]
            #/!\ indices semblent bon. Reste les signes... à vérifier
        elif left=='fixed':
            print('LEft Not Checked Yet!')  # XXX
            self.Force[it, 0] = self.Force[it-1, 1] - self.Z[0]*self.Veloc[it-1, 1]  # XXX TOCHECK!!
            self.Veloc[it, 0] = 0            
        elif left=='infinite':
            self.Force[it, 0] = (self.Force[it-1, 1] + self.Z[0]*self.Veloc[it-1, 1])/2
            self.Veloc[it, 0] = (self.Force[it-1, 1] + self.Z[0]*self.Veloc[it-1, 1])/(2*self.Z[0])
        elif left=='interf':
            Zi = lseg.Z[-1]
            Zii = self.Z[0]  # self.z
            Fl = lseg.Force[it-1, -2]
            Vl = lseg.Veloc[it-1, -2]
            Fr = self.Force[it-1, 1]
            Vr = self.Veloc[it-1, 1]
            F = (Zii*Fl + Zi*Fr + Zi*Zii*(Vr-Vl))/(Zi+Zii)
            if F<0:
                #Ok, this is compression!
                self.Force[it, 0] = F
                self.Veloc[it, 0] =  (Fr - Fl + Zi*Vl + Zii*Vr)/(Zi+Zii)
            else:
                #Ach, this is traction... So same as free end !
                self.Force[it, 0] = 0
                self.Veloc[it, 0] = Vr + Fr/Zii
        elif left=='impact':
            #rebasculer sur 'infinite' ou 'free'... si possible
            self.Force[it, 0] = (2*self.Z[1]*incw + self.Z[0]*(self.Force[it-1, 1] +self.Z[1]*self.Veloc[it-1, 1]))/(self.Z[0] + self.Z[1])
            self.Veloc[it, 0] = (self.Force[it-1, 1] + self.Z[1]*self.Veloc[it-1, 1] -2*incw)/(self.Z[0] + self.Z[1])
        
    def compRight(self, it, rseg=None, right=None):
        """Compute state of right bar end.
        
        Bar end can be: free, infinite, interf (interface with another :class:`Segment`).
        
        :param int it: time index
        :param obj rseg: right :class:`Segment`        
        :param str right: right boundary condition (supersedes :attr:`Segment.right`)
        """
        if not right:
            right = self.right
        
        if right=='free':
            self.Force[it, -1] = 0
            self.Veloc[it, -1] = self.Veloc[it-1, -2] - self.Force[it-1, -2]/self.Z[-1]
        elif right=='fixed':
            self.Force[it, -1] = self.Force[it-1, -2] - self.Z[-1]*self.Veloc[it-1, -2]  # XXX TOCHECK!!
            self.Veloc[it, -1] = 0           
        elif right=='infinite':
            self.Force[it, -1] = (self.Force[it-1, -2] - self.Z[-1]*self.Veloc[it-1, -2])/2
            self.Veloc[it, -1] = -self.Force[it-1, -2]/2/self.Z[-1] + self.Veloc[it-1, -2]/2
        elif right=='interf':
            Zi = self.Z[-1]
            Zii = rseg.Z[0]
            Fl = self.Force[it-1, -2]
            Vl = self.Veloc[it-1, -2]
            Fr = rseg.Force[it-1, 1]
            Vr = rseg.Veloc[it-1, 1]
            F = (Zii*Fl + Zi*Fr + Zi*Zii*(Vr-Vl))/(Zi+Zii)
            if F<0:
                #Ok then, this is compression
                self.Force[it, -1] = F
                self.Veloc[it, -1] = (Fr - Fl + Zi*Vl + Zii*Vr)/(Zi+Zii)
            else:
                self.Force[it, -1] = 0
                self.Veloc[it, -1] = Vl - Fl/Zi
        
    def compDispl(self, it):
        """Compute displacement of the bar nodes at given time index.
        
        :param int it: time index
        """
        self.Displ[it,:] = self.Displ[it-1,:] + self.Veloc[it,:]*self.dt
    
    def computeStressStrain(self):
        """Compute Strain from Displacement and then Stress, in the elements        
        
        """
        self.Strain = (self.Displ[:,1:]-self.Displ[:,:-1])/self.dx  # @elements
        self.Stress = self.Strain*self.E  # @elements

    
    def plotProperties(self, figname=None, label=None):
        """
        
        :param str figname: name for the figure
        :param str color: filling color of elements
        """
        plt.figure(figname)
        plt.step(self.x[:-1], self.Z, '.-', where='mid', label=label)
        print('Markers and step positions are not precise yet...')  # XXX
    
    def plot(self, typ='VF', vert=None, autovert=True):
        """Plot lagrange diagram.
        
        Wrapper for :meth:`Segment.plotmatrix` allowing to choose the plotted data.
        
        :param str typ: choose the diagram to plot ('V': Velocity, 'F':Force)
        :param list vert: vertical lines to add
        :param bool autovert: automatically plot vertical lines at bar ends        
        """
        if 'F' in typ.upper():
            self.plotmatrix(self.Force, 'Force [N]', plt.cm.PiYG, vert=vert, autovert=autovert)
        if 'V' in typ.upper():
            self.plotmatrix(self.Force, 'Velocity [m/s]', vert=vert, autovert=autovert)
            

    def plotmatrix(self, Zvalues, title=None, cmap=plt.cm.PRGn, vert=None, autovert=True):
        '''Plot lagrange diagram of matrix *Zvalues*.
        
        Mainly used in :meth:`Segment.plot` or directly for development.
        '''
        ampli = getMax(Zvalues)
        plt.figure()
        plt.title(title)
        # *pcolormesh* est effectivement beaucoup plus rapide que *pcolor*
        xg, tg = np.meshgrid(self.xplot, self.time) # XXX not sure xplot is still available!
        plt.pcolormesh(xg, tg, Zvalues, cmap=cmap, vmin=-ampli, vmax=ampli) 
        plt.colorbar()
        plt.xlabel('x [m]')
        plt.ylabel('t [s]')
        
        if not vert==None:
            for v in vert:
                plt.axvline(x=v, color='.8')
        if autovert:
            verts = [self.x[0], self.x[-1]]
            for v in verts:
                plt.axvline(x=v, color='.7')


    def __repr__(self):
        """Instance representation method"""
        # XXX pas extraordinaire...
        s = '\n'
        s+= 'L: %g m\n'%self.l
        # s+= 'Z: %g kg/s\n'%self.z#[0]
        Zu = np.unique(self.Z)
        Zstr = ['%g'%zz for zz in Zu]
        s+= 'Z: %s kg/s\n'%Zstr
        s+= 'Left: %s\n'%self.left
        s+= 'Right: %s\n'%self.right
        s+= 'nX: %i\n'%self.nX
        return s


class Bar:
    '''Description d'une barre continue par morceaux, avant discrétisation.
    
    Internally used in :class:`Barhomo` and :class:`Barhete`
    '''
    def __init__(self, E, rho, L, d):
        '''Compute area **A**, celerity **c_o** and impedance **Z** of bar segments.
        
        All imput variables should have the same length and should be lists.
        
        :param list E: Young's moduli
        :param list rho: densities
        :param list L: lengthes of the corresponding segments/bars
        :param list d: diameters
        '''
        # a few things to compute
        self.A = np.pi*np.array(d)**2/4
        self.co = np.sqrt(np.array(E)/np.array(rho))
        self.Z = self.A*np.array(rho)*self.co
        # a few things to simply store
        self.E = E
        self.rho = rho
        self.L = L
        self.d = d
        self.x = np.hstack([0, np.cumsum(L)])
        
        
    def plot(self):
        """Subplot of continuous variables across the bar length:
        
        * diameter d;
        * area A;
        * density rho;
        * modulus E;
        * celerity c_o;
        * impedance Z.        
        """
        def plotstairs(x,y, ylabel):
            '''Plot y variable, with length -1 /x. Stairs.            
            '''
            plt.plot(x, np.hstack([y, y[-1]]), '.-', drawstyle='steps-post')
            plt.ylim(ymin=.9*np.min(y), ymax=1.1*np.max(y))
            plt.xlim(xmax=x.max())
            plt.ylabel(ylabel)
        plt.figure()
        plt.box(on=False)
        ax = plt.subplot(611)
        plotstairs(self.x, self.d, 'd [m]')
        plt.subplot(612, sharex=ax), plotstairs(self.x, self.A, 'A [m2]')
        plt.subplot(613, sharex=ax), plotstairs(self.x, self.rho, 'rho [kg/m3]')
        plt.subplot(614, sharex=ax), plotstairs(self.x, self.E, 'E [Pa]')
        plt.subplot(615, sharex=ax), plotstairs(self.x, self.co, '$c_0$ [m/s]')
        plt.subplot(616, sharex=ax), plotstairs(self.x, self.Z, 'Z [kg/s]')
        plt.xlabel('x [m]')
        
        
    def printtable(self):
        '''Text representation of the bar through a table'''
        colonnes = np.array(['L [m]', 'd [m]', 'A [m2]', 'rho [kg/m3]', 'E [Pa]', 'c_0 [m/s]', 'Z [kg/s]'])
        data = np.array([self.L, self.d, self.A, self.rho, self.E, self.co, self.Z])
        
        rep = np.vstack([colonnes, data.T]).T
        print(rep)
        # well, ce n'est pas encore au point question mise en page...
        

def groovedBar(interv, lg=0.003, LL=2, d0=0.030, d1=0.0278, E=78e9, rho=2800, pin=False):
    """Construct :class:`Barhete` object with grooves
    
    :param list interv: interval length seperating each groove
    :param float lg: lenght of groove along bar axis
    :param float LL: total length of grooved stricker + impacted bar
    :param float d0: initial diameter of bar
    :param float d1: groove diameter
    :param float E: Young's modulus
    :param float rho: density
    """
    if pin:
        # pin across the bar
        dpin = d1
        # suppose square hole!, and compute equivalent section of bar
        R = d0/2
        h = d1/2
        area = R**2 * np.arccos(h/R) - h*np.sqrt(R**2-h**2) # aire d'un segment
        Req = np.sqrt(2*area/np.pi)
        d1 = 2*Req
        lg = dpin
        
    # groove length is supposed to be negligible
    d = []
    l = []
    for ll in interv:
        d.extend([d0, d1])
        l.extend([ll, lg])
    # remove last groove
    d = d[:-1]
    l = l[:-1]
    # add second bar
    d.append(d0)
    l.append(LL-l[-1])
    
    Eg = [E for ii in range(len(d))]
    rhog = [rho for ii in range(len(d))]
    
    bg = Barhete(Eg, rhog, l, d, nmin=1, right='free')
    
    #get index of last impactor element
    indelt = bg.nelt[:-1].sum()
    return bg, indelt


class ElasticImpact(object):
    """Bussac, M.-N., P. Collet, G. Gary, B. Lundberg, and S. Mousavi. 2008. 
    ‘Viscoelastic Impact between a Cylindrical Striker and a Long Cylindrical Bar’.
    International Journal of Impact Engineering 35 (4): 226–39.
    https://doi.org/10.1016/j.ijimpeng.2007.02.003.

    
    """
    def __init__(self, E=210e9, rho=7800, d=0.03, L=1., V=5.):
        """
        
        Striker and bar of the same material. Only cross-section can change
        
        :param float E: Young's modulus [Pa]
        :param float rho: density [kg/m3]
        :param list d: striker and bar diamter (can be a single float) [m]
        :param float L: length of the striker [m]
        :param flat V: impact velocity  [m/s]
        """
        if not type(d) in (list, tuple):
            d = [d , d]
        #---COMPUTE A FEW PARAMETERS---
        c = np.sqrt(E/rho)
        
        A = [np.pi*dd*dd/4 for dd in d]
        Z = [aa*np.sqrt(E*rho) for aa in A]
        
        r = A[0]/A[1]
        R = (1 - r)/(1 + r)
        
        te = 2*L/c
        Fe = Z[0]*V/2
        m = A[0]*L*rho
        
        #---STORE DATA---
        self.mat = {'E':E, 'rho':rho, 'c':c}
        self.sec = {'d':d, 'A':A, 'Z':Z}
        self.interf = {'r':r, 'R':R}
        self.striker = {'L':L, 'te':te, 'Fe':Fe, 'm':m, 'V':V}
        
        print("comment calculer l'eq. 35 pour un choc viscoelastique??")
    
    
    def computeImpact(self, t, n=16, y0=0.5, plot=True):
        """Compute impact of stricker on bar.
        
        :param array t: time array
        :param int n: number of terms in the summation
        :param float y0: value of Heaviside function when t=0
        """
        H = lambda x: np.heaviside(x, y0)
        te = self.striker['te']
        R = self.interf['R']
        
        #---COMPUTE FORCE---
        if self.interf['r']>1:
            #---striker imp. higher than bar imp., -1<R<=0---
            print("ça va pas !!")
            contrib = []
            NN = list(range(n))
            for nn in NN:
                temp = (-R)**nn *(H(t - nn*te) - H(t - (nn+1)*te))
                contrib.append(temp)

            f = np.array(contrib).sum(axis=0)
            f *= 1 + R
            self.Rn = (-R)**np.array(NN)
        
        elif self.interf['r']==1:
            #---equal bar and striker impedance; r=1, R=0---
            f = H(t) - H(t - te)
            
        elif self.interf['r']<1:
            #---striker imp. lower than bar imp.
            f = (1 + R)*(H(t) - H(t - te))
        
        #---COMPUTE MOMENTUM AND ENERGY---
        p1 = self.striker['m'] * self.striker['V']
        W1 = 0.5*self.striker['m'] * self.striker['V']**2
        
        if self.interf['r']>=1:
            mom = 1
            ene = 1
        else:
            mom = 2/(1 + self.interf['r'])
            ene = 4*self.interf['r']/((1 + self.interf['r'])**2)
        
        #---STORE RESULTS---
        self.time = t
        self.force = f*self.striker['Fe']
        self.momentum = {'p1':p1, 'ratio':mom}
        self.energy = {'W1':W1, 'ratio':ene}
    
    
    def plotForce(self, figname=None, label=None):
        """
        
        :param str figname: name for the figure
        """
        plt.figure(figname)
        plt.plot(self.time, self.force, '.-', label=label)
        plt.xlabel('time [s]')
        plt.ylabel('force [N]')
    
    
    def plotRn(self, figname=None):
        """Plot amplitude of successive steps in case striker impendace is greater
        than bar impedance
        
        :param str figname: name for the figure        
        """
        plt.figure(figname)
        ax = plt.subplot(211)
        plt.grid()
        plt.bar(list(range(1, len(self.Rn)+1)), self.Rn, zorder=10)
#        plt.step(self.Rn, 'k.', where='mid')
        plt.yscale('log')
        plt.ylabel('$(-R)^n$')
        
        plt.subplot(212, sharex=ax)
#        plt.bar(self.Rn)#, '.' , where='post')
        plt.axhline(color='0.8')
        plt.bar(list(range(1, len(self.Rn)+1)), self.Rn)
        plt.xlabel('n')
        plt.ylabel('$(-R)^n$')
        
        
        

if __name__ == '__main__':
    plt.close('all')
    plotBars = False
    
    #%% ---TEST BARHOMO, BARHETE, WAVEPROP & WP2 CLASSES---
    if True:
        plt.close('all')
        n = 50 # number of points (spatial)
        E = 201e9 # modules de young
        rho = 7800
        d = 0.020
        k = 2.4
        
        
        ## Barre homogène:
        D = np.ones(n) * d # diameters
        D2 = np.hstack((np.ones(n)*d, np.ones(n)*d*k))
        bb = Barhomo(0.01, D,  E, rho) # only section change is possible
        b2 = Barhomo(0.01, D2, E, rho)
        b3 = Barhomo(0.01, D2[::-1], E, rho)
        if plotBars:
            bb.plot()
        
        ## La même barre avec des coupures
        nm = 15
        bc = Barhete([E, E], [rho, rho], [.1, .1], [d, d], nmin=nm)
        bc2 = Barhete([E, E], [rho, rho], [.1, .1], [d, k*d], nmin=nm)
        bc3 = Barhete([E, E], [rho, rho], [.1, .1], [k*d, d], nmin=nm)
        bc4 = Barhete([E, E], [rho, rho], [.1, .3], [d, d], nmin=nm)
        
        ## Barres hétérogènes
        Ee = [210e9,210e9, 210e9]  # Young moduli
        Re = [7800, 7800, 7800]  # densities
        Le = [2, 0.020, 2.71]  # Lengths
        De = [0.020, 0.010, 0.020]  # diameters
        plic = Barhete(Ee, Re, Le, De, nmin=8)
        if plotBars:
            plic.plot()
            plic.bar_continuous.plot()
            plic.bar_continuous.printtable()
        
        
        incw = np.zeros(80)  # incident wave
        incw[0:20] = 1  # /!\ traction pulse
        #%%---TEST WAVEPROP CLASS---
        if True:
            print('transfered to examples')
            test = Waveprop(bb, -incw*1e5, nstep=3*len(incw), left='free', right='free')
            test.plot()
            
            test.plot(typ='DS') # is this useful ?
            test.plotcut(x=bb.x[int(n/2)])
            test.plotcut(t=bb.dt*len(incw)/2)
            
            test.plot('stress-X')
            test.plotDeSaintVenant(scale=100, figname='deStVenant')
        
        #%% ---TEST WP2 CLASS---
        if False:
            L = 1  # [m]
            doubleWave = -np.ones(20)
            #doubleWave[:20] = -1
            #doubleWave[50:60] = -2
            bar = Barhete([E, E], [rho, rho], [L, 2*L], [d, d], nmin=6)
            testk = WP2(bar, nstep=100, left='free', right='free', Vinit=5,
                        contactLoss=None)
            testk.plot()
            testk.plotInterface(figname='testinterf')
            testk.plotDeSaintVenant(figname='deStV', ms=10)

            testk.getSignal(x=0.5, figname='checkVinit')
                        
            bar = Barhete([E, E], [rho, rho], [L, 1.5*L], [d, 1.5*d], nmin=6)
            testl = WP2(bar, incw=-incw, nstep=100, left='free', right='free', Vinit=0)
            testl.plot()
            testl.plotInterface(figname='interf')

            
    #%% ---TEST SHPB CONFIGURATION---
    if False:
        print("not checked yet...")
        # et ragarder dans l'échantillon! : config SHPB
        # plic.seg[0].right = 'free'
        inci = np.zeros(400)  # incident wave
        inci[0:300] = 1  # /!\ traction pulse

        # trap  = trapezeWave() # le trapèze ne change rien...
        toto = WP2(plic, -inci, nstep=2000)  # must be compression pulse to work!!
        toto.bar.seg[1].plot('F')  # OK, la traction ne passe plus!
        toto.plotForce()
        toto.getSignal(x=1)
        toto.getSignal(x=3)
        toto.getState(t=0.0005)
        
        # see what happens in sample
        fl, vl, dl, xx1, indx1 = toto.getSignal(x=0, iseg=1, plot=True)
        fr, vr, dr, xx2, indx2 = toto.getSignal(x=0.02, iseg=1, plot=True)
        plt.figure()
        plt.plot(toto.time, -fl, '.-')
        plt.plot(toto.time, -fr, '.-')
        plt.legend(('left', 'right'), title='sample force')
    
        # see what happens in sample (detail)
        ploc = Barhete(Ee, Re, [0.030, 0.030, 0.030], De, nmin=10)
        exc = np.ones(int(np.rint(100e-6/ploc.dt)))  # 100µs excitation
        prop = WP2(ploc, exc, nstep=600, left='infinite', right='infinite')
        prop.plotForce()
        prop.getSignal(x=0.045)  # middle of sample
        
        # Compare left and right side force in sample
        fl = prop.bar.seg[1].Force[:,0]
        fr = prop.bar.seg[1].Force[:,-1]
        t = prop.bar.seg[1].time
        plt.figure()
        plt.plot(t, fl, label='left')
        plt.plot(t, fr, label='right')
        
#        ## Sort of convergence study: refining spatial discretization
#        L2 = [.4, .02, .503]
#        nmin = range(1,10)
#        plt.figure('cut1')
#        fu.degrade(len(nmin))
#        plt.figure('cut2')
#        fu.degrade(len(nmin))
#        for nn in nmin:
#            bh = Barhete(Ee, Re, L2, De, nmin=nn)
#            incw = np.ones(int(100e-6/bh.dt))
#            nstep = int(2e-3/bh.dt)
#            pp = Waveprop(bh, incw, nstep)
#            
#            xx, ff, vv = pp.getcut(x=L2[0]/2)
#            plt.figure('cut1')
#            plt.plot(xx, ff)
#            
#            xxx,fff,vvv= pp.getcut(x=np.sum(L2)-L2[-1]/2)
#            plt.figure('cut2')
#            plt.plot(xxx, fff)
#            
#        pp.plot(vert=[L2[0]/2, np.sum(L2)-L2[-1]/2])
#        #this last graph seems to get troubles with TC state...
    #
    
    # %% ---COMPUTE IMPACTOR PULSE---
    if False:
        # ---GIVEN PULSE ON SECTION CHANGE---
        stricker = Barhete([210e9, 210e9], [7800, 7800], [0.3, 0.9], [0.055, 0.020], nmin=10)
        contact = np.ones(50)
        impact = Waveprop(stricker, contact, nstep=100, left='infinite', right='free')
        impact.plot()
        
        # ---GIVEN SPEED AND MOOVING PART OF BAR---
        # left: impacted end, right:free end. 
        speed = Waveprop(stricker, contact, left='free', right='infinite', Vinit=10, indV=10, nstep=100)
        speed.plot()
        # Indeed, we need to fix the initial velocity to non zero value !
        
        # ---Groove or hole influence on pulse shape---
        if True:
            bg, indc = groovedBar([0.100, 0.015, 0.200, 0.015, 0.100], LL=0.6)  # d1=0.004, pin=True
            grooved = Waveprop(bg, contact, left='free', right='infinite', Vinit=10, indV=indc, nstep=500)
            grooved.plot()
            grooved.plotcut(x=0.4)
            
    
    # %% ---REFLECTION ON FREE END---
    if False:
        stric = Barhete([210e9], [7800], [0.3], [0.030], nmin=10)
        cont = np.ones(15)
        impact = Waveprop(stric, cont, nstep=3*len(cont), left='infinite', right='free')
        impact.plot()
    

    
    
    # %% ---TEST ELASTICIMPACT CLASS---
    if False:
        time = np.linspace(-10e-6, 10e-3, num=1000)
        EI = ElasticImpact()
        EI.computeImpact(time)
        EI.plotForce('comp')
        
        EJ = ElasticImpact(d=[0.02, 0.03])
        EJ.computeImpact(time)
        EJ.plotForce('comp')
        
        EK = ElasticImpact(d=[0.03, 0.02])
        EK.computeImpact(time)
        EK.plotForce('comp')
        EK.plotRn()
        
        
