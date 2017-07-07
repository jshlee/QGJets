from subprocess import PIPE, Popen
import select
import os
import shutil


# outdir = 'MinBias'; writeOut = True; minBias = True
# outdir = 'PythiaMinBias_TuneCUETP8M1'; writeOut = False; minBias = True
outdir = 'PythiaQCD_CUETP8M1_flat'; writeOut = False; minBias = False

print("Running Delphes+Pythia8 in Pythia8 generation mode using {} command file".format(outdir))

cmndname = 'Cards/config_'+outdir+'.cmnd'
if writeOut:
    print("writing minbias command file")
    cmnd = open(cmndname, 'w')
    cmnd.write("""! Lines not beginning with a letter or digit are comments.
    ! Names are case-insensitive  -  but spellings-sensitive!
    ! The changes here are illustrative, not always physics-motivated.

    ! from generatePileUpCMS.cmnd card in Delphes distribution

    ! 1) Settings that will be used in a main program.
    Main:numberOfEvents = 100000          ! number of events to generate
    Main:timesAllowErrors = 3          ! abort run after this many flawed events

    ! 2) Settings related to output in init(), next() and stat().
    Init:showChangedSettings = on      ! list changed settings
    Init:showAllSettings = off         ! list all settings
    Init:showChangedParticleData = on  ! list changed particle data
    Init:showAllParticleData = off     ! list all particle data
    Next:numberCount = 5            ! print message every n events
    Next:numberShowLHA = 1             ! print LHA information n times
    Next:numberShowInfo = 1            ! print event information n times
    Next:numberShowProcess = 1         ! print process record n times
    Next:numberShowEvent = 1           ! print event record n times
    Stat:showPartonLevel = on          ! additional statistics on MPI
    Random:setSeed = on
    Random:setSeed = 10

    ! 3) Beam parameter settings. Values below agree with default ones.
    Beams:idA = 2212                   ! first beam, p = 2212, pbar = -2212
    Beams:idB = 2212                   ! second beam, p = 2212, pbar = -2212
    Beams:eCM = 13000.                 ! CM energy of collision

    ! Common Settings

    Tune:preferLHAPDF = 2
    Main:timesAllowErrors = 10000
    Check:epTolErr = 0.01
    Beams:setProductionScalesFromLHEF = off
    SLHA:keepSM = on
    SLHA:minMassSM = 1000.
    ParticleDecays:limitTau0 = on
    ParticleDecays:tau0Max = 10
    ParticleDecays:allowPhotonRadiation = on

    ! CUEP8M1 Settings

    Tune:pp 14
    Tune:ee 7
    MultipartonInteractions:pT0Ref=2.4024
    MultipartonInteractions:ecmPow=0.25208
    MultipartonInteractions:expPow=1.6

    ! Process parameters

    SoftQCD:nonDiffractive = on
    SoftQCD:singleDiffractive = on
    SoftQCD:doubleDiffractive = on
    """)
    cmnd.close()

delphes_log = open(outdir+'_delphes.log', 'w')
delphes = Popen(["./DelphesPythia8", "./Cards/delphes_card_CMS.tcl", cmndname, "delphes_"+outdir+".root"], stdin=PIPE, stdout=PIPE)
while True:
    nextline = delphes.stdout.readline()
    if nextline == '' and delphes.poll() is not None:
        break
    delphes_log.write(nextline)

delphes_log.close()
if minBias:
    print("Converting to pileup file")
    os.system("../install/Delphes-3.4.1/root2pileup MinBias.pileup delphes_%s.root" % outdir)