# encoding: utf-8

import os

import roms

def path_is_higan_gen(path):
  """
  We want to ignore all higan generated files since we can just launch
  higan roms via the folder (rom_name.sf(c)). These files include:
    - program.rom
    - ines.rom
    - character.rom
    - cx4.data.rom
    - save.ram
  As you can probably tell, there is a common pattern here: they all
  end with ".rom", so we'll just look for that.
  NOTE: Except for save.ram, so we'll check for .ram too
  """

  path_check = path[-4] + path[-3] + path[-2] + path[-1]

  # print path <-- debug info
  # print path_check

  return (path_check == ".rom" or path_check == ".ram")

def console_roms_directory(configuration, console):
  """
  If the user has specified a custom ROMs directory in consoles.txt then
  return that.

  Otherwise, append the shortname of the console to the default ROMs
  directory given by config.txt.
  """
  if console.custom_roms_directory:
    return console.custom_roms_directory
  return os.path.join(roms.roms_directory(configuration), console.shortname)

def path_is_rom(console, path):
  """
  This function determines if a given path is actually a valid ROM file.
  If a list of extensions is supplied for this console, we check if the path has a valid extension
  If no extensions are defined for this console, we just accept any file
  """
  if path_is_higan_gen(path):
    return False;

  if console.extensions == "":
    return True

  # Normalize the extension based on the things we validly ignore.
  # Aka capitalization, whitespace, and leading dots
  normalize = lambda ext: ext.lower().strip().lstrip('.')

  (name, ext) = os.path.splitext(path)
  valid_extensions = console.extensions.split(',')
  return normalize(ext) in map(normalize, valid_extensions)
