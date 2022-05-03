Supplementary material workshop MTUQ 2022 for Iceland

EV4. 20140825161903000 :  Caldera Collapse  Mw. 4.3 event
SA. 20140828081339000 : Caldera Collapse  Mw. 5.3 event
SB. 20140826115645000 : Strike-slip Mw. 4.2 event triggered by dike propagation 

GridSearch.DoubleCouple_EV4.py: Double couple test EV4 event
GridSearch.DoubleCouple_SA.py: Double couple test SA event
GridSearch.DoubleCouple_SB.py: Double couple test SB event
GridSearch.FullMomentTensor_SA.py: Full MT test SA event
GridSearch.FullMomentTensor_SB.py: Full MT test SB event

********

Add these lines (from the Hashtag)to event_input_mtuq2022.py for dowloading the supplementary material data

# Iceland Event SA
    if iex == 5:
        ev_info.overwrite_ddir = 1
        ev_info.use_catalog = 0
        #CHANGE THIS vvvvvvvvv
        #
        ev_info.otime = obspy.UTCDateTime("2014-08-28T08:13:39.0")
        ev_info.min_dist = 50
        ev_info.max_dist = 300
        ev_info.tbefore_sec = 60
        ev_info.tafter_sec = 360
        #^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # RAW and ENZ files can be used when checking if you are receiving all possible data
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False
        
        # Network and Channel requests CHANGE THIS vvvvvvvv
        ev_info.network = 'Z7'
        ev_info.channel = 'HH?'
        #ev_info.station = 'MOFO,DYFE,VADA,KLUR,RIFR,ASK,DREK,LOKT,VIFE,SVAD,BRU,HRUR,BOTN,BRUN,UTYR,MIDF,FLAT,SKAF,HETO,MYVO,TOLI,LAUF,HALI,KOLL,HELI,KODA,ARNA,FAG,SVIN,K250'
        ev_info.station = 'VADA,RIFR,DREK,VIFE,SVAD,BRU,BOTN,UTYR,MIDF,SKAF,HETO,LAUF,FAG,SVIN,K250'
       
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # Event specific information CHANGE THIS vvvvvvvvvvvv
        ev_info.elat = 64.654
        ev_info.elon = -17.385
        ev_info.edep =  7000.0
        ev_info.emag = 5.3
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # scaling and resampling
        ev_info.resample_TF = True
        ev_info.resample_freq = 50
        # See iex == 1 for more info
        ev_info.scale_factor = 100
    
# Iceland Event SB
    if iex == 6:
        ev_info.overwrite_ddir = 1
        ev_info.use_catalog = 0
        #CHANGE THIS vvvvvvvvv
        #
        ev_info.otime = obspy.UTCDateTime("2014-08-26T11:56:45.0")
        ev_info.min_dist = 20
        ev_info.max_dist = 300
        ev_info.tbefore_sec = 60
        ev_info.tafter_sec = 360
        #^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # RAW and ENZ files can be used when checking if you are receiving all possible data
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False
        
        # Network and Channel requests CHANGE THIS vvvvvvvv
        ev_info.network = 'Z7'
        ev_info.channel = 'HH?'
        #ev_info.station = 'STAM,MOFO,EFJA,GODA,FJAS,OSKV,KLUR,DYFE,DJK,VIFE,LOKT,BJK,BRU,LOGR,MIDF,FLAT,KOLL,HVAF,KODA,SVIN,SKAF,K250,KALF,LAUF' 
        ev_info.station = 'FJAS,OSKV,KLUR,DYFE,DJK,VIFE,LOKT,BJK,BRU,MIDF,KOLL,KODA,SVIN,SKAF,K250,KALF,LAUF'
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # Event specific information CHANGE THIS vvvvvvvvvvvv
        ev_info.elat = 64.8
        ev_info.elon = -16.897
        ev_info.edep =  7000.0
        ev_info.emag = 4.2
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # scaling and resampling
        ev_info.resample_TF = True
        ev_info.resample_freq = 50
        # See iex == 1 for more info
        ev_info.scale_factor = 100
