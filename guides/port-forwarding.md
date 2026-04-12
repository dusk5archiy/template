# Windows Port Forwarding

```bash
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=windows_port connectaddress=wsl_addr connectport=wsl_port
```

Check:

```bash
netsh interface portproxy show v4tov4
```

Delete:


```bash
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=windows_port
```
