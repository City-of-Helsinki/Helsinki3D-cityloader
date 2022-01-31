@echo off
set leftcornerx=%1
set leftcornery=%2
set rightcornerx=%3
set rightcornery=%4
set lod=%5
blender --background --python %~dp0/install_required_packages.py
blender --background --python %~dp0/city_miniature_loader.py %leftcornerx% %leftcornery% %rightcornerx% %rightcornery% %lod%
blender --background --python %~dp0/generate_city_model.py %leftcornerx% %leftcornery% %rightcornerx% %rightcornery% %lod%