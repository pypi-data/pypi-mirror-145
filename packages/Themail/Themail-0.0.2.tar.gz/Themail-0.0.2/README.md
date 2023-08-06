# Themail

## To install

```
pip install Themail
```

## To import the library

```
from themail import *
```

## Defining the sender, key, smtp and port  

```
email = Themail("<YOUR EMAIL>","<YOUR KEY>","<SMTP>","<PORT>")
```

## or null to use our email

```
email = Themail()
```

## Sending an email

```
send = email.send("<RECEIVER>","<SUBJECT>","<BODY>")
```

## Sending to more than one recipient

```
send = email.send(["<RECEIVER #1>","<RECEIVER #2>"],"<SUBJECT>","<BODY>")
```

## Get message

```
print(send)
```

## Links

See my [GitHub](https://github.com/claudiotorresarbe).