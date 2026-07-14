I use a Mac M2, and the installation of OpenUSD for MacOS involes cloning a Github repo. This can lead to lots of version and installation issues.  
_Keep your laptop plugged in.  
Also, your machine might heat up BTW._

1. I used Ninja for the build since Xcode was giving me issues.
   
2. In case you keep getting the error that xcode is required even though your command line tools are isntalled, you don't need to install the full app. Run the below code in your terminal. This gives a fake response to the repo, which is trying to run a check for xcode app installation, even though the official readme says that CLI tools will work. After this, the build script command should work.

```
mkdir -p ~/.xcode_hack
cat << 'EOF' > ~/.xcode_hack/xcodebuild
#!/bin/bash
echo "Xcode 15.0"
echo "Build version 15A240d"
EOF
chmod +x ~/.xcode_hack/xcodebuild
export PATH="$HOME/.xcode_hack:$PATH"
```

And when your build finally reaches the USD building phase, run the below. Because CMake will look for the xcode app otherwise. We just point it to the CLI headersin ourselves.
```
sudo ln -s /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Headers

python3 OpenUSD/build_scripts/build_usd.py ~/USD_Install --generator Ninja
```

2. Another issue I faced (and this might just be me) was with software updates. I had a full software update for my OS that was pending, only after I installed it did the xcode CLI install and get recognized properly. Note that after updates, you might have to reset or even reinstall some tools so going over the installation from scratch would save you time.

3. Recent update: the build scripts install their python bindings into site-packages instead of lib/python like they used to. so you can set path dynamically.
```
export PYTHONPATH="$(find /Users/{your home folder}/USD_Install/lib -name 'pxr' -type d -prune -exec dirname {} \;):$PYTHONPATH"
```


