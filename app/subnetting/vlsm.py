# -*- coding: utf-8 -*-
__author__ = 'SirHades696'
__email__ = 'djnonasrm@gmail.com'

from app.subnetting.subnetting import Subnetting

class VLSM:
    @staticmethod
    def vlsm_calc(ip:str, req_hosts:list):
        values_ip, dec_mask, req_hosts = VLSM.transform_strings(ip, req_hosts)
        clase = Subnetting.net_class(values_ip)
        if clase != 'Error':
            bin_ip = Subnetting.binary(values_ip)
            bin_mask, bin_wc, tb = VLSM.mask_wildcard(dec_mask)
            bin_netw = Subnetting.network(bin_ip, bin_mask)
            ctrl_bits, alloc_p = VLSM.get_n_bits(bin_wc,req_hosts)
            treq = sum(req_hosts)
            tn = 2**tb
            if ctrl_bits != 'Error':
                net = VLSM.sub_vlsm(VLSM,bin_netw,ctrl_bits)
                #VLSM.formatting_string(VLSM,net)
                return net, tn, treq, alloc_p
            else:
                return 'Subnetting Failed'
            
        else:
            return 'Network Address Error', '', '', ''
            
    def sub_vlsm(self, bin_netw, ctrl_bits):
        networks = {}
        dec_net = Subnetting.decimal(bin_netw)
        min, max, broadcast = Subnetting.min_max_broadcast(bin_netw, ctrl_bits[0][0][1])
        d_min = Subnetting.decimal(min)
        d_max = Subnetting.decimal(max)
        d_bc = Subnetting.decimal(broadcast)
        
        networks[1] = [ctrl_bits[0][2], #need size
                       ctrl_bits[0][3], #allocated size
                       Subnetting.concat_values(dec_net), #addres,
                       '/' + str(ctrl_bits[0][1]), #mask
                       Subnetting.concat_values(Subnetting.decimal(ctrl_bits[0][0][0])), #dec mask
                       Subnetting.concat_values(d_min), #assig_range_min
                       Subnetting.concat_values(d_max), #Assignable range max
                       Subnetting.concat_values(d_bc) #broadcast
                       ]
        
        for i in range(1,len(ctrl_bits)):
            new_addr = broadcast
            new_addr[3] = bin(int(new_addr[3],2) + 1).replace('0b','')
            if int(new_addr[3],2) == 256:
                new_addr[3] = '00000000'
                new_addr[2] = bin(int(new_addr[2],2) + 1).replace('0b','')
                
            while len(new_addr[3]) < 8:
                new_addr[3] = '0'+ new_addr[3]
                
            while len(new_addr[2]) < 8:
                new_addr[2] = '0'+ new_addr[2]
                
            bin_netw = Subnetting.network(new_addr,ctrl_bits[i][0][0])
            dec_net = Subnetting.decimal(new_addr)
            min, max, broadcast = Subnetting.min_max_broadcast(bin_netw, ctrl_bits[i][0][1])
            d_min = Subnetting.decimal(min)
            d_max = Subnetting.decimal(max)
            d_bc = Subnetting.decimal(broadcast)
            broadcast = broadcast.copy()
            
            networks[i+1] = [ctrl_bits[i][2], #need size
                       ctrl_bits[i][3], #allocated size
                       Subnetting.concat_values(dec_net), #addres,
                       '/' + str(ctrl_bits[i][1]), #mask
                       Subnetting.concat_values(Subnetting.decimal(ctrl_bits[i][0][0])), #dec mask
                       Subnetting.concat_values(d_min), #Assignable range min
                       Subnetting.concat_values(d_max), #Assignable range max
                       Subnetting.concat_values(d_bc) #broadcast
                       ]
        
        return networks
    
    def formatting_string(self, networks):
        print("{:<14} {:<12} {:<15} {:<16} {:<5} {:<16} {:<35} {:<16}".format(
            'Subnet Number','Needed Size','Allocated Size','Address', 'Mask', 'Dec Mask', 'Assignable Range', 'Broadcast'))
        for i,v in networks.items():
            n_size, alloc, addr, mask, dec_mask, assig_range_min, assig_range_max, bc = v
            print ("{:<14} {:<12} {:<15} {:<16} {:<5} {:<16} {:<15}{:<4}{:<16} {:<16}".format(
                i, n_size, alloc, addr, mask, dec_mask, assig_range_min, ' - ' ,assig_range_max, bc))
    @staticmethod  
    def mask_wildcard(dec_mask):
        b = ''
        wild = ''
        while len(b) < int(dec_mask):
            b += '1'
        while len(b) < 32:
            b +='0'
            
        for i in b:
            if i == '1':
                wild += i.replace('1','0')
            else:
                wild += i.replace('0','1')
        tb = int(wild.count('1'))
        return [b[i:i + 8] for i in range(0, 32, 8)], [wild[i:i + 8] for i in range(0, 32, 8)], tb
    
    @staticmethod
    def transform_strings(string_ip:str, req_hosts:list):
        ip = string_ip
        hts = req_hosts
        return ip.split('/')[0].split('.'), ip.split('/')[1], sorted([int(i) for i in hts], reverse=True)
    
    @staticmethod
    def get_n_bits(wildcard, req_hosts):
        bits = wildcard[0]+wildcard[1]+wildcard[2]+wildcard[3]
        n_bits = int(bits.count('1'))
        n_hosts = (2**n_bits) - 2
        if req_hosts[0] <= n_hosts:
            control_bits = []
            for req in req_hosts:
                n = ''
                while (2**int(n.count('1'))-2) < req:
                    n += '1'
                control_bits.append(n)
            for i in range(0, len(control_bits)):
                while len(control_bits[i]) < 32:
                    control_bits[i] = '0'+ control_bits[i]
            index = []
            for ctrl in control_bits:
                for i in range(0,32):
                    if ctrl[i] == '1':
                        index.append(i)
                        break
            values = {}
            alloc_p = 0
            for i, v in enumerate(index):
                alloc_p += (2**int(control_bits[i].count('1'))-2)
                values[i] = [VLSM.mask_wildcard(v), v,req_hosts[i], (2**int(control_bits[i].count('1'))-2)]
                # return [mask, wildcard], mask, req_hosts, total_hosts
            return values, alloc_p
        else:
            #print("Subnetting failed")
            return "Error"