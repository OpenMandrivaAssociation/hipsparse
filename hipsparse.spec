# HIP sparse wrapper over rocSPARSE (TheRock 10.1)

Name:		hipsparse
Version:	10.1.0
Release:	1
Summary:	HIP sparse linear algebra (rocSPARSE wrapper)
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.1/hipsparse.tar.gz#/hipsparse-%{version}.tar.gz
# Clang 23 / freestanding headers: host memcpy not visible without <cstring>
Patch0:		0001-include-cstring.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	rocsparse-devel
BuildRequires:	python3


%description
hipSPARSE is a thin HIP API wrapper over rocSPARSE. GPU targets include gfx803.

%package devel
Summary:	Development files for hipsparse
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel
Requires:	rocsparse-devel
Provides:	hipsparse-devel = %{EVRD}

%description devel
Headers and CMake package for hipsparse.

%prep
%autosetup -n hipsparse -p1

export CXX=hipcc
export CC=clang
export ROCM_PATH=%{_prefix}
export HIP_PATH=%{_prefix}
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
export LDFLAGS=$(printf '%s' "%{?__global_ldflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DHIPSPARSE_ENABLE_CLIENT=OFF \
	-DHIPSPARSE_BUILD_TESTING=OFF \
	-DHIPSPARSE_BUILD_SHARED_LIBS=ON \
	-DHIPSPARSE_ENABLE_HIP=ON \
	-DHIPSPARSE_ENABLE_CUDA=OFF \
	-DHIPSPARSE_BUILD_DOCS=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/hipsparse ] && [ ! -d %{buildroot}%{_libdir}/cmake/hipsparse ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/hipsparse %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/hipsparse/LICENSE.md
%{_libdir}/libhipsparse.so.*

%files devel
%{_includedir}/hipsparse/
%{_libdir}/libhipsparse.so
%{_libdir}/cmake/hipsparse/
