''' This client gets the raw bro logs from PCAP files '''
import zerorpc
import os
import argparse
import ConfigParser

def main():
    ''' This client gets the raw bro logs from PCAP files '''
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    workbench_conf.read('config.ini')
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.getint('workbench', 'server_port') 

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=port, help='port used by workbench server')
    parser.add_argument('-s', '--server', type=str, default=server, help='location of workbench server')
    args = parser.parse_args()
    port = str(args.port)
    server = str(args.server)

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300)
    workbench.connect('tcp://'+server+':'+port)


    # Test out getting the raw Bro logs from a PCAP file
    # Note: you can get a super nice 'generator' python list of dict by using
    #       'stream_sample' instead of 'get_sample'.
    file_list = [os.path.join('../data/pcap', child) for child in os.listdir('../data/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'pcap')
            results = workbench.work_request('pcap_bro', md5)

            # Results is just a dictionary of Bro log file names and their MD5s in workbench
            for log_name, md5 in results['pcap_bro'].iteritems():

                # Just want the logs
                if log_name.endswith('_log'):
                    bro_log = workbench.get_sample(md5)['sample']['raw_bytes']
                    print '\n\n<<< Bro log: %s >>>\n %s' % (log_name, bro_log)
def test():
    ''' pcap_bro_raw test '''
    main()

if __name__ == '__main__':
    main()
