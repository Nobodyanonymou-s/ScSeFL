import os
import platform
import socket


# 获取本机ip地址
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        st.close()
    return ip


# OS是windows
def is_inuse_windows(port):
    # os.popen()函数与cmd命令窗口之间建立一个双向通道，可以从cmd窗口和程序间相互读取信息
    if os.popen('netstat -an | findstr :' + str(port)).readlines():
        port_inuse = True
        print('{} is in use'.format(port))
    else:
        port_inuse = False
        print('{} is free'.format(port))
    return port_inuse

def find_available_nPorts(startPort, n):
    # 死循环一直查找，直到找到为止。
    while True:
        flag, endPort = checkPorts(startPort, n)
        # 直到n个连续ports都可用，才跳出循环。否则一直往后查找。
        if (flag == True):  # ninePort is ok
            break
        else:
            startPort = endPort + 1

    print(f'First port of {n} free ports is {startPort}')
    ports = list(range(startPort, startPort + n))
    print(f'{n} available ports: {ports}')
    return ports


# 从startport开始找n个连续可用的端口
def checkPorts(startPort, n):
    # 返回的是function：不同OS上检查端口是否占用的函数
    isInuseFunc = choosePlatform()
    nPortsIsFree = True
    for i in range(1, n + 1):
        # 如果端口被占用，跳出循环，如果端口未被占用，开始端口往后延一位
        if (isInuseFunc(startPort)):
            nPortsIsFree = False
            break
        else:
            startPort = startPort + 1
    return nPortsIsFree, startPort


# 获取本机操作系统，使用对应的命令查看端口号是否被占用
def choosePlatform():
    # 'Windows-7-6.1.7601-SP1'
    # 'AIX-1-00F739CE4C00-powerpc-32bit'
    # 'HP-UX-B.11.31-ia64-32bit'
    # 'Linux-3.0.101-0.35-default-x86_64-with-SuSE-11-x86_64'
    # 'SunOS-5.10-sun4u-sparc-32bit-ELF'

    # 获取本机的系统
    machine = platform.platform().lower()
    print(f"本机系统是：{machine} ")
    if 'windows-' in machine:
        return is_inuse_windows
    elif 'linux-' in machine:
        return is_inuse_linux
    elif 'aix-' in machine:
        return is_inuse_aix
    elif 'hp-' in machine:
        return is_inuse_hp
    elif 'sunos-' in machine:
        return is_inuse_sun
    else:
        print('Error, sorry, platform is unknown')
        exit(-1)


if __name__ == '__main__':
    print("本机ip地址: ", extract_ip())
    ports = find_available_nPorts(18887, 10)