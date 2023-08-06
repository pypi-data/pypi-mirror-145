try:
    from main import ClassA, ClassB
except:
    try:
        from pyInet import ClassA, ClassB
    except:
        from pyInet.main import ClassA, ClassB
        
if __name__ == "__main__":
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

      ipv4 = "192.230.212.159"
      ipv6 = "f18d:5980:50d1:cf2d:b204:dc2:ad87:6a58"

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


