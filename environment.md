# environment settings
  1. linux setting(ubuntu)
  2. miniconda(linux system)
  3. tensorflow
      ````
      - conda install -c anaconda cudatoolkit
      - conda install -c anaconda cudnn
      - conda install -c anaconda tensorflow-gpu
      ````
  4. [pytorch(Just in Ubuntu)](https://pytorch.org/tutorials/)
      ````
      - conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
      - 
      ````
  5. [scikit-learn](https://scikit-learn.org/stable/auto_examples/index.html)
      ````
      - pip3 install -U scikit-learn
      ````
  6. [rapids](https://docs.rapids.ai/start)
      ````
      - conda create -n rapids-22.04 -c rapidsai -c nvidia -c conda-forge \\
        rapids=22.04 python=3.8 cudatoolkit=11.5 dask-sql
      ````      
