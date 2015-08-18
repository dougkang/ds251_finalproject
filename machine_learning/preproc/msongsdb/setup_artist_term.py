import argparse
import sqlite3

def get_tags(conn):
  d = {}
  c = conn.cursor()
  for row in c.execute("SELECT artist_id, term FROM artist_term"):
    (artist_id, term) = row
    if artist_id not in d:
      d[artist_id] = []
    d[artist_id].append(term)
  return d

def output(d, out):
  with open(out, "w") as f:
    for k,v in d.iteritems():
      f.write("%s\t%s\n" % (k, "\t".join(v)))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Preprocess artist metadata')
  parser.add_argument('input', metavar='<input>', type=str,
                         help='input sqlite db')
  parser.add_argument('output', metavar='<output>', type=str,
                         help='output file')
  args = parser.parse_args()

  print "Connecting to %s" % args.input
  conn = sqlite3.connect(args.input)
  tags = get_tags(conn)

  print "Outputting %d artists to %s" % (len(tags), args.input)
  output(tags, args.output)

  print "Complete!"
