# TrackMo: An Animal Tracking Toolbox for Behavioral Experiments

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Key Features](#features)
4. [Citation](#citation)

## Installation <a name="installation"></a>

* Download and install Anaconda (Python 3.7) at [https://www.anaconda.com/products/individual](https://www.anaconda.com/products/individual) based on your operating system. For example, if you are a MacOS user, please download the *MacOS 64-Bit Command Line Installer*. This codebase is developed and tested on
a 2017 Macbook Pro with *3.1 GHz Intel Core i5* and *16 GB 2133 MHz LPDDR3* memory.

* Download this package via `git`:
    ```
    git clone https://github.com/zudi-lin/tracking_toolbox.git
    cd tracking_toolbox
    ```
    If `git` is not installed in your machine, download it at [https://git-scm.com/downloads](https://git-scm.com/downloads).

* Create a new conda environment by running:
    ```
    conda create -n tracking python=3.7 jupyter 
    source activate tracking
    conda install ffmpeg
    pip install -r requirements.txt
    ```

* To watch the video before/after processing, we recommend the open-source portable VLC media player, which can be downloaded at [https://www.videolan.org/vlc/index.html](https://www.videolan.org/vlc/index.html).

## Key Features <a name="features"></a>

1. Run all processing using a single Jupyter notebook.
2. Support video trimming and interactive video cropping.
3. Support parallelism with Python `multiprocessing`.


## Quick Start <a name="quick-start"></a>

* If the virtual env is not activated, run `source activate tracking`.
* If you are not in the `tracking_toolbox` folder, navigate to the folder.
* Run `jupyter notebook` and open `tracking_parallel.ipynb` (please use `which jupyter` to check if the jupyter in this virtual env is being used).
* For earlier version of the notebooks check `/others`.

## Citation <a name="citation"></a>
If you find **TrackMo** useful in your research, please cite:

```bibtex
@misc{lin2019trackmo,
  author =       {Zudi Lin},
  title =        {TraceMo: An Animal Tracking Toolbox for Behavioral Experiments},
  howpublished = {\url{https://github.com/zudi-lin/tracking_toolbox}},
  year =         {2020}
}
```
