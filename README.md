# Welcome to day 2 of the MTUQ 2022 workshop!

Here you will find some useful template scripts to invert the moment tensor for our three test cases:

- 2014 Iceland caldera collapse -  [GridSearch.FullMomentTensor_ICELAND.py](https://github.com/thurinj/mtuq_workshop_2022/blob/main/GridSearch.FullMomentTensor_ICELAND.py)
- 2017 North Korean nuclear test -  [GridSearch.FullMomentTensor_NK.py](https://github.com/thurinj/mtuq_workshop_2022/blob/main/GridSearch.FullMomentTensor_NK.py)
- 2020 South-California earthquake -  [GridSearch.FullMomentTensor_SOCAL.py](https://github.com/thurinj/mtuq_workshop_2022/blob/main/GridSearch.FullMomentTensor_SOCAL.py)

## FK model files
We have also included 2 model files in order to generate FK databases. They contain the subsurface parameters used to compute custom green's function databases used in MTUQ. You can find them here:
- [scak](https://github.com/thurinj/mtuq_workshop_2022/blob/main/scak)
- [socal](https://github.com/thurinj/mtuq_workshop_2022/blob/main/scak)

Feel free to open them to have a look at the model parameters.

## Green's function by using FK
Using 1D models (hk, scak, socal) to generate Greens function
```shell
python create_FK_greens_hk.py
python create_FK_greens_scak.py
python create_FK_greens_socal.py 
```
