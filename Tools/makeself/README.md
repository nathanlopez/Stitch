# makeself - Make self-extractable archives on Unix

[makeself.sh][1] is a small shell script that generates a self-extractable
compressed tar archive from a directory. The resulting file appears as a shell script
(many of those have a **.run** suffix), and can be launched as is. The archive
will then uncompress itself to a temporary directory and an optional arbitrary
command will be executed (for example an installation script). This is pretty
similar to archives generated with WinZip Self-Extractor in the Windows world.
Makeself archives also include checksums for integrity self-validation (CRC
and/or MD5 checksums).

The makeself.sh script itself is used only to create the archives from a
directory of files. The resultant archive is actually a compressed (using
gzip, bzip2, or compress) TAR archive, with a small shell script stub at the
beginning. This small stub performs all the steps of extracting the files,
running the embedded command, and removing the temporary files when done.
All the user has to do to install the software contained in such an
archive is to "run" the archive, i.e **sh nice-software.run**. I recommend
using the ".run" (which was introduced by some Makeself archives released by
Loki Software) or ".sh" suffix for such archives not to confuse the users,
so that they will know they are actually shell scripts (with quite a lot of binary data
attached to them though!).

I am trying to keep the code of this script as portable as possible, i.e it is
not relying on any bash-specific features and only calls commands that are
installed on any functioning UNIX-compatible system. This script as well as
the archives it generates should run on any Unix flavor, with any compatible
Bourne shell, provided of course that the compression programs are available.

As of version 2.1, Makeself has been rewritten and tested on the following
platforms :

  * Linux (all distributions)
  * Sun Solaris (8 and above)
  * HP-UX (tested on 11.0 and 11i on HPPA RISC)
  * SCO OpenUnix and OpenServer
  * IBM AIX 5.1L
  * MacOS X (Darwin)
  * SGI IRIX 6.5
  * FreeBSD
  * UnicOS / Cray
  * Cygwin (Windows)

If you successfully run Makeself and/or archives created with it on another
system, then please [let me know][2]!

Examples of publicly available archives made using makeself are :

  * Game patches and installers for [Id Software][3] games like Quake 3 for Linux or Return To Castle Wolfenstein ;
  * All game patches released by [Loki Software][4] for the Linux version of popular games ;
  * The [nVidia drivers][5] for Linux
  * The installer for the Linux version of [Google Earth][6]
  * The [VirtualBox][7] installers for Linux
  * The [Makeself][1] distribution itself ;-)
  * and countless others...

**Important note for Apache users:** By default, most Web servers will think that Makeself archives are regular text files and thus they may show up as text in a Web browser. The correct way to prevent this is to add a MIME type for this file format, like so (in httpd.conf) :

`AddType application/x-makeself .run`

**Important note for certain GNU/Linux distributions:** Archives created with Makeself prior to v2.1.2 were using an old syntax for the _head_ and _tail_ Unix commands that is being progressively obsoleted in their GNU forms. Therefore you may have problems uncompressing some of these archives. A workaround for this is to set the environment variable $_POSIX2_VERSION to enable the old syntax, i.e. :

`export _POSIX2_VERSION=199209`

## Usage

The syntax of makeself is the following:

`makeself.sh [args] archive_dir file_name label startup_script [script_args]`

  * _args_ are optional options for Makeself. The available ones are :

    * **--version** : Prints the version number on stdout, then exits immediately
    * **--gzip** : Use gzip for compression (the default on platforms on which gzip is commonly available, like Linux)
    * **--bzip2** : Use bzip2 instead of gzip for better compression. The bzip2 command must be available in the command path. It is recommended that the archive prefix be set to something like '.bz2.run', so that potential users know that they'll need bzip2 to extract it.
    * **--pbzip2** : Use pbzip2 instead of gzip for better and faster compression on machines having multiple CPUs. The pbzip2 command must be available in the command path. It is recommended that the archive prefix be set to something like '.bz2.run', so that potential users know that they'll need bzip2 to extract it.
    * **--xz** : Use xz instead of gzip for better compression. The xz command must be available in the command path. It is recommended that the archive prefix be set to something like '.xz.run' for the archive, so that potential users know that they'll need xz to extract it.
    * **--lzo** : Use lzop instead of gzip for better compression. The lzop command must be available in the command path. It is recommended that the archive prefix be set to something like '.lzo.run' for the archive, so that potential users know that they'll need lzop to extract it.
    * **--lz4** : Use lz4 instead of gzip for better compression. The lz4 command must be available in the command path. It is recommended that the archive prefix be set to something like '.lz4.run' for the archive, so that potential users know that they'll need lz4 to extract it.
    * **--base64** : Encode the archive to ASCII in Base64 format (base64 command required).
    * **--gpg-encrypt** : Encrypt the archive using "gpg -ac -z $COMPRESS_LEVEL". This will prompt for a password to encrypt with. Assumes that potential users have gpg installed.
    * **--ssl-encrypt** : Encrypt the archive using "openssl aes-256-cbc -a -salt". This will prompt for a password to encrypt with. Assumes that the potential users have openssl installed. 
    * **--compress** : Use the UNIX "compress" command to compress the data. This should be the default on all platforms that don't have gzip available.
    * **--nocomp** : Do not use any compression for the archive, which will then be an uncompressed TAR.
    * **--complevel** : Specify the compression level for gzip,bzip2,pbzip2,xz,lzo or lz4. (default to 9)
    * **--notemp** : The generated archive will not extract the files to a temporary directory, but in a new directory created in the current directory. This is better to distribute software packages that may extract and compile by themselves (i.e. launch the compilation through the embedded script).
    * **--current** : Files will be extracted to the current directory, instead of in a subdirectory. This option implies **--notemp** above.
    * **--follow** : Follow the symbolic links inside of the archive directory, i.e. store the files that are being pointed to instead of the links themselves.
    * **--append** _(new in 2.1.x)_: Append data to an existing archive, instead of creating a new one. In this mode, the settings from the original archive are reused (compression type, label, embedded script), and thus don't need to be specified again on the command line.
    * **--header** : Makeself 2.0 uses a separate file to store the header stub, called "makeself-header.sh". By default, it is assumed that it is stored in the same location as makeself.sh. This option can be used to specify its actual location if it is stored someplace else.
    * **--copy** : Upon extraction, the archive will first extract itself to a temporary directory. The main application of this is to allow self-contained installers stored in a Makeself archive on a CD, when the installer program will later need to unmount the CD and allow a new one to be inserted. This prevents "Filesystem busy" errors for installers that span multiple CDs.
    * **--nox11** : Disable the automatic spawning of a new terminal in X11.
    * **--nowait** : When executed from a new X11 terminal, disable the user prompt at the end of the script execution.
    * **--nomd5** and **--nocrc** : Disable the creation of a MD5 / CRC checksum for the archive. This speeds up the extraction process if integrity checking is not necessary.
    * **--lsm _file_** : Provide and LSM file to makeself, that will be embedded in the generated archive. LSM files are describing a software package in a way that is easily parseable. The LSM entry can then be later retrieved using the '-lsm' argument to the archive. An exemple of a LSM file is provided with Makeself.
    * **--tar-extra opt** : Append more options to the tar command line.
    * **--keep-umask** : Keep the umask set to shell default, rather than overriding when executing self-extracting archive.
  * _archive_dir_ is the name of the directory that contains the files to be archived
  * _file_name_ is the name of the archive to be created
  * _label_ is an arbitrary text string describing the package. It will be displayed while extracting the files.
  * _startup_script_ is the command to be executed _from within_ the directory of extracted files. Thus, if you wish to execute a program contain in this directory, you must prefix your command with "./". For example, ./program will be fine. The _script_args_ are additionnal arguments for this command.

Here is an example, assuming the user has a package image stored in a
**/home/joe/mysoft**, and he wants to generate a self-extracting package named
**mysoft.sh**, which will launch the "setup" script initially stored in
/home/joe/mysoft :

`makeself.sh /home/joe/mysoft mysoft.sh "Joe's Nice Software Package" ./setup
`

Here is also how I created the [makeself.run][1] archive which contains the
Makeself distribution :

`makeself.sh --notemp makeself makeself.run "Makeself by Stephane Peter" echo
"Makeself has extracted itself" `

Archives generated with Makeself 2.1 can be passed the following arguments:

  * _--keep_ : Prevent the files to be extracted in a temporary directory that will be removed after the embedded script's execution. The files will then be extracted in the current working directory and will stay here until you remove them.
  * _--verbose_ : Will prompt the user before executing the embedded command
  * _--target dir_ : Allows to extract the archive in an arbitrary place.
  * _--nox11_ : Do not spawn a X11 terminal.
  * _--confirm_ : Prompt the user for confirmation before running the embedded command.
  * _--info_ : Print out general information about the archive (does not extract).
  * _--lsm_ : Print out the LSM entry, if it is present.
  * _--list_ : List the files in the archive.
  * _--check_ : Check the archive for integrity using the embedded checksums. Does not extract the archive.
  * _--nochown_ : By default, a "chown -R" command is run on the target directory after extraction, so that all files belong to the current user. This is mostly needed if you are running as root, as tar will then try to recreate the initial user ownerships. You may disable this behavior with this flag.
  * _--tar_ : Run the tar command on the contents of the archive, using the following arguments as parameter for the command.
  * _--noexec_ : Do not run the embedded script after extraction.

Any subsequent arguments to the archive will be passed as additional arguments
to the embedded command. You must explicitly use the _--_ special command-
line construct before any such options to make sure that Makeself will not try
to interpret them.

## License

Makeself is covered by the [GNU General Public License][8] (GPL) version 2 and
above. Archives generated by Makeself don't have to be placed under this
license (although I encourage it ;-)), since the archive itself is merely data
for Makeself.

## Download

Get the latest official distribution [here][9] (version 2.2.0).

The latest development version can be grabbed from [GitHub][10]. Feel free to
submit any patches there through the fork and pull request process.

## Version history

  * **v1.0:** Initial public release
  * **v1.1:** The archive can be passed parameters that will be passed on to the embedded script, thanks to John C. Quillan
  * **v1.2:** Cosmetic updates, support for bzip2 compression and non-temporary archives. Many ideas thanks to Francois Petitjean.
  * **v1.3:** More patches from Bjarni R. Einarsson and Francois Petitjean: Support for no compression (--nocomp), script is no longer mandatory, automatic launch in an xterm, optional verbose output, and -target archive option to indicate where to extract the files.
  * **v1.4:** Many patches from Francois Petitjean: improved UNIX compatibility, automatic integrity checking, support of LSM files to get info on the package at run time..
  * **v1.5.x:** A lot of bugfixes, and many other patches, including automatic verification through the usage of checksums. Version 1.5.5 was the stable release for a long time, even though the Web page didn't get updated ;-). Makeself was also officially made a part of the [Loki Setup installer][11], and its source is being maintained as part of this package.
  * **v2.0:** Complete internal rewrite of Makeself. The command-line parsing was vastly improved, the overall maintenance of the package was greatly improved by separating the stub from makeself.sh. Also Makeself was ported and tested to a variety of Unix platforms.
  * **v2.0.1:** First public release of the new 2.0 branch. Prior versions are officially obsoleted. This release introduced the '--copy' argument that was introduced in response to a need for the [UT2K3][12] Linux installer.
  * **v2.1.0:** Big change : Makeself can now support multiple embedded tarballs, each stored separately with their own checksums. An existing archive can be updated with the --append flag. Checksums are also better managed, and the --nochown option for archives appeared.
  * **v2.1.1:** Fixes related to the Unix compression (compress command). Some Linux distributions made the insane choice to make it unavailable, even though gzip is capable of uncompressing these files, plus some more bugfixes in the extraction and checksum code.
  * **v2.1.2:** Some bug fixes. Use head -n to avoid problems with POSIX conformance.
  * **v2.1.3:** Bug fixes with the command line when spawning terminals. Added --tar, --noexec for archives. Added --nomd5 and --nocrc to avoid creating checksums in archives. The embedded script is now run through "eval". The --info output now includes the command used to create the archive. A man page was contributed by Bartosz Fenski.
  * **v2.1.4:** Fixed --info output. Generate random directory name when extracting files to . to avoid problems. Better handling of errors with wrong permissions for the directory containing the files. Avoid some race conditions, Unset the $CDPATH variable to avoid problems if it is set. Better handling of dot files in the archive directory.
  * **v2.1.5:** Made the md5sum detection consistent with the header code. Check for the presence of the archive directory. Added --encrypt for symmetric encryption through gpg (Eric Windisch). Added support for the digest command on Solaris 10 for MD5 checksums. Check for available disk space before extracting to the target directory (Andreas Schweitzer). Allow extraction to run asynchronously (patch by Peter Hatch). Use file descriptors internally to avoid error messages (patch by Kay Tiong Khoo).
  * **v2.1.6:** Replaced one dot per file progress with a realtime progress percentage and a spining cursor. Added --noprogress to prevent showing the progress during the decompression. Added --target dir to allow extracting directly to a target directory. (Guy Baconniere)
  * **v2.2.0:** First major new release in years! Includes many bugfixes and user contributions. Please look at the [project page on Github][10] for all the details.

## Links

  * Check out the ["Loki Setup"][11] installer, used to install many Linux games and other applications, and of which I am the co-author. Since the demise of Loki, I am now the official maintainer of the project, and it is now being hosted on [icculus.org][13], as well as a bunch of other ex-Loki projects (and a lot of other good stuff!).
  * Bjarni R. Einarsson also wrote the **setup.sh** installer script, inspired by Makeself. [Check it out !][14]

## Contact

This script was written by [Stéphane Peter][2] (megastep at megastep.org). Any enhancements and suggestions are welcome.

Contributions were included from John C. Quillan, Bjarni R. Einarsson,
Francois Petitjean, Ryan C. Gordon, and many contributors on GitHub. If you think I forgot
your name, don't hesitate to contact me.

This project is now hosted on GitHub. Feel free to submit patches and bug reports on the [project page][10].

* * *

[Stephane Peter][2]

   [1]: makeself.run
   [2]: mailto:megastep@megastep.org
   [3]: http://www.idsoftware.com/
   [4]: http://www.lokigames.com/products/myth2/updates.php3
   [5]: http://www.nvidia.com/
   [6]: http://earth.google.com/
   [7]: http://www.virtualbox.org/
   [8]: http://www.gnu.org/copyleft/gpl.html
   [9]: http://cdn.megastep.org/makeself/makeself-2.2.0.run
   [10]: http://github.com/megastep/makeself
   [11]: http://www.icculus.org/loki_setup/
   [12]: http://www.unrealtournament2003.com/
   [13]: http://www.icculus.org/
   [14]: http://bre.klaki.net/programs/setup.sh/
