import enum
# Using enum class create enumerations
class Days(enum.Enum):
   Sun = "sun"
   Mon = "asd"
   Tue = "djf"

# print the enum member as a string
print ("The enum member as a string is : ",end="")
print (Days.Mon)

# print the enum member as a repr
print ("he enum member as a repr is : ",end="")
print (repr(Days.Sun))

# Check type of enum member
print ("The type of enum member is : ",end ="")
print (type(Days.Mon))

# print name of enum member
print ("The name of enum member is : ",end ="")
print (Days.Tue.name)
