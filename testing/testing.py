a = 1/3
b = int(1/3)
c = 10.3%1
#print(a, b, c)

d = 3
for i in range(d):
    print(i)

e = 5
for i in range(d, e): # range is only calculate once, before entering the loop
    print('fff')
    print(i)
    print('e is', e)
    e = e+5
    print('e is', e)


keywords = 'google'
url = ('https://newsapi.org/v2/everything?'
       'q=' + keywords + '&'
        'from=2018-10-13' + '&'
        'sortBy=popularity' + '&'
        'apiKey=443b379064a7437abceec0b03e215f72' + '&'
        )
print(url)


fl = 3.3
str = 'f' + str(int(fl))
print(type(str))
