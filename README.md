# prayer-times
## Git Errors on Local Machines 
After creating new branch in Github then when checkout new branch in local machine Error was received 
then the below command 
```sh
git remote -v
origin  https://github.com/haskhr/prayer-times.git (fetch)
origin  https://github.com/haskhr/prayer-times.git (push)
```
after getting the above output we used below command to fetch new branch info from Github

```sh
git fetch origin
From https://github.com/haskhr/prayer-times
 * [new branch]        4-making-the-program-autorun -> origin/4-making-the-program-autorun
```
after checkout new branch was sucessfull 

```sh
git checkout 4-making-the-program-autorun 
branch '4-making-the-program-autorun' set up to track 'origin/4-making-the-program-autorun'.
Switched to a new branch '4-making-the-program-autorun'

```
once  ckeckout new branch successfully ,we can add all the changes which was stashed earlier by 

```git stash
Saved working directory and index state WIP on main: 9c18f592 Merge pull request #3 from haskhr/1-uploading-the-file-to-github-from-local-machine
```
then you can retrieve all changes by below command 

```
git stash apply
On branch 4-making-the-program-autorun
Your branch is up to date with 'origin/4-making-the-program-autorun'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   r.txt
```
