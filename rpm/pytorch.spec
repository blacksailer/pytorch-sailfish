Name:          pytorch
Version:       1.3.0
Release:       0
Summary:       Collection of algorithms for deep learning
Group:         Development/Libraries
URL:           https://github.com/opencv
Source:        %{name}-%{version}.tar.gz
License:       BSD 
BuildRequires: libgflags-dev libgoogle-glog-dev libprotobuf-dev protobuf-compiler
BuildRequires: cmake python3-dev
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
OpenCV (Open Source Computer Vision) is a library of programming functions for real time computer vision.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
OpenCV (Open Source Computer Vision) is a library of programming functions for real time computer vision. 
This package contains static libraries and header files need for development.

%prep
%setup -q
%build

%install
export PYTORCH_BUILD_MOBILE=1
CAFFE2_ROOT="$( cd "$(dirname "$0")"/.. ; pwd -P)"
echo "Caffe2 path: $CAFFE2_ROOT"
BUILD_ROOT=${BUILD_ROOT:-"$CAFFE2_ROOT/build_mobile"}
INSTALL_PREFIX=${BUILD_ROOT}/install
cd $BUILD_ROOT

cmake -DCMAKE_INSTALL_PREFIX=/usr      \
      -DCMAKE_BUILD_TYPE=Release       \
      -DBUILD_CAFFE2_MOBILE=OFF \ 
      -DCMAKE_PREFIX_PATH=$(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())') \
      -DPYTHON_EXECUTABLE=$(python -c 'import sys; print(sys.executable)') \
      -DBUILD_CUSTOM_PROTOBUF=OFF \
      -DBUILD_SHARED_LIBS=OFF \
      -DUSE_CUDA=OFF \
      -DUSE_GFLAGS=OFF \
      -DUSE_OPENCV=OFF \
      -DUSE_LMDB=OFF \ 
      -DUSE_LEVELDB=OFF \ 
      -DUSE_MPI=OFF  \
      -DUSE_OPENMP=OFF
      -Wno-dev  ..


cmake --build . --target install


%clean
rm -rf "%{buildroot}"

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%exclude /usr/lib/debug
%exclude %{_datadir}/OpenCV/licenses/*
%{_bindir}/opencv_*
%{_libdir}/libopencv_*.so.*
%dir %{_datadir}/OpenCV

%files devel
%defattr(-,root,root)
%dir %{_includedir}/opencv
%{_includedir}/opencv/*
%dir %{_includedir}/opencv2
%{_includedir}/opencv2/*
%{_libdir}/libopencv_*.so
%{_libdir}/pkgconfig/opencv.pc
%{_datadir}/OpenCV/*.cmake
%{_datadir}/OpenCV/haarcascades/*
%{_datadir}/OpenCV/lbpcascades/*
%{_datadir}/OpenCV/valgrind.supp
%{_datadir}/OpenCV/valgrind_3rdparty.supp

%changelog