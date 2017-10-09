![Artist-Critic A.I.](https://raw.githubusercontent.com/scottmudge/scottmudge.github.io/master/orchestrion_smallest.png)

Artist-Critic A.I. aimed at autonomous composition of musical pieces, featuring weighted genres and unsupervised learning of stochastic style. 

## What is it?
***Orchestrion*** aims to merge two models of artificial intelligence -- supervised learning [Critic] and unsupervised learning [Artist]. The former [Critic] will be trained to differentiate "good" musical compositions of a specific genre (e.g., jazz) from others and from entirely stochastic musical pieces. The other [Artist] will be trained by the critic to compose music of a specific genre, or weighted mixture of genres, in an unsupervised fashion. 

The end result are (hopefully) novel musical compositions unfettered by impressions of existing works normally created during supervised learning, and also the ability to blend genres by using multiple, weighted genre-specific Critic models to create entirely new musical genres.

In addition to the specific notes, note lengths, velocities, and other standard musical parameters, the Artist A.I. will determine other compositional features, including:

* Tempo (including any desired changes)
* Instrument Selection (permitted within the standard midi catalog)

**Orchestrion** is still in **very** early development, so there may not be much in terms of results for quite some time.

## Requirements

* TensorFlow >= v1.3
   * Compiled w/ GPU for fast training, AVX/AVX2 for even faster training. 
        * Compiling w/ AVX support on Windows is difficult. To install a prebuilt
        package of TensorFlow v1.3.1 with AVX/AVX2 and GPU support (CUDA compute capability 5.2 and 6.1), 
        run the following in your Anaconda (>=v5.0.0 w/ Python 3.6) console:
            
            ``` pip install http://scottmudge.com/files/tensorflow_gpu-1.3.1-cp36-cp36m-win_amd64.whl ```
        
        * You may also use the standard release (v1.3) from TensorFlow/Google, but it lacks AVX/AVX2 support, and is not compiled with CUDA compute capability 6.1 support.
        
            
* Anaconda >= v5.0
   * w/ Python >= v3.6.2
* Mido >= v1.2.8


## Contributors

Scott Mudge

mail@scottmudge.com -- http://www.scottmudge.com

### License

Orchestrion is licensed under the GNU Affero General Public License v3.0

See LICENSE for more information.

--------

Orchestrion -- Artist-Critic A.I. 
Copyright (C) 2017  Scott Mudge 
