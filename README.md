# Mouse Tracking Toolbox for Behavior Experiments

1. [Installation](#installation)
2. [Quick Start](#quick-start)

## Installation <a name="installation"></a>

* Download and install Anaconda (Python 3.7) at [https://www.anaconda.com/products/individual](https://www.anaconda.com/products/individual) based on your operating system. For example, if you are a MacOS user, please download the *MacOS 64-Bit Command Line Installer*.

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

## Quick Start <a name="quick-start"></a>

* If the virtual env is not activated, run `source activate tracking`.
* If you are not in the `tracking_toolbox` folder, navigate to the folder.
* Run `jupyter notebook` and open `tracking.ipynb` (please use `which jupyter` to check if the jupyter in this virtual env is being used).
