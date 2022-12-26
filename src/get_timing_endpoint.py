import re

def get_timing_endpoint(sdc_path):
    '''If a port is constrainted in .sdf file, then it is a timing endpoint'''
    with open(sdc_path) as f:
        content = f.read()
    pattern = re.compile(r'\[get_ports \{([\w\[\]]+?)\}\]')
    res = pattern.findall(content)
    return res


if __name__ == "__main__":
    print(get_timing_endpoint('data\\6_final.sdc'))