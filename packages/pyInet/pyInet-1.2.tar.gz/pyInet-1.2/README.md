# pyInet
Python module that works to manipulate IPv4/6 addresses, calculate Network/IP addresses. 
What you get:
1. ip validation by class or ip version
2. Generate IPv4/6, and Mac address bit by bit
3. Calculate IPv4/6
4. Light and fast
### Installation

- Pip

  ```python -V```

  - Windows:
  
    `python -m pip install pyInet`
  
  - Unix or Mac:
  
    `pip install pyInet`
  
- GIT

  - Windows, Unix and Mac:
  
    ````
       git clone https://github.com/LcfherShell/pyInet
       cd pyInet
       python -m pip install . or python setup.py
    ````
### Usage Example
```````````````````````````````````````````````
from pyInet import ClassA, ClassB
child = ClassA #Public Class
network = ClassB #Private Class

print("Call function using public class")
for i in range(3):
    for ipv4 in child.IPv4(i):
         print("IPv4:", ipv4)
    for ipv6 in child.IPv6(i):
         print("IPv6:", ipv6)
    print("MacAddresss:", child.MacAddresss(),"\n")
i = 0
print("\nCall function using private class")
for i in range(3):
    for ipv4 in network.IPv4(i):
         print("IPv4:", ipv4) 
    for ipv6 in network.IPv6(i):
         print("IPv6:", ipv6)
    print("MacAddresss:", network.MacAddresss(),"\n")

ipv4 = "192.222.02.00"
ipv6 = "f18d:5980:50d1::cf2d"

print("Check Version and Class Ip addresses")
print("IP version:", child.Validate_IP(ipv4))
print("IPv4 Class:",  child.IPv4_Class(ipv4))
print("\nIP version:", child.Validate_IP(ipv6))
print("IPv6 Class:",  child.IPv6_Class(ipv6))
print("\nManipulate IPv4 :")
for x in range(1, 33):
   child.IPv4_Calculator("{}/{}".format(ipv4, x))
   print(child.saving.output)
print("\nManipulate IPv6 :")
for y in range(0, 33):
   ipv6range = "{}/{}".format(ipv6, y)
child.IPv6_Calculator(ipv6range)
print(child.saving.output)

```````````````````````````````````````````````
You can find or find this module via this link:
<h4 align="left">
  <p align="left">
    <a href="https://pypi.org/user/alfiandecker2" target="blank">https://pypi.org/user/alfiandecker2/</a>
  </p>
  <p align="left">
    <a href="https://github.com/LcfherShell" target="blank">https://github.com/LcfherShell</a>
  </p>
</h4>

If you find any bugs/problems, please contact email:
      **LCFHERSHELL@TUTANOTA.COM** or **alfiandecker2@gmail.com**

Happy coding :). Sorry, my English is very bad
