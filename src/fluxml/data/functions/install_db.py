from bpyutils.util.system import popen

DATABASES = {
    "nr": {
        "uri": "ftp://ftp.ncbi.nlm.nih.gov/blast/db/nr.tar.gz"
    }
}

def install_db():
    database = DATABASES["nr"]