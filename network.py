import wmi
import json

nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration()

for nw in nic_configs:
    if nw.IPAddress and nw.ServiceName != "VBoxNetAdp":
        default_adapter = nw.Index


def open_json(filename: str):
    
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            jsn = json.loads(f.read())

        return jsn
    
    except:
        return 0
    


def enable_static(adapter: int, ip: str, subnetmask: str, gateway: str, dns: str):

    nic = nic_configs[adapter]

    if not ip:
        ip = nic.IPAddress


    print("Ответ от статики: ", nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask]))
    print("Ответ от шлюза: ", nic.SetGateways(DefaultIPGateway=[gateway]))
    print("Ответ от DNS: ", nic.SetDNSDomain(DNSDomain=gateway))
    print("Ответ от массива порядка DNS серверов: ", nic.SetDNSServerSearchOrder(DNSServerSearchOrder=dns))


def enable_dhcp(adapter: int):
    nic = nic_configs[adapter]

    print("Ответ от DHCP: ", nic.EnableDHCP())



def information_of_networks():
    print("\n")
    for nw in nic_configs:
        print(f"Адаптер: {nw.Description}", "(по умолчанию)" if default_adapter == nw.Index else "")
        print("     Номер сети: ", nw.Index)
        print("     IP: ", nw.IPAddress)
        print("     Маска: ", nw.IPSubnet)
        print("     DNS: ", nw.DNSDomain)
        print("\n")


def debug():
    for nw in nic_configs:
        print(nw)


if __name__ == "__main__":
    
    #debug()
        

    while True:
        print("Меню")
        print("1 - Выбрать файл конфигурации сети и подключить")
        print("2 - Включить DHCP")
        print("3 - Информация об подключенных соединениях")
        print("4 - Выход")

        num = input("")

        if num.isdigit():
            
            match int(num):

                case 1:
                    while True:
                        file = input("Введите название файла конфигурации в формате JSON: ")
                        schema = open_json(file)
                        if schema != 0:
                            ip, subnetmask, gateway, dns = schema.get("ip"), schema.get("subnetmask"), schema.get('gateway'), schema.get('dns')
                            break

                        else:
                            print(f"Файл \"{file}\" не найден")

                    adapter = input(f"Выберете адаптер [0-{len(nic_configs)-1}] (по умолчанию - {default_adapter}): ")

                    while True:
                        if adapter.isdigit():
                            if int(adapter) >= 0 and int(adapter) <= len(nic_configs)-1:
                                enable_static(int(adapter), ip, subnetmask, gateway, dns)
                                break

                            else:
                                print("Адаптер с данным номером не найден")

                        else:
                            print("Некорретный номер адаптера")

                case 2:
                    adapter = input(f"Выберете адаптер [0-{len(nic_configs)-1}] (по умолчанию - {default_adapter}): ")

                    while True:
                        if adapter.isdigit():
                            if int(adapter) >= 0 and int(adapter) <= len(nic_configs)-1:
                                enable_dhcp(int(adapter))
                                break

                            else:
                                print("Адаптер с данным номером не найден")

                        else:
                            print("Некорретный номер адаптера")
                    

                case 3:
                    information_of_networks()

                case 4:
                    exit(0)

                case _:
                    print("Номер пункта не найден")

        else:
            print("Некорректный номер")