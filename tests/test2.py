from disco import disco

business_name = "Hello World, llc."
print("Inputted Business Name: %s" % business_name)
x = disco(business_name)
print("Clean Name: %s" % x.clean_name())
print("Business Type: %s" % x.type())
print("Country: %s" % x.country())
