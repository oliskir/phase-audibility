
# SRKW call experiments


## AR-exp-20220216

The folder [AR-exp-20220216](AR-exp-20220216) contains the results of an 
experiment involving a human analyst listening to phase-modified S19 calls created
with the [create_exp_s19.py](create_exp_s19.py) script using as input the call samples in 
[s19_examples](s19_examples) (which originate from the HALLO project).


## JK-exp-20220311

The folder [JK-exp-20220311](JK-exp-20220311) contains the results of an experiment involving a (different) 
human analyst listening to variety of phase-modified SRKW calls created
with the [create_exp_catalog.py](reate_exp_catalog.py) script, using as input the call samples 
in [orcasound_call_catalog](orcasound_call_catalog) (which originate from 
the [Ford-Osborne catalog](https://www.orcasound.net/FordOsborneVocabulary/_SouthernVocabularyTable.html)).

The outcome of the experiment may be summarized as follows,

 * The analyst had 0 false positives, i.e., they only detected a difference when there actually was one. Well done!

 * The analyst suggested that the phase modifications may be easier to detect for 1) calls that are perceptibly pulsed and/or 2) calls that the analyst is particularly familiar with. I think it would be very interesting to investigate these ideas further!

 * Based on the results of the experiment, I'd say there is perhaps a small loss of information by discarding the 
 complex phase (as measured by the human ear, at least), but the information that is retained in the magnitude 
 spectrogram should be sufficient for the neural net to still perform a very good discrimination between killer whale sounds.