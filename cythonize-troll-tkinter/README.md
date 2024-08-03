# Cythonize a small tkinter script

## Build process

```bash
pip install cython
# Use your desired compiler, for example MINGW on windows.
python setup.py build_ext --inplace --compiler=mingw32 --force
# PyInstaller package the module.
# First, recompile PyInstaller bootloaders.
git clone https://github.com/pyinstaller/pyinstaller --depth=100
cd pyinstaller/bootloader
# Again, use your desired compiler, for example MINGW(gcc)
python waf all --gcc -j21
cd ../../
pip3 install -e pyinstaller
# Next, package as executable.
pyinstaller --noconfirm --onefile --windowed --clean main.py --hidden-import=tkinter --hidden-import=tkinter.ttk
```

## How does it compared with pure python?

```bash
pyinstaller --noconfirm --onefile --windowed --clean troll.py
```

Nearly identical startup speed.
Larger file size compared with pure python.

## Conclusion

`Cython` is not suitable for small projects like this. It complicates the workflow and
brings nearly no benefit.
