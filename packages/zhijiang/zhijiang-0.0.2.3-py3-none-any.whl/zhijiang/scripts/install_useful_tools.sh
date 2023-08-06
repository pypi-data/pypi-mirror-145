sudo apt install -y tldr tmux
sudo apt install -y vim-gtx  # vim with +clipboard, so vim can use os's clipboard

sudo apt install -y gdb cgdb 

sudo pip install  py-spy python3.8-dbg

sudo pip install cmake==3.21.4

# tab complete of git
curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
echo "source ~/.git-completion.bash" >> ~/.bashrc
