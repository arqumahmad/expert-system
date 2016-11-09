import sqlite3

conn = sqlite3.connect('codes.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Countries''')

cur.execute('''
CREATE TABLE Countries (codes VARCHAR(3), country VARCHAR(20))''')


fh = open("countryList.txt", "r")
for line in fh:
    codes = line[:2]
    country = line[3:]



    cur.execute('SELECT country FROM Countries WHERE codes = ? ', (codes, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Countries (codes, country)
                VALUES ( ?,? )''', ( codes,country ) )

    # This statement commits outstanding changes to disk each
    # time through the loop - the program can be made faster
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT codes, country FROM Countries ORDER BY country'

print
print "Countries:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()
