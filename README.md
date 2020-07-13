# Mouse Tracking Toolbox for Behavior Experiments

1. [Installation](#installation)
2. [Quick Start](#quick-start)

## Installation <a name="installation"></a>

* Download and install Anaconda (Python 3.7) at [https://www.anaconda.com/products/individual](https://www.anaconda.com/products/individual) based on your operating system. For example, if you are a MacOS user, please download the *MacOS 64-Bit Command Line Installer*.

* Create a new conda environment by running:
    ```
    conda create -n tracking python=3.7
    source activate tracking
    pip install -r requirements.txt
    ```

* Download this package:
    ```
    git clone https://github.com/zudi-lin/tracking_toolbox.git
    ```
    To process, open the package folder and put the videos into this folder. Then run `jupyter notebook`.

* To watch the video before/after processing, we recommend the open-source portable VLC media player, which can be downloaded at [https://www.videolan.org/vlc/index.html](https://www.videolan.org/vlc/index.html).

## Quick Start <a name="quick-start"></a>

Run `jupyter notebook` and open `tracking.ipynb`.
