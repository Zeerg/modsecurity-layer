# modsecurity-layer
A serverless modsecurity AWS lambda layer with OWASP CRS. Check the working POC in example/

## Building

To build run 

```
make build
```

No cache build can be done with 
```
make rebuild
```

Cleanup can be done with

```
make clean
```

## Deploy
```
make deploy
```

## References
https://github.com/actions-security/pymodsecurity

https://modsecurity.org/crs/

https://github.com/SpiderLabs/ModSecurity
