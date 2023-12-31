#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.
# $Revision: 458 $ -  $Date: 2008-01-31 15:48:40 +1030 (Thu, 31 Jan 2008) $ $Author: mlampard $

AC_INIT([g15daemon],[3.0.1],[dmenelkir@gmail.com])
AC_PREFIX_DEFAULT(/usr)
AC_CONFIG_AUX_DIR(config)
AC_CANONICAL_HOST()
AC_CANONICAL_TARGET()

AM_INIT_AUTOMAKE()
AC_CONFIG_HEADERS([config.h])

_LT_SET_OPTION([LT_INIT],[dlopen])

# Checks for programs.
AC_PROG_CC
LT_INIT

# Checks for libraries.
AC_CHECK_LIB([g15], [initLibG15],,AC_MSG_ERROR(["libg15 (or its devel package) not found. please install it"]))
AC_CHECK_LIB([g15render], [g15r_loadWbmpSplash],,AC_MSG_ERROR([">=libg15render-3.0 (or its devel package) not found.  please install it"]))
AC_CHECK_LIB([m], [sin])
AC_CHECK_LIB([pthread], [pthread_mutex_init])

AC_CHECK_FUNC(daemon,AC_DEFINE(HAVE_DAEMON,1,[Define if daemon() is available]),[])

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_TYPE_PID_T
AC_TYPE_SIZE_T

# Checks for library functions.
AC_PROG_GCC_TRADITIONAL
AC_FUNC_SELECT_ARGTYPES
AC_FUNC_STRFTIME
AC_CHECK_FUNCS([memset select socket strerror backtrace backtrace_symbols])

# Checks for header files.
AC_CHECK_INCLUDES_DEFAULT
AC_PROG_EGREP

AC_HEADER_SYS_WAIT
AC_CHECK_HEADERS([ linux/input.h ])
AC_CHECK_HEADERS([ execinfo.h ])
AC_CHECK_HEADERS([ linux/uinput.h ], [have_linux_uinput_h=yes],[have_linux_uinput_h=],[])
AC_CHECK_HEADERS([ arpa/inet.h fcntl.h stdlib.h string.h sys/socket.h unistd.h libg15.h],,,
[#if HAVE_LINUX_INPUT_H
#include <linux/input.h>
#endif
],,[])

AC_ARG_ENABLE([--disable-uinput],[  --disable-uinput	do not build linux uinput plugin (default: autodetect)])

if test "x$enable_uinput" != "xno"; then
  if test "x$have_linux_uinput_h" = "xyes"; then
    #if HAVE_LINUX_UINPUT_H 
	dnl check for uinput.h version 2.4 or 2.6 ?
	AC_CHECK_MEMBER([struct uinput_user_dev.id],
              [AC_DEFINE(HAVE_UINPUT_USER_DEV_ID, 1,
              [Define if struct uinput_user_dev has id member.])],,
              [
			#include <linux/input.h>
			#include <linux/uinput.h>
	      ]
	)
	uinput=true
	dnl end of uinput version checks
	AC_MSG_NOTICE([Necessary includes exist: Compiling Uinput Plugin])
	
    #endif
  else
	AC_MSG_NOTICE([Linux Specific Includes Not Found. NOT COMPILING UINPUT PLUGIN.])
  fi
else
  AC_MSG_NOTICE([Linux UINPUT plugin disabled by request.])
  uinput=false
fi

case $host_os in
	*linux*) 
	  AC_DEFINE([OSTYPE_LINUX], [1],[Target OS is Linux])
	  AC_MSG_NOTICE([OS is Linux, using uinput if available])
	  ;;
	*freebsd*)
	  AC_DEFINE([OSTYPE_FREEBSD], [1],[Target OS is FreeBSD])
	  AC_MSG_NOTICE([OS is FreeBSD, using uinput if available])
	  uinput=true
	  ;;
	*darwin*)
	  AC_DEFINE([OSTYPE_DARWIN], [1],[Target OS is Darwin])
	  AC_SUBST(KEXT_LOCATION,["/System/Library/Extensions/"])
	  AC_MSG_NOTICE([OS is Darwin, using OS specific workarounds])
          install_kext=true
	  uinput=false
	  ;;
        *solaris*)
          AC_DEFINE([OSTYPE_SOLARIS], [1],[Target OS is Solaris])
	  AC_SEARCH_LIBS([connect],socket,[],[],[])
	  AC_SEARCH_LIBS([gethostent],nsl,[],[],[])
	  AC_SEARCH_LIBS([inet_aton],resolv,[],[],[])
          AC_SEARCH_LIBS([nanosleep],rt,[],[],[])
	  AC_MSG_NOTICE([OS is Solaris, using OS specific workarounds])
	  uinput=false
	  libusb_blocks=true
          ;;
	*) 
	  AC_DEFINE([OSTYPE_OTHER], [1],[Target OS is unknown])
	  AC_MSG_NOTICE([Unknown OS type, your milage may vary....])
	  uinput=false
	  ;;
esac

AM_CONDITIONAL([KEXT_INSTALL], [test x$install_kext = xtrue])
AM_CONDITIONAL(UINPUT_INTERFACE_PLUGIN, [test x$uinput = xtrue])

dnl Some versions of libusb do not honour timeout and block. Suns' version is one of them.
if test "x$libusb_blocks" = "xtrue"; then 
      AC_DEFINE([LIBUSB_BLOCKS], [1],[Define if libusb implementation blocks on read or write])
fi

G15D_BUILD_CC="`$CC -v 2>&1 | tail -n 1`"
G15D_BUILD_OS="`uname -s -r -m`"
G15D_BUILD_DATE="`date \"+%a %d %b %Y %T\"`"

AC_DEFINE_UNQUOTED([BUILD_OS_NAME],"${G15D_BUILD_OS}",[Build OS Particulars])
AC_DEFINE_UNQUOTED([BUILD_DATE],"${G15D_BUILD_DATE}",[Date of compilation])
AC_DEFINE_UNQUOTED([COMPILER_VERSION],"${G15D_BUILD_CC}",[Compiler Version])

CPPFLAGS=$CPPFLAGS_save
CPPFLAGS="$CPPFLAGS "'-DDATADIR="\"$(datadir)\""'

AC_SUBST(G15DAEMON_PLUGIN_DIR,["$libdir/g15daemon/$PACKAGE_VERSION/plugins"])
CPPFLAGS="$CPPFLAGS "'-DPLUGINDIR=\"$(G15DAEMON_PLUGIN_DIR)\"'

CPPFLAGS="$CPPFLAGS "'-I$(includedir)'

AC_CONFIG_FILES([Makefile g15daemon/Makefile libg15daemon_client/Makefile plugins/Makefile])

AC_OUTPUT
