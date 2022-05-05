#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'SirHades696'
__email__ = 'djnonasrm@gmail.com'

class Subnetting:
    @staticmethod
    def subnetting_calc(ip):
        values_ip, dec_mask = Subnetting.transform_string(ip)
        n_class = Subnetting.net_class(values_ip)
        if n_class != 'Error':
            b = Subnetting.binary(values_ip)
            bin_m, wild, hosts = Subnetting.bin_wild_mask(Subnetting,dec_mask)

            dec_m = Subnetting.decimal(bin_m)
            wild_m = Subnetting.decimal(wild)

            net = Subnetting.network(b,bin_m)
            dec_net = Subnetting.decimal(net)
    
            b_min, b_max, b_bc = Subnetting.min_max_broadcast(net, wild)
            
            dec_min = Subnetting.decimal(b_min)
            dec_max = Subnetting.decimal(b_max)
            dec_bc = Subnetting.decimal(b_bc)
            
            addr = Subnetting.concat_values(values_ip) 
            bin_addr = Subnetting.concat_values(b)

            mask = Subnetting.concat_values(dec_m)
            bin_mask = Subnetting.concat_values(bin_m)

            wildcard = Subnetting.concat_values(wild_m)
            bin_wild = Subnetting.concat_values(wild)

            network = Subnetting.concat_values(dec_net)+'/'+dec_mask
            bin_net = Subnetting.concat_values(net)
            
            d_m = Subnetting.concat_values(dec_min)
            b_m = Subnetting.concat_values(b_min)
            
            d_mx = Subnetting.concat_values(dec_max)
            b_mx = Subnetting.concat_values(b_max)
            
            d_bc = Subnetting.concat_values(dec_bc)
            b_bct = Subnetting.concat_values(b_bc)
            
            values = [addr, bin_addr, mask, bin_mask,  wildcard, bin_wild, network, bin_net, hosts, n_class, d_m, b_m, d_mx, b_mx, d_bc, b_bct]

            return values
        else:
            return 'Network Address Error'
    @staticmethod
    def transform_string(ip):
        return ip.split('/')[0].split('.'), ip.split('/')[1]
         
    @staticmethod
    def binary(values):
        bin_values = []
        for i,value in enumerate(values):
            bin_values.append(bin(int(value)).replace('0b',''))
            while len(bin_values[i]) < 8:
                bin_values[i] = '0'+bin_values[i]
        return bin_values
    
    @staticmethod
    def decimal(values):
        d = []
        for value in values:
            d.append(str(int(value,2)))
        return d
    
    def bin_wild_mask(self,dec):
        b = ''
        wild = ''
        while len(b) < int(dec):
            b += '1'
        while len(b) < 32:
            b +='0'
            
        for i in b:
            if i == '1':
                wild += i.replace('1','0')
            else:
                wild += i.replace('0','1')
        bits = int(wild.count('1'))
        hosts = str((2**bits) - 2)
        return [b[i:i + 8] for i in range(0, 32, 8)], [wild[i:i + 8] for i in range(0, 32, 8)], hosts
    
    @staticmethod
    def network(bin_ip, bin_mask):
        b_ip = bin_ip[0]+bin_ip[1]+bin_ip[2]+bin_ip[3]
        b_mask = bin_mask[0]+bin_mask[1]+bin_mask[2]+bin_mask[3]
        net = ''
        for i in range(32):
            if b_ip[i]=='1' and b_mask[i] == '1':
                net += '1'
            else:
                net += '0'
        return [net[i:i + 8] for i in range(0, 32, 8)]
    
    @staticmethod
    def net_class(values):
        if (int(values[1]) >= 0  and int(values[1]) < 256) and (int(values[2]) >= 0 and int(values[2])<256) and (int(values[3]) >= 0 and int(values[3])<256):
            if int(values[0]) >= 0 and int(values[0])<128:
                return "Class A"
            elif int(values[0]) > 127 and int(values[0])<192:
                return "Class B"
            elif int(values[0]) > 191 and int(values[0])<224:
                return "Class C"
            elif int(values[0]) > 223 and int(values[0])<240:
                return "Class D"
            elif int(values[0]) > 239 and int(values[0])<256:
                return "Class E"
            else:
                return "Error"
        else:
            return "Error"
        
    @staticmethod
    def min_max_broadcast(network, wildcard):
        net = network[0]+network[1]+network[2]+network[3]
        wd = wildcard[0]+wildcard[1]+wildcard[2]+wildcard[3]
        bc = ''
        for i in range(32):
            if (net[i] == '0' and wd[i] == '1') or (net[i] == '1' and wd[i] == '0'):
                bc += '1'
            else:
                bc += '0'
        broadcast = [bc[i:i + 8] for i in range(0, 32, 8)] 
        max = broadcast.copy()
        max[3] = bin(int(max[3],2) - 1).replace('0b','')
        if int(max[3],2) == 256:
            max[3] = '00000000'
            max[2] = bin(int(max[2],2) - 1).replace('0b','')
        while len(max[3]) < 8:
            max[3] = '0'+ max[3]
        min = network.copy()
        min[3] = bin(int(min[3],2) + 1).replace('0b','')
        if int(min[3],2) == 256:
            min[3] = '00000000'
            min[2] = bin(int(min[2],2) + 1).replace('0b','')
                    
        while len(min[3]) < 8:
                min[3] = '0'+ min[3]
        return min, max, broadcast
    
    @staticmethod
    def concat_values(value):
        cadena = ''
        for i,c in enumerate(value):
            if i < 3:
                cadena += str(c) + '.'
            else:
                cadena +=str(c)
        return cadena
        
    def formatting_string(self,values):      
        print('{:<12} {:<16} {:<3} {:<16}'.format('Address: ', values[0], ' - ', values[1]))
        print('{:<12} {:<16} {:<3} {:<16}'.format('Netmask: ', values[2], ' - ', values[3]))
        print('{:<12} {:<16} {:<3} {:<16}'.format('Wildcard: ', values[4], ' - ', values[5]))
        print('{:<12} {:<16} {:<3} {:<16}'.format('Network: ', values[6], ' - ', values[7]))
        print('{:<12} {:<16} {:<3} {:<16}'.format('Broadcast: ', values[14], ' - ', values[15]))
        print('{:<12} {:<16} {:<3} {:<16}'.format('Hostmin: ', values[10], ' - ', values[11]))
        print('{:<12} {:<16} {:<3} {:<16}'.format('Hostmax: ', values[12], ' - ', values[13]))
        print('{:<12} {:<16}'.format('Hosts/Net:',values[8]))
        print('{:<12} {:<16}'.format('Type:',values[9]))