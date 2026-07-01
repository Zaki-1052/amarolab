# Globus

Globus is an efficient file-transfer program that you can use to transfer large files to and from a supercomputer. 

For small file transfers (<1GB), consider using SCP or SFTP. 

## Install Globus Connection Personal[edit](</mediawiki/index.php?title=Globus&action=edit&section=1> "Edit section: Install Globus Connection Personal")]

You can find detailed information at this website: <https://docs.globus.org/how-to/globus-connect-personal-linux/>
    
    
    wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
    

Now Untar and enter the directory: 
    
    
    tar xzf globusconnectpersonal-latest.tgz
    # this will produce a versioned globusconnectpersonal directory
    # replace `x.y.z` in the line below with the version number you see
    cd globusconnectpersonal-x.y.z
    

Start up the program: 
    
    
    ./globusconnectpersonal
    

Complete the setup by following the prompts. 

Once the setup is completed successfully, you should see the Globus Connect Personal GUI running. 

## Using Globus[edit](</mediawiki/index.php?title=Globus&action=edit&section=2> "Edit section: Using Globus")]

If not already started, you can start the Globus Connect Personal: 
    
    
    ./globusconnectpersonal &
    

Although you may want to run with no GUI: 
    
    
    ./globusconnectpersonal -start &
    

Now you can use the Globus web server to transfer files (<https://www.globus.org/>), or you can follow instructions in the next section for Globus CLI to transfer files by command line. 

(WARNING: on Expanse, your home directory is found at /expanse/home/username, not /home/username.) 

In the Globus web server, you can search for remote endpoints, and also register your own Endpoints. 

To set up your own endpoint in the Globus web server, click "Endpoints" in the menu to the left. Click "Create personal endpoint" 

Fill out the necessary information. Be sure to copy the setup key to your clipboard. 

You can enter your setup key into your Globus Connect Personal client by typing: 
    
    
    ./globusconnectpersonal -setup --setup-key PASTE KEY HERE
    

Finish filling out the personal endpoint information in the Globus web server and submit. The endpoint will now be available for you. 

## Installing Globus CLI[edit](</mediawiki/index.php?title=Globus&action=edit&section=3> "Edit section: Installing Globus CLI")]

You can find information on the Globus CLI website: <https://docs.globus.org/cli/>. 

These are an overview of the steps you can follow to install Globus on your local computer. 

Make sure you've installed Conda if you haven't already: 
    
    
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sh Miniconda3-latest-Linux-x86_64.sh
    

And follow the prompts. 

Now install the Globus client locally: 
    
    
    conda install -c conda-forge globus-cli
    

Next, log in: 
    
    
    globus login
    

A browser window will open and you can enter your active directory username and password. 

Once you are logged in, you can check that the login was successful by running: 
    
    
    globus get-identities -v 'go@globusid.org'
    

Now, register the Globus Endpoint. For instance, we will demonstrate with the endpoint for SDSC Expanse, which is "xsede#expanse". If you need to find an Endpoint for a particular machine, you can consult the manual or reach out to tech support for that machine and they can tell you. 
    
    
    globus endpoint search xsede#expanse
    

You'll see a similar output to this: 
    
    
    ID                                   | Owner              | Display Name 
    ------------------------------------ | ------------------ | -------------
    b256c034-1578-11eb-893e-0a5521ff3f4b | xsede@globusid.org | XSEDE Expanse
    

The number that begins with b25... is the endpoint's ID. You'll use this ID for future steps. 

Activate the Endpoint: 
    
    
    globus endpoint activate b256c034-1578-11eb-893e-0a5521ff3f4b
    

Or 
    
    
    globus endpoint activate b256c034-1578-11eb-893e-0a5521ff3f4b --web
    

The latter command will open a browser for you to verify your XSEDE login. 

You can see your local globus endpoint ID (if you've installed Globus Connect Personal): 
    
    
    globus endpoint local-id
    

Now, to transfer files via command line, use the following command: 
    
    
    globus transfer LOCAL_ID_VALUE:/path/to/local/file DESTINATION_ID_VALUE:/path/to/write/file
    

Of course, fill out the correct ids and paths to transfer the file. Use the "--encrypt" argument to encrypt the transfer. 
    
    
    globus transfer --encrypt LOCAL_ID_VALUE:/path/to/local/file DESTINATION_ID_VALUE:/path/to/write/file
