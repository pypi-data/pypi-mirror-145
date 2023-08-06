# lesscli
> A dead simple library for generating CLI  
> 「嘞是CLI」

CLI = command line interfaces

## Install
For both python2 and python3 : `pip install lesscli`

## Usage of `lesscli.run(callback, single='')`
```
$ cat index.py:
    import lesscli
    def work(*a, **b):
        print(a, b)
    lesscli.run(work, single='ab')

$ python index.py a b
    ('a', 'b') {}

$ python index.py -a 1 -b
    ('1',) {'a': '', 'b': ''}

$ python index.py -a 1 --bob=2 c.txt
    ('1', 'c.txt') {'a': '', 'bob': '2'}

$ python index.py --bob -o c.txt d.txt
    ('d.txt',) {'bob': '', 'o': 'c.txt'}

$ python index.py -a 1 -c 2 -d -e
    ('1',) {'a': '', 'c': '2', 'd': '', 'e': ''}

$ python index.py --bob='1 2' -c " 3 " ''
    ('',) {'bob': '1 2', 'c': ' 3 '}
```

## lesscli command: show help information
```
$ lesscli

    
    Boilerplate of Installable Project:
        git clone https://github.com/qorzj/lesscli.git

    Documentation of "Writing the Setup Script":
        https://docs.python.org/2/distutils/setupscript.html
        https://docs.python.org/3/distutils/setupscript.html

    Documentation of lesscli.run:
        >>> import lesscli
        >>> help(lesscli.run)


```