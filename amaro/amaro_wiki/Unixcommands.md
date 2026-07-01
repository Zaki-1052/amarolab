# Unixcommands

##### Useful Unix/Linux commands:[edit](</mediawiki/index.php?title=Unixcommands&action=edit&section=1> "Edit section: Useful Unix/Linux commands:")]
    
    
    ### Unix Manual ###
    man: MANual for any command
    
    ### FileSystem traversal ###
    ls: LiSt files/directories(folders)
    cd: Change Directory
    pwd: Print Working Directory: find out where you are
    
    ./     current directory
    ../    parent directory
    /      root directory
    ~/     home directory
    
    ### Files & Folders ###
    mv: MoVe/rename file
    cp: CoPy file (cp -r for entire directory)
    ln: LiNk file
    cat: conCATenate file to standard output
    less: file viewer
    wc: Word Count (can also be used to count characters/lines)
    rm: ReMove file
    mkdir: MaKe DIRectory
    rmdir: ReMove DIRectory
    file: see file type
    diff: see differences between two files
    head: see lines at the top of the file
    tail: see lines at the bottom of the file
    xxd: view file as hexdump
    
    ### I/O Streams ###
    >    write standard output to file (erasing what was in file before)
    >>   append standard output to file (keeping what was in file before)
    <    read standard input from file
    |    pipe output to another command
    tee: write to file as well as standard output
    
    ### Processes ###
    top: process TOPology, shows what programs are running
    ps: lists all current running programs as standard output
    kill: kill a process
    fg: bring background process to foreground
    bg: send foreground process to background
    &    run a command in the background
    at: run a command at a specific time
    crontab: run a command repeatedly at a specific time
    
    ### Variables ###
    export: assign an environmental variable
    echo: print the value of a variable, or repeat a string
    alias: encapsulate a command into an alias for easy calling
    ~/.bashrc   a file to execute commands upon opening a terminal
    $PATH     variable that contains the location of important programs
    
    ### editing/viewing files ###
    vi: text editor in the terminal
    gedit: text editor in a window
    eog: image viewer
    evince: PDF file viewer
    
    ### loops and conditionals ###
    if,then,fi: evaluates whether a condition is true and if so, will execute specific code
    for,do,done: executes a portion of code a given number of times
    while,do,done: executes a portion of code repeatedly until a criteria is satisfied
    break: break out of a loop
    continue: skip current iteration of loop
    
    ### users & permissions ###
    whoami: see your username
    hostname: see which host (computer) you are logged into
    who: see who else is logged in
    chmod: change file permissions
    sudo: execute commands as superuser
    
    ### other useful commands ###
    grep: filters lines based on criteria
    tr: TRanslate, converts a character to another, or removes/squashes characters
    sed: Stream EDitor, modifies standard output
    cut: cut column in file
    paste: paste two files together side by side
    awk: advanced scripting language/string processing
    bc: Basic Calculator
    
    ### NOTE: most of these commands have flags denoted with a dash '-'. Example "ls -l", which lists more details than a plain "ls" command. See 'man' for specific command flags. ###
