# 4it.me-api
Unfortunately this beautiful site(https://4it.me) doesn`t have open api, so I wrote this.


get_city_list(self,city:str)
This function returns you all found cities with given name
in returned data you can find codes of city they will be needed
for this function:
get_ip_list(self,city,id_net=None, id_nic=None)
So this function returnes ip adresses of the city

whois(self,target:str)
This function returnes information about domain or ip adress

port_scan(self,target:str,ports:list)
So this funtion allows you to check ports on the target
on behalf of the 4it.me server

other functions are just functons of 4it.me api 
