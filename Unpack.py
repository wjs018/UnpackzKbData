import os
import tarfile
import gzip
import multiprocessing as mp
import datetime


def untar(tarPath, destPath="."):
    """
    Unpacks a .tar file located at tarPath to a directory specified by
    destPath. Defaults to unpacking in same folder as the .tar file.
    The .tar file is not deleted after this is run.
    """
    
    tar = tarfile.open(tarPath)
    tar.extractall(path=destPath)
    tar.close
    
def ungz(args):
    """
    Extracts a .gz file. The newly extracted file will have the same
    file name as the .gz file, just without the .gz extension. For
    example:
    
        foo.bar.gz will become foo.bar
        
    The newly extracted file will be located in the same directory as
    the .gz file. After extracting is complete, the original .gz file
    will be deleted.
    
    Inputs:
    
        args    Contains a tuple where the first element is the parent
                directory of the .gz file and the second element is the
                filename of the .gz file.
    """
    
    # Input arguments
    
    root, name = args
    
    # Build filepaths
    
    gzPath = os.path.join(root, name)
    destPath = os.path.join(root, name[:-3])
    
    # Open and read the .gz file, saving the contents to a variable
    
    gz = gzip.GzipFile(filename=gzPath, mode='rb')
    contents = gz.read()
    gz.close()
    
    # Write the contents of the .gz file to its own file, expanding it
    
    gzOut = file(destPath, 'wb')
    gzOut.write(contents)
    gzOut.close
    
    # Delete the original .gz file
    
    os.remove(gzPath)
    

if __name__ == '__main__':
    
    #===========================================================================
    # Below are parameters to be changed for your particular setup.
    #===========================================================================
    
    # This is where you should specify the path to the .tar file to be unpacked
    
    tarPathName = "/media/sf_G_DRIVE/Other Torrents/zkb-killmails.tar"
    
    # This is where the destination folder path is specified
    # This folder should be empty to start
    
    destPathName = "/media/sf_G_DRIVE/zkb-Killmails/"
    
    #===========================================================================
    # End of configurable parameters.
    #===========================================================================
    
    # First unpack the tar file
    
    untar(tarPathName, destPath=destPathName)
    
    print "Done extracting .tar"
    
    # Then recursively find all the gz files that need decompressed
    
    startTime = datetime.datetime.now()
    
    for root, dirs, files in os.walk(destPathName):
        
        # Fire up our pool of workers, one for each core
        
        workers = mp.Pool()
        
        # Build the arguments used in the function call
        
        args = [(root, name) for name in files]
        
        # Run the ungz function in parallel
        
        result = workers.map(ungz, args)
        
    # Print the total time it took to run
    
    endTime = datetime.datetime.now()
    elapsed = endTime - startTime

    print "Done extracting .gz files, " + str(int(round(elapsed.total_seconds()))) + " seconds elapsed"