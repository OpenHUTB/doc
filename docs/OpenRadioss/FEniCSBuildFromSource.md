## 环境
* C++ 编译器 (支持 C++20 标准)

        apt install build-essential
* Boost, with the following compiled Boost components

        apt install libboost-all-dev

* CMake [build dependency]

        // 安装特定版本
        sudo wget https://cmake.org/files/v3.27/cmake-3.27.0.tar.gz
        sudo tar -zxvf cmake-3.27.0.tar.gz
        cd cmake-3.27.0
        sudo ./configure
        sudo make
        sudo make install
        // 查看版本
        cmake --version

* pkg-config

        apt install pkgconf

* Basix

        // 建议使用 conda 创建新环境之后安装
        // 不使用pip install fenics-basix是因为从源码编译需要使用0.7版本，而上述命令是0.6版本
        pip install git+https://github.com/FEniCS/basix.git


* pugixml

        apt install pugixml-doc

* UFCx [ufcx.h, provided by FFCx]

    * pip 安装 
        * pip install fenics-ffcx
        * 此时安装的是0.6版本。从源码编译需要0.7版本
    * 从源码安装
        * git clone https://github.com/FEniCS/ffcx.git
        * pip install .
        * 此时编译失败=…=        

* MPI

        sudo apt-get install openmpi-bin openmpi-doc libopenmpi-dev

* HDF5 (with MPI support enabled)

        apt install libhdf5-mpi-dev

* PETSc 

        git clone -b release https://gitlab.com/petsc/petsc.git petsc
        ./configure
        // ./configure 后会提示如何make
        make PETSC_DIR=安装位置 PETSC_ARCH=arch-linux-c-debug all
        // 之后按提示check
        make PETSC_DIR=安装位置 PETSC_ARCH=arch-linux-c-debug check
        // 安装外部包mumps、
        apt install bison
        ./configure --download-mumps --download-scalapack --download-parmetis --download-metis --download-ptscotch
        // ./configure完提示make
        make PETSC_DIR=安装位置 PETSC_ARCH=arch-linux-c-debug all

* At least one of ParMETIS, KaHIP or PT-SCOTCH

        apt install libparmetis-dev
