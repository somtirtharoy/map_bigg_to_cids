import cobra
import os


data_file_path = 'data'

def extract_inchikeys_from_model():
    model =  cobra.io.load_json_model('iJO1366.json')
    bigg_to_inchikey = {}
    allCount = 0
    inchiCount = 0

    # if data folder doesn't exist create it
    if not os.path.isdir(data_file_path):
        os.mkdir(data_file_path)
    inchikey_id_file = f"{data_file_path}/inchikey_ids.txt"
    
    with open(inchikey_id_file, 'w') as fh:
        for m in model.metabolites:
            allCount +=1
            if 'inchi_key' in m.annotation:
                inchiCount +=1
                bigg_to_inchikey[m.id] = m.annotation[ 'inchi_key'][0]

                # writing the InchiKey ids into a flatfile
                fh.write(m.annotation[ 'inchi_key'][0] + "\n")
    print("Number of total metabolites:", allCount)
    print(f"Number of metabolites with inchikey ids: {inchiCount}")
    print(f"Number of unique keys in the bigg_to_inchikey dictionary {len(bigg_to_inchikey.keys())} \n")
    fh.close()


def duplicate_inchikey_ids():
    inchikey_to_cid = {}
    inchikey_to_cid_count = {}
    total_ids = 0
    ids_with_cids = 0
    no_values = 0

    # if data folder doesn't exist create it
    if not os.path.isdir(data_file_path):
        os.mkdir(data_file_path)
    inchikey_to_cid_file = f"{data_file_path}/inchikey_to_cid.txt"

    with open(inchikey_to_cid_file, 'r') as fh, open(' .txt', 'w') as fh_write:
        try:
            line = fh.readline()
            while line:
                total_ids +=1
                if (len(line.split()) > 1):
                    ids_with_cids +=1

                    # if inchikey id present in dict
                    if line.split()[0] in inchikey_to_cid_count.keys():
                        # if there is already a single count of the inchikey mapping
                        if inchikey_to_cid_count[line.split()[0]] == 1:
                            fh_write.write(line.split()[0] + ", "  + inchikey_to_cid[line.split()[0]] + "\n")
                            fh_write.write(line.split()[0] + ", "  + line.split()[1] + "\n")
                        
                        # else write the line if the count more than 1
                        else:
                            fh_write.write(line.split()[0] + ", "  + line.split()[1] + "\n")
                    
                        # increasing the dict count for this inchikey
                        inchikey_to_cid_count[line.split()[0]] +=1

                    else:
                        inchikey_to_cid[line.split()[0]] = line.split()[1]
                        inchikey_to_cid_count[line.split()[0]] =1
                        # fh_write.write(line.split()[0] + ", "  + line.split()[1] + "\n")
                else:
                    no_values +=1

                line = fh.readline()
        except Exception as ex:
            print("Error in reading file!")
            print(ex)

        fh.close()
        fh_write.close()

# reading output from pubchem mapping of inchikey to CIDs to a dictionary
def read_pubchem_id_file():
    inchikey_to_cid = {}
    inchikey_to_cid_count = {}
    total_ids = 0
    ids_with_cids = 0
    no_values = 0

    # if data folder doesn't exist create it
    if not os.path.isdir(data_file_path):
        os.mkdir(data_file_path)
    inchikey_to_cid_file = f"{data_file_path}/inchikey_to_cid.txt"
    multiple_cids_file_name = f"{data_file_path}/inchikeys_with_multiple_cids.txt"

    with open(inchikey_to_cid_file, 'r') as fh, open(multiple_cids_file_name, 'w') as fh_write:
            try:
                line = fh.readline()
                while line:
                    total_ids +=1
                    if (len(line.split()) > 1):
                        ids_with_cids +=1
                        inchikey_to_cid[line.split()[0]] = line.split()[1]
                        if line.split()[0] in inchikey_to_cid_count.keys():
                            inchikey_to_cid_count[line.split()[0]] +=1
                        else:
                            inchikey_to_cid_count[line.split()[0]] =1
                    else:
                        no_values +=1

                    line = fh.readline()
            except Exception as ex:
                print("Error in reading file!")
                print(ex)

            # the number of keys in the dictionary is less because of duplicate records in the mapping from inchikey to CIDs
            print("Total number of keys in inchikey_to_cid dictionary", len(inchikey_to_cid.keys()))
            print("Total number of records in the inchikey_to_cid file that have a mapping", ids_with_cids)
            print("Total number of records calculated from the values in inchikey_to_cid_count dict:", sum(inchikey_to_cid_count.values()))
            print("Total number of records in the inchikey_to_cid file that have no mapping", no_values)
            print("Total ids from pubchem after transformation", total_ids)
    fh.close()
    fh_write.close()


if __name__ =="__main__":
    # extract the inchikeys formth emodel and write in to a file
    # extract_inchikeys_from_model()

    # After using the inchikey id file on https://pubchem.ncbi.nlm.nih.gov/idexchange/idexchange.cgi 
    # to map them to corresponding CID's we download the mapping file which has multiple CID's for the same inchikey ID.
    # we convert them to a single CID, either  by selecting any one of them or by manually curating them and generate a mapping file that has unique 
    # inchi key ID to CID mapping
    duplicate_inchikey_ids()