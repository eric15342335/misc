// https://github.com/embeddedmz/16-Games/tree/master/05%20Minesweeper
// todo: make this script fully automatic

cmake -B build -S . -G "MinGW Makefiles" -DSFML_USE_STATIC_STD_LIBS=TRUE -DBUILD_SHARED_LIBS=FALSE -DCMAKE_BUILD_TYPE=DEBUG -DCMAKE_CXX_FLAGS="-g3 -march=sandybridge -mtune=native -O0"
cmake --build build
cmake --install build --prefix SFML

// abc

g++ main.cpp -g3 -march=sandybridge -mtune=native -O0 -isystem SFML/include -LSFML/lib -static -Wl,-Bstatic -lsfml-graphics-s -lsfml-window-s -lsfml-system-s -lopengl32 -lwinmm -lgdi32 -Wl,-subsystem,windows

// Release build with -flto -O3 -m*=native optimization
cmake -B build -S . -G "MinGW Makefiles" -DSFML_USE_STATIC_STD_LIBS=TRUE -DBUILD_SHARED_LIBS=FALSE -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_CXX_FLAGS="-s -march=haswell -mtune=native -Os -flto -ffat-lto-objects -D_FORTIFY_SOURCE=2 -fstack-protector-strong --no-ident -fPIC"
cmake --build build
cmake --install build --prefix SFML

g++ main.cpp -s -march=haswell -mtune=native -Os -flto -D_FORTIFY_SOURCE=2 -fstack-protector-strong -isystem SFML/include -LSFML/lib -static -Wl,-Bstatic -lsfml-graphics-s -lsfml-window-s -lsfml-system-s -lopengl32 -lwinmm -lgdi32 -Wl,-subsystem,windows