"""

Adapted from display_song.py code written by:
Thierry Bertin-Mahieux (2010) Columbia University
tb2332@columbia.edu

Extracts certain features from an hdf5 file

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import hdf5_getters
import numpy as np

def die_with_usage():
    """ HELP MENU """
    print 'extract_features.py'
    print 'usage:'
    print '   python extract_features.py <HDF5 file> <feature> [ <feature> ... ]'
    print 'example:'
    print '   python extract_features.py mysong.h5 danceability beat'
    print 'INPUTS'
    print '   <HDF5 file>  - any song / aggregate /summary file'
    print '   <song idx>   - if file contains many songs, specify one'
    print '                  starting at 0 (OPTIONAL)'
    print '   <feature>    - feature to extract'
    sys.exit(0)

if __name__ == '__main__':
    """ MAIN """

    # help menu
    if len(sys.argv) < 2:
        die_with_usage()

    # get params
    hdf5path = sys.argv[1]
    features = sys.argv[2:]

    # sanity check
    if not os.path.isfile(hdf5path):
        print 'ERROR: file',hdf5path,'does not exist.'
        sys.exit(0)
    h5 = hdf5_getters.open_h5_file_read(hdf5path)
    numSongs = hdf5_getters.get_num_songs(h5)

    print >> sys.stderr, "Extracting features %s from %d songs" % (",".join(features), numSongs)

    getters = filter(lambda x: x[:4] == 'get_' and x[4:] in set(features), hdf5_getters.__dict__.keys())
    if "get_num_songs" in getters:
      getters.remove("get_num_songs")

    if len(getters) != len(features):
      print >> sys.stderr, 'ERROR: specified invalid getter:'
      h5.close()
      sys.exit(0)

    cnt = 0
    for songidx in range(numSongs):
      print >> sys.stderr, "Extracting features from song %d" % songidx
      print "%d" % cnt,
      cnt = cnt + 1
      # print them in csv form
      for feature in features:
        print "",
        try:
          res = hdf5_getters.__getattribute__('get_' + feature)(h5,songidx)
        except AttributeError, e:
          print >> sys.stderr, e
          print >> sys.stderr, 'specified wrong getter?'

        if res.__class__.__name__ == 'ndarray' and res.dtype == np.float64:
          np.savetxt(sys.stdout, res, fmt="%0.6f", newline="", delimiter="")
        elif res.__class__.__name__ == 'ndarray':
          np.savetxt(sys.stdout, res, fmt="%s", newline="", delimiter="")
        else:
          print res,
      print

    print >> sys.stderr, 'DONE, showed %d songs' % cnt
    h5.close()
    
