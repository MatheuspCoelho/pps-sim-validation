# pps-sim-validation
Validation tools for the PPS simulations

Full simulation: follows CMS default vertex smearing by using the ```generatorSmeared``` source for ```LHCTransport``` and default CMS beamspot position. Disable the hit position from pipeline in ```produceHitsRelativeToBeam``` since DS uses pipeline as reference (CMS uses the beam position).

Direct simulation: employs TOTEM vertex smearing in ```beamDivergenceVtxGenerator```, which sources the ```Unsmeared``` collection in CMS. Additional vertex displacement is applied.

**All samples using ```CMSSW_12_3_0_pre1``` as validation started at Dec/21. Will be moved to newer releases as soon as a good understading between DS and FS is reached.**

Variations are produced following the description below for simulation scenarios:

1 - ```vtx0```: forcing the beamspot position to (0,0,0) by using internal ```LHCInfo``` collection

2 - ```noLHCInfo```: use beamspot position from DB

3 - ```vtx0_ApertureCutsOn```: ```vtx0``` scenario plus using ```ApertureCuts```

4 - ```vtx0_BeamFalse_Smeared```: ```vtx0``` scenario plus hits at pipeline reference as ```produceHitsRelativeToBeam==False```

5 - ```vtx0_BeamFalse_Unsmeared```: forcing the beamspot position to (0,0,0) by using internal ```LHCInfo``` collection and hits at pipeline reference as ```produceHitsRelativeToBeam==False``` plus using ```beamDivergenceVtxGenerator``` for TOTEM vertex smearing

6 - ```vtx0_BeamFalse_Unsmeared_xi1```: ```vtx0_BeamFalse_Unsmeared``` scenario with protons with xi < 0.5

7 - ```vtx_shift```: forcing the beamspot position to CMS position by using internal ```LHCInfo``` collection

8 - ```vtx0_ib```: ```vtx0``` scenario but with ```CMSSW_12_3_X_2022-01-19-1100```
